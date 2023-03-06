import module
import module_xgb_constants
import module_preprocessor
import pandas as pd
#from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

class ModuleXgb(module.Module):
    dataPd = None
    dataGt = None
    clf = None
    preprocessor = None
   
    def __init__(self, modelPath=None):
        self.selectedFields = module_xgb_constants.defaultSelectedFields
        self.fieldLabels = module_xgb_constants.defaultFieldsLabels
        self.parsedFields = module_xgb_constants.defaultParsedFields
        self.hotencFields = module_xgb_constants.defaultHotencFields
        self.hotencLabels = {}
        if modelPath is None:
            self.clf = XGBClassifier()
        else:
            import joblib
            self.hotEncoder,self.clf = joblib.load(modelPath)            
        self.preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldLabels,self.parsedFields, withGt=True)

    def saveModel(self,modelPath):
        import joblib
        joblib.dump((self.hotEncoder,self.clf),modelPath)
        
    def processHit(self, dataset):
#        import pdb; pdb.set_trace()
        if type(dataset) == str:
            hitPd,_ = self.preprocessHit(dataset)
        elif type(dataset) == pd.core.frame.DataFrame:
            hitPd = dataset
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

    def preprocess(self,dataset):
        if len(self.hotencFields)>0:
            dataPd,_ = self.hotEncodeFields(dataset,self.hotencFields)
        return dataPd,_

    def preprocessHit(self,hit):
        dataPd,dataGt = self.preprocessor.preProcessHit(hit)
        dataPd,_ = self.hotEncodeFields(dataPd,self.hotencFields)
        return dataPd,dataGt

    # open json file and preprocess it
    def preprocessTrainset(self,trainSet):
        if type(trainSet) == str:
            with open(trainSet)as fid:
                trainSet = fid.readlines()
        if type(trainSet) is not list:
            print(f"Error while training XGB with trainSet not a list nor a path")
            return None                
        if len(trainSet)<1:
            print(f"Empty train set. Doing nothing...")
            return None
        print("Preprocessing jsons and building training set")
        #import pdb; pdb.set_trace()
        preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldLabels,self.parsedFields, withGt=True)
        dataPd,dataGt = preprocessor.preProcessHit(trainSet[0])
        dataGt = [dataGt]
        for s in range(1,len(trainSet)):
            onepd,onegt = preprocessor.preProcessHit(trainSet[s])
            dataPd = pd.concat([dataPd,onepd],axis=0)
            dataGt.append(onegt)
        # hot encode fields
        if len(self.hotencFields)>0:
            dataPd,_ = self.hotEncodeFields(dataPd,self.hotencFields)
        return dataPd,dataGt
    
    def trainXgb(self,trainSet):
        if type(trainSet) == str :
            # trainSet refers to a path, see if it's a preprocessed data or json to preprocess
            if trainSet[-5:] == '.json': # its a json file, let's preprocess it
                dataPd,dataGt = self.preprocess(trainSet)
                if len(self.saveTrainPath)>0:
                    print(f"Saving train data to {self.saveTrainPath}")
                    import joblib
                    joblib.dump((dataPd,dataGt,self.hotEncoder),self.saveTrainPath,compress=('bz2',6))
            if trainSet[-4:] == '.bz2': # is a preprocessed file
                print(f"Restoring train data from {trainSet}")
                import joblib
                loaded = joblib.load(trainSet)
                dataPd = loaded[0]
                dataGt = loaded[1]
                self.hotEncoder = loaded[2]
        elif type(trainSet) == list:
            dataPd,dataGt = self.preprocessTrainset(trainSet)
        elif type(trainSet) == pd.core.frame.DataFrame:
            dataPd = trainset.drop('gt',axis=1)
            dataGt = trainset['gt']
        self.dataPd = dataPd
        self.dataGt = dataGt
        testCut = int(len(dataPd)*.7) # 70% for train, 30% for test
        trainPd = dataPd.iloc[0:testCut]
        trainGt = dataGt[0:testCut]
        testPd = dataPd.iloc[testCut:]
        testGt = dataGt[testCut:]
        print("Train XGB...")
        self.clf.fit(trainPd,trainGt)
        trainScore = self.clf.score(trainPd,trainGt)
        testScore = self.clf.score(testPd,testGt)
        phiTest,tprTest,tnrTest = self.computePhi(self.clf.predict(testPd),testGt,3)
        print(f"Done! Train Score: {trainScore}; Test Score: {testScore}, phi: {phiTest}, tpr: {tprTest}, tnr: {tnrTest}")
        if len(self.saveModelPath) > 0:
            import joblib
            joblib.dump(self.clf,self.saveModelPath,compress=('bz2',6))
        return trainScore

