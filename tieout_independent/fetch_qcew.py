import requests, os, zipfile, io, sys
UA={"User-Agent":"Mozilla/5.0 (Data4ThePeople research; connect@data4thepeople.com)"}
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"raw","qcew")
N=["621420","621330","621112"]
for y in range(2014,2025):
    for n in N:
        p=f"{OUT}/api_{y}_{n}.csv"
        if os.path.exists(p): continue
        r=requests.get(f"https://data.bls.gov/cew/data/api/{y}/a/industry/{n}.csv",headers=UA,timeout=120); r.raise_for_status()
        open(p,"wb").write(r.content)
print("api done",flush=True)
for y in range(2001,2014):
    p=f"{OUT}/zip_{y}.zip"
    if not os.path.exists(p):
        with requests.get(f"https://data.bls.gov/cew/data/files/{y}/csv/{y}_annual_by_industry.zip",headers=UA,timeout=600,stream=True) as r:
            r.raise_for_status()
            with open(p+".part","wb") as f:
                for c in r.iter_content(1<<20): f.write(c)
        os.rename(p+".part",p)
    z=zipfile.ZipFile(p)
    for name in z.namelist():
        for n in N:
            if f".{n} " in name or name.endswith(f"{n}.csv") or f" {n} " in name:
                tgt=f"{OUT}/zip_{y}_{n}.csv"
                open(tgt,"wb").write(z.read(name))
    print("zip",y,flush=True)
