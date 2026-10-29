import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
txt = re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",t))).replace("‑","-")
seen=set()
for pat in sys.argv[2:]:
    for m in re.finditer(pat, txt, re.I):
        s = txt[max(0,m.start()-300):m.end()+400]
        key = s[:80]
        if key in seen: continue
        seen.add(key); print("...", s, "...\n")
