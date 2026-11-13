import pandas as pd, sys
pd.set_option('display.width',200)
d=pd.read_sas(sys.argv[1],encoding='latin1')
n=d[(d.stname=='National')&d.outcome.isin(['ALCMON','ABODALC','DEPNDALC'])]
print(n[['outcome','outname']].drop_duplicates())
t=n.pivot_table(index=['outcome','pyearnm'],columns='agegrp',values=['BSAE','est_total'])
print(t.round(4).to_string())
a=n.set_index(['outcome','pyearnm','agegrp'])
for o in ['ALCMON','ABODALC']:
    b=a.loc[(o,'2002-2003',0),'BSAE']; e=a.loc[(o,'2018-2019',0),'BSAE']
    print(o,'12+ BSAE',round(b,5),round(e,5),f'{(e/b-1)*100:.2f}%')
    b=a.loc[(o,'2002-2003',0),'est_total']; e=a.loc[(o,'2018-2019',0),'est_total']
    print(o,'12+ count',b,e,f'{(e/b-1)*100:.2f}%')
for w in ['2002-2003','2018-2019','2010-2011 (published)','1999-2000']:
    if (('ABODALC',w,3) in a.index):
        print(w,'26+ share of ABODALC', a.loc[('ABODALC',w,3),'est_total'], a.loc[('ABODALC',w,0),'est_total'], round(a.loc[('ABODALC',w,3),'est_total']/a.loc[('ABODALC',w,0),'est_total']*100,2),
              ' sum of age groups', a.loc[('ABODALC',w,1),'est_total']+a.loc[('ABODALC',w,2),'est_total']+a.loc[('ABODALC',w,3),'est_total'])
for g in [1,2,3]:
    b=a.loc[('ABODALC','2002-2003',g),'BSAE']; e=a.loc[('ABODALC','2018-2019',g),'BSAE']
    print('agegrp',g, round(b*100,2), round(e*100,2), f'{(e/b-1)*100:.1f}% rel, {(e-b)*100:.2f} pts')
