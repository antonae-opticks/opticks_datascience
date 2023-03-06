import module
import module_mlp_constants
import module_preprocessor
import joblib
import pandas 

class ModuleMlp(module.Module):
    def __init__(self, modelPath):
        self.selectedFields = module_mlp_constants.defaultSelectedFields
        self.fieldsLabels = module_mlp_constants.defaultFieldsLabels
        self.parsedFields = module_mlp_constants.defaultParsedFields
        self.preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields,self.fieldsLabels,self.parsedFields)
        if modelPath is not None:
            self.mlp = joblib.load(modelPath)
        else:
            self.mlp = None

    def preProcessHit(self,jsonhit):
        dataPd, dataGt = self.preprocessor.preProcessHit(jsonhit)
        return dataPd,dataGt

    def processHit(self,hit):
        if self.mlp is None:
            return [-1.2] # model not trained or loaded
        #import pdb; pdb.set_trace()
        if type(hit) == str:
            hitPd,_ = self.preProcessHit(hit)
        elif type(hit) == pandas.core.frame.DataFrame:
            hitPd = hit
        else:
            return [-1.1] # unknown input format
        if len(hitPd.columns) != self.mlp.input_shape[1]:
#            print(f"Dimensions missmatch: hit {len(hitPd.columns)} mlp {self.mlp.input_shape[1]}")
#            print(hitPd.columns)
            return [-1.0] # dimensions missmatch between input and trained model
        predict = self.mlp.predict(hitPd)
        return predict[:,-1] 

    def trainMlp(self,data): # data should be a clean DataFrame only with features columns and a [0-1] gt column
         import keras
         X = data.drop('gt',axis=1).values
         y = data['gt'].values
         input_ = keras.layers.Input(shape=X.shape[1:])
         hidden1 = keras.layers.Dense(60,activation="relu")(input_)
         hidden3 = keras.layers.Dense(10,activation="relu")(hidden1)
         output = keras.layers.Dense(1,activation="sigmoid")(hidden3)
         model = keras.Model(inputs=[input_],outputs=[output])
         model.compile(loss='binary_crossentropy',optimizer="adam",metrics=['accuracy'])
         model.fit(X,y,epochs=150,batch_size=100, verbose=0)
         self.mlp = model
         return model
         
    def getGraphModelSession(self):
        import keras
        import tensorflow as tf
        graph = tf.get_default_graph()
        session = tf.Session()
        return graph,self.mlp,session
