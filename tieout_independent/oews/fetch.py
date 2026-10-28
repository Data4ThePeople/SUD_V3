import sys, time, urllib.request, os
out = sys.argv[1]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 (contact: connect@data4thepeople.com)"
names = []
for y in range(2001, 2025):
    yy = f"{y%100:02d}"
    for k in ("st", "nat"):
        names.append(f"oes{yy}{k}.zip" if y < 2003 else f"oesm{yy}{k}.zip")
for n in names:
    p = os.path.join(out, n)
    if os.path.exists(p) and os.path.getsize(p) > 10000: continue
    req = urllib.request.Request("https://www.bls.gov/oes/special-requests/" + n, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
    try:
        b = urllib.request.urlopen(req, timeout=120).read()
        open(p, "wb").write(b); print(n, len(b), flush=True)
    except Exception as e:
        print(n, "ERR", e, flush=True)
    time.sleep(1.2)
