import sys, pandas as pd
f1, f2 = sys.argv[1], sys.argv[2]
df = pd.read_sas(f1, format='sas7bdat', encoding='latin-1')
n = df[(df.stname=='National') & (df.agegrp==0) & df.outcome.isin(['ALCMON','ABODALC','DEPNDALC'])]
t = n.pivot_table(index='pyearnm', columns='outcome', values='BSAE')*100
print(t.round(3).to_string())
print(n[n.outcome=='ABODALC'][['pyearnm','outname']].drop_duplicates().to_string())
ci = n[n.pyearnm.isin(['2002-2003','2018-2019'])][['pyearnm','outcome','BSAE','low_sae','up_sae','est_total']]
print(ci.to_string())
for o in ['ALCMON','ABODALC']:
    a,b = t.loc['2002-2003',o], t.loc['2018-2019',o]
    print(o, '2002-03 %.3f  2018-19 %.3f  change %+.2f%%  (pp %+.2f)'%(a,b,100*(b/a-1),b-a))
    a2,b2 = round(a,1), round(b,1); print('   from 1-dec published: %+.2f%%'%(100*(b2/a2-1)))
d2 = pd.read_sas(f2, format='sas7bdat', encoding='latin-1')
d2.columns=[c.lower() for c in d2.columns]
print(d2.columns.tolist())
m = d2[(d2.stname=='National') & (d2.agegrp==0) & d2.outcome.isin(['ALCMON','UDYR5ALC'])]
print((m.pivot_table(index='pyearnm', columns='outcome', values='bsae')*100).round(3).to_string())
