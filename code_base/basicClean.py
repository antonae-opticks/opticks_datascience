import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn' WARNING, BE CAUTIOUS WHEN DISABLING WARNINGS

def parseTimezone(strTime):
    ret = [-10000,0]
    try:
        val = float(strTime)
        if val>10000:
            return ret
        return [val,1]
    except:
        return ret

def parsePlatform(strPlt):
    ret = ["","",0]
    if len(str(strPlt))<1:
        return ret
    try:
        split = strPlt.split();
    except:
        return ret
    if len(split)!=2:
        ret[0] = split[0]
        return ret
    return split[0],split[1],1

def parseNetworkSpeed(strSpd):
    ret = [-1,0]
    try:
        val = float(strSpd)
        if val>10000:
            return ret
        return [val,1]
    except:
        return ret

def parseRtt(strRtt):
    ret = [-1000,0]
    try:
        val = float(strRtt)
        if val>100000:
            return ret
        return [val,1]
    except:
        return ret

def parseFlv(strFlv):
    ret = [-1,0]
    if strFlv == 'true':
        return [1,1]
    if strFlv == 'false':
        return [0,1]
    return ret

def parseMtp(strMtp):
    ret = [-1,0]
    try:
        val = int(strMtp)
        if val>10000:
            return ret
        return [val,1]
    except:
        return ret

def parseInt(strInt, max = 10000):
    ret = [-1,0]
    try:
        val = int(strInt)
        if val > max:
            return ret
        return [val,1]
    except:
        return ret

def parseFloat(strFlt, max = 10000.0):
    ret = [-1000.0,0]
    try:
        val = float(strFlt)
        if val>max:
            return ret
        return [val,1]
    except:
        return ret

def basicClean(d, inplace=False, novalue='NoValue', oldClean=0):
    if not inplace:
        d=d.copy()
    renamedictColons = {'security:analysis:level':'risk_level',
                  'security:analysis:score':'score',
                  'security:clientdata:ah':'ah',
                  'security:clientdata:aw':'aw',
                  'security:clientdata:ih':'ih',
                  'security:clientdata:iw':'iw',
                  'security:clientdata:dm':'dm',
                  'security:clientdata:dpr':'dpr',
                  'security:clientdata:evln':'evln',
                  'security:clientdata:flv':'flv',
                  'security:clientdata:fpv':'fpv',
                  'security:clientdata:frm':'frm',
                  'security:clientdata:hsfc':'hsfc',
                  'security:clientdata:mtp':'mtp',
                  'security:clientdata:ornt':'ornt',
                  'security:clientdata:plt':'plt',
                  'security:clientdata:rtt':'rtt',
                  'security:clientdata:scd':'scd',
                  'security:clientdata:spd':'spd',
                  'security:clientdata:tch':'tch',
                  'security:clientdata:tz':'tz',
                  'security:clientdata:lng':'lng',
                  'security:clientdata:nt':'nt',
                  'security:clientdata:oscpu':'oscpu',
                  'security:clientdata:hls':'hls',
                  'security:clientdata:cntp':'cntp',
                  'security:clientdata:a43':'a43',
                  'security:clientdata:a44':'a44',
                  'security:clientdata:av':'av',
                  'security:clientdata:ua':'ua_client',
                  'visitor:device:extras:max_image_height':'max_image_height',
                  'visitor:device:extras:max_image_width':'max_image_width',
                  'visitor:device:extras:resolution_height':'resolution_height',
                  'visitor:device:extras:resolution_width':'resolution_width',
                  'visitor:headers:User-Agent':'ua_headers',
                  'visitor:network:geo:latitude':'latitude',
                  'visitor:network:geo:longitude':'longitude',
    }
    renamedictPipes = {'security|analysis|level':'risk_level',
                  'security|analysis|score':'score',
                  'security|clientdata|ah':'ah',
                  'security|clientdata|aw':'aw',
                  'security|clientdata|ih':'ih',
                  'security|clientdata|iw':'iw',
                  'security|clientdata|dm':'dm',
                  'security|clientdata|dpr':'dpr',
                  'security|clientdata|evln':'evln',
                  'security|clientdata|flv':'flv',
                  'security|clientdata|fpv':'fpv',
                  'security|clientdata|frm':'frm',
                  'security|clientdata|hsfc':'hsfc',
                  'security|clientdata|mtp':'mtp',
                  'security|clientdata|ornt':'ornt',
                  'security|clientdata|plt':'plt',
                  'security|clientdata|rtt':'rtt',
                  'security|clientdata|scd':'scd',
                  'security|clientdata|spd':'spd',
                  'security|clientdata|tch':'tch',
                  'security|clientdata|tz':'tz',
                  'security|clientdata|lng':'lng',
                  'security|clientdata|nt':'nt',
                  'security|clientdata|oscpu':'oscpu',
                  'security|clientdata|hls':'hls',
                  'security|clientdata|cntp':'cntp',
                  'security|clientdata|a43':'a43',
                  'security|clientdata|a44':'a44',
                  'security|clientdata|av':'av',
                  'security|clientdata|ua':'ua_client',
                  'visitor|device|extras|max_image_height':'max_image_height',
                  'visitor|device|extras|max_image_width':'max_image_width',
                  'visitor|device|extras|resolution_height':'resolution_height',
                  'visitor|device|extras|resolution_width':'resolution_width',
                  'visitor|headers|User-Agent':'ua_headers',
                  'visitor|network|geo|latitude':'latitude',
                  'visitor|network|geo|longitude':'longitude',
    }
    renamedictMongo = {'security:analysis:level':'risk_level',
                  'security:analysis:score':'score',
                  'clientData:ah':'ah',
                  'clientData:aw':'aw',
                  'clientData:ih':'ih',
                  'clientData:iw':'iw',
                  'clientData:dm':'dm',
                  'clientData:dpr':'dpr',
                  'clientData:evln':'evln',
                  'clientData:flv':'flv',
                  'clientData:fpv':'fpv',
                  'clientData:frm':'frm',
                  'clientData:hsfc':'hsfc',
                  'clientData:mtp':'mtp',
                  'clientData:ornt':'ornt',
                  'clientData:plt':'plt',
                  'clientData:rtt':'rtt',
                  'clientData:scd':'scd',
                  'clientData:spd':'spd',
                  'clientData:tch':'tch',
                  'clientData:tz':'tz',
                  'clientData:lng':'lng',
                  'clientData:nt':'nt',
                  'clientData:oscpu':'oscpu',
                  'clientData:hls':'hls',
                  'clientData:cntp':'cntp',
                  'clientData:a43':'a43',
                  'clientData:a44':'a44',
                  'clientData:av':'av',
                  'clientData:ua':'ua_client',
                  'visitor:device:extras:max_image_height':'max_image_height',
                  'visitor:device:extras:max_image_width':'max_image_width',
                  'visitor:device:extras:resolution_height':'resolution_height',
                  'visitor:device:extras:resolution_width':'resolution_width',
                  'visitor:headers:User-Agent':'ua_headers',
                  'visitor:network:geo:latitude':'latitude',
                  'visitor:network:geo:longitude':'longitude',
    }
    d.rename(columns=renamedictColons, inplace=True)
    d.rename(columns=renamedictPipes, inplace=True)
    d.rename(columns=renamedictMongo, inplace=True)
    if oldClean==1:
        for c in d.columns:
            if c not in {**renamedictColons,**renamedictPipes,**renamedictMongo}.values():
                d.drop(c,axis=1,inplace=True)
    if d.columns[-1][0:9] == 'Unnamed: ':
        d.drop(d.columns[-1],axis=1,inplace=True)
    #d.dropna(inplace=True)
    if oldClean == 1:
        if 'datetime' in d.columns:
            d.drop('datetime', axis=1, inplace=True)
#    if 'id' in d.columns:
#        d.drop('id',axis=1,inplace=True)
    if 'risk_level' in d.columns:
        d['risk_level'] = d['risk_level'].map({'high':3,'medium':2,'low':1})
    if 'score' in d.columns and d['score'].dtype != 'int64':
        d['score'][d['score']=='No_data_for_score']=50
        d['score'][d['score']=='None']=60
        d['score'] = d['score'].astype('int64')
    if 'timezone' in d.columns:
        timezone,timezone_flag = zip(*[parseTimezone(t) for t in d["timezone"]])
        d['timezone'] = timezone
    if 'platform' in d.columns:
        platform,_,_ = zip(*[parsePlatform(p) for p in d["platform"]])
        d['platform'] = platform
    if 'network_speed' in d.columns:
        speed,speed_flag = zip(*[parseNetworkSpeed(s) for s in d["network_speed"]])
        d['network_speed'] = speed
    if 'evln' in d.columns:
        evln,evlnflag = zip(*[parseInt(i) for i in d["evln"]])
        d['evln'] = evln
    if 'hls' in d.columns:
        hls,hlsflag = zip(*[parseInt(i) for i in d["hls"]])
        d['hls'] = hls
    if 'dm' in d.columns:
        dm,dmflag = zip(*[parseInt(i) for i in d["dm"]])
        d['dm'] = dm
    if 'mtp' in d.columns:
        mtp,mtpflag = zip(*[parseInt(i) for i in d["mtp"]])
        d['mtp'] = mtp
    if 'rtt' in d.columns:
        rtt,rttflag = zip(*[parseInt(i) for i in d["rtt"]])
        d['rtt'] = rtt
    if 'flv' in d.columns:
        flv,flvflag = zip(*[parseInt(i) for i in d["flv"]])
        d['flv'] = flv
    if 'spd' in d.columns:
        spd,spdflag = zip(*[parseInt(i) for i in d["spd"]])
        d['spd'] = spd
    if 'tch' in d.columns:
        tch,tchflag = zip(*[parseInt(i) for i in d["tch"]])
        d['tch'] = tch
    if 'scd' in d.columns:
        scd,scdflag = zip(*[parseInt(i) for i in d["scd"]])
        d['scd'] = scd
    if 'dpr' in d.columns:
        dpr,dprflag = zip(*[parseFloat(f) for f in d["dpr"]])
        d['dpr'] = dpr
    for c in d.columns:
        for u in d[c].unique():
            if type(u) is type('s'):
                if u[0:14] == 'Key_not_found_':
                    d[c][d[c]==u]=novalue
                if u[0:12] == 'No_data_for_':
                    d[c][d[c]==u]=novalue
                if oldClean == 1:
                    if u == '!':
                        d[c][d[c]==u]=np.nan
#    d['evln'][['evln']=='!']='-1'
    if not inplace:
        return d
    return None
        
