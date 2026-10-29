import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t = re.sub(r"<(script|style).*?</\1>", " ", t, flags=re.S)
print(re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",t))).replace("‑","-"))
