# Module HNSSVM
# Version 1.1
# Jan 2023
# 
# by Anton Albajes-Eizagirre
# anton.albajes-eizagirre@optickssecurity.com
#
#


import sys
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hns/')
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hnsSvmClassifier/')
sys.path.insert(1,'/home/anton/Documents/code_base/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hns/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hnsSvmClassifier/')
sys.path.insert(1,'/home/users/aalbajes/code_base/')
import module
import module_preprocessor
import module_hnssvm_constants as hnsct
import hierarchicalNominalSimilarity as hns
import hnsSvmClassifier as hnssvm
import numpy as np
from sklearn import svm
import pandas as pd

def testParams(traindata,traingt,testdata,testgt,params):
    tpr=0.0;tnr=0.0;phi=0.0
    print(f"Let's test for C{params['C']} G{params['gamma']} K{params['kernel']}")
    try: 
        clf = svm.SVC(probability=True,C=params['C'],gamma=params['gamma'],kernel=params['kernel'])
        clf.fit(traindata,traingt)
        preds = clf.predict(testdata)
        tpr,tnr,phi = hnssvm.phi(testgt,preds,3,1)
    except Exception as e:
        print(e)
        tpr=-1.0;tnr=-1.0;phi=-1.0
    print(f"Done! {tpr:.3f} {tnr:.3f} {phi:.3f}")
    return  tpr,tnr,phi,params


class ModuleHnsSvm(module.Module):
    version = '1.1' # Jan 2023
    mode = 2 # 1 = single HNS diff mode, 2 = matrix HNS diff mode 
    hns = None
    nomdata = None
    builtdata = None
    traindata = None
    trainfeatures = None
    traingt = None
    trainfeaturesMat = None
    traingtMat = None
    clf = None
    clfMat = None
    built = 0
    trained = 0
    nsamplestrain = 300
    nsamplesbuild = 300
    nbuildUsed = 0
    ntrainUsed = 0
    todrop = None
    meantrainedlows = 0.0
    meantrainedhigs = 0.0
    stdtrainedlows = 0.0
    stdtrainedhigs = 0.0
    stdthreshold = 2.5
    targets = [1,3]
    jkCols = None
    jkClfs = None
    verbose = 1
    # DEPRECATED VARS
    explainability_enabled = False

    def __init__(self,modelPath=None, data=None, todrop=None, targetcol=None, nsamplestrain=300, nsamplesbuild=300,mode=2):
        if modelPath is None:
            if data is None or todrop is None or targetcol is None:
                print("Error. If modelPath==None, data, todrop and targetcol need to be provided.")
            self.nomdata = data
            self.built = 0
            self.trained = 0
            self.todrop = todrop
            self.targetcol = targetcol
            self.selectedFields = hnsct.defaultSelectedFields
            self.fieldLabels = hnsct.defaultFieldsLabels
            self.parsedFields = hnsct.defaultParsedFields
            self.hotencFields = hnsct.defaultHotencFields
        else:
            self.selectedFields = hnsct.defaultSelectedFields
            self.fieldLabels = hnsct.defaultFieldsLabels
            self.parsedFields = hnsct.defaultParsedFields
            self.hotencFields = hnsct.defaultHotencFields
            import joblib
            self.hns, self.builtdata, self.nsamplestrain, self.targetcol, self.targets, self.todrop, self.clf = joblib.load(modelPath)
        self.mode = mode
        self.moduleId = 'HNSSVM-v'+self.version+'-m'+str(self.mode)
        self.label = None
        self.nsamplesbuild = nsamplesbuild
        self.nsamplestrain = nsamplestrain

    def saveModel(self,modelPath):
        packet = [self.hns, self.builtdata,self.nsamplestrain,self.targetcol,self.targets,self.todrop,self.clf]
        import joblib
        joblib.dump(packet,modelPath)
            
    def preprocess(self,trainSet,withGt=False):
        #import pdb; pdb.set_trace()
        if self.module_preprocessor is None:
            self.module_preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldLabels,self.parsedFields,withGt=withGt,version=3)
        preprocessor = self.module_preprocessor
        totaliter = len(trainSet)
        curiter = 0
        lastper = 0
        #import pdb; pdb.set_trace()
        dataPd,agt = preprocessor.preProcessHit(trainSet[0],funcParse=hnsct.getDictVars)
        gt = [agt]
        if self.verbose>0:
            print("Samples preprocessed: ",end="")
        for s in range(1,len(trainSet)):
            onepd,onegt = preprocessor.preProcessHit(trainSet[s],funcParse=hnsct.getDictVars)
            dataPd = pd.concat([dataPd,onepd],axis=0)
            gt.append(onegt)
            if self.verbose>0:
                curiter = curiter + 1
                if int(curiter*100/totaliter) > lastper:
                    lastper = int(curiter*100/totaliter)
                    print(f"{curiter} {lastper}%| ", end='')                
                    sys.stdout.flush()
        if self.verbose>0:
            print("... al samples preprocessed!")
        # hot encode fields
        if len(self.hotencFields)>0:
            dataPd,_ = self.hotEncodeFields(dataPd,self.hotencFields)
        if self.module_preprocessor.version==2:
            dataPd['risk_level'] = gt
        return dataPd,gt
        
    def buildHns(self, builtdata=None, traindata=None, whole=False):
        if self.built==0:
            if builtdata is None and traindata is None:
                nsample = min(150000,len(self.nomdata))
                self.builtdata,self.traindata, _=hnssvm.subsampleAndSplit(self.nomdata,nsample,0.6,0.4)
            else:
                self.builtdata = builtdata
                self.traindata = traindata
            print("[MOD_HNSSVM] building HNS...")
            if not whole:
                self.hns = hnssvm.buildHns(self.builtdata,nsamples=self.nsamplesbuild,todrop=self.todrop,verbose=1)
            else:
                self.hns = hnssvm.buildHnsWhole(self.builtdata,self.todrop,verbose=1)
            print("[MOD_HNSSVM] ... done building HNS!")
            self.built = 1
        if builtdata is not None:
            self.builtdata = builtdata
        if traindata is not None:
            self.traindata = traindata

    def useBuiltHns(self,hns,builtdata=None,traindata=None):
        if builtdata is None or traindata is None:
            nsample = min(150000,len(self.nomdata))
            splitbuiltdata,splittraindata,_ = hnssvm.subsampleAndSplit(self.nomdata,nsample,0.6,0.4)
            if builtdata is None:
                self.builtdata = splitbuiltdata
            else:
                self.builtdata = builtdata
            if traindata is None:
                self.traindata = splittraindata
            else:
                self.traindata = traindata
        self.hns = hns
        self.built = 1

    def taskDone(future):
        try:
            res = future.result()
        except TimeoutError as error:
            print("Function took longer than %d seconds" % error.args[1])
        except Exception as error:
            print("Function raised %s" % error)

    def performGridSearch(self,params_grid,traindata,traingt,testdata,testgt):
        from sklearn.model_selection import ParameterGrid
        from pebble import ProcessPool
        from concurrent.futures import TimeoutError
        bestPhi=0.0
        bestTpr=0.0
        bestTnr=0.0
        bestParams=None
        futures = []
        with ProcessPool(max_workers=10, max_tasks=40) as pool:
            for param in ParameterGrid(params_grid):
                #import pdb; pdb.set_trace()
                # tpr,tnr,phi,aparam = testParams(traindata,traingt,testdata,testgt,param)
                # if phi> bestPhi:
                #     bestPhi = phi
                #     bestTpr = tpr
                #     bestTnr = tnr
                #     bestParams = aparam
                future = pool.schedule(testParams,(traindata,traingt,testdata,testgt,param),timeout=60)
#                future.add_done_callback(taskDone)
                futures.append(future)
        for f in futures:
            if f.done():
                #import pdb; pdb.set_trace()
                try:
                    tpr,tnr,phi,params = f.result()
                except Exception as e:
                    tpr = 0.0; tnr = 0.0; phi = 0.0; params = {'C':'0','gamma':'0','kernel':'None'}
                    print(f"Exception {e}")
                if phi>bestPhi:
                    bestPhi = phi
                    bestTpr = tpr
                    bestTnr = tnr
                    bestParams = params
        print(f"All done. With C {bestParams['C']} G {bestParams['gamma']} K {bestParams['kernel']} we got TPR {bestTpr} TNR {bestTnr} PHI {bestPhi}")
        return bestParams,bestPhi

    def trainHns(self, builtdata=None, traindata=None):
        if self.built==0:
            if builtdata is None and traindata is None:
                nsample = min(150000,len(self.nomdata))
                self.builtdata,self.traindata, _=hnssvm.subsampleAndSplit(self.nomdata,nsample,0.6,0.4)
            else:
                self.builtdata = builtdata
                self.traindata = traindata
            print("[MOD_HNSSVM] building HNS...")
            self.hns = hnssvm.buildHns(self.builtdata,nsamples=self.nsamplesbuild,todrop=self.todrop,verbose=1)
            print("[MOD_HNSSVM] ... done building HNS!")
            self.built = 1
        if builtdata is not None:
            self.builtdata = builtdata
        if traindata is not None:
            self.traindata = traindata
        print("[MOD_HNSSVM] Running HNS...")
        #import pdb; pdb.set_trace()
        simsPath = 'sims_simsMat_targetsUsed_'+self.getModuleLabel()+'.bz2'
        import os
        if os.path.exists(simsPath):
            print(f"Found sims file at {simsPath}. Using it")
            import joblib
            sims,simsMat,targetsUsed,self.nbuildUsed,self.ntrainUsed = joblib.load(simsPath)
            #sims,simsMat,targetsUsed = joblib.load(simsPath); self.nbuildUsed = self.nsamplesbuild; self.ntrainUsed = self.nsamplestrain
            #import pdb; pdb.set_trace()
        else:
            sims,simsMat,targetsUsed,nbuildUsed,ntrainUsed = hnssvm.runHns(self.hns, self.builtdata, self.traindata, self.nsamplesbuild,self.nsamplestrain, self.targetcol,self.targets,self.todrop)
            self.nbuildUsed = nbuildUsed
            self.ntrainUsed = ntrainUsed
            import joblib
            joblib.dump([sims,simsMat,targetsUsed,nbuildUsed,ntrainUsed],simsPath)
        print("[MOD_HNSSVM] ... done running HNS!")
        # generate gt/labels array
        gt=np.concatenate((np.ones(self.ntrainUsed),np.ones(self.ntrainUsed)*3))
        features = None
        if self.mode==1:
            simsrearanged = hnssvm.rearangeSims(sims,self.nbuildUsed,self.ntrainUsed)
            lows=np.concatenate((simsrearanged[0],simsrearanged[1]))
            higs=np.concatenate((simsrearanged[2],simsrearanged[3]))
            df=pd.DataFrame(data={'lows':lows,'higs':higs})
            self.trainfeatures = df
            self.traingt = gt
            self.meantrainlows = np.mean(df['lows'])
            self.meantrainhigs = np.mean(df['higs'])
            self.stdtrainlows = np.std(df['lows'])
            self.stdtrainhigs = np.std(df['higs'])
            features = df
        if self.mode==2:
            simsMatRearanged = hnssvm.rearangeSimsMats(simsMat,self.nbuildUsed,self.ntrainUsed)
            dfMat = pd.concat([pd.DataFrame(data=np.concatenate([simsMatRearanged[0],simsMatRearanged[1]])).add_prefix('lows_'),pd.DataFrame(data=np.concatenate([simsMatRearanged[2],simsMatRearanged[3]])).add_prefix('higs_')],axis=1)
            dfMix = dfMat[dfMat.columns[1::2]].multiply(np.array(dfMat[dfMat.columns[0::2]]))
            #import pdb; pdb.set_trace()
            newcols = self.builtdata.drop(self.todrop,axis=1).columns
            renames = {'lows_'+str(c*2):'l_'+newcols[c] for c in range(0,len(newcols))}
            {renames.update({'lows_'+str(c*2+1):'li_'+newcols[c]}) for c in range(0,len(newcols))}
            {renames.update({'higs_'+str(c*2):'h_'+newcols[c]}) for c in range(0,len(newcols))}
            {renames.update({'higs_'+str(c*2+1):'hi_'+newcols[c]}) for c in range(0,len(newcols))}
            dfMat = dfMat.rename(columns=renames)
            self.trainfeaturesMat = dfMat
            self.traingtMat = gt
            features = dfMat
        # PERFORM A GRID SEARCH 
        print("[MOD_HNSSVM] Performing grid search for SVC params...")
        #import pdb; pdb.set_trace()
        param_grid = {'C':[1,3,10,30,100],'gamma':['scale',1,0.1,0.001,0.0001], 'kernel':['rbf']}
        bestParams,bestPhi = self.performGridSearch(param_grid,features,gt,features,gt)
        print(f"[MOD_HNSSVM] ... done! Params C {bestParams['C']} Gamma {bestParams['gamma']} Kernel {bestParams['kernel']}")
        clf = svm.SVC(C=bestParams['C'],gamma=bestParams['gamma'],kernel=bestParams['kernel'],probability=True)
        clf.fit(features,gt)
        preds = clf.predict(features)
        if self.mode==1:
            self.clf = clf
            self.trained = 1
            self.labelModel()
        if self.mode==2:
            self.clfMat = clf
            self.trained = 2
            self.labelModel()
        tpr,tnr,phi = hnssvm.phi(gt,preds,3,1)
        return tpr,tnr,phi

    def processHit(self, hit, plot=False):
        if self.mode==1:
            clf = self.clf
        if self.mode==2:
            clf = self.clfMat
        pred,features = hnssvm.classifySamples(self.hns,self.builtdata,self.nbuildUsed,self.targetcol,self.targets,self.todrop,clf=clf,samples=hit, explain=self.explainability_enabled,mode=self.mode)
        #import pdb; pdb.set_trace()
        if plot:
            self.plotClassifier(features)
        if self.mode==1:
            if features['lows'].iloc[0] < (self.meantrainlows - self.stdtrainlows*self.stdthreshold) or features['lows'].iloc[0] > (self.meantrainlows + self.stdtrainlows*self.stdthreshold) or features['higs'].iloc[0] < (self.meantrainhigs - self.stdtrainhigs*self.stdthreshold) or features['higs'].iloc[0] > (self.meantrainhigs + self.stdtrainhigs*self.stdthreshold):
                pred = pred+100        
        return pred,features


    def isSampleNew(self, sample,newandused=False):
        data2search = self.builtdata
        if newandused:
            data2search = self.builtdata.iloc[0:self.nbuildUsed]
        found = pd.concat([data2search,sample]).duplicated().iloc[-1]
        return not found
        
    def explainPrediction(self,features,gt,method=1, nfeatures=20):
        # method = 1 sklearn.inspection.permutation_importance
        # method = 2 jackknife col removal & clf
        if method==1:
            from sklearn.inspection import permutation_importance
            if self.mode==1:
                clf = self.clf
            if self.mode==2:
                clf = self.clfMat
            import pdb; pdb.set_trace()
            perm_importance = permutation_importance(clf,features,gt)
            sorted_idx = list(reversed(perm_importance.importances_mean.argsort()))
            #import joblib
            #joblib.dump(perm_importance,'perm_importance.bz2')
            if nfeatures > 0:
                sorted_idx = sorted_idx[0:nfeatures]
            print(f"returning {nfeatures} features")
            return features.columns[sorted_idx],perm_importance.importances_mean[sorted_idx],perm_importance.importances_std[sorted_idx]
        if method==2:
            preds = self.clfMat.predict_proba(features)
            #import pdb; pdb.set_trace()
            explainDist = np.zeros((len(features),len(self.jkCols)))
            explainContr = np.zeros((len(features),len(self.jkCols)))
            for i,(f,c) in enumerate(zip(self.jkCols,self.jkClfs)):
                aJkFeatures = features.drop(f,axis=1)
                jkPreds = c.predict_proba(aJkFeatures)
                explainDist[:,i] = [np.linalg.norm(j-p) for j,p in zip(jkPreds,preds)]
                explainContr[:,i] = preds[:,-1]-jkPreds[:,-1]
            return [features.columns[c][2:] for c in range(0,len(features.columns)//2,2)] ,explainDist,explainContr

        return None,None,None

    def buildJacknifeClfs(self):
        ncols = len(self.trainfeaturesMat.columns)//2
        self.jkCols = []
        self.jkClfs = []
        for c in range(0,ncols,2):
            jkCols = [self.trainfeaturesMat.columns[c],self.trainfeaturesMat.columns[(c+1)],self.trainfeaturesMat.columns[(c+ncols)],self.trainfeaturesMat.columns[(c+ncols+1)]]
            aJkFeatures = self.trainfeaturesMat.drop(jkCols,axis=1)

            clf = svm.SVC(C=self.clfMat.C,gamma=self.clfMat.gamma,kernel=self.clfMat.kernel,probability=True)
            clf.fit(aJkFeatures,self.traingtMat)
            self.jkCols.append(jkCols)
            self.jkClfs.append(clf)


# FROM HERE, DEPRECATED CODE

    def plotClassifier(self, features=None, exportFile=None):
        import matplotlib.pyplot as plt
        if self.clf is None:
            print("Classifier not yet trained")
            return
        minPlot = 0
        maxPlot = 1
        step = 0.002
        xx,yy=np.meshgrid(np.arange(minPlot,maxPlot,step),np.arange(minPlot,maxPlot,step))
        Z = self.clf.predict(np.c_[xx.ravel(),yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.6)
        if features is not None:
            for f in range(len(features)):
                feature = features.iloc[f]
                plt.scatter(feature['lows'],feature['higs'],c='black')
        if exportFile is not None:
            plt.savefig(exportFile)


