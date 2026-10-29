import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
tabs = re.findall(r"<table.*?</table>", t, re.S)
tb = [x for x in tabs if re.search(r"<caption[^>]*>\s*Table "+sys.argv[2]+r"\b", x)][0]
rows = re.findall(r"<tr.*?</tr>", tb, re.S)
for r in rows[:int(sys.argv[3])]:
    cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)
    print([re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>","",c))).strip() for c in cells])
i = t.find(tb); after = t[i+len(tb):i+len(tb)+3000]
print(re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",after)))[:1500])
