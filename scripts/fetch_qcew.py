"""Pull QCEW annual averages for the supply NAICS codes, all ownerships, 2001-2024.

Writes data/raw/qcew/qcew_<year>.csv holding the unmodified BLS rows for our codes.
2014+ comes from the open-data industry slices; earlier years from the annual
by-industry zip, which is streamed and filtered, then discarded.
"""
import csv, io, sys, zipfile
from datetime import date
from pathlib import Path
import requests

CODES = ["621420", "621330", "621112"]
UA = {"User-Agent": "Mozilla/5.0 (Data4ThePeople research; connect@data4thepeople.com)"}
OUT = Path(__file__).resolve().parents[1] / "data/raw/qcew"
OUT.mkdir(parents=True, exist_ok=True)


def from_api(year):
    rows, header = [], None
    for code in CODES:
        r = requests.get(f"https://data.bls.gov/cew/data/api/{year}/a/industry/{code}.csv", headers=UA, timeout=120)
        if r.status_code != 200:
            return None
        rd = list(csv.reader(io.StringIO(r.text)))
        header = rd[0]
        rows += rd[1:]
    return header, rows


def from_zip(year):
    url = f"https://data.bls.gov/cew/data/files/{year}/csv/{year}_annual_by_industry.zip"
    tmp = OUT / f"_{year}.zip"
    with requests.get(url, headers=UA, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    header, rows = None, []
    with zipfile.ZipFile(tmp) as z:
        for name in z.namelist():
            if not any(f" {c} " in name for c in CODES):
                continue
            with z.open(name) as fh:
                rd = list(csv.reader(io.TextIOWrapper(fh, "utf-8")))
            header = rd[0]
            rows += [r for r in rd[1:] if r[header.index("industry_code")] in CODES]
    tmp.unlink()
    return header, rows


def main(years):
    for y in years:
        dest = OUT / f"qcew_{y}.csv"
        if dest.exists():
            continue
        got = from_api(y) or from_zip(y)
        header, rows = got
        found = {r[header.index("industry_code")] for r in rows}
        if found != set(CODES):
            sys.exit(f"{y}: missing codes {set(CODES) - found}")
        with open(dest, "w", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            w.writerow(header)
            w.writerows(rows)
        print(y, len(rows), "rows", flush=True)
    with open(OUT / "PULLED.txt", "a") as f:
        f.write(f"{date.today()} QCEW annual averages, NAICS {','.join(CODES)}, all ownerships, years {years[0]}-{years[-1]}. "
                "2014+ from data.bls.gov/cew/data/api/<yr>/a/industry/<code>.csv; earlier from "
                "data.bls.gov/cew/data/files/<yr>/csv/<yr>_annual_by_industry.zip (rows for our codes kept unchanged).\n")


if __name__ == "__main__":
    main(list(range(2001, 2025)))
