import sys
sys.path.insert(1,'/home/anton/Documents/code/code_base/')
sys.path.insert(1,'/home/anton/Documents/code/db_access/')
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hns/')
sys.path.insert(1,'/Users/bielcasals/Dropbox/opticks_datascience/code_base')
sys.path.insert(1,'/Users/bielcasals/Dropbox/opticks_datascience/db_access/')
sys.path.insert(1,'/Users/bielcasals/Dropbox/opticks_datascience/categoricaldata/hns')

import parseJson
import json
import numpy as np
import pandas as pd
import basicClean as bc
import myUaParser as uaparser

class ModulePreprocessor:
    selectedFields = []
    fieldLabels = []
    parsedFields = []
    #fieldsMap = {}
    #hitPd = None
    uaFields = [] # parsed UA fields
    otherFields = [] # other parsed fields
    withGt = False
    version = 1
    i2catPp = False
    def __init__(self, selectedFields,fieldLabels,parsedFields=[], withGt=False, version=1):
        if self.setSelectedFields(selectedFields,fieldLabels,parsedFields) <0:
            print("Couldn't correctly initialize modules preprocessor")
        else:
            self.selectedFields = selectedFields
            self.fieldLabels = fieldLabels
            self.parsedFields = parsedFields
        self.withGt = withGt
        if self.withGt and 'risk_level' not in fieldLabels:
            print("Ground truth selected for preprocessing, yet not risk_level field selected")
        self.version = version
            
    def setSelectedFields(self,selectedFields,fieldLabels,parsedFields=[]):
        if len(selectedFields) != len(fieldLabels):
            print(f"Error. Len of selectedFields {len(selectedFields)} differs from len of fieldLabels {len(fieldLabels)}")
            return -1
        self.uaFields = []
        self.otherFields = []
        for f in parsedFields:
            if f[0:3] == 'ua_':
                self.uaFields.append(f)
            else:
                self.otherFields.append(f)
        if len(self.uaFields)>0 and ('ua_headers'  not in fieldLabels):
            print(f"Error, requesting to parse UA fields without having selected any UA field")
            return -2
        self.selectedFields = selectedFields
        self.fieldLabels = fieldLabels
        self.parsedFields = parsedFields
        return len(selectedFields)

    def parseHitJson(self,jsonhit,funcParse=None):
        loadedjson = json.loads(jsonhit)
        if self.version<3:
            extractedFields = parseJson.extractSelected(self.selectedFields,loadedjson).split('\t')
            fieldsMap = {}
            if len(extractedFields) != len(self.fieldLabels):
                print("Error while parsing hit json")
                return None
            fieldsMap = {k:v for k,v in zip(self.fieldLabels,extractedFields)}
        if self.version==3:
            fieldsMap = funcParse(loadedjson)
        return fieldsMap

    def cleanFields(self,fieldsMap):
        if self.version>=2:
            import basicCleanV2 as bc2
            clean = bc2.basicClean(fieldsMap)
            return clean
        hitPd = pd.DataFrame(data=None,columns=fieldsMap.keys())
        hitPd.loc[0] = list(fieldsMap.values()) 
        bc.basicClean(hitPd,inplace=True)
        return hitPd
        

    def parseUa(self,strua, fields):
        uafields = uaparser.parseUserAgentFields(strua,fields)
        if self.version>=2:
            return uafields
        uaPd = pd.DataFrame(data=None,columns=uafields.keys())
        uaPd.loc[0] = list(uafields.values())
        return uaPd

    def parseOther(self,hitD,otherFields):
        #import pdb; pdb.set_trace()
        if 'midnight_seconds' in otherFields:
            from datetime import datetime
            if self.version==1:
                strDate = hitD['datetime'].values[0]
                strDate = strDate.replace('T',' ')
                strDate = strDate[0:18]
                #print("string date " +strDate)
                d = datetime.strptime(strDate,"%Y-%m-%d %H:%M:%S")
                hitD['midnight_seconds'] = [(d-d.replace(hour=0,minute=0,second=0)).total_seconds()]
                hitD.drop('datetime',axis=1,inplace=True)
            elif self.version>=2:
                strDate = hitD['datetime']
                strDate = strDate.replace('T',' ')
                strDate = strDate[0:18]
                #print("string date " +strDate)
                d = datetime.strptime(strDate,"%Y-%m-%d %H:%M:%S")
                hitD['midnight_seconds'] = (d-d.replace(hour=0,minute=0,second=0)).total_seconds()
                hitD.pop('datetime')
        if 'cdgciu' in otherFields:
            if self.version==1:
                datacdgciu = pd.DataFrame([list(c1+c2) for c1,c2 in zip(hitD['cdg'].tolist(),hitD['ciu'].tolist())]).add_prefix('cdgciu') 
                hitD.drop('ciu',axis=1,inplace=True)
                hitD.drop('cdg',axis=1,inplace=True)
                #import pdb; pdb.set_trace()
                hitD = pd.concat([hitD.reset_index(drop=True),datacdgciu.reset_index(drop=True)],axis=1)
            if self.version>=2:
                for n in range(0,len(hitD['cdg'])):
                    hitD['cdg'+str(n)] = hitD['cdg'][n]
                hitD.pop('cdg')
                for n in range(0,len(hitD['ciu'][0])):
                    hitD['ciu'+str(n)] = hitD['ciu'][n]
                hitD.pop('ciu')
        if 'httpsOn' in otherFields:
            if self.version==1:
                dataHttpsOn = pd.DataFrame([1 if h == 'https' else 0 for h in hitD['scheme'].tolist()]).add_prefix('httpsOn')
                hitD.drop('scheme',axis=1,inplace=True)
                hitD = pd.concat([hitD.reset_index(drop=True),dataHttpsOn.reset_index(drop=True)],axis=1)
            if self.version>=2:
                if hitD['scheme'] == 'https':
                    hitD['httpsOn']=1
                else:
                    hitD['httpsOn']=0
        if 'nt' in otherFields:
            if self.version==1:
                datant = pd.DataFrame(data=None,columns=['nt'+str(i) for i in range(0,len(hitD['nt'][0]))])
                datant.loc[0] = [int(i) for i in hitD['nt'][0]]
                hitD.drop('nt',axis=1,inplace=True)
                hitD = pd.concat([hitD.reset_index(drop=True),datant.reset_index(drop=True)],axis=1)
            if self.version>=2:
                #import pdb; pdb.set_trace()
                if hitD['nt'][0] == '!':
                    for n in range(0,9):
                        hitD['nt'+str(n)] = -1
                else:
                    for n in range(0,len(hitD['nt'])):
                        hitD['nt'+str(n)] = int(hitD['nt'][n])
                hitD.pop('nt')
        if 'rtt_diff' in otherFields:
            rttjs = hitD['rtt']
            rttha = hitD['x-ha-rtt']
#            import pdb; pdb.set_trace()
            if rttjs <0:
                hitD['rtt_diff'] = 1000
            else:
                hitD['rtt_diff'] = np.abs(rttjs-rttha)
        if 'rtt_var_ratio' in otherFields:
            rtt = hitD['x-ha-rtt']
            var = hitD['x-ha-rtt-var']
            if rtt != 0:
                hitD['rtt_var_ratio'] = var/rtt
            else:
                hitD['rtt_var_ratio'] = 0.0
        if 'x-ssl-uid' in otherFields:
            if self.i2catPp:
                if hitD['x-ssl-uid'] != hitD['x-ssl-uid']:
                    hitD['x-ssl-uid'] = 0 
                else:
                    hitD['x-ssl-uid'] = 1
        if 'x-ssl-sid' in otherFields:
            if self.i2catPp:
                if hitD['x-ssl-sid'] != hitD['x-ssl-sid']:
                    hitD['x-ssl-sid'] = 0 
                else:
                    hitD['x-ssl-sid'] = 1
        if 'x-ssl-resumed' in otherFields:
            if self.i2catPp:
                if hitD['x-ssl-resumed'] != hitD['x-ssl-resumed']:
                    hitD['x-ssl-resumed'] = 0 
                else:
                    hitD['x-ssl-resumed'] = 1
        if 'x-ssl-alg-keysize' in otherFields:
            if self.i2catPp:
                if hitD['x-ssl-alg-keysize'][0:2] == '128':
                    hitD['x-ssl-alg-keysize'] = 0
                else:
                    hitD['x-ssl-alg-keysize'] = 1
        if 'x-ssl-cipher' in otherFields:
            if self.i2catPp:
                if hitD['x-ssl-cipher'] == 'ECDHE-RSA-AES256-GCM-SHA384':
                    hitD['x-ssl-cipher'] = 1
                else:
                    hitD['x-ssl-cipher'] = 0
        if 'x-ha-O' in otherFields:
            if self.i2catPp:
                if 'x-ha-tcp' in hitD.keys():
                    hitD['x-ha-O'] = hitD['x-ha-tcp'].split(';')[-1].split('=')[-1]
                else:
                    hitD['x-ha-O'] = -1
        if 'x-ha-U' in otherFields:
            if self.i2catPp:
                if 'x-ha-tcp' in hitD.keys():
                    hitD['x-ha-U'] = hitD['x-ha-tcp'].split(';')[0].split('=')[-1]
                else:
                    hitD['x-ha-u'] = -1
        if 'os_version' in otherFields:
            if type(hitD) == dict:
                hitD['os_version'] = '.'.join(hitD['os_version'].split(sep='.')[0:2])
            else:
                hitD['os_version'] = '.'.join(hitD['os_version'][0].split(sep='.')[0:2])
        if 'browser_version' in otherFields:
            if type(hitD) == dict:
                hitD['browser_version'] = '.'.join(hitD['browser_version'].split(sep='.')[0:2])
            else:
                hitD['browser_version'] = '.'.join(hitD['browser_version'][0].split(sep='.')[0:2])
        return hitD

    def preProcessHit(self,jsonhit,returnDict = False,funcParse=None):
        #import pdb; pdb.set_trace()
        gt = 0.0
        fieldsMap = self.parseHitJson(jsonhit,funcParse)
        hitD = self.cleanFields(fieldsMap)
        if 'ua_headers' in fieldsMap.keys() and len(self.uaFields)>0:
            uaD = self.parseUa(fieldsMap['ua_headers'],self.uaFields)
            if self.version==1:
                hitD = pd.concat([hitD,uaD],axis=1)
                hitD.drop('ua_headers',axis=1,inplace=True)
            if self.version>=2:
                hitD.pop('ua_headers')
                hitD = {**hitD,**uaD}
        if len(self.otherFields)>0:
            hitD = self.parseOther(hitD,self.otherFields)
        if self.withGt:
            if self.version==1:
                gt = hitD['risk_level'].values[0]
                hitD.drop('risk_level',axis=1,inplace=True)
            if self.version>=2:
                gt = hitD['risk_level']
                hitD.pop('risk_level')
        if self.version>=2:
            if returnDict:
                return hitD,gt
            hitPd = pd.DataFrame(hitD,index=[0])
            return hitPd,gt
        return hitD,gt

    def getProcessedFields(self,fieldsLabels, parsedFields):
        ppFields = fieldsLabels.copy()
        uaFields = []
        #import pdb; pdb.set_trace()
        for f in parsedFields:
            if f[0:3] == 'ua_':
                uaFields.append(f)
        if 'ua_headers' in ppFields and len(uaFields)>0:
            ppFields.remove('ua_headers')
            ppFields = ppFields + uaFields
        return ppFields
