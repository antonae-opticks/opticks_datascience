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

def parseInt(strInt, max = 10000, errVal = -1):
    ret = [errVal,0]
    try:
        val = int(strInt)
        if val > max:
            return ret
        return [val,1]
    except:
        return ret

def parseFloat(strFlt, max = 10000.0, errVal = -1000.0):
    ret = [errVal,0]
    try:
        val = float(strFlt)
        if val>max:
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

def renameKey(d, oldKey, newKey):
    if oldKey in d.keys():
        d[newKey] = d.pop(oldKey)

def renameKeys(d,keys2rename):
    for k in keys2rename.keys():
        renameKey(d,k,keys2rename[k])

def basicClean(d,novalue='Novalue'):
    renameKeys(d,renamedictColons)
    renameKeys(d,renamedictPipes)
    if 'Unnamed' in d.keys():
        d.pop('Unnamed')
    if 'risk_level' in d.keys():
        if d['risk_level']=='high':
            d['risk_level'] = 3
        if d['risk_level']=='medium':
            d['risk_level'] = 2
        if d['risk_level']=='low':
            d['risk_level'] = 1
    if 'score' in d.keys():
        score,_ = parseInt(d['score'])
        d['score']=score
    if 'timezone' in d.keys():
        tz,tzflag = parseFloat(d['timezone'])
        d['timezone'] = tz
    if 'platform' in d.keys():
        platform,_,_=parsePlatform(d['platform'])
        d['platform'] = platform
    if 'network_speed' in d.keys():
        ns,_ = parseFloat(d['network_speed'],errVal=-1)
        d['network_speed'] = ns
    if 'evln' in d.keys():
        evln,evlnflag = parseInt(d['evln'])
        d['evln'] = evln
    if 'hls' in d.keys():
        hls,hlsflag = parseInt(d['hls'])
        d['hls'] = hls
    if 'dm' in d.keys():
        dm,dmflag = parseInt(d['dm']) 
        d['dm'] = dm
    if 'mtp' in d.keys():
        mtp,mtpflag = parseInt(d['mtp'])
        d['mtp'] = mtp
    if 'rtt' in d.keys():
        rtt,rttflag = parseInt(d['rtt'])
        d['rtt'] = rtt
    if 'flv' in d.keys():
        flv,flvflag = parseInt(d['flv'])
        d['flv'] = flv
    if 'spd' in d.keys():
        spd,spdflag = parseInt(d['spd'])
        d['spd'] = spd
    if 'tch' in d.keys():
        tch,tchflag = parseInt(d['tch'])
        d['tch'] = tch
    if 'scd' in d.keys():
        scd,scdflag = parseInt(d['scd'])
        d['scd'] = scd
    if 'dpr' in d.keys():
        if d['dpr']=='!':
            import pdb; pdb.set_trace()
        dpr,dprflag = parseFloat(d['dpr']) 
        d['dpr'] = dpr
    if 'rtt' in d.keys():
        rtt,_ = parseInt(d['rtt'],errVal=-100000)
        d['rtt'] = rtt
    if 'x-ha-rtt' in d.keys():
        rtt,_ = parseInt(d['x-ha-rtt'],errVal=-10000)
        d['x-ha-rtt'] = rtt
    if 'x-ha-conn-rate' in d.keys():
        rate,_ = parseInt(d['x-ha-conn-rate'],max=100000000)
        d['x-ha-conn-rate'] = rate
    if 'x-ha-rtt-var' in d.keys():
        var,_ = parseInt(d['x-ha-rtt-var'])
        d['x-ha-rtt-var'] = var
    if 'x-ha-in-rate' in d.keys():
        rate,_ = parseInt(d['x-ha-in-rate'],max=100000000)
        d['x-ha-in-rate'] = rate
    if 'x-ha-out-rate' in d.keys():
        rate,_ = parseInt(d['x-ha-out-rate'],max=100000000)
        d['x-ha-out-rate'] = rate
    for k in d.keys():
        if d[k] == 'Key_not_found' or d[k] == 'No_data_for_':
            d[k] = novalue
    return d
