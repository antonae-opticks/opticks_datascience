import module_preprocessor
import pandas as pd

class Module:

    saveModelPath = ''
    saveTrainPath = ''
    hotEncoders = {}
    moduleId = ''
    modelId = ''
    module_preprocessor = None
    moduleLabel=''

    def __init__(self):
        self.selectedFields = []
        self.fieldLabels = []
        self.parsedFields = []
        self.hotencFields = []
        self.hotEncoders = {} # one hot encoder per field
        self.module_preprocessor = None
        import random
        import string
        self.moduleLabel =  ''.join(random.choice(string.ascii_lowercase) for i in range(6))

        
    def labelModel(self, label=''):
        if len(self.modelId)> 0 and len(label)==0:
            return
        from datetime import datetime
        now = datetime.now()
        date = now.strftime("%Y%m%d%H%M")
        if len(label)>0 and label[0] != '_':
            label = "_"+label
        self.modelId = self.moduleId+label+"_"+date

    def setModuleLabel(self,label):
        self.moduleLabel = label

    def getModuleLabel(self):
        if len(self.moduleLabel)<1:
            import random
            import string
            self.moduleLabel =  ''.join(random.choice(string.ascii_lowercase) for i in range(6))
        return self.moduleLabel

        
    def hotEncodeFields(self,dataPd, hotencFields):
#        import pdb; pdb.set_trace()
        from sklearn.preprocessing import OneHotEncoder
        ncats=0
        for h in hotencFields:
            #import pdb; pdb.set_trace()
            if not pd.api.types.is_numeric_dtype(dataPd[h]):
                dataPd.loc[dataPd[h]!=dataPd[h],h]='!' # substitute NaNs with !
            else:
                dataPd.loc[dataPd[h]!=dataPd[h],h]=0.0
            dataPd[h] = dataPd[h].astype(object)
            if h not in self.hotEncoders.keys():
                #if h=='dpr':
                    #import pdb; pdb.set_trace()
                self.hotEncoders[h] = OneHotEncoder(sparse=False, handle_unknown='ignore')
                encoded = self.hotEncoders[h].fit_transform(dataPd[h].values.reshape(-1,1)).transpose()
            else:
                encoded = self.hotEncoders[h].transform(dataPd[h].values.reshape(-1,1)).transpose()
            cats = self.hotEncoders[h].categories_[0]
            ienc=0
            for c in cats:
                dataPd[str(h)+"_"+str(c)] = encoded[:][ienc]
                ienc=ienc+1
            ncats=ncats+len(cats)
        for h in hotencFields:
            dataPd.drop(h,axis=1,inplace=True)
        return dataPd, ncats
            
    def processHit(self,hit):
        try:
            return self.notImplementedException()
        except Exception as detail:
            print("Error ", detail)
        return None

    def setSaveModelPath(self,path):
        self.saveModelPath = path

    def setSaveTrainPath(self,path):
        self.saveTrainPath = path
    
    def getFields(self):
        return self.selectedFields, self.fieldLabels, self.parsedFields, self.hotencFields

    def setFields(self, selectedFields,fieldLabels, parsedFields, hotencFields):
        if len(selectedFields) != len(fieldLabels):
            print(f"Error. Len of selectedFields {len(selectedFields)} differs from len of fieldLabels {len(fieldLabels)}")
            return -1
        self.selectedFields = selectedFields
        self.fieldLabels = fieldLabels
        self.parsedFields = parsedFields
        for h in hotencFields:
            if (h not in fieldLabels) and (h not in parsedFields):
                print(f"Error, requesting hot enconding for field {h}, but it is not in selected fields")
            return -3
        self.hotencFields = hotencFields

    def setPreprocessor(self,preprocessor):
        self.module_preprocessor = preprocessor

    def getPreprocessor(self):
        return self.module_preprocessor
        
    def notImplementedException (self):
        raise Exception("Not implemented")
        
