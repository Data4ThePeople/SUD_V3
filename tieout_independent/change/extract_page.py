import json, re, sys
src = open(sys.argv[1]).read()
line = [l for l in src.splitlines() if l.startswith("const D = ")][0]
D = json.loads(line[len("const D = "):].rstrip().rstrip(";"))
out = {"years": D["years"], "change": D["change"],
       "geo": {k: {f: g.get(f) for f in ("name","abbr","death_rate","death_rate_drug","death_rate_alcohol","deaths","deaths_drug","deaths_alcohol")} for k, g in D["geo"].items()}}
json.dump(out, open(sys.argv[2], "w"), indent=0)
ch = D["change"]
print({k: {p: len(v) for p, v in c.items()} for k, c in ch.items()})
print(list(ch["alc10"]["alcohol"].items())[:3])
