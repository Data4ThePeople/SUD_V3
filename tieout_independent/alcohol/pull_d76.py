"""Independent D76 pull: national alcohol-induced deaths by year (crude + AAR) and by year x 10-yr age."""
import re, sys, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent.parent / "data/raw/wonder_api/D76_Example2-req.xml"

def build(by_age):
    tree = ET.parse(TEMPLATE); root = tree.getroot()
    params = {p.find("name").text: p for p in root.findall("parameter")}
    def setp(name, values):
        p = params.get(name)
        if p is None:
            p = ET.SubElement(root, "parameter"); ET.SubElement(p, "name").text = name; params[name] = p
        for v in p.findall("value"): p.remove(v)
        for v in values: ET.SubElement(p, "value").text = v
    setp("B_1", ["D76.V1-level1"])
    setp("B_2", ["D76.V5"] if by_age else ["*None*"])
    setp("B_3", ["*None*"])
    setp("O_ucd", ["D76.V25"])
    setp("V_D76.V25", ["A"])          # Alcohol-induced causes
    setp("F_D76.V25", ["A"])
    setp("I_D76.V25", ["A (Alcohol-induced causes)"])
    setp("V_D76.V2", [])
    setp("F_D76.V2", ["*All*"])
    setp("V_D76.V22", ["*All*"])
    setp("V_D76.V52", ["*All*"])
    setp("V_D76.V5", ["*All*"])
    setp("O_age", ["D76.V5"])
    setp("O_aar", ["aar_none" if by_age else "aar_std"])
    setp("O_aar_pop", ["0000"])
    if not by_age:
        setp("M_4", ["D76.M4"])
    setp("dataset_label", ["Underlying Cause of Death, 1999-2020"])
    setp("dataset_vintage", ["2020"])
    setp("O_precision", ["3"])
    return ET.tostring(root, encoding="unicode")

def post(xml):
    if "--dump" in sys.argv: print(xml)
    data = urllib.parse.urlencode({"request_xml": xml, "accept_datause_restrictions": "true"}).encode()
    req = urllib.request.Request("https://wonder.cdc.gov/controller/datarequest/D76", data=data,
                                 headers={"User-Agent": "python-urllib"})
    return urllib.request.urlopen(req, timeout=300).read().decode()

import sys
which = sys.argv[1:] or ["d76_year", "d76_year_age"]
for name, by_age in [(n, n.endswith("age")) for n in which]:
    out = post(build(by_age))
    (HERE / "raw" / f"{name}.xml").write_text(out)
    print(name, len(out), "error" if "<message" in out and "error" in out.lower()[:5000] else "")
    time.sleep(3)
