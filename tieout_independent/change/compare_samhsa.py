"""Parse SAMHSA change tables (12+ columns) and compare with D.change in the page."""
import sys, re, html, json
raw, pagejson = sys.argv[1], sys.argv[2]
P = json.load(open(pagejson))
FIPS = {"Alabama":"01","Alaska":"02","Arizona":"04","Arkansas":"05","California":"06","Colorado":"08","Connecticut":"09","Delaware":"10","District of Columbia":"11","Florida":"12","Georgia":"13","Hawaii":"15","Idaho":"16","Illinois":"17","Indiana":"18","Iowa":"19","Kansas":"20","Kentucky":"21","Louisiana":"22","Maine":"23","Maryland":"24","Massachusetts":"25","Michigan":"26","Minnesota":"27","Mississippi":"28","Missouri":"29","Montana":"30","Nebraska":"31","Nevada":"32","New Hampshire":"33","New Jersey":"34","New Mexico":"35","New York":"36","North Carolina":"37","North Dakota":"38","Ohio":"39","Oklahoma":"40","Oregon":"41","Pennsylvania":"42","Rhode Island":"44","South Carolina":"45","South Dakota":"46","Tennessee":"47","Texas":"48","Utah":"49","Vermont":"50","Virginia":"51","Washington":"53","West Virginia":"54","Wisconsin":"55","Wyoming":"56","Total U.S.":"US"}
def parse(path, n):
    t = open(path, encoding="utf-8", errors="replace").read()
    tabs = re.findall(r"<table.*?</table>", t, re.S)
    tb = [x for x in tabs if re.search(r"<caption[^>]*>\s*Table " + n + r"\b", x)]
    assert len(tb) == 1
    out = {}
    for r in re.findall(r"<tr.*?</tr>", tb[0], re.S):
        c = [re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", "", x))).strip() for x in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
        if not c or c[0] not in FIPS: continue
        m = re.fullmatch(r"([\d.]+)\s*([ab]?)", c[1]); assert m, c
        frm, mark = float(m.group(1)), m.group(2)
        to = float(re.fullmatch(r"[\d.]+", c[2]).group(0)); p = float(c[3])
        res = "no significant change"
        if mark == "a": res = "increased" if to > frm else "decreased" if to < frm else "TIE"
        out[FIPS[c[0]]] = dict(name=c[0], frm=frm, to=to, p=p, mark=mark, res=res)
    assert len(out) == 52, len(out)
    return out
comps = [("alc10", "alcohol", "longterm.htm", "9"), ("sud1", "all", "chg2024.htm", "21"),
         ("sud1", "alcohol", "chg2024.htm", "22"), ("sud1", "drug", "chg2024.htm", "24")]
total = diffs = 0; summary = {}; mine = {}
for comp, part, f, n in comps:
    S = parse(raw + "/" + f, n); pg = P["change"][comp][part]
    mine[f"{comp}/{part}"] = S
    cnt = {"increased": 0, "decreased": 0, "no significant change": 0}
    bmarks = []; checks = []
    if set(S) != set(pg): print("KEY MISMATCH", comp, part, set(S) ^ set(pg)); diffs += 1
    for k, s in S.items():
        cnt[s["res"]] += 0 if k == "US" else 1
        if s["mark"] == "a" and not s["p"] < 0.05: checks.append(("a but p>=.05", s["name"], s["p"]))
        if s["mark"] != "a" and s["p"] < 0.05: checks.append(("p<.05 but no a", s["name"], s["p"], s["mark"]))
        if s["mark"] == "b": bmarks.append(s["name"])
        g = pg.get(k)
        if g is None: continue
        for i, (fld, v) in enumerate([("from", s["frm"]), ("to", s["to"]), ("p", s["p"]), ("res", s["res"])]):
            total += 1
            if (g[i] != v) if fld == "res" else abs(g[i] - v) > 1e-9:
                diffs += 1; print("DIFF", comp, part, s["name"], fld, "page", g[i], "samhsa", v)
    summary[f"{comp}/{part} (Table {n})"] = dict(states=cnt, us=S["US"], b_only=bmarks, marker_checks=checks,
        p000=[s["name"] for s in S.values() if s["p"] == 0])
print("values compared:", total, "differences:", diffs)
print(json.dumps(summary, indent=1))
json.dump(mine, open("samhsa_parsed.json", "w"), indent=1)
