datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfound = set(datacsvgt['plt','oscpu','ua','risk_level'].index)
combsfound = set(datacsvgt[['plt','oscpu','ua','risk_level']].value_counts().index)
combsfound
len(combsfound)
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
len(combsfound)
foo = set('a','b','c')
('a','b','c')
set(('a','b','c'))
{'a','b','c'}+{'f'}
{'a','b','c'}union({'f'})
{'a','b','c'}.union({'f'})
{'a','b','c'}.union({'f'}).union({'b'})
for c in combsfound:
    rcomb = c.union{'low'}
for c in combsfound:
    rcomb = c.union({'low'})
foo = ('a','b')
foo+'c'
foo+('c')
foo
foo+('c')
foo+('c',)
for c in combsfound:
    rcomb = c+('low',)
for c in combsfound:
    rcomb = c+('low',)
    rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index
for c in combsfound:
    rcomb = c+('low',)
    print(rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index)
for c in combsfound:
    rcomb = c+('low',)
    found = rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index
    print(f"{rcomb} found {found}")
for c in combsfound:
    rcomb = c+('high',)
    found = rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index
    print(f"{rcomb} found {found}")
'high'.toupper()
'high'.upper()
len(combsfound)
for c in combsfound:
    rcomb = c+('high',)
    found = rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index
    if found:
       print(f"{rcomb} found {found}")
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    found = rcomb in datacsvgt[['plt','oscpu','ua']].value_counts().index
    print(f"{rcomb} found {found}")
    if i>10:
        break
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    found = c in datacsvgt[['plt','oscpu','ua']].value_counts().index
    print(f"{c} found {found}")
    if i>10:
        break
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    found = rcomb in datacsvgt[['plt','oscpu','ua','risk_level']].value_counts().index
    print(f"{rcomb} found {found}")
    if i>10:
        break
highgt = 0
highref = 0
lowgt = 0
lowref = 0
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    if rcomb in datacsvgt[['plt','oscpu','ua','risk_level']].value_counts().index:
        highgt = highgt+datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()[rcomb] 
    if rcomb in datacsvref[['plt','oscpu','ua','risk_level']].value_counts().index: 
        highref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()[rcomb]
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index:
    foundhref rcomb in combsfoundref.index: 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index:
    foundhref rcomb in combsfoundref.index: 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
history
history -f ~/tmp/log.combinations.py
history -f /tmp/log.combinations.py
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index:
    foundhref rcomb in combsfoundref.index: 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    elif:
        print(f"Not found {c}")    
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    else:
        print(f"Not found {c}")    
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    else:
        print(f"Not found {rcomb}")    
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i>100:
        print(f"{highboth} {highgt} {highref}")
        break
datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i%100==0:
        print(f"{highboth} {highgt} {highref}")
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i%100==0:
        print(f"{i} {highboth} {highgt} {highref}")
len(datacsvgt.plt.unique())
len(datacsvgt.oscpu.unique())
len(datacsvgt.ua.unique())
55*39
len(datacsvgt[['plt','oscpu','ua']].value_counts().index)
len(datacsvgt[['ua','plt','oscpu']].value_counts().index)
len(datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts'))
datacsvgt.ua.unique()
set(datacsvgt.ua.unique())
len(set(datacsvgt.ua.unique()))
foo = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')
foo
foo['ua'].unique()
len(foo['ua'].unique())
datacsvgt.plt.unique()
datacsvgt.oscpu.unique()
foo = datacsvgt.dropna()
foo
for c in datacsvgt.columns:
    print(datacsvgt[c].unique())
datacsvgt.columns
datacsvgt['msisdn']
datacsvgt['msisdn'].dropna()
history
foo = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')
foo = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')['ua'].unique()
foo
len(foo)
foo = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')
len(foo['ua'].unique())
uas1 = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')['ua'].unique()
uas2 = datacsvgt['ua'].unique()
uas1-uas2
set(uas1)-set(uas2)
uas1
uas1[0]
uas1[0] in uas2
uas3 = [ua for ua in uas1 if ua not in uas2]
len(uas3)
uas3 = [ua for ua in uas2 if ua not in uas1]
len(uas3)
len(uas3)+len(uas1)
len(uas2)
uas3[0]
foo = datacsvgt[datacsvgt.ua==uas3[0]]
foo
foo[['plt','oscpu']]
datacsv.iloc[0]
datacsvgt.iloc[0]
uas3[0]
datacsvgt.iloc[1]
datacsvgt.at[datacsvgt.oscpu==NaN,'oscpu']=''
datacsvgt.at[datacsvgt.oscpu==np.nan,'oscpu']=''
datacsvgt.iloc[1]
datacsvgt.iloc[1]['oscpu']
datacsvgt.iloc[1]['oscpu']=nan
datacsvgt.iloc[1]['oscpu']=np.nan
datacsvgt.iloc[1]['oscpu']
datacsvgt.iloc[1]['oscpu']
datacsvgt.iloc[1]['oscpu']==np.nan
datacsvgt.iloc[1]['oscpu']==NaN
datacsvgt.iloc[1]['oscpu'].isna()
datacsvgt.iloc[1]['oscpu'].isnan()
datacsvgt.iloc[1]['oscpu']
datacsvgt.iloc[1]['oscpu']==datacsvgt.iloc[1]['oscpu']
datacsvgt.at[datacsvgt.oscpu==datacsvgt.oscpu,'oscpu']=''
datacsvgt.iloc[1]['oscpu']
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvgt.at[datacsvgt.oscpu!=datacsvgt.oscpu,'oscpu']=''
datacsvgt.iloc[1]['oscpu']
history
foo = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')
uas1 = datacsvgt[['ua','plt','oscpu']].value_counts().reset_index(name='counts')['ua'].unique()
uas2 = datacsvgt['ua'].unique()
uas3 = [ua for ua in uas2 if ua not in uas1]
uas3
len(uas3)
len(uas1)
len(uas2)
datacsvgt[datacsvgt.ua==uas3[0]]
datacsvref.at[datacsvref.oscpu!=datacsvgt.oscpu,'oscpu']=''
len(datacsvref[['plt','oscpu','ua']].values_count().index)
len(datacsvref[['plt','oscpu','ua']].value_counts().index)
len(datacsvgt[['plt','oscpu','ua']].value_counts().index)
history
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
len(combsfound)
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i%1000==0:
        print(f"{i} {highboth} {highgt} {highref}")
datacsvref.at[datacsvref.plt!=datacsvgt.plt,'plt']=''
datacsvgt.at[datacsvgt.plt!=datacsvgt.plt,'plt']=''
datacsvgt.at[datacsvgt.ua!=datacsvgt.ua,'ua']=''
datacsvref.at[datacsvref.ua!=datacsvref.ua,'ua']=''
datacsvref = pd.read_csv('/opt/rad/datascience/datasets/gt/general_https_js_2023Jan_200k_reliablemethodsvars.csv',sep='^')
datacsvgt = pd.read_csv('/opt/rad/datascience/datasets/gt/gt_brainstormings_reliablemed_jan2023_reliablemethodsvars.csv',sep='^')
datacsvref.at[datacsvref.ua!=datacsvref.ua,'ua']=''
datacsvgt.at[datacsvgt.ua!=datacsvgt.ua,'ua']=''
datacsvgt.at[datacsvgt.plt!=datacsvgt.plt,'plt']=''
datacsvref.at[datacsvref.plt!=datacsvref.plt,'plt']=''
datacsvref.at[datacsvref.oscpu!=datacsvref.oscpu,'oscpu']=''
datacsvgt.at[datacsvgt.oscpu!=datacsvgt.oscpu,'oscpu']=''
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    if i%1000==0:
        print(f"{i} {highboth} {highgt} {highref}")
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
lowboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    rcomb = c+('low',)
    foundlgt = rcomb in combsfoundgt.index
    foundlref = rcomb in combsfoundref.index
    if foundlgt and foundlref:
        lowboth+=1
    elif foundlgt:
        lowgt+=1
    elif foundlref:
        lowref+=1
    if i%1000==0:
        print(f"{i} {highboth} {highgt} {highref} {lowboth} {lowgt} {lowref}")
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
lowboth = 0
lowgt = 0
lowref = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    rcomb = c+('low',)
    foundlgt = rcomb in combsfoundgt.index
    foundlref = rcomb in combsfoundref.index
    if foundlgt and foundlref:
        lowboth+=1
    elif foundlgt:
        lowgt+=1
    elif foundlref:
        lowref+=1
    if i%1000==0:
        print(f"{i} {highboth} {highgt} {highref} {lowboth} {lowgt} {lowref}")
        
print(f"{i} both h {highboth} gt h {highgt} ref h {highref} both l {lowboth} gt l {lowgt} ref l {lowref} total {highboth+highgt+highref+lowboth+lowgt+lowref}")
685+3562
685+3562+43369
44751-43369
highgt = 0
highref = 0
highboth = 0
lowgt = 0
lowref = 0
lowboth = 0
lowgt = 0
lowref = 0
foundbothgt = 0
foundbothref = 0
foundbothboth = 0
combsfoundgt = datacsvgt[['plt','oscpu','ua','risk_level']].value_counts()
combsfoundref = datacsvref[['plt','oscpu','ua','risk_level']].value_counts()
combsfound = set(datacsvgt[['plt','oscpu','ua']].value_counts().index).union(set(datacsvref[['plt','oscpu','ua']].value_counts().index))
for i,c in enumerate(combsfound):
    rcomb = c+('high',)
    foundhgt = rcomb in combsfoundgt.index
    foundhref = rcomb in combsfoundref.index 
    if foundhgt and foundhref:
        highboth +=1
    elif foundhgt:
        highgt +=1
    elif foundhref:
        highref +=1
    rcomb = c+('low',)
    foundlgt = rcomb in combsfoundgt.index
    foundlref = rcomb in combsfoundref.index
    if foundlgt and foundlref:
        lowboth+=1
    elif foundlgt:
        lowgt+=1
    elif foundlref:
        lowref+=1
    if foundhgt and foundlgt:
        foundbothgt+=1
        if foundhref and foundlref:
            foundbothboth+=1
            foundbothref+=1
    elif foundhref and foundlref:
        foundbothref+=1        
    if i%1000==0:
        print(f"{i} {highboth} {highgt} {highref} {lowboth} {lowgt} {lowref}")
        
print(f"{i} both h {highboth} gt h {highgt} ref h {highref} both l {lowboth} gt l {lowgt} ref l {lowref} total {highboth+highgt+highref+lowboth+lowgt+lowref} bothboth {foundbothboth} both gt {foundbothgt} both ref {foundbothref}")
813+731
813+731-210
44751-43369
history
pwc
pwd
import gtcoverage as gtc
gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
history
from importlib import reload
reload(gtc)
gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
reload(gtc); gtc.gtCoverage(datacsvgt,datacsvref,[['plt','oscpu','ua']])
history -f logcombinations.py
