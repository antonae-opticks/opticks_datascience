import sys
sys.path.insert(1,'/home/users/aalbajes/code/')
sys.path.insert(1,'/home/users/aalbajes/code/code_base/')
sys.path.insert(1,'/home/users/aalbajes/code/db_access/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hns/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hnsSvmClassifier/')
sys.path.insert(1,'/home/users/aalbajes/code/modules/')
import module
import module_rf
import module_rf_constants as mrc
import module_expertrules_lite as mel
import module_mlp
import joblib 
import threading

class ModuleEnsemble(module.Module):
    defaultModelRfPath = 'modrf.bz2'
    defaultModelHnsPath = 'Data/modhns.bz2'
    defaultModelMlpPath = 'Data/mlp.bz2'
    modrf = None
    modex = None
    modhns = None
    modmlp = None

    def __init__(self, modelRfPath=None, modelHnsPath=None, modelMlpPath=None):
        if modelRfPath is None:
            modelRfPath = self.defaultModelRfPath
        if modelHnsPath is None:
            modelHnsPath = self.defaultModelHnsPath
        if modelMlpPath is None:
            modelMlpPath = self.defaultModelMlpPath
        self.modrf = joblib.load(modelRfPath)
        self.modex = mel.ModuleExpertRules(modelPath='data/rlz_scoresv2.bz2')
        self.modhns = joblib.load(self.defaultModelHnsPath)
        self.modmlp = module_mlp.ModuleMlp(modelPath=modelMlpPath)

    def modulesLabels(self):
        return "EnsembleAvg RF ExpLite HnsSvm Mlp GT"

    def determineGt(self,hit):
        strlow = '"level":"low"' 
        strhigh = '"level":"high"'
        strmed = '"level":"medium"'
        if hit.find(strlow)>-1:
            return 0.0
        if hit.find(strhigh)>-1:
            return 1.0
        if hit.find(strmed)>-1:
            return 0.5
        return -1.0

    def runRf(self,hit, pred):
        pred.append(self.modrf.processHit(hit))

    def runExp(self,hit, pred):
        pred.append(self.modex.processHit(hit))

    def runHns(self,hit, pred):
        ppHns = self.modhns.preprocess([hit])[0]
        pred.append(self.modhns.processHit(ppHns)[0][0][1])

    def runMlp(self,hit,pred):
        pred.append(self.modmlp.processHit(hit)[0])

    def processHit(self,hit):
        gt= self.determineGt(hit)
        predEx = []
        predRf = []
        predHns = []
        predMlp = []
        tRf = threading.Thread(target=self.runRf,args=(hit,predRf,))
        tRf.start()
#        predRf= self.modrf.processHit(hit)
#        predEx = self.modex.processHit(hit)
        tEx = threading.Thread(target=self.runExp,args=(hit,predEx,))
        tEx.start()
        tHns = threading.Thread(target=self.runHns,args=(hit,predHns,))
        tHns.start()
#        tMlp = threading.Thread(target=self.runMlp,args=(hit,predMlp,))
#        tMlp.start()
        self.runMlp(hit,predMlp)
        tRf.join()
        tEx.join()
        tHns.join()
#        tMlp.join()
        pred = (predRf[-1]+predEx[-1]+predHns[-1]+predMlp[-1])/4 # dirty average for now
        return pred, [predRf[-1],predEx[-1],predHns[-1],predMlp[-1]], ['randomForest','expertLite','hnssvm','mlp'],[0,0,0,0],gt
