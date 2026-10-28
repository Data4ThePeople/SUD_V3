import sys, pandas as pd
O=sys.argv[1]
a=pd.read_pickle(O+"/s9919.pkl"); b=pd.read_pickle(O+"/s2124.pkl")
d=pd.concat([a,b])
for oc in ["ABODILL","UDPYILL","UD5ILANY","ABODALC","UDYR5ALC","ABODILAL","UDPYILAL","UD5IAANY","DEPNDILL"]:
    s=d[(d.outcome==oc)&(d.agegrp==0)]
    print(oc, s.outname.unique(), s.groupby("pyearnm").size().to_dict())
