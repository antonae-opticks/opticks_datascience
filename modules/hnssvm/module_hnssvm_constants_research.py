defaultSelectedFields = [
                         'security:clientdata:nt',
                         'security:clientdata:ornt',
                         'security:clientdata:plt',
                         'security:clientdata:tch',
                         'security:analysis:level',
                         'visitor:device:os:name',
                         'visitor:device:os:version',
                         'visitor:device:browser:name',
                         'visitor:device:browser:version',
                         'security:clientdata:ciphers',
                         'security:clientdata:wglv',
                         'security:clientdata:vnd',
                         'security:clientdata:dpr',
                         'security:clientdata:cntp',
                         'security:clientdata:mtp',

]

defaultFieldsLabels = [
                       'nt',
                       'ornt',
                       'plt',
                       'tch',
                       'risk_level',
                       'os_name',
                       'os_version',
                       'browser_name',
                       'browser_version',
                       'ciphers',
                       'wglv',
                       'vnd',
                       'dpr',
                       'connection_type',
                       'mtp',
]

defaultParsedFields = ['os_version',
                      'browser_version',
]

defaultHotencFields = []

def getDictVars4(adict,key1,key2,key3,key4):
    try:
        return adict.get(key1).get(key2).get(key3).get(key4)
    except:
        return f"No_value_{key1}_{key2}_{key3}_{key4}"

def getDictVars3(adict,key1,key2,key3):
    try:
        return adict.get(key1).get(key2).get(key3)
    except:
        return f"No_value_{key1}_{key2}_{key3}"

def getDictVars2(adict,key1,key2):
    try:
        return adict.get(key1).get(key2)
    except:
        return f"No_value_{key1}_{key2}"

def getDictVars1(adict,key1):
    try:
        return adict.get(key1)
    except:
        return f"No_value_{key1}"

def getDictVars(adict):
    ret = {}
    ret['nt'] = getDictVars3(adict,'security','clientdata','nt')
    ret['ornt'] = getDictVars3(adict,'security','clientdata','ornt')
    ret['plt'] = getDictVars3(adict,'security','clientdata','plt')
    ret['tch'] = getDictVars3(adict,'security','clientdata','tch')
    ret['risk_level'] = getDictVars3(adict,'security','analysis','level')
    ret['os_name'] = getDictVars4(adict,'visitor','device','os','name')
    ret['os_version'] = getDictVars4(adict,'visitor','device','os','version')
    ret['browser_name'] = getDictVars4(adict,'visitor','device','browser','name')
    ret['browser_version'] = getDictVars4(adict,'visitor','device','browser','version')
    ret['ciphers'] = getDictVars3(adict,'security','clientdata','ciphers')
    ret['wglv'] = getDictVars3(adict,'security','clientdata','wglv')
    ret['vnd'] = getDictVars3(adict,'security','clientdata','vnd')
    ret['dpr'] = getDictVars3(adict,'security','clientdata','dpr')
    ret['connection_type'] = getDictVars3(adict,'security','clientdata','cntp')
    ret['mtp'] = getDictVars3(adict,'security','clientdata','mtp')
    return ret
