import numpy as np
import pandas as pd

def gtCoverage(datagt, dataref, combinations):
    for col in datagt.columns:
        if pd.api.types.is_numeric_dtype(datagt[col]):
            datagt.at[datagt[col]!=datagt[col],col] = -10000
        else:
            datagt.at[datagt[col]!=datagt[col],col] = ''
    for col in dataref.columns:
        if pd.api.types.is_numeric_dtype(dataref[col]):
            dataref.at[dataref[col]!=dataref[col],col] = -10000
        else:
            dataref.at[dataref[col]!=dataref[col],col] = ''
    coverage = {}
    for c in combinations:
        #import pdb; pdb.set_trace()
        cardinality = 1
        for v in c:
            cardinality *= len(set(datagt[v].unique()).union(set(dataref[v].unique())))
        dcGt = datagt[c].value_counts()
        dcRef = dataref[c].value_counts()
        dcGtR = datagt[c+['risk_level']].value_counts()
        dcRefR = dataref[c+['risk_level']].value_counts()
        combsfound = set(dcGt.index).union(set(dcRef.index))
        mat = np.zeros((2,2)) # (Gt1, Gt0) x (R1, R0)
        matR = np.zeros((4,4)) # (hGt1, hGt0, lGt1, lGt0) x (hR1, hR0, lR1, lR0)
        for cb in combsfound:
            hc = cb+('high',)
            lc = cb+('low',)
            fhgt = hc in dcGtR.index
            flgt = lc in dcGtR.index
            fhref = hc in dcRefR.index
            flref = lc in dcRefR.index
            fgt = cb in dcGt.index
            fref = cb in dcRef.index
            if fgt:
                if fref:
                    mat[0][0]+=1
                else:
                    mat[0][1]+=1
            else:
                if fref:
                    mat[1][0]+=1
                else:
                    mat[1][1]+=1
            if fhgt:
                if fhref:
                    matR[0][0]+=1
                else:
                    matR[0][1]+=1
                if flref:
                    matR[0][2]+=1
                else:
                    matR[0][3]+=1
            else:
                if fhref:
                    matR[1][0]+=1
                else:
                    matR[1][1]+=1
                if flref:
                    matR[1][2]+=1
                else:
                    matR[1][3]+=1
            if flgt:
                if fhref:
                    matR[2][0]+=1
                else:
                    matR[2][1]+=1
                if flref:
                    matR[2][2]+=1
                else:
                    matR[2][3]+=1
            else:
                if fhref:
                    matR[3][0]+=1
                else:
                    matR[3][1]+=1
                if flref:
                    matR[3][2]+=1
                else:                
                    matR[3][3]+=1
        print(f"Combination {c} {len(combsfound)} {cardinality} ({len(combsfound)*1000/cardinality}‰)")
        print(f"{mat}")
        print(f"{matR}")
        dct = {}
        dct['cardinality'] = cardinality
        dct['mat'] = mat
        dct['matR'] = matR
        dct['combinations'] = combsfound
        coverage[tuple(c)] = dct        
    return coverage
