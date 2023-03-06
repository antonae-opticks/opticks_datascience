import sys
import joblib
sys.path.insert(1,'/home/users/aalbajes/code/')
sys.path.insert(1,'/home/users/aalbajes/code/code_base/')
sys.path.insert(1,'/home/users/aalbajes/code/db_access/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hns/')
sys.path.insert(1,'/home/users/aalbajes/code/categoricaldata/hnsSvmClassifier/')
import module
import module_expertrules_lite_constants
import module_preprocessor
import numpy as np

class ModuleExpertRules(module.Module):
    rulesScores = {}
    scoreDict = {}

    def __init__(self, modelPath=None):
        self.selectedFields = module_expertrules_lite_constants.defaultSelectedFields
        self.fieldLabels = module_expertrules_lite_constants.defaultFieldsLabels
        self.rulesScores = module_expertrules_lite_constants.defaultRulesScores
        self.scoreDict = joblib.load("Data/rlz_scores.bz2")

    def preProcessHit(self, jsonhit):
        preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields, self.fieldLabels)

        return preprocessor.parseHitJson(jsonhit)

    # PROCESSHIT MUST RETURN A DOUBLE 0-1 (MIN RISK - MAX RISK)
    def processHit(self, jsonhit):
        # Parse hit without cleaning
        hitMap = self.preProcessHit(jsonhit)
        #import pdb; pdb.set_trace()

        #Get sorted triggers
        rules = self.expertRules(hitMap)
#        print(f"Rules {rules}")
        if len(rules) < 1:
            return 0.0
        if len(rules) >= 4:
            return 1.0
        else:
            if tuple(rules) not in self.scoreDict.keys():
                score = 0.5 * len(rules)
            else:
                score = self.scoreDict[tuple(rules)]
            normscore = np.tanh(score)
 #           print(f"Score {score} normscore {normscore}")
            return normscore




    # Returns a sorted list of triggered methods
    def expertRules(self, hitMap):
        ruleList = []
        methods = hitMap['triggeredmethods']
        methods = methods.replace('[','').replace(']','').replace('\'','').split(',')

        for m in methods:
            rule = m.strip()
            if len(rule)>0:
                ruleList.append(rule)

        return sorted(ruleList)
