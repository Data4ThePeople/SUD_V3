import pandas as pd, math, csv
n = pd.read_csv("nsduh_national_independent.csv").set_index(["outcome","pyearnm"])
for oc in ["ALCMON","ABODALC"]:
    a, b = n.loc[(oc,"2002-2003")], n.loc[(oc,"2018-2019")]
    z = (b.BSAE-a.BSAE)/math.hypot(a.ste_sae, b.ste_sae)
    print(f"{oc}: {a.BSAE*100:.2f}% [{a.low_sae*100:.2f}-{a.up_sae*100:.2f}] -> {b.BSAE*100:.2f}% [{b.low_sae*100:.2f}-{b.up_sae*100:.2f}]  "
          f"change {(b.BSAE/a.BSAE-1)*100:+.2f}%  diff {(b.BSAE-a.BSAE)*100:+.2f} pts  z={z:.2f}")
d = {int(r["year"]): float(r["d76_aar"]) for r in csv.DictReader(open("deaths_independent.csv")) if r["d76_aar"]}
e, l = (d[2002]+d[2003])/2, (d[2018]+d[2019])/2
print(f"AAR {e:.3f} -> {l:.3f} change {(l/e-1)*100:+.2f}%")
