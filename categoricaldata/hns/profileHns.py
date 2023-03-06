import pandas as pd
dnorm = pd.read_pickle('~/Documents/categorical/hns_test/dnorm.pkl')
import hierarchicalNominalSimilarity as hns
import time
starttime = time.time()
myhns = hns.Hns(dnorm)
res = myhns.hns([(0,6)])
stop = time.time()
print("Ellapsed "+str(stop-starttime)+" and res="+str(res))
