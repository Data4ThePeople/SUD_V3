# usage: fetch.py OUTDIR URL [URL...]  -> saves each to OUTDIR/basename, logs to OUTDIR/PULLED.txt
import sys, os, time, requests, datetime, urllib.parse
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36 (independent tie-out; connect@data4thepeople.com)"}
out=sys.argv[1]
for u in sys.argv[2:]:
    name=os.path.basename(urllib.parse.urlparse(u).path.rstrip("/")) or "index"
    if "." not in name: name+=".html"
    p=os.path.join(out,name)
    if os.path.exists(p): print("have",p); continue
    r=requests.get(u,headers=UA,timeout=300); print(r.status_code,len(r.content),u)
    if r.ok:
        open(p,"wb").write(r.content)
        open(os.path.join(out,"PULLED.txt"),"a").write(f"{datetime.datetime.now().isoformat()}\t{u}\t{name}\t{len(r.content)}\n")
    time.sleep(1.1)
