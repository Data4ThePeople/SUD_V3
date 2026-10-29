import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for n in sys.argv[2:]:
    m = re.search(r"<caption[^>]*>\s*Table "+n+r"\b", t)
    end = t.find("</table>", m.start())
    seg = re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",t[m.start():end+3000]))).replace("‑","-")
    i = seg.find("Wyoming")
    print("TABLE", n, ":", seg[i:i+2500], "\n")
