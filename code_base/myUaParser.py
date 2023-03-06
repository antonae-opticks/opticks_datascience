def parseUserAgent(strUA):
    if len(str(strUA))<1:
        print(strUA, " empty")
    # User-Agent: <product> (<system-information>) <platform> (<platform-details>) <extensions>
    import re
    product = 'unknown'
    productV = 'unkown'
    sysinfo = 'unknown'
    arch='unknown'
    os='unknown'
    build='unknown'
    platform = 'unknown'
    platdtls = 'unknown'
    extensions = 'uknown'
    wv = ''
    whole=0
    ret = [product.strip(),productV.strip(),arch.strip(),os.strip(),build.strip(),platform.strip(),platdtls.strip(),extensions.strip(),wv,whole]
    try:
        split = re.split('[\(\)]',strUA)
    except:
        #print("Exception on parsing ",strUA)
        return ret
    if len(split)<2:
#        print(strUA," was only split in ",str(len(split))," splits")
        return ret
    if len(split)>4:
        extensions = split[4]
        whole=1
    if len(split)>3:
        platdtls = split[3]
    if len(split)>2:
        platform = split[2]
    if len(split)>1:
        sysinfo = split[1]
    if len(sysinfo)>0:
        split2 = sysinfo.split(';')
        if len(split2)>3:
            wv = split2[3]
        if len(split2)>2:
            build = split2[2]
        if len(split2)>1:
            os = split2[1]
        if len(split2)>0:
            arch=split2[0]
        else:
            arch=sysinfo
    if len(split)>0:
        try:
            splitProd = re.split('\/',split[0])
            if len(splitProd)==2:
                product=splitProd[0]
                productV=splitProd[1]
            else:
                product = split[0]
                whole=0
        except:
            product = split[0]
    return [product.strip(), productV.strip(), arch.strip(), os.strip(), build.strip(), platform.strip(), platdtls.strip(), extensions.strip(),wv.strip(),whole]


def getHeader():
    return ["product", "productV", "arch", "os", "build", "platform", "platdtls", "extensions","whole"]

def parseUserAgentFields(strUa, fields):
    #import pdb; pdb.set_trace()
    product,productV,arch,os,build,platform,pltDtls,extensions,wv,whole=parseUserAgent(strUa)
    retFields={}
    if 'ua_product' in fields:
        retFields['ua_product'] = product
    if 'ua_productV' in fields:
        retFields['ua_productV'] = productV
    if 'ua_arch' in fields:
        retFields['ua_arch'] = arch
    if 'ua_os' in fields:
        retFields['ua_os'] = os
    if 'ua_build' in fields:
        retFields['ua_build'] = build
    if 'ua_platform' in fields:
        retFields['ua_platform'] = platform
    if 'ua_pltDtls' in fields:
        retFields['ua_pltDtls'] = pltDtls
    if 'ua_extesions' in fields:
        retFields['ua_extensions'] = extensions
    if 'ua_wv' in fields:
        retFields['ua_wv'] = wv
    return retFields
