import sys
rows={}
for line in open(sys.argv[1]):
    f=line.split()
    if len(f)==14 and f[0].isdigit() and len(f[0])==4 and f[1]=='99':
        y,t=int(f[0]),int(f[2]); g=lambda s: None if s=='.' else float(s)
        rows[(y,t)]=dict(bev=g(f[3]),eth=g(f[4]),pop14=g(f[5]),pc14=g(f[6])/1e4,pop21=g(f[8]),pc21=g(f[9])/1e4,abv=None if f[12]=='.' else g(f[12])/1e3,ethtv=g(f[13]))
Y=sorted({y for y,t in rows})
print('years',Y[0],Y[-1])
S={}
for y in Y:
    if y<2000: continue
    p=rows[(y,4)]['pop14']
    bev=sum(rows[(y,t)]['bev'] for t in (1,2,3))
    tv=sum(rows[(y,t)]['ethtv'] for t in (1,2,3))
    fx=rows[(y,4)]['eth']; assert abs(fx-sum(rows[(y,t)]['eth'] for t in (1,2,3)))<5
    assert abs(rows[(y,4)]['ethtv']-tv)<5, (y, rows[(y,4)]['ethtv'], tv)
    S[y]=dict(bev_pc=bev/p, tv_pc=tv/p, fx_pc=fx/p, fx_pc_pub=rows[(y,4)]['pc14'], abv=tv/bev, fx_pc21=rows[(y,4)]['pc21'],
              beer=rows[(y,3)]['ethtv']/p, wine=rows[(y,2)]['ethtv']/p, spir=rows[(y,1)]['ethtv']/p, spir_fx=rows[(y,1)]['eth']/p,
              spir_abv=rows[(y,1)]['abv'])
for y in [2002,2003,2018,2019,2022,2023,2024]:
    print(y,{k:round(v,4) for k,v in S[y].items()})
def ch(k, how='mean'):
    if how=='mean':
        b=(S[2002][k]+S[2003][k])/2; e=(S[2018][k]+S[2019][k])/2
    return b,e,(e/b-1)*100
for k in ['bev_pc','abv','tv_pc','fx_pc','fx_pc_pub','fx_pc21']:
    b,e,c=ch(k); print(k, round(b,4), round(e,4), f'{c:+.2f}%')
# pooled version (total gallons / total pop)
def pooled(num):
    b=sum(num(y) for y in (2002,2003))/sum(rows[(y,4)]['pop14'] for y in (2002,2003))
    e=sum(num(y) for y in (2018,2019))/sum(rows[(y,4)]['pop14'] for y in (2018,2019))
    return (e/b-1)*100
print('pooled bev', round(pooled(lambda y: sum(rows[(y,t)]['bev'] for t in (1,2,3))),2), 'pooled tv', round(pooled(lambda y: rows[(y,4)]['ethtv']),2), 'pooled fx', round(pooled(lambda y: rows[(y,4)]['eth']),2))
# abv as ratio of averages
b=(S[2002]['tv_pc']+S[2003]['tv_pc'])/(S[2002]['bev_pc']+S[2003]['bev_pc']); e=(S[2018]['tv_pc']+S[2019]['tv_pc'])/(S[2018]['bev_pc']+S[2019]['bev_pc'])
print('abv ratio-of-avgs', f'{(e/b-1)*100:+.2f}%')
print('2002 bev', round(S[2002]['bev_pc'],2), '2024 bev', round(S[2024]['bev_pc'],2), 'abv 2002', round(S[2002]['abv']*100,2), '2024', round(S[2024]['abv']*100,2))
print('2002-2024 tv', round(S[2002]['tv_pc'],3), round(S[2024]['tv_pc'],3), f"{(S[2024]['tv_pc']/S[2002]['tv_pc']-1)*100:+.1f}%")
for y in range(2016,2025): print(y,'spirits abv',S[y]['spir_abv'],'spir tv',round(S[y]['spir'],3),'fx',round(S[y]['spir_fx'],3),'beer',round(S[y]['beer'],3),'wine',round(S[y]['wine'],3))
