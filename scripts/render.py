"""Write dist/index.html: the template with data/build/dashboard.json inlined."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "scripts/template.html").read_text()
data = (ROOT / "data/build/dashboard.json").read_text()
if html.count("/*DATA*/null") != 1:
    raise SystemExit("template must contain exactly one /*DATA*/null placeholder")
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist/index.html").write_text(html.replace("/*DATA*/null", data))
print("dist/index.html", len(html) // 1024 + len(data) // 1024, "KB")
