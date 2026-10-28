import sys, time, urllib.request, os
out = sys.argv[1]; urls = sys.argv[2:]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 (contact: connect@data4thepeople.com)"
for u in urls:
    n = u.split("://")[1].replace("/", "_")
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "en-US"}), timeout=60).read()
        open(os.path.join(out, n), "wb").write(b); print("OK", u, len(b))
    except Exception as e: print("ERR", u, e)
    time.sleep(1.2)
