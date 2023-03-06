import module
import module_expertrules_constants
import module_preprocessor
import badBotRule
import IframeRule
import MSISDNInjectionRule
import IpRIskRule
import ast
import InvalidAppNameRule
import ClassRule
import AppPlayStoreRule
import sys
import bypassAttemptRule
import joblib

sys.path.insert(1, 'Rules')

placeholders = ["cdgChecker", "RepeatedUserRule", "CampaignFpCDRealtimeRule",
                "MalwareAPKRule", "invalidChecksum", "AdultKeywordsRule", "ctmsBot", "reverseCdg", "pkFarm"]


class ModuleExpertRules(module.Module):
    rulesScores = {}
    scoreDict = {}

    def __init__(self, modelPath=None):
        self.selectedFields = module_expertrules_constants.defaultSelectedFields
        self.fieldLabels = module_expertrules_constants.defaultFieldsLabels
        self.rulesScores = module_expertrules_constants.defaultRulesScores
        self.scoreDict = joblib.load("Data/rlz_scores.bz2")

    def preProcessHit(self, jsonhit):
        preprocessor = module_preprocessor.ModulePreprocessor(self.selectedFields, self.fieldLabels)

        return preprocessor.parseHitJson(jsonhit)

    # PROCESSHIT MUST RETURN A DOUBLE 0-1 (MIN RISK - MAX RISK)
    def processHit(self, jsonhit):
        # Parse hit without cleaning
        hitMap = self.preProcessHit(jsonhit)

        #Get sorted triggers
        rules = self.expertRules(hitMap)
        print(f"Rules {rules}")
        if len(rules) >= 4:
            return 1.0
        else:
            return self.scoreDict[tuple(rules)]




    # Returns a sorted list of triggered methods
    def expertRules(self, hitMap):
        ruleList = []

        triggers = []
        try:
            triggers = ast.literal_eval(hitMap['triggeredMethods'])
        except:
            triggers = [hitMap['triggeredMethods']]

        # Execute each rule
        badBotRule.execute(hitMap, ruleList)

        IframeRule.execute(hitMap, ruleList)

        MSISDNInjectionRule.execute(hitMap, ruleList)

        IpRIskRule.execute(hitMap, ruleList)

        InvalidAppNameRule.execute(hitMap, ruleList)

        ClassRule.execute(hitMap, ruleList)

        AppPlayStoreRule.execute(hitMap, ruleList)

        bypassAttemptRule.execute(hitMap, ruleList)


        # Bypass GoodBotRule
        if "Good" in ",".join(triggers):
            ruleList = triggers

        # False positives detected with these two rules
        if "AppPlayStoreRule" in ruleList and "AppPlayStoreRule" not in triggers:
            ruleList.remove("AppPlayStoreRule")

        if "chromeHeadLess" in ruleList and "chromeHeadLess" not in triggers:
            ruleList.remove("chromeHeadLess")

        # Placeholders for not implemented rules
        for p in placeholders:
            if p in triggers:
                ruleList.append(p)

        return sorted(ruleList)
