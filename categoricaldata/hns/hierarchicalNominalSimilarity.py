import numpy as np
import math
from datetime import date

class Hns:
    data = None
    n = 0 # sample size
    m = 0 # dimensionality / number of features
    IR = {}
    IFF = {}
    SIMT = {}
    SIMA = {}
    beta = 0.005
    debugging = 0
    fastoperational = 0
    version = 1.0
    simAMode = 1
    verbose = 1
    
    def __init__(self, data, beta=0.005):
        self.setData(data)
        self.beta = beta

    def setData(self,data):
        self.data = data
        self.n = len(self.data)
        self.m = len(self.data.columns)
        IR = {}
        IFF = {}
        SIMT = {}
        SIMA = {}        

    def setDebugging(self, deb):
        self.debugging = deb

    def setFastOperational(self,oper):
        self.fastoperational = oper

    def setVerbose(self,verbose):
        self.verbose=verbose

    def resetCache(self):
        self.IR = {}
        self.IFF = {}
        self.SIMT = {}
        self.SIMA = {}        

    def storeToFile(self, path):
        # https://stackabuse.com/reading-and-writing-xml-files-in-python/
        import xml.etree.ElementTree as ET
        import bz2
        data = ET.Element('HNS_instance')
        version = ET.SubElement(data,'version')
        version.text= str(self.version)
        n = ET.SubElement(data,'n')
        n.text = str(self.n)
        m = ET.SubElement(data,'m')
        m.text = str(self.m)        
        beta = ET.SubElement(data,'beta')
        beta.text = str(self.beta)
        simamode = ET.SubElement(data,'simAMode')
        simamode.text = str(self.simAMode)
        irt = ET.SubElement(data,'IR')
        for k in self.IR.keys():
            iritem = ET.SubElement(irt,'IRItem')
            iritem.set('key1',k[0])
            iritem.set('key2',k[1])
            iritem.text = str(self.IR[k])
        ifft = ET.SubElement(data,'IFF')
        for k in self.IFF.keys():
            iffitem = ET.SubElement(ifft,'IFFItem')
            iffitem.set('key1',k)
            iffitem.text=str(self.IFF[k])
        simtt = ET.SubElement(data,'SIMT')
        for k in self.SIMT.keys():
            simtitem = ET.SubElement(simtt,'SIMTItem')
            simtitem.set('key1',k[0])
            simtitem.set('key2',k[1])
            simtitem.set('key3',k[2])
            simtitem.text = str(self.SIMT[k])
        simat = ET.SubElement(data,'SIMA')
        for k in self.SIMA.keys():
            simaitem = ET.SubElement(simat,'SIMAItem')
            simaitem.set('key1',k[0])
            simaitem.set('key2',k[1])
            simaitem.set('key3',k[2])
            simaitem.text = str(self.SIMA[k])
#        import pdb; pdb.set_trace()
        xmldata = ET.tostring(data)
        with bz2.open(path,'wb') as fid:
            fid.write(xmldata)
            fid.close()
        
    def restoreFromFile(self, path):
        import xml.etree.ElementTree as ET
        import bz2
        xmldata=None
        with bz2.open(path,'rb') as fid:
            xmldata = fid.read()
            fid.close()
        if xmldata is None:
            print("ERROR. Couldn't read bz2 file "+str(path))
            return
        tree = ET.fromstring(xmldata)
        # get n,m,beta
        tn = tree.find('n')
        n = str(tn.text)
        tm = tree.find('m')
        m = tm.text
        if int(m)!=self.m:
            print("ERROR. Current data dimensionality ("+str(self.n)+","+str(self.m)+") doesn't match specifications on "+path+" ("+str(n)+","+str(m)+"). Aborting.")
            return
        tbeta = tree.find('beta')
        self.beta = float(tbeta.text)
        self.n = int(n)
        self.m = int(m)
        tsimamode = tree.find('simAMode')
        self.simAMode = int(tsimamode.text)
        self.IR={}
        self.IFF={}
        self.SIMT={}
        self.SIMA={}
        for ir in tree.iter(tag='IRItem'):
            k1 = ir.attrib['key1']
            k2 = ir.attrib['key2']
            val = ir.text
            self.IR[(str(k1),str(k2))] = float(val)
        for iff in tree.iter(tag='IFFItem'):
            k1 = iff.attrib['key1']
            val = iff.text
            self.IFF[str(k1)] = float(val)
        for simt in tree.iter(tag='SIMTItem'):
            k1 = simt.attrib['key1'] 
            k2 = simt.attrib['key2']
            k3 = simt.attrib['key3']
            val = simt.text
            self.SIMT[(str(k1),str(k2),str(k3))] = float(val)
        for sima in tree.iter(tag='SIMAItem'):
            k1 = sima.attrib['key1'] 
            k2 = sima.attrib['key2']
            k3 = sima.attrib['key3']
            val = sima.text
            self.SIMA[(str(k1),str(k2),str(k3))] = float(val)
           
        
    def simA(self, i, x,y):
#        if self.debugging == 7:
#            import pdb; pdb.set_trace()
        sim = self.SIMA.get((str(i),str(x),str(y)))
        if sim is not None:
#            print("Catched sima i "+str(i)+" x "+str(x)+" y "+ str(y)+" : "+str(sim))
            return sim
        # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
        if self.fastoperational == 1:
            return -1
        sim = 0.0
        uniques = self.data[i].unique()
        if not x in uniques:
            self.SIMA[(str(i),str(x),str(y))] = sim
            return sim
        if not y in uniques:
            self.SIMA[(str(i),str(x),str(y))] = sim
            return sim
        if self.simAMode == 1:
            counts = self.data[i].value_counts()/self.data[i].size
            sim = (counts[x]+counts[y])/(counts[x]+counts[y]+counts[x]*counts[y])
        elif self.simAMode == 2:
            counts = self.data[i].value_counts()
            sim = (counts[x]*counts[y])/(counts[x]+counts[y]+counts[x]*counts[y])
        self.SIMA[(str(i),str(x),str(y))] = sim
        return sim

    def simTk(self,k,i,x,y):
#        if self.debugging == 5:
#            import pdb; pdb.set_trace()
        dataixK = self.data[k][self.data[i]==x]
        dataiyK = self.data[k][self.data[i]==y]
        skx = dataixK.unique()
        sky = dataiyK.unique()
        #    skx = sK(dataixK)
        #    sky = sK(dataiyK)
        sim = 0.0
        simAixy = self.simA(i,x,y)
        if simAixy == -1:
            return -1
        #    print("SIMTK:simA "+"{:0.3f}".format(simAixy))
        fkls = {}
#        print("simtk k"+str(k)+" i "+str(i)+" x "+str(x)+" y "+str(y))
#        if skx.size==1: # f**** workaround for modin[ray] glitch when |unique()|=1
#            skx=[skx]
#        if sky.size==1:
#            sky=[sky]
        for r in skx:
            for l in sky:
#                print("k " + str(k)+" i "+str(i)+" x " + str(x)+" y "+str(y)+" r "+str(r)+" l "+str(l))
                # if x==y, skx and sky will be the same and, therefore, we can use already fkl computed for fkr
                if x==y:
                    fkr = fkls.get(str(r)) # see if we had fkl for this r
                    if fkr is None:
                        # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
                        if self.fastoperational == 1:
                            return -1
                        fkr = self.fK(dataixK,r,skx)
                        fkls[str(r)] = fkr # we can reuse it for fkl as well, because x=y => skx=sky
                else:
                    fkr = self.fK(dataixK,r,skx)
                fkl = fkls.get(str(l)) # trying to catch fkl
                if fkl is None: # new value for flk, calculate and catch
                    # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
                    if self.fastoperational == 1:
                        return -1                    
                    fkl = self.fK(dataiyK,l,sky)
                    fkls[str(l)] = fkl
                sim+=fkr*fkl*simAixy
                #            print(str(r)+" "+str(l)+" fkr "+"{:0.3f}".format(fkr)+" fkl "+"{:0.3f}".format(fkl)+" sim "+"{:0.3f}".format(fkr*fkl*simAixy))
        return sim
            
    def fK(self,dataixK,r,skx):
#        if self.debugging == 6:
#            import pdb; pdb.set_trace()
        lamb= 0.0
        counts = dataixK.value_counts()        
        for l in skx:
            val = counts.get(str(l))
            if val is not None:
                lamb+=val
            #lamb+=np.count_nonzero(dataixK==l) # TODO: use value_counts of datai
        if lamb == 0.0:
            return 0.0
        val = counts.get(str(r))
        if val is None:
            return 0.0
        return val/lamb
#        return np.count_nonzero(dataixK==r)/lamb

    def interdependenceRedundancy(self,i,j):
#        if self.debugging == 4:
#            import pdb; pdb.set_trace()
        ir = self.IR.get((str(i),str(j)))
        if ir is not None:
            return ir
        # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
        if self.fastoperational == 1:
            return -1
        information = 0.0
        entropy = 0.0
        ret = 0.0
        px = 0.0
        py = 0.0
        jointp = 0.0
        lendata = len(self.data)
        countsX = self.data[i].value_counts()/lendata
        countsY = self.data[j].value_counts()/lendata
        #    print(str(len(countsX))+" unique X and "+str(len(countsY))+" unique y")
        for x in countsX.keys():
            dataix = self.data[i]==x
            px = countsX[x]
            #        print(str(x)+" "+str(px))
            datajx = self.data[j][dataix]
            countsjx = datajx.value_counts()/lendata
            for y in countsY.keys():
                py = countsY[y]
                # jointp = np.count_nonzero(datajx==y)/lendata
                jointp = countsjx.get(y)
                #            print(str(y)+" "+str(py)+" "+str(jointp))            
                if jointp == None:
                    continue
                information+=jointp*math.log10(jointp/(px*py))
                #            print("- "+str(jointp*math.log10(jointp/(px*py))))
                entropy+=jointp*math.log10(jointp)
                #            print("- "+str(jointp*math.log10(jointp)))
        if entropy != 0.0:
            ret = information/-entropy
        self.IR[(str(i),str(j))] = ret
        return ret

    def simT(self, i, x, y):
#        if self.debugging == 3:
#            import pdb; pdb.set_trace()
        sim = self.SIMT.get((str(i),str(x),str(y)))
        if sim is not None:
#            print("Catched simT i="+str(i)+" x="+str(x)+" y="+ str(y)+" : "+str(sim))
            return sim
        # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
        if self.fastoperational == 1:
            return -1
        sim = 0.0
        ncols = len(self.data.columns)
        ir = 0.0
        for j in self.data.columns:
            if j==i:
                continue
            #print(i+" "+j)
            irj = self.interdependenceRedundancy(i,j)
            if irj == -1:
                return -1
            #print("ir "+str(irj)+" beta "+str(self.beta))
            if irj<=self.beta:
                continue
            #        print("Calling simtk with "+j+" "+i+" "+x+" "+y)
            simtk = self.simTk(j,i,x,y)
            if simtk == -1:
                return 1;
            sim+=irj*simtk
            ir+=irj
            #        print("irj "+str(irj)+" simTk "+str(simtk))
        if ir == 0.0:
            self.SIMT[(str(i),str(x),str(y))] = 0.0
            return 0.0
        self.SIMT[(str(i),str(x),str(y))] = sim/ir
        return sim/ir

    def iff(self, i):
#        if self.debugging == 2:
        #import pdb; pdb.set_trace()
        iff = self.IFF.get(str(i))
        if iff is not None:
 #           print("Catched IFF i="+str(i)+" : "+str(iff))
            return iff
        # OPERATIONAL HACK: return directly -1 as these are 'new' unknown values
        if self.fastoperational == 1:
            return -1
        lendata=len(self.data)
        counts = self.data[i].value_counts()
        p = counts/lendata
        p_ = (counts-1)/(lendata-1)
        iff = 0.0
        for r in counts.keys():
            iff += p[r]*p_[r]
            #        print(i+" "+r+" p "+str(p[r])+" p- "+str(p_[r]))
        #    print("iff "+str(iff))
        self.IFF[str(i)] = iff
        return iff

    def trainAll(self, nsamples):
        if nsamples<=1 and nsamples>0:
            nsamples = float(self.n)*nsamples        
        allduples = []
        nrange = int(np.sqrt(nsamples*2))
        for i in range(0,nrange):
            for j in range(i,nrange):
                allduples.append((i,j))
        sims = self.hns(allduples)
        return sims
    
    # object duples = duples of object INDEXES
    def hns(self,objectDuples):
        if self.verbose == 1:
            from progress.bar import ChargingBar
        from datetime import datetime
        similarity = 0.0
        sumiff = 0.0
        ret=[] # result array of similarities, size len(objectDuples)
        retMatrix = np.zeros((len(objectDuples),len(self.data.columns)*2)) # result matrix of similarity of each columns for each object, size len(objectDuples) x len(data.columns)
#        if self.debugging == 1:
#        import pdb; pdb.set_trace()
        iterations=len(objectDuples)
        iterationsDone=0
        started = datetime.now()
        lastpercentage=-1
        if self.verbose == 1:
            print("Started "+str(iterations)+" iterations on "+started.strftime("%Y-%m-%d %H:%M:%S"))
            oBar = ChargingBar('Progress obj*cols ',max=iterations*len(self.data.columns), suffix='%(percent)d%% %(index)d/%(max)d')
        indObjects=0
        indColumns=0
        for d in objectDuples:
            if isinstance(d[0],int) or isinstance(d[0],np.int64):
                x = self.data.iloc[d[0]]
                y = self.data.iloc[d[1]]
            else:
                x = d[0]
                y = d[1]
            similarity=0.0
            sumiff=0.0
            indColumns=0
            for i in self.data.columns:
                if self.verbose == 1:
                    oBar.next()
                iffi = self.iff(i)
                if iffi == -1:
                    return -1,None
                if x[i]==y[i]:
                    iffi = 1-iffi
                simTi = self.simT(i,x[i],y[i])
                if simTi == -1:
                    return -1,None
                similarity += iffi*simTi
                sumiff +=iffi
                retMatrix[indObjects][(indColumns*2)]=simTi
                retMatrix[indObjects][(indColumns*2)+1]=iffi
                indColumns+=1
            if sumiff == 0.0:
                ret.append(0.0)
            else:
                #print(f"sumiff {sumiff} similarity {similarity}")
                ret.append(similarity/sumiff)
            indObjects+=1
        ended = datetime.now()
        if self.verbose == 1:
            oBar.finish()
            print("Ended on "+ended.strftime("%Y-%m-%d %H:%M:%S")+". Ellapsed: "+str(ended-started))
        return ret, retMatrix

    def buildHns(nsamples):
        buildsamples=[]
        for i in range(nsamples):
            for j in range(i+1, nsamples):
                buildsamples.append((i,j))
        self.setVerbose(0)
        self.resetCache()
        self.hns(buildsamples)        

    def classify(self,objects,targets):
        if self.verbose == 1:
            from progress.bar import ChargingBar
        from datetime import datetime
#        import pdb; pdb.set_trace()
        for o in objects:
            x = o
            maxsim = -1
            simmax = 0.0
            ret=[]
            for g in targets:
                ind = 0
                for t in g:
                    y = self.data.iloc[t]
                    sim = 0.0
                    for c in self.data.columns:
                        iffi = self.iff(c)
                        if x[c]==y[c]:
                            iffi = 1-iffi
                        simTi = self.simT(c,x[c],y[c])
                        similarity += iffi*simTi
                        sumiff +=iffi
                    if sumiff == 0.0:
                        sim = 0.0
                    else:
                        sim = similarity/sumiff
                    if sim>simmax:
                        maxsim = ind
                        simmax = sim
                    ind +=1
            ret.append(maxsim)
        return ret
