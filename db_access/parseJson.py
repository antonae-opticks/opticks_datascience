import json
import sys

def returnJsonFields(json):
    fields = []
    if type(json) is type(None):
        return fields
    if type(json) is not dict:
        if type(json) == str:
            return [str(json).replace('\t',' ')]
        else:
            return ['']
    sortedKeys = list(json.keys())
    sortedKeys.sort()
    for k in sortedKeys:
        if type(json[k]) == str:
            fields.append(k)
        else:
            if not type(json) == type(None):
                newfields = returnJsonFields(json[k])
                for n in newfields:
                    if type(n) == str and len(n)>0:
                        fields.append(k+":"+n)
                    else:
                        fields.append(k)
                    
    return fields

def getLeaf(keys,data):
    if len(keys)==1: # if we're asqued for a leaf node, seek for it
        if type(data) is type(None):
            return 'No_data_for_'+str(keys[0]).replace('\t',' ')
        if type(data) is not dict:
            print("Warning: data "+str(data).replace('\t',' ')+ " and keys "+str(keys)).replace('\t',' ')
            return str(data)
        if keys[0] not in data.keys(): # we didn't find the leaf labeled as selected, return error string
            newdata = {k.lower():v for k,v in data.items()} # HACK TO DEAL WITH 'SUDDENLY' CAMELCASEd KEYS
            if str(keys[0]).lower() in newdata.keys():
                content = str(newdata[str(keys[0]).lower()]).replace('\t',' ')
                return content
            return 'Key_not_found_'+str(keys[0]).replace('\t',' ')
        # we found the leaf. Return the contents of the data assigned to, converted to string in case it was not an actual leaf on the data
        else:
            content = str(data[keys[0]]).replace('\t',' ')
            return content
    else:
        if type(data) is type(None):
            return 'No_data_for_'+str(keys[0])
        nextkey = keys[0]
        if nextkey not in data.keys():
            newdata = {k.lower():v for k,v in data.items()} # HACK TO DEAL WITH 'SUDDENLY' CAMELCASEd KEYS
            if str(nextkey).lower() in newdata.keys():
                return getLeaf(keys[1:],newdata[str(nextkey).lower()]) # if its a tree node, recursively seek the leaf on the children
            else:
                return 'Key_not_found_'+str(nextkey).replace('\t',' ')
        return getLeaf(keys[1:],data[str(nextkey)])
        

    
def extractSelected(selected,data, sepToUse = '\t'):
    #import pdb; pdb.set_trace()
    extracted = ''
    sep = '' # trick to avoid sep at begin of line
    for s in selected:
        selectedKeys = s.split(':')
        extracted = extracted + str(sep) + getLeaf(selectedKeys,data)
        sep = sepToUse
    return extracted

def parseFile(path, selectedKeys, keyLabels, out=''):
    file = open(path,'r')
    if len(out)>0:
        fout = open(out,'w')
    aline = file.readline()
    sep = '\t'
#    import pdb; pdb.set_trace()
    if len(out)>0: # write to file
        [fout.write(str(l)+sep) for l in keyLabels]
        fout.write("\n")
    else: #write to stdout
        [print(str(l)+sep,end='') for l in keyLabels]
        print("")
    while aline:
        if len(aline)>10: #assume if its longer than 10 it's a valid line
            if len(out)>0: #write to file
                fout.write(extractSelected(selectedKeys,json.loads(aline),sep)+"\n")
            else: #write to stdout
                print(extractSelected(selectedKeys,json.loads(aline),sep))
        aline = file.readline()
    file.close()
    if len(out)>0:
        fout.close()
