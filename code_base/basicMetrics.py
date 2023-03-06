def phi(gt, pred,threshold):
    import numpy as np
    #import pdb; pdb.set_trace()
    gt = np.array(gt)
    pred = np.array(pred)
    if len(np.where(gt>threshold)[0]) == 0:
        tpr = 0
    else:
        tpr = len(np.where((pred>threshold) & (gt>threshold))[0])/len(np.where(gt>threshold)[0])
    if len(np.where(gt<=threshold)[0])==0:
        tnr = 0
    else:
        tnr = len(np.where((pred<=threshold) & (gt<=threshold))[0])/len(np.where(gt<=threshold)[0])
    phi=tpr+tnr
    return phi,tpr,tnr
