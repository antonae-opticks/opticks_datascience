import sys
import path_inserts
import module_hnssvm
import module_hnssvm_constants as mhc
import module_preprocessor
import joblib
import pandas as pd
import numpy as np
import hierarchicalNominalSimilarity as hns

# NSAMPLES TO BE USED
nsamplesbuild=280
nsamplestrain=100
defaultnsamplesbuild=1500
defaultnsamplestrain=40000
#nsamplesbuild=600
#nsamplestrain=600
explain=False

def trainHnssvmModel(data,selectedFields,fieldsLabels,parsedFields,hotencFields,output,label='',useHns=None, nsamplesbuild=defaultnsamplesbuild,nsamplestrain=nsamplestrain):
    mhs = module_hnssvm.ModuleHnsSvm(data=data,todrop=['risk_level'],targetcol='risk_level', nsamplesbuild=nsamplesbuild, nsamplestrain=nsamplestrain)
    mhs.selectedFields = selectedFields
    mhs.fieldsLabels = fieldsLabels
    mhs.parsedFields = parsedFields
    mhs.hotencFields = hotencFields
    ppPath = data+".ppHns.bz2"
    ppPath = data+".ppHns-v"+mhs.version+".bz2"
    import os
    if os.path.exists(ppPath) and os.path.getmtime(ppPath)> os.path.getmtime(data):
        print(f"Using found preprocessed data file at {ppPath}")
        import joblib
        ppData = joblib.load(ppPath)
        mhs.nomdata = ppData
    else:
        print(f"Preprocessing data...")
        fid = open(data)
        #import pdb; pdb.set_trace()
        mhs.nomdata,_ = mhs.preprocess(fid.readlines())
        print(f"Saving ppData on {ppPath}")
        import joblib
        joblib.dump(mhs.nomdata,ppPath)
    modulelabel = os.path.basename(data).replace('.json','')
    mhs.setModuleLabel(modulelabel)
    modulepath = modulelabel+'.bz2'
    if os.path.exists(modulepath):
        if not os.path.exists(ppPath) or os.path.getmtime(modulepath)> os.path.getmtime(ppPath):
            print(f"Using found module file at {modulepath}")
            mhs = joblib.load(modulepath)
        else:               
            if useHns is None:
                print("Building HNS...")
                mhs.buildHns()
                print("..done building HNS!")
                joblib.dump(mhs,modulepath)
            else:
                print("Using pre-built HNS...")
                #import pdb; pdb.set_trace()
                hns2use = joblib.load(useHns)
                mhs.useBuiltHns(hns2use)
    else:
        if useHns is not None:
            print("Using pre-built HNS...")
            #import pdb; pdb.set_trace()
            hns2use = joblib.load(useHns)
            mhs.useBuiltHns(hns2use)
    print("Training HNSSVM...")
    #import pdb; pdb.set_trace()
    phi = mhs.trainHns()
    print(f"Train returned PHI {phi}")
    if len(label)>0:
        mhs.labelModel(label)
    import joblib
    joblib.dump(mhs,output,compress=('bz2',3))

    
def parseParams(argv):
    params = {'dataset':'',
              'output_model':'',
              'hns_file':None,
              'samples_build':nsamplesbuild,
              'samples_train':nsamplestrain}
    for a in range(1,len(argv)):
        if argv[a]=='-d' and not len(argv)<a:
            params['dataset']=argv[a+1]
        if argv[a]=='-o' and not len(argv)<a:
            params['output_model'] = argv[a+1]
        if argv[a]=='-h' and not len(argv)<a:
            params['hns_file'] = argv[a+1]
        if argv[a]=='-sb' and not len(argv)<a:
            params['samples_build'] = int(argv[a+1])
        if argv[a]=='-st' and not len(argv)<a:
            params['samples_train'] = int(argv[a+1])
        if argv[a]=='-l' and not len(argv)<a:
            params['label'] = argv[a+1]
    return params

        

if __name__ == "__main__":
    if len(sys.argv)<5:
        print(f"Error. Usage {sys.argv[0]} -d dataset -d output_model [-h Hns file] [-sb samples_build(nsamplesbuild)] [-st samples_train(nsampelstrain)] [-l label]")
        sys.exit()
    else:
        # trainHnssvmModel(data,selectedFields,fieldsLabels,parsedFields,hotencFields,output):
        #import pdb; pdb.set_trace()
        params = parseParams(sys.argv)
        import os
        if len(params['label'])<1:
            params['label'] = os.path.basename(params['dataset']).replace('.json','')
        trainHnssvmModel(data=params['dataset'],selectedFields=mhc.defaultSelectedFields,fieldsLabels=mhc.defaultFieldsLabels,parsedFields=mhc.defaultParsedFields,hotencFields=[],output=params['output_model'], label=params['label'], useHns = params['hns_file'], nsamplesbuild=params['samples_build'],nsamplestrain=params['samples_train'])
