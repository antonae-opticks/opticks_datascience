import sys
sys.path.insert(1,'.')
import path_inserts
import module_rf as modrf
import re
import joblib
import basicMetrics as bm
import os

if __name__== "__main__":
    if len(sys.argv) < 2:
        print(f"Client for module_rf, ERROR! Usage: {sys.argv[0]} traindataset.json [moduleID]")
        sys.exit()
    datapath = sys.argv[1]
    import os
    label = os.path.basename(sys.argv[1]).replace('.json','')
    moduleId = ''
    if len(sys.argv)>2:
        moduleId = sys.argv[2]    
    else:
        moduleId = label
    import os
    if not os.path.exists(moduleId):
        os.makedirs(moduleId)
    #import pdb; pdb.set_trace()
    mrf = modrf.ModuleRandomForest(preprocessorVersion=2)
    trainsetpath = os.path.basename(datapath)
    mrf.saveTrainPath = moduleId+"/"+moduleId+"_trainset.bz2"
    print(f"Well save training path to {mrf.saveTrainPath}")
#    trainscore = mrf.trainRF(mrf.saveTrainPath)
    trainscore = mrf.trainRF(datapath)
    mrf.labelModel(label)
    from datetime import datetime
    datenow = datetime.today().strftime("%Y%m%d%H%M")
    modulePath = moduleId+"/"+moduleId+"_"+datenow+".bz2"
    joblib.dump(mrf,modulePath)
    joblib.dump(mrf.hotEncoders,modulePath+'.hotencoders.bz2')
    print(f"Module stored at: {modulePath}")
