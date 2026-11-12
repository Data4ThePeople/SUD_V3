import pandas as pd, sys
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
d = pd.concat([pd.read_sas("raw/nsduh/sae9919.sas7bdat", encoding="latin-1"), pd.read_sas("raw/nsduh/sae2124.sas7bdat", encoding="latin-1")])
n = d[(d.stname=="National") & (d.agegrp==0) & d.outcome.isin(["ALCMON","ABODALC","UDYR5ALC","U_ALCMON","U_UDYALC"])]
n = n[["outcome","outname","pyearnm","BSAE","low_sae","up_sae","ste_sae","est_total"]].sort_values(["outcome","pyearnm"])
print(n.to_string())
n.to_csv("nsduh_national_independent.csv", index=False)
