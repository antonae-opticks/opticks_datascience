import sys 
import path_inserts
import module_rf as modrf
import module_rf_constants_mongo as modct
import joblib

if __name__== "__main__":
    if len(sys.argv) < 3:
        print(f"Client for predicting with module_rf: ERROR! Usage {sys.argv[0]} mrf.bz2 afile.json predict_output")
        sys.exit()
    print("Loading modules... ",end='',flush=True)
    mrf = joblib.load(sys.argv[1])
    mrf.hotEncoders = joblib.load(sys.argv[1]+'.hotencoders.bz2')
    print("Done!")
#    mrf.selectedFields = modct.defaultSelectedFields
#    mrf.preprocessor.selectedFields = modct.defaultSelectedFields
    fid = open(sys.argv[2])
    lines = fid.readlines()
    preds = []
    lastper = 0
    niter = len(lines)
    for i,l in enumerate(lines):
        #import pdb; pdb.set_trace()
        preds.append(mrf.processHit(l))
        perdone = int((i/niter)*100)
        if perdone>lastper:
            lastper = perdone
            print(f"Done {i} hits ({perdone}%)")
        if i<100:
            print(f"{preds[-1]:.3f},",end='',flush=True)
    joblib.dump(preds,sys.argv[3])
