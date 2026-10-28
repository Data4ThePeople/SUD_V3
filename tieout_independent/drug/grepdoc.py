# usage: grepdoc.py FILE REGEX [width]
import sys, re, html
t=open(sys.argv[1],encoding="latin-1",errors="ignore").read()
t=html.unescape(re.sub(r"<[^>]+>"," ",t)); t=re.sub(r"\s+"," ",t)
w=int(sys.argv[3]) if len(sys.argv)>3 else 250
seen=set()
for m in re.finditer(sys.argv[2],t,flags=re.I):
    s=t[max(0,m.start()-w):m.end()+w]
    k=s[:80]
    if k in seen: continue
    seen.add(k); print("...",s,"...\n")
