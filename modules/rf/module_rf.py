import module
import module_rf_constants
#import module_rf_constants_research as module_rf_constants
#import module_rf_constants_mongo
import module_preprocessor
import pandas as pd
import sys
from sklearn.ensemble import RandomForestClassifier

class ModuleRandomForest(module.Module):
    version = '1.0'
    dataPd = None
    dataGt = None
    clf = None
    preprocessor = None
    preprocessorVersion = 1
    percentageTest = 0.7
    featuresDimension = 0
    dataPd = None
    dataGt = None
    trainPd = None
    testPd = None
    trainGt = None
    testGt = None

    def __init__(self, modelPath=None, preprocessorVersion=1):
        self.selectedFields = module_rf_constants.defaultSelectedFields
        self.fieldLabels = module_rf_constants.defaultFieldsLabels
        self.parsedFields = module_rf_constants.defaultParsedFields
        self.hotencFields = module_rf_constants.defaultHotencFields
        self.hotencLabels = {}
        if modelPath is None:
            self.clf = RandomForestClassifier()
        else:
            import joblib
            self.hotEncoders,self.clf = joblib.load(modelPath)            
        self.preprocessorVersion = preprocessorVersion
        self.module_preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldLabels,self.parsedFields, withGt=True, version = self.preprocessorVersion)
        self.moduleId = 'RF-v'+self.version

    def saveModel(self,modelPath):
        import joblib
        joblib.dump((self.hotEncoders,self.clf),modelPath)
        
    def processHit(self, dataset):
        #import pdb; pdb.set_trace()
        if type(dataset) == str:
            hitPd,_ = self.preprocessHit(dataset)
        elif type(dataset) == pd.core.frame.DataFrame:
            hitPd = dataset
        if 'id' in hitPd.columns:
            hitPd = hitPd.drop('id',1)            
        if len(hitPd.columns) != len(self.trainPd.columns):
            print(f"Different dimensions between sample {len(hitPd.columns)} and trainset {len(self.trainPd.columns)}. Not performing pred")
            import numpy as np
            return np.nan
        predict = self.clf.predict_proba(hitPd)[0] # first position because predict_proba returns an array with a prediction for each row
        return predict[-1]/(predict[-1]+predict[0])

    def computePhi(self,pred,gt,pos):
        import numpy as np
        gt = np.array(gt)
        if len(np.where(gt==pos)[0]) == 0:
            tpr = 0
        else:
            tpr = len(np.where((pred==pos) & (gt==pos))[0])/len(np.where(gt==pos)[0])
        if len(np.where(gt!=pos)[0])==0:
            tnr = 0
        else:
            tnr = len(np.where((pred!=pos) & (gt!=pos))[0])/len(np.where(gt!=pos)[0])
        phi=tpr+tnr
        return phi,tpr,tnr

    # def preprocess(self,dataset):
    #     if len(self.hotencFields)>0:
    #         dataPd,_ = self.hotEncodeFields(dataset,self.hotencFields)
    #     return dataPd,_

    def preprocessHit(self,hit):
        dataPd,dataGt = self.module_preprocessor.preProcessHit(hit)
        dataPd,_ = self.hotEncodeFields(dataPd,self.hotencFields)
        return dataPd,dataGt

    def preprocessSet(self,dataSet):
        if type(dataSet) == str:
            with open(dataSet)as fid:
                dataSet = fid.readlines()
        if type(dataSet) is not list:
            print(f"Error while training RF with dataSet not a list nor a path")
            return None                
        if len(dataSet)<1:
            print(f"Empty train set. Doing nothing...")
            return None
        print("Preprocessing jsons and building training set.")
        #import pdb; pdb.set_trace()
        if self.module_preprocessor == None:
            self.module_preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldLabels,self.parsedFields, withGt=True, version=self.preprocessorVersion)
            print(f"preprocessor version {self.preprocessorVersion}")
        preprocessor = self.module_preprocessor
        print(f"\tPreprocessor version {self.preprocessorVersion} {preprocessor.version}")
        totaliter = len(dataSet)
        curiter = 0
        lastper = 0
        import time
        prepStart = time.time()
        dataPd,dataGt = preprocessor.preProcessHit(dataSet[0])
        dataGt = [dataGt]
        print("Samples preprocessed: ",end="")
        for s in range(1,len(dataSet)):
            if self.preprocessorVersion==1:
                onepd,onegt = preprocessor.preProcessHit(dataSet[s])
                dataPd = pd.concat([dataPd,onepd],axis=0)
            if self.preprocessorVersion==2:
                onepd,onegt = preprocessor.preProcessHit(dataSet[s],returnDict=True)
                dataPd = dataPd.append(onepd,ignore_index=True)
            dataGt.append(onegt)
            curiter = curiter + 1
            if int(curiter*100/totaliter) > lastper:
                lastper = int(curiter*100/totaliter)
                print(f"{curiter} {lastper}%| ", end='')                
                sys.stdout.flush()
        prepEnd = time.time()
        print(f"... al samples preprocessed in {prepEnd-prepStart:.5f} seconds!")
        import pdb; pdb.set_trace()
        self.dataPd = dataPd.copy()
        self.dataGt = dataGt.copy()
        return dataPd, dataGt

    # open json file and preprocess it
    def preprocessTrainset(self,trainSet):
        dataPd,dataGt = self.preprocessSet(trainSet)
        import joblib
        # hot encode fields
        print(dataPd.columns)
        #import pdb; pdb.set_trace()
        if len(self.hotencFields)>0:
            try:
                dataPd,_ = self.hotEncodeFields(dataPd,self.hotencFields)
            except:
                print("There was some error hotencoding. We'll safe dataPd to inspect and throw debugger")
                joblib.dump(dataPd,'/tmp/dataPd.hotencFailed.bz2')
                #import pdb; pdb.set_trace()                
        dataPd['gt'] = dataGt
        dataPd.dropna(inplace=True)
        joblib.dump(dataPd,'foo_data_trainrf.bz2')
        return dataPd.drop('gt',axis=1),dataPd['gt']
    
    def trainRF(self,trainSet):
        if type(trainSet) == str :
            # trainSet refers to a path, see if it's a preprocessed data or json to preprocess
            if trainSet[-5:] == '.json': # its a json file, let's preprocess it
                dataPd,dataGt = self.preprocessTrainset(trainSet)
                if len(self.saveTrainPath)>0:
                    print(f"Saving train data to {self.saveTrainPath}")
                    import joblib
                    joblib.dump((dataPd,dataGt,self.hotEncoders),self.saveTrainPath,compress=('bz2',6))
            if trainSet[-4:] == '.bz2': # is a preprocessed file
                print(f"Restoring train data from {trainSet}")
                import joblib
                loaded = joblib.load(trainSet)
                dataPd = loaded[0]
                dataGt = loaded[1]
                self.hotEncoders = loaded[2]
        elif type(trainSet) == list:
            dataPd,dataGt = self.preprocessTrainset(trainSet)
        elif type(trainSet) == pd.core.frame.DataFrame:
            dataPd = trainSet.drop('gt',axis=1)
            dataGt = trainSet['gt']
        #self.dataPd = dataPd
        #self.dataGt = dataGt
        testCut = int(len(dataPd)*self.percentageTest) # 70% for train, 30% for test
        trainPd = dataPd.iloc[0:testCut]
        trainGt = dataGt[0:testCut]
        testPd = dataPd.iloc[testCut:]
        testGt = dataGt[testCut:]
        # remove id columns if present
        if 'id' in trainPd.columns:
            trainPd = trainPd.drop('id',1)
            testPd = testPd.drop('id',1)
        self.trainPd = trainPd
        self.testPd = testPd
        self.trainGt = trainGt
        self.testGt = testGt
        print("Train RF...")
        from sklearn.model_selection import GridSearchCV
        n_estimators = [50,100, 200,300]
        max_depth = [15, 25, 30]
        min_samples_split = [10, 15, 20]
        min_samples_leaf = [1, 2, 5] 
        hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,min_samples_split = min_samples_split, min_samples_leaf = min_samples_leaf)
        forest = RandomForestClassifier(random_state = 1, class_weight='balanced')
        gridF = GridSearchCV(forest, hyperF, cv = 5, verbose = 1, n_jobs = 5)
        bestF = gridF.fit(trainPd,trainGt)
        print(f"Done... best params: n_estimators {bestF.best_params_['n_estimators']} max_depth {bestF.best_params_['max_depth']} min_split {bestF.best_params_['min_samples_split']} min_leaf {bestF.best_params_['min_samples_leaf']}")
        self.clf = RandomForestClassifier(n_estimators=bestF.best_params_['n_estimators'],max_depth=bestF.best_params_['max_depth'],min_samples_leaf=bestF.best_params_['min_samples_leaf'],min_samples_split=bestF.best_params_['min_samples_split'], class_weight='balanced')
        self.clf.fit(trainPd,trainGt)
        trainScore = self.clf.score(trainPd,trainGt)
        testScore = self.clf.score(testPd,testGt)
        phiTest,tprTest,tnrTest = self.computePhi(self.clf.predict(testPd),testGt,3)
        print(f"Done! Train Score: {trainScore}; Test Score: {testScore}, phi: {phiTest}, tpr: {tprTest}, tnr: {tnrTest}")
        if len(self.saveModelPath) > 0:
            import joblib
            joblib.dump(self.clf,self.saveModelPath,compress=('bz2',6))
        return trainScore

    def featureSelection(self):
        from sklearn.base import clone
        if self.trainPd is None or self.trainGt is None or self.testPd is None or self.testGt is None or self.clf is None:
            print("ERROR: Some of the pieces are missing for the feature selection (was the training performed?). Aborting feature selection")
            return None
        phiTest,tprTest,tnrTest = self.computePhi(self.clf.predict(self.testPd),self.testGt,3)
        #import pdb; pdb.set_trace()
        rawdata = self.dataPd.copy()
        if 'id' in rawdata:
            rawdata = rawdata.drop('id',axis=1)
        cols = rawdata.columns
        print(f"Initial Phi {phiTest:.4f} with columns {cols}")
        for c in cols:
            x = rawdata.drop(c,axis=1)
            hotencFields = self.hotencFields.copy()
            if c in hotencFields:
                hotencFields.remove(c)
            if len(hotencFields)>0:
                try:
                    dataPd,_ = self.hotEncodeFields(x,hotencFields)
                except:
                    print("There was some error hotencoding. We'll safe dataPd to inspect and throw debugger")
            testCut = int(len(dataPd)*self.percentageTest) # 70% for train, 30% for test
            trainPd = dataPd.iloc[0:testCut]
            trainGt = self.dataGt[0:testCut]
            testPd = dataPd.iloc[testCut:]
            testGt = self.dataGt[testCut:]
            #self.clf = RandomForestClassifier(n_estimators=bestF.best_params_['n_estimators'],max_depth=bestF.best_params_['max_depth'],min_samples_leaf=bestF.best_params_['min_samples_leaf'],min_samples_split=bestF.best_params_['min_samples_split'], class_weight='balanced')
            clf = clone(self.clf)
            clf.fit(trainPd,trainGt)
            phiTest,tprTest,tnrTest = self.computePhi(clf.predict(testPd),testGt,3)
            print(f"Feature selection removed col {c}. On test, phi: {phiTest} tpr: {tprTest} tnr: {tnrTest}")

    def featureSelectionTestCombination(self, combination):
        rawdata = self.dataPd.copy()
        if 'id' in rawdata:
            rawdata = rawdata.drop('id',axis=1)
        if len(combination) != len(rawdata.columns):
            print(f"ERROR: Combination size {len(combination)} doesn't match columns size {len(rawdata.columns)}")
            return -1
        selectedcols = [] 
        hotencFields = []
        for b,c in zip(combination,rawdata.columns):
            if b:
                selectedcols.append(c)
                if c in self.hotencFields:
                    hotencFields.append(c)
        x = rawdata[selectedcols]
        if len(hotencFields)>0:
            try:
                dataPd,_ = self.hotEncodeFields(x,hotencFields)
            except:
                print("There was some error hotencoding. We'll safe dataPd to inspect and throw debugger")
            
        testCut = int(len(dataPd)*self.percentageTest) # 70% for train, 30% for test
        trainPd = dataPd.iloc[0:testCut]
        trainGt = self.dataGt[0:testCut]
        testPd = dataPd.iloc[testCut:]
        testGt = self.dataGt[testCut:]
        clf = clone(self.clf)
        clf.fit(trainPd,trainGt)
        phiTest,tprTest,tnrTest = self.computePhi(clf.predict(testPd),testGt,3)
        print(f"selected {selectedcols} phi {phitest:.4f}")
        return phiTest
