"""Minimal CDC WONDER API client (national data only). Usage: wonder_api.py <db> <out.xml> k=v ..."""
import re, sys, urllib.parse, urllib.request
from xml.sax.saxutils import escape
import os; EX = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "..", "data", "raw", "wonder_api", "D76_Example2-req.xml")
db, out, kv = sys.argv[1], sys.argv[2], dict(a.split("=", 1) for a in sys.argv[3:])
base = dict((n, v.strip()) for n, v in re.findall(r"<name>(.*?)</name>\s*<value>(.*?)</value>", open(EX).read(), re.S))
p = {k.replace("D76", db): v.replace("D76", db) for k, v in base.items()}
p.update({"B_1": f"{db}.V1-level1", "B_2": "*None*", "O_title": "", "dataset_code": db,
          "V_%s.V22" % db: "*All*", "V_%s.V52" % db: "*All*", "O_ucd": f"{db}.V2", "O_age": f"{db}.V5",
          "O_aar": "aar_none", "accept_datause_restrictions": "true"})
for k in ("dataset_label", "dataset_vintage"): p.pop(k, None)
if kv.pop("MIN", None):
    p = {k: v for k, v in p.items() if not k.startswith(("V_", "F_", "I_", "VM_", "finder-stage", "O_V"))}
    pass
for k, v in kv.items():
    if v == "DEL": p.pop(k, None)
    else: p[k] = v
xml = "<request-parameters>" + "".join(
    "<parameter><name>%s</name>%s</parameter>" % (escape(k), "".join("<value>%s</value>" % escape(x) for x in v.split("|")))
    for k, v in p.items()) + "</request-parameters>"
data = urllib.parse.urlencode({"request_xml": xml, "accept_datause_restrictions": "true"}).encode()
import urllib.error
try:
    body = urllib.request.urlopen(urllib.request.Request(f"https://wonder.cdc.gov/controller/datarequest/{db}", data=data), timeout=300).read()
except urllib.error.HTTPError as e:
    body = e.read(); print("HTTP", e.code)
open(out, "wb").write(body)
t = open(out, errors="ignore").read()
rows = re.findall(r"<r>(.*?)</r>", t, re.S)
print(len(rows), "rows")
for r_ in rows[:40]:
    print(" | ".join((a or b) for a, b in re.findall(r'<c (?:l|c)="([^"]*)"|<c v="([^"]*)"', r_)))
if not rows: print(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", t))[:1500])
