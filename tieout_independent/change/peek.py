import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
caps = re.findall(r"<caption[^>]*>(.*?)</caption>", t, re.S)
for i, c in enumerate(caps): print(i, re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>","",c)))[:200])
