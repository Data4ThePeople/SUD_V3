"""Download NSDUH state small-area-estimate files from SAMHSA, unchanged.

Usage: python -I scripts/fetch_nsduh.py <subdir> <url> "<description>" [<url> "<description>" ...]
Saves into data/raw/nsduh/<subdir>/ and appends a line to data/raw/nsduh/PULLED.txt.
Skips a file already on disk.
"""
import datetime
import pathlib
import sys
import urllib.parse

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw" / "nsduh"
UA = "Mozilla/5.0 (Data4ThePeople research; connect@data4thepeople.com)"


def fetch(subdir, url, desc):
    out_dir = ROOT / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    name = urllib.parse.unquote(pathlib.PurePosixPath(urllib.parse.urlparse(url).path).name).strip()
    dest = out_dir / name
    if dest.exists() and dest.stat().st_size > 0:
        print("exists", dest)
        return
    r = requests.get(url, headers={"User-Agent": UA}, timeout=300)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "")
    if "text/html" in ctype and not name.endswith((".htm", ".html")):
        raise SystemExit(f"Got HTML instead of a file for {url}")
    dest.write_bytes(r.content)
    with open(ROOT / "PULLED.txt", "a") as f:
        f.write(f"{datetime.date.today().isoformat()}\t{url}\t{subdir}/{name}\t{desc}\n")
    print("saved", dest, len(r.content))


if __name__ == "__main__":
    args = sys.argv[1:]
    subdir = args[0]
    pairs = args[1:]
    for i in range(0, len(pairs), 2):
        fetch(subdir, pairs[i], pairs[i + 1])
