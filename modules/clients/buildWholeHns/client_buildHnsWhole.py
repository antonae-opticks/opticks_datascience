import sys
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hns/')
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hnsSvmClassifier/')
sys.path.insert(1,'/home/anton/Documents/code_base/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hns/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hnsSvmClassifier/')
sys.path.insert(1,'/home/users/aalbajes/code/modules/')
sys.path.insert(1,'/home/users/aalbajes/code/code_base/')
sys.path.insert(1,'/home/users/aalbajes/code/db_access/')
import module_hnssvm 
import module_hnssvm_constants as mhc
import module_preprocessor
import hnsSvmClassifier as hnssvm

if __name__ == '__main__':
    import sys
    mhs = module_hnssvm.ModuleHnsSvm(data=sys.argv[1],todrop=['risk_level'],targetcol='risk_level',nsamplesbuild=600,nsamplestrain=600)
    mhs.selectedFields = mhc.defaultSelectedFields
    mhs.fieldLabels = mhc.defaultFieldsLabels
    mhs.parsedFields = mhc.defaultParsedFields
    mhs.hotencFields = []
    maxsamples = int(sys.argv[2])
    #import pdb;pdb.set_trace()
    fid = open(sys.argv[1])
    mhs.nomdata,_ = mhs.preprocess(fid.readlines())
    import joblib
    #mhs.nomdata,_ = joblib.load('ppNomData_hnssvm-v1.1.1.bz2')
    joblib.dump(mhs.nomdata,'ppNomData.bz2')
    myhns = hnssvm.buildHnsWhole(mhs.nomdata,['risk_level'],verbose=1,maxsamples=maxsamples)
    joblib.dump(myhns,'myhns.bz2')
                                     
