import sys, re, html, glob, os
pat = re.compile(sys.argv[2], re.I)
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.htm*"))):
    t = open(f, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", t); t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
    title = re.search(r"(?i)(Page Not Found|404)", t)
    hits = [m.start() for m in pat.finditer(t)]
    print("==", os.path.basename(f), "NOTFOUND" if title and len(hits)==0 else "", len(hits))
    for h in hits[: int(sys.argv[3]) if len(sys.argv) > 3 else 4]:
        print("   ...", t[max(0, h-250): h+350])
