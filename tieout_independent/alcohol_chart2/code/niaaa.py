import re
import sys
D=sys.argv[1]
table1={2002:2.20,2003:2.22,2018:2.36,2019:2.38}
def load(fn):
    out={}
    for line in open(fn,encoding='latin-1'):
        if not re.match(r'^\d{4} ',line): continue
        c=lambda a,b: line[a-1:b].strip()
        if c(6,7)!='99': continue
        f=lambda a,b: None if c(a,b) in ('','.') else float(c(a,b))
        y,b=int(c(1,4)),int(c(9,9))
        out[(y,b)]=dict(eth=f(22,30),pop14=f(32,40),pc14=f(43,47)/1e4,pop21=f(52,60),pc21=f(63,67)/1e4,
                        abv=None if f(74,76) is None else f(74,76)/1000, tveth=f(78,86))
    return out
def ch(a,b): return 100*((b[0]+b[1])/2/((a[0]+a[1])/2)-1)
print('Table 1 (PDF, rounded): all bev 14+ fixed ABV: %.2f%%'%ch([table1[2002],table1[2003]],[table1[2018],table1[2019]]))
for fn in ['pcyr1970-2023.txt','pcyr1970-2024_final.txt']:
    d=load(D+'/'+fn)
    print('==',fn)
    for y in [2002,2003,2018,2019]:
        r=d[(y,4)]; print(y,'pc14 %.4f eth/pop %.5f tv/pop %.5f pc21 %.4f spiritsABV %s'%(r['pc14'],r['eth']/r['pop14'],r['tveth']/r['pop14'],r['pc21'],d[(y,1)]['abv']))
    g=lambda k,f:[f(d[(y,4)]) for y in k]
    A,B=[2002,2003],[2018,2019]
    print(' 14+ fixed (file, unrounded): %.2f%%'%ch(g(A,lambda r:r['eth']/r['pop14']),g(B,lambda r:r['eth']/r['pop14'])))
    print(' 14+ time-varying ABV:        %.2f%%'%ch(g(A,lambda r:r['tveth']/r['pop14']),g(B,lambda r:r['tveth']/r['pop14'])))
    print(' 21+ fixed:                   %.2f%%'%ch(g(A,lambda r:r['eth']/r['pop21']),g(B,lambda r:r['eth']/r['pop21'])))
    print(' 21+ time-varying:            %.2f%%'%ch(g(A,lambda r:r['tveth']/r['pop21']),g(B,lambda r:r['tveth']/r['pop21'])))
    print(' total ethanol gallons fixed: %.2f%%'%ch(g(A,lambda r:r['eth']),g(B,lambda r:r['eth'])))
    for y in [2021,2022,2023,2024]:
        if (y,4) in d: r=d[(y,4)]; print(' ',y,'14+ fixed %.3f tv %.3f spiritsABV %s'%(r['eth']/r['pop14'],r['tveth']/r['pop14'],d[(y,1)]['abv']))
