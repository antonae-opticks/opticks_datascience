import numpy as np
import pandas as pd
import sys
sys.path.insert(1,'/home/anton/Documents/code/db_playing/')
sys.path.insert(1,'/home/anton/Documents/code/code_base/')
sys.path.insert(1,'/home/anton/Documents/code/categoricaldata/hns/')
import basicClean as bc
import myUaParser as myUa
import hierarchicalNominalSimilarity as hns
import statistics as st
from sklearn import svm
from datetime import datetime

def prepareDataset(data):
    #import pdb; pdb.set_trace()
    clean = bc.basicClean(data)
    platform=[];product=[];os=[];arch=[]
    for u in clean['ua_headers']:
        p,_,a,o,_,pl,_,_,_=myUa.parseUserAgent(u)
        product.append(p) 
        arch.append(a)
        os.append(o)
        platform.append(pl)
    clean['ua_platform'] = platform
    clean['ua_product'] = product
    clean['ua_arch']=arch
    clean['ua_os']=os
    nomcols=['cntp','evln','flv','hls','lng','nt','ornt','plt','tch','ua_platform','ua_product','ua_arch','ua_os', 'risk_level']
    risk = clean['risk_level']
#    score = clean['score']
    nominals = clean[nomcols]
    nominals.drop(['risk_level'],axis=1,inplace=True)
    nominals.dropna(axis=0,inplace=True)
    return nominals,risk

def subsampleAndSplit(data,nsample,pbuild,ptrain):
    subdata=data.sample(n=nsample)
    randprob = np.random.rand(len(subdata))
    mskbuild = randprob < pbuild
    msktrain = (randprob < pbuild+ptrain) & (randprob>pbuild)
    msktest = ~msktrain & ~mskbuild
    builddata = subdata[mskbuild]
    traindata = subdata[msktrain]
    testdata =subdata[msktest]
    return builddata, traindata,testdata

def buildHns(builddata,nsamples,todrop, verbose=0):
    buildnom = builddata.drop(todrop,axis=1)
    buildsamples=[]
#    print(f"Before building train indexes with nsamples {nsamples}",flush=True)
    for i in range(nsamples):
        for j in range(i+1, nsamples):
            buildsamples.append((i,j))
#    print(f"After building train indexes len {len(buildsamples)}",flush=True)
    myhns = hns.Hns(buildnom)
    myhns.setVerbose(verbose)
    myhns.resetCache()
    myhns.hns(buildsamples)
    return myhns

def buildHnsWhole(builddata,todrop,verbose=0,maxsamples=0):
    buildnom = builddata.drop(todrop,axis=1)
    buildsamples=[]
    nsamples = len(builddata)
    if maxsamples>0 and maxsamples<nsamples:
        nsamples = maxsamples
    myhns = hns.Hns(buildnom)
    myhns.setVerbose(verbose=verbose)
    myhns.resetCache()
    for i in range(0,nsamples-1):
        for j in range(0,nsamples-1):
            if i==j:
                continue
            buildsamples.append((i,j))
    myhns.hns(buildsamples)
    return myhns

def computeHnsTestFeatures(builthns, builtdata,testdata,nsamplesbuild,nsamplestest, targetcol, targets,todrop):
    targetbuild = builtdata[targetcol]
    buildnom = builtdata.drop(todrop,axis=1)
    sims = []
    simsMatrix = []
    targetsused=[]
    for t in range(len(targets)):
        indbuild = np.where(targetbuild==targets[t])[0]
        objects4sim=[]
        for i in range(nsamplestest):
            for j in range(nsamplesbuild):
                objects4sim.append((testdata.iloc[i],buildnom.iloc[indbuild[j]]))
        similarities,similaritiesMatrix = builthns.hns(objects4sim)
        sims.append(similarities)
        simsMatrix.append(similaritiesMatrix)
        targetsused.append(t)
    return sims, simsMatrix,targetsused

# run HNS of M train samples against N build samples for TxT (T = ntargets) combinations
# and obtain TxT arrays of MxN hns-differences, build-sample-wise 
# build samples = samples used to build HNS instance
# train samples = samples used to train SVM classifier
# also obtain TxT matrices of (MxN)xC column/feature differences build-sample-wise
def runHns(builthns, builddata,traindata,nsamplesbuild, msamplestrain,targetcol,targets,todrop):
    timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Starting runHns on {timenow}")
    targetbuild =builddata[targetcol] # GT of build data
    buildnom = builddata.drop(todrop,axis=1) # build data
    targettrain = traindata[targetcol] # GT of train data
    trainnom = traindata.drop(todrop,axis=1) # train data
    sims=[] # resulting TxT arrays
    simsMatrix=[] # resulting TxT matrices of differences per column
    targetsused=[] # resulting TxT combinations or targets used for each resulting array    
    # check availability of samples per target. 
    # check in advance so all combinations or targets use the same 
    # number of samples
    for t1 in range(len(targets)):
        indbuild = np.where(targetbuild==targets[t1])[0] # indices where build data's GT equals current target        for t2 in range(len(targets)):
        if nsamplesbuild > len(indbuild):
            print(f"WARNING: Requesteed {nsamplesbuild} samples from build data for target {targets[t1]}, but only {len(indbuild)} available. Using those...")
            nsamplesbuild = len(indbuild)-1 
        indtrain = np.where(targettrain==targets[t1])[0] # indices where train data's GT equals current target
        if msamplestrain> len(indtrain):
            print(f"WARNING: Requesteed {msamplestrain} samples to train for target {targets[t1]}, but only {len(indtrain)} available. Using those...")
            msamplestrain = len(indtrain)-1 

    for t1 in range(len(targets)): 
        indbuild = np.where(targetbuild==targets[t1])[0] # indices where build data's GT equals current target
            #import pdb; pdb.set_trace()
        for t2 in range(len(targets)):
            indtrain = np.where(targettrain==targets[t2])[0] # indices where train data's GT equals current target
            objects4sim=[]
            #import pdb; pdb.set_trace()
            for i in range(msamplestrain): 
                for j in range(nsamplesbuild):
                    objects4sim.append((buildnom.iloc[indbuild[j]],trainnom.iloc[indtrain[i]]))
            timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Objects for targets {targets[t1]} and {targets[t2]} ready {timenow}. Running HNS... ")
            similarities,similaritiesMatrix= builthns.hns(objects4sim)
            timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"HNS done! ({timenow})")
            sims.append(similarities)
            simsMatrix.append(similaritiesMatrix)
            targetsused.append((targets[t1],targets[t2]))
    return sims,simsMatrix,targetsused,nsamplesbuild,msamplestrain

def runHnsClassify(builthns,builddata,nsamplesbuild,targetcol,targets,todrop, samples2clf, explain=False, mode=1):
    targetbuild =builddata[targetcol] # GT of build data
    buildnom = builddata.drop(todrop,axis=1) # build data
    sims=[] # resulting TxT arrays
    simsMats = []
    simsExplain = []
    for t1 in range(len(targets)): 
        indbuild = np.where(targetbuild==targets[t1])[0] # indices where build data's GT equals current target
        objects4sim=[]
        for s in range(len(samples2clf)):
            for j in range(nsamplesbuild):
                objects4sim.append((buildnom.iloc[indbuild[j]],samples2clf.iloc[s]))
        similarities,simsMat= builthns.hns(objects4sim)
        sims.append(similarities)
        simsMats.append(simsMat)
        if explain:
            simsMats.append(simsMat)
            explainData = builthns.data
            print("here")
            import pdb; pdb.set_trace()
            for c in explainData.columns:
                builthns.data = explainData.drop(c,axis=1)
                simsC,_= builthns.hns(objects4sim)
                simsExplain.append(simsC)
            builthns.data = explainData
    return sims,simsMats, simsExplain


def rearangeSims(sims,nsamplesbuild, nsamplestrain):
    simsrearranged = []
    for s in sims:
        sim = np.zeros(nsamplestrain)
        for n in range(nsamplestrain):
            sim[n] = st.mean(s[n*nsamplesbuild:(n+1)*nsamplesbuild])
        simsrearranged.append(sim)
    return simsrearranged

def rearangeSimsMats(simsMats,nsamplesbuild,nsamplestrain):
    simsrearranged = []
    for s in simsMats:
        sim = np.zeros((nsamplestrain,s.shape[1]))
        for n in range(nsamplestrain):
            sim[n] = s[n*nsamplesbuild:(n+1)*nsamplesbuild].mean(0)
        simsrearranged.append(sim)
    return simsrearranged

def renameSimsMatCols(df,builtdata,todrop):
    newcols = builtdata.drop(todrop,axis=1).columns
    renames = {'lows_'+str(c*2):'l_'+newcols[c] for c in range(0,len(newcols))}
    {renames.update({'lows_'+str(c*2+1):'li_'+newcols[c]}) for c in range(0,len(newcols))}
    {renames.update({'higs_'+str(c*2):'h_'+newcols[c]}) for c in range(0,len(newcols))}
    {renames.update({'higs_'+str(c*2+1):'hi_'+newcols[c]}) for c in range(0,len(newcols))}
    return df.rename(columns=renames)


def trainSvm(data,gt):
    svmclf = svm.SVC()
    svmclf.fit(data,gt)
    return svmclf

def checkTargetSamples(data, dataname, nsamples, targetcol, targets):
    for t in targets:
        ninds = len(np.where(data[targetcol]==t)[0])
        if ninds < nsamples:
            print(f"Not enough samples on data {dataname} for target {f}")
            return False
    return True

def buildClassifier(data,builthns=None, nsamples=400000, nsamplesbuild=1400,nsamplestrain=1000, targetcol='risk_level', targets=[1,3], todrop=['risk_level','score']):
    print(f"Select {nsamples} samples and split")
    builddata,traindata,testdata=subsampleAndSplit(data,nsamples,0.6,0.4)
    if not checkTargetSamples(builddata,'Build-data',nsamplesbuild,targetcol, targets):
        return None,None,None,None
    if not checkTargetSamples(traindata,'Train-data',nsamplestrain,targetcol,targets):
        return None,None,None,None
    buildtarget=builddata['risk_level']
    if builthns is None:
        print("HNS to be built. Building....")
        builthns = buildHns(builddata,nsamples=nsamplesbuild,todrop=todrop)
    print("HNS ready. Let's use it to compute features...")
    builthns.setVerbose(0)
    sims,simsMatrix, targetsused = runHns(builthns, builddata, traindata, nsamplestrain,nsamplestrain, targetcol,targets,todrop)
    simsrearanged = rearangeSims(sims,nsamplestrain,nsamplestrain)
    lows=np.concatenate((simsrearanged[0],simsrearanged[1]))
    higs=np.concatenate((simsrearanged[2],simsrearanged[3]))
    # add artificial training points to rigg unknown areas's classification as positives
#    nartificial=400
#    lows=np.concatenate((lows,np.ones(nartificial)*.11))
#    higs=np.concatenate((higs,np.ones(nartificial)*.11))
    df=pd.DataFrame(data={'lows':lows,'higs':higs})
    gt=np.concatenate((np.ones(nsamplestrain),np.ones(nsamplestrain)*3))
#    gt=np.concatenate((gt,np.ones(nartificial)*3))
    print("Features ready. Let's train the SVM...")
    svmclf =trainSvm(df,gt)
    return svmclf,builthns,builddata,svmclf.score(df,gt), df, gt

def classifySamples(hns,builtdata,nsamplesbuild,targetcol,targets,todrop,clf,samples, explain=False,mode=1):
    sims,simsMats,simsExplain=runHnsClassify(hns,builtdata,nsamplesbuild,targetcol,targets,todrop,samples,explain)
    if mode==1:
        simsrearanged = rearangeSims(sims,nsamplesbuild,len(samples))
        df=pd.DataFrame(data={'lows':simsrearanged[0],'higs':simsrearanged[1]})
    if mode==2:
        simsMatRearanged = rearangeSimsMats(simsMats,nsamplesbuild,len(samples))
        dfMat = pd.concat([pd.DataFrame(data=simsMatRearanged[0]).add_prefix('lows_'),pd.DataFrame(data=simsMatRearanged[1]).add_prefix('higs_')],axis=1)
        df = renameSimsMatCols(dfMat,builtdata,todrop)
    pred = clf.predict_proba(df)
    return pred,df

def phi(gt,pred,pos,neg):
    if len(np.where(gt==pos)[0]) >0:
        tpr = len(np.where((pred==pos) & (gt==pos))[0])/len(np.where(gt==pos)[0])
    else:
        tpr = 0.0
    if len(np.where(gt==neg)[0]) >0:
        tnr = len(np.where((pred==neg) & (gt==neg))[0])/len(np.where(gt==neg)[0])
    else:
        tnr = 0.0
    phi = tpr+tnr
    return tpr,tnr,phi

def storeSvmToFile(clf, path):
    from joblib import dump, load
    dump(clf,path)

def loadSvmFromFile(path):
    from joblib import dump, load
    clf = load(path)
    return clf

def storeObjectToFile(obj,path):
    from joblib import dump
    dump(obj,path)

def loadObjectFromFile(path):
    from joblib import load
    obj = load(path)
    return obj
