# usage: extract_page.py dist/index.html OUT.json
import sys, json, re
h=open(sys.argv[1],encoding="utf-8").read()
i=h.index("const D = ")+len("const D = ")
D,end=json.JSONDecoder().raw_decode(h[i:])
json.dump(D,open(sys.argv[2],"w"))
print(D.keys()); print(D["years"]); g=D["geo"]; print(len(g), list(g)[:5]); print(list(g["US"].keys()))
for k in ["sud_drug_pct","sud_drug_lo","sud_drug_hi","sud_drug_count","sud_drug_count_lo","sud_drug_count_hi","deaths_drug","death_rate_drug"]:
    print(k, g["US"][k])
