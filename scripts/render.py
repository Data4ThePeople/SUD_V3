"""Write one self-contained page per version: the template with that version's data inlined.

dist/v1-oews/index.html             People per Worker uses OEWS clinicians
dist/v2-qcew-private/index.html     People per Worker uses QCEW private outpatient workers
dist/index.html                     a short page linking the two, for side-by-side review
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {"v1_oews": "v1-oews", "v2_qcew_private": "v2-qcew-private"}

html = (ROOT / "scripts/template.html").read_text()
if html.count("/*DATA*/null") != 1:
    raise SystemExit("template must contain exactly one /*DATA*/null placeholder")
for name, folder in VERSIONS.items():
    data = (ROOT / f"data/build/dashboard_{name}.json").read_text()
    out = ROOT / "dist" / folder / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html.replace("/*DATA*/null", data))
    print(out.relative_to(ROOT), (len(html) + len(data)) // 1024, "KB")
(ROOT / "dist/index.html").write_text("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Demand Without A Door: versions</title>
<style>body{background:#13161b;color:#eef0f3;font-family:Georgia,serif;padding:48px 16px;max-width:720px;margin:0 auto}
a{color:#5aa9ff;font-size:20px}li{margin:14px 0}</style></head><body>
<h1>Demand Without A Door: two versions for review</h1><ul>
<li><a href="v1-oews/index.html">Version 1: People per Worker with OEWS clinicians</a></li>
<li><a href="v2-qcew-private/index.html">Version 2: People per Worker with QCEW private outpatient workers</a></li>
</ul><p>Built by Data 4 The People</p></body></html>
""")
