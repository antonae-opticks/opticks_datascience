from importlib import reload
import gtcoverage as gtc
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
datacsvgt.columns
datacsvref.columns
datacsvref['x-requested-with'].describe()
datacsvref['x-requested-with'].unique()
datacsvgt['x-requested-with'].unique()
history
datacsvgt
datacsvref
import combinations_reliablemethods as crm
history
crm.combinations
gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
datacsvgt.columns
datacsvref.columns
datacsvref.columns
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
datacsvref.columns
datacsvgt.columns
datacsvgt['ciphers'] = datacsvgt['ciphers ']
datacsvref['ciphers'] = datacsvref['ciphers ']
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
ls
selected=joblib.load('selectedFields_fieldsLabels_reliablemethods.bz2')
type(selected)
selected
selected.selectedFields
selected['selectedFields']
type(selected['selectedFields'])
selected['selectedFields'].append('security:clientdata:ehdCC')
selected['selectedFields'].insert('security:clientdata:ehdCC')
np.append
np.append(selected['selectedFields'],'security:clientdata:dpr')
selected['selectedFields'] =np.append(selected['selectedFields'],'security:clientdata:dpr')
selected['selectedFields'] =np.append(selected['selectedFields'],'security:clientdata:ehdCC')
selected['selectedFields'] =np.append(selected['selectedFields'],'security:clientdata:ehdIsp')
selected['fieldsLabels']
selected['fieldsLabels'] = np.append(selected['fieldsLabels'],'dpr')
selected['fieldsLabels'] = np.append(selected['fieldsLabels'],'ehdCC')
selected['fieldsLabels'] = np.append(selected['fieldsLabels'],'ehdIsp')
len(selected['fieldsLabels'])
len(selected['selectedFields'])
joblib.dump(selected,'selectedFields_fieldsLabels_reliablemethods.bz2')
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
datacsvref.columns
datacsvref['dpr'].describe()
datacsvref['dpr'].unique()
len(datacsvref['dpr'].unique())
len(datacsvgt['dpr'].unique())
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
len(datacsvgt['dpr'].unique())
len(datacsvref['dpr'].unique())
len(datacsvref['ehdIsp'].unique())
len(datacsvref['ehdCC'].unique())
len(datacsvgt['ehdCC'].unique())
len(datacsvgt['ehdIsp'].unique())
datacsvref['ehdCC'].unique()
datacsvref['ehdIsp'].unique()
selected['fieldsLabels'] = np.append(selected['fieldsLabels'],'chromium_v')
selected['selectedFields'] =np.append(selected['selectedFields'],'security:clientdata:chromium_v')
len(selected['fieldsLabels'])
len(selected['selectedFields'])
joblib.dump(selected,'selectedFields_fieldsLabels_reliablemethods.bz2')
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
len(datacsvgt['chromium_v'].unique())
len(datacsvref['chromium_v'].unique())
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
selected['fieldsLabels']
selected['fieldsLabels'][22]
selected['fieldsLabels'][30]
selected['fieldsLabels'][31]
selected['fieldsLabels'][31] = 'ciphers'
joblib.dump(selected,'selectedFields_fieldsLabels_reliablemethods.bz2')
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
reload(gtc);reload(crm); gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
foo = [[ 544. 2011. 1094. 1461.]
 [ 253. 4826. 3323. 1756.]
 [ 414. 2392. 1735. 1071.]
 [ 383. 4445. 2682. 2146.]]
2011+4826+2392+4445+544+253+414+383
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
combinations
coverage
coverage
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
coverage
coverage.keys()
len(coverage[('plt', 'oscpu', 'ua')]['combinations'])
coverage[('plt', 'oscpu', 'ua')]['mat']
coverage[('plt', 'oscpu', 'ua')]['mat'][0][0]
coverage[('plt', 'oscpu', 'ua')]['mat'][0][1]
coverage[('plt', 'oscpu', 'ua')]['mat'][0][2]
coverage[('plt', 'oscpu', 'ua')]['mat'][0][3]
np.trace(coverage[('plt', 'oscpu', 'ua')]['mat'])
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
coverage['mat']
coverage.keys()
coverage[('plt','oscpu','ua')]['mat']
len(coverage[('plt','oscpu','ua')]['combinations'])
sum(coverage[('plt','oscpu','ua')]['mat'])
sum(sum(coverage[('plt','oscpu','ua')]['mat']))
foo = set(datacsvgt.plt.unique()).union(datacsvref.plt.unique())
foo
len(foo)
foo = set(datacsvgt.oscpu.unique()).union(datacsvref.oscpu.unique())
len(foo)
foo
foo = set(datacsvgt.ua.unique()).union(datacsvref.ua.unique())
len(foo)
foo
card = len(set(datacsvgt.plt.unique()).union(set(datacsvref.plt.unique())))*len(set(datacsvgt.oscpu.unique()).union(set(datacsvref.oscpu.unique())))*len([1])
card
card = len(set(datacsvgt.plt.unique()).union(set(datacsvref.plt.unique())))*len(set(datacsvgt.oscpu.unique()).union(set(datacsvref.oscpu.unique())))*len(set(datacsvgt.ua.unique()).union(set(datacsvref.ua.unique())))
card
foo = set(datacsvgt.ua.unique()).union(datacsvref.ua.unique())
len(foo)
len(foo)*47*61
coverage
card
coverage[('plt','oscpu','ua')]['mat']/card
coverage[('plt','oscpu','ua')]['mat']*100/card
coverage[('plt','oscpu','ua')]['mat']*1000/card
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
datacsvgt.browser_name.unique()
datacsvgt.browser_version.unique()
len(datacsvgt.browser_version.unique())
selected['selectedFields']
selected['selectedFields'][34]
selected['selectedFields'][33]
selected['selectedFields'][32]
selected['selectedFields'][32]=
selected['selectedFields'][32]='visitor:device:browser:name'
joblib.dump(selected,'selectedFields_fieldsLabels_reliablemethods.bz2')
selected['fieldsLabels']
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
reload(gtc);reload(crm); coverage = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref,combinations=crm.combinations)
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); for c in coverage:
    print(f"c]
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); for c in coverage:
    print(f"c['combination']\t\t\t{len(c['combsfound'])}\t{c['cardinality']")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"c['combination']\t\t\t{len(c['combsfound'])}\t{c['cardinality']")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"c['combination']\t\t\t{len(c['combsfound'])}\t{c['cardinality']}")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c['combination']}")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t\t\t{coverage[c]['ncombsfound']}")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t\t\t{coverage[c]['combinations']}")
print("Combination\t\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t\t\t{len(coverage[c]['combinations'])}")
print("Combination\\t\t\tt\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t\t\t\t\t\t{len(coverage[c]['combinations'])}")
print("Combination\t\t\t\t\t\t\tt\t\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t\t\t\t\t\t\t\t\t\t{len(coverage[c]['combinations'])}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])} {coverage[c]['cardinality']} {len(coverage[c]['combinations'])*1000/cardinality}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])} {coverage[c]['cardinality']} {len(coverage[c]['combinations'])*1000/coverage[c]['cardinality']}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])} {coverage[c]['cardinality']} {len(coverage[c]['combinations'])*1000/coverage[c]['cardinality']:.7f}")
coverage[('plt','oscpu','ua')].mat
coverage[('plt','oscpu','ua')]['mat']
coverage[('plt','oscpu','ua')]['mat'][1,:]
coverage[('plt','oscpu','ua')]['mat'][0,:]
sum(coverage[('plt','oscpu','ua')]['mat'][0,:])
sum(coverage[('plt','oscpu','ua')]['mat'][0,:])/coverage[('plt','oscpu','ua')]['cardinality']
sum(coverage[('plt','oscpu','ua')]['mat'][0,:])/coverage[('plt','oscpu','ua')]['cardinality']/1000
sum(coverage[('plt','oscpu','ua')]['mat'][0,:])/coverage[('plt','oscpu','ua')]['cardinality']*1000
coverage[('plt','oscpu','ua')]['mat'][::-1].trace()
coverage[('plt','oscpu','ua')]['mat'][0][1]/coverage[('plt','oscpu','ua')]['mat'][::-1].trace()
coverage[('plt','oscpu','ua')]['mat'][0][1]/coverage[('plt','oscpu','ua')]['mat'][::-1].trace()*100
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{coverage[c]['mat'][0,:]/sum(sum(coverage[c]['mat'])}\t{coverage[c]['mat'][0,:]/coverage[c]['cardinality']*1000}")
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{coverage[c]['mat'][0,:]/sum(sum(coverage[c]['mat']))}\t{coverage[c]['mat'][0,:]/coverage[c]['cardinality']*1000}")
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{sum(coverage[c]['mat'][0,:])/sum(sum(coverage[c]['mat']))}\t{sum(coverage[c]['mat'][0,:])/coverage[c]['cardinality']*1000}")
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{sum(coverage[c]['mat'][0,:])/sum(sum(coverage[c]['mat'])):.3f}\t{sum(coverage[c]['mat'][0,:])/coverage[c]['cardinality']*1000:.5f}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])} {coverage[c]['cardinality']} {len(coverage[c]['combinations'])*1000/coverage[c]['cardinality']:.7f}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage:
    print(f"{c}\t{len(coverage[c]['combinations'])}\t{coverage[c]['cardinality']}\t {len(coverage[c]['combinations'])*1000/coverage[c]['cardinality']:.7f}")
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{sum(coverage[c]['mat'][0,:])/sum(sum(coverage[c]['mat'])):.3f}\t{sum(coverage[c]['mat'][0,:])/coverage[c]['cardinality']*1000:.5f}")
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{sum(coverage[c]['mat'][0,:])/sum(sum(coverage[c]['mat']))*100:.3f}\t{sum(coverage[c]['mat'][0,:])/coverage[c]['cardinality']*1000:.5f}")
coverage[('wglr2','wglv2')]['mat']
datacsvref[['wglrw','wglv2']].values_count()
datacsvref[['wglr2','wglv2']].values_count()
datacsvref[['wglr2','wglv2']].value_counts()
datacsvgt[['wglr2','wglv2']].value_counts()
datacsvref[['wglr2','wglv2']].value_counts()
len(datacsvref[['wglr2','wglv2']].value_counts())
len(datacsvref[['evln','ua']].value_counts())
len(datacsvgt[['evln','ua']].value_counts())
coverage[('evln','ua')].mat
coverage[('evln','ua')]['mat']
datacsvref[['evln','ua']].value_counts()
len(datacsvref[datacsvref.evln!=datacsvref.evln])
len(datacsvref[datacsvref.ua!=datacsvref.ua])
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage:
    print(f"{c}\t{sum(coverage[c]['mat'][0,:])/sum(sum(coverage[c]['mat']))*100:.3f}\t{sum(coverage[c]['mat'][0,:])/coverage[c]['cardinality']*1000:.5f}")
datacsvref1M = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_1M_reliablemethodsvars.csv',sep='^')
reload(gtc);reload(crm); coverage1M = gtc.gtCoverage(datagt= datacsvgt,dataref=datacsvref1M,combinations=crm.combinations)
print("Combination\tPercentage of GT coverage wrt combinations found in data\t‰ of GT coverage wrt potential universe"); 
for c in coverage1M:
    print(f"{c}\t{sum(coverage1M[c]['mat'][0,:])/sum(sum(coverage1M[c]['mat']))*100:.3f}\t{sum(coverage1M[c]['mat'][0,:])/coverage1M[c]['cardinality']*1000:.5f}")
print("Combination\tUnique combinations found\tCardinality\t‰ found"); 
for c in coverage1M:
    print(f"{c}\t{len(coverage1M[c]['combinations'])}\t{coverage1M[c]['cardinality']}\t {len(coverage1M[c]['combinations'])*1000/coverage1M[c]['cardinality']:.7f}")
ls
history -f  logcombinations_2.py
