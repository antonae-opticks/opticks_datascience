import json

def generateParser(fields,labels, sepJson=':', sepCsv="^"):
    fieldsStr = f"def parseLine(aline,sep='{sepCsv}'): \n\timport json; \n\tadict = json.loads(aline)\n"
    fieldsStr += "\tif adict is None:\n\t\treturn ''\n"
    labels_clean=[]
    for f,l in zip(fields,labels):
        label_clean = l.replace('-','_')
        labels_clean.append(label_clean)
        keys = f.split(sep=sepJson)
        if len(keys)>0:
            fieldsStr +=f"\ttry:\n\t\t{label_clean} = adict"
        for k in keys:
            fieldsStr+=f".get('{k}')"
        if len(keys)>0:
            fieldsStr+=f"\n\texcept:\n\t\t{label_clean} = 'No_value_for_{l}'\n"
        else:
            fieldsStr+='\n'
    fieldsStr+="\treturn f\""
    if len(labels)>0:
        fieldsStr+="{"+f"{labels_clean[0]}"+"}"
    for l in range(1,len(labels)):
        fieldsStr+="{"+"sep"+"}{"+f"{labels_clean[l]}"+"}"
    fieldsStr+='\\n"\n'
    return fieldsStr

def parseParams(argv):
    params = {'input_path':'',
              'output_path':'',
              'selecteds_path':'',
              'separator_json':':',
              'separator_csv':'^',
    }
    for a in range(1,len(argv)):
        if argv[a]=='-j' and not len(argv)<a:
            params['input_path']=argv[a+1]
        if argv[a]=='-c' and not len(argv)<a:
            params['output_path'] = argv[a+1]
        if argv[a]=='-s' and not len(argv)<a:
            params['selected_path'] = argv[a+1]
        if argv[a]=='-sj' and not len(argv)<a:
            params['separator_json'] = argv[a+1]
        if argv[a]=='-sc' and not len(argv)<a:
            params['separator_csv'] = argv[a+1]
    return params


if __name__=='__main__':
    import sys
    if len(sys.argv)<5:
        print(f"Usage {sys.argv[0]} -j in.json -c out.csv [-cj separator_json] [-cs separator_csv] [-s selecteds_fields.bz2]")
        sys.exit(-1)
    params = parseParams(sys.argv)
    selected=[]
    labels=[]
    if len(params['selected_path'])<1:        
        import module_hnssvm_constants as mhnsct
        selected = mhnsct.defaultSelectedFields
        labels= mhnsct.defaultFieldsLabels
        #parserstr = generateParser(mhnsct.defaultSelectedFields,mhnsct.defaultFieldsLabels,sepJson=sepJson,sepCsv=sepCsv)
    else:
        import joblib
        selected_dict = joblib.load(params['selected_path'])
        selected = list(selected_dict['selectedFields'])
        labels = list(selected_dict['fieldsLabels'])
    if len(params['input_path'])<1 or len(params['output_path']) <0:
        print(f"Usage {sys.argv[0]} -j in.json -c out.csv [-cj separator_json] [-cs separator_csv] [-s selecteds_fields.bz2]")
        sys.exit(-1)
    parserstr = generateParser(selected,labels,sepJson=params['separator_json'],sepCsv=params['separator_csv'])
    import time
    generatedParserPath = 'generatedparser_'+str(time.time()).replace('.','')
    fidout = open(generatedParserPath+'.py','w')
    fidout.write(parserstr)
    fidout.close()
    import sys
    sys.path.insert(1,'.')
    generatedparser = __import__(generatedParserPath)
    fidin = open(params['input_path'])
    fidout = open(params['output_path'],'w')
    header = params['separator_csv'].join(labels)
    fidout.write(header+'\n')
    while fidin:
        linein = fidin.readline()
        if not linein:
            break
        lineout = generatedparser.parseLine(linein,sep=params['separator_csv'])
        fidout.write(lineout)
    fidin.close()
    fidout.close()
