# usage: grepdoc.py FILE kw1 kw2 ...
import sys,re,html
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=' '.join(t.split())
for kw in sys.argv[2:]:
    for m in list(re.finditer(kw,t,re.I))[:4]:
        print('['+kw+']',t[max(0,m.start()-300):m.end()+400]); print()
