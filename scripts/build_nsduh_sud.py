"""Build data/clean/nsduh_sud.csv: NSDUH state small area estimates of past-year
substance use disorder (any SUD), ages 12+, one row per window x state.

Sources (all saved unchanged under data/raw/nsduh/):
  * Per-window published tables (xlsx or HTML) where SAMHSA still hosts them:
    2009-2010 through 2023-2024.
  * SAMHSA's 1999-2019 state SAE dataset (SAS) for the windows whose tables are
    no longer hosted on samhsa.gov: 2000-2001 and 2002-2003 through 2008-2009.
    SAMHSA says this file "does not provide any new information" beyond the
    published tables.

Rules: values are copied as published. Excel and SAS store proportions; pct is
that proportion times 100 done in decimal arithmetic (no rounding). HTML tables
(2009-2010 pct) are already percents with 2 decimals and are copied as is.
Nothing is filled, interpolated, or derived.

Run with: .venv/bin/python -I scripts/build_nsduh_sud.py
"""
import csv
import html
import pathlib
import re
from decimal import Decimal
from html.parser import HTMLParser

import openpyxl
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "nsduh"
OUT = ROOT / "data" / "clean" / "nsduh_sud.csv"

STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
    "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
]
KEEP = set(STATES) | {"United States"}

DSM4_NAME = "Dependence or Abuse of Illicit Drugs or Alcohol in the Past Year"

# window -> (pct source, count source); each source is (kind, relative path)
TABLES = {
    "2009-2010": (("html", "2009-2010/NSDUHsaeMainReport2010.htm"), ("html", "2009-2010/NSDUHsaeCountTabs2010.htm")),
    "2010-2011": (("xlsx", "2010-2011/NSDUHsaeExcelTab20-2011.xlsx"), ("html", "2010-2011/NSDUHsaeCountTabs2011.htm")),
    "2011-2012": (("xlsx", "2011-2012/NSDUHsaeExcelTab20-2012.xlsx"), ("xlsx", "2011-2012/NSDUHsaeTotals2012.xlsx")),
    "2012-2013": (("xlsx", "2012-2013/NSDUHsaeExcelTabs2013.xlsx"), ("xlsx", "2012-2013/NSDUHsaeTotals2013.xlsx")),
    "2013-2014": (("xlsx", "2013-2014/NSDUHsaeExcelTabs2014.xlsx"), ("xlsx", "2013-2014/NSDUHsaeTotals2014.xlsx")),
    "2015-2016": (("xlsx", "2015-2016/NSDUHsaeExcelTabs2016.xlsx"), ("xlsx", "2015-2016/NSDUHsaeTotals2016.xlsx")),
    "2016-2017": (("xlsx", "2016-2017/NSDUHsaeExcelTabs2017.xlsx"), ("xlsx", "2016-2017/NSDUHsaeTotals2017.xlsx")),
    "2017-2018": (("xlsx", "2017-2018/NSDUHsaeExcelTabs2018.xlsx"), ("xlsx", "2017-2018/NSDUHsaeTotals2018.xlsx")),
    "2018-2019": (("xlsx", "2018-2019/2019NSDUHsaeExcelTabs.xlsx"), ("xlsx", "2018-2019/2019NSDUHsaeTotals.xlsx")),
    "2021-2022": (("xlsx", "2021-2022/2022-nsduh-sae-tables-percent.xlsx"), ("xlsx", "2021-2022/2022-nsduh-sae-totals-tables.xlsx")),
    "2022-2023": (("xlsx", "2022-2023/2023-nsduh-sae-tables-percent.xlsx"), ("xlsx", "2022-2023/2023-nsduh-sae-totals-tables.xlsx")),
    "2023-2024": (("xlsx", "2023-2024/2024-nsduh-sae-tables-percent.xlsx"), ("xlsx", "2023-2024/2024-nsduh-sae-totals-tables.xlsx")),
}
SAS_9919 = "sae_dataset_1999-2019/NSDUH_99_19_state_saes_final.sas7bdat"
SAS_2124 = "sae_dataset_2021-2024/state_saes_final_2124.sas7bdat"
SAS_WINDOWS = ["2000-2001", "2002-2003", "2003-2004", "2004-2005", "2005-2006",
               "2006-2007", "2007-2008", "2008-2009"]

TITLE_RE = re.compile(r"(Dependence or Abuse of Illicit Drugs or Alcohol in the Past Year|"
                      r"^Table \d+\. Substance Use Disorder in the Past Year)", re.I)


def norm_state(s):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return "United States" if s in ("Total U.S.", "National", "Total US") else s


def dec(x):
    """Exact decimal form of a stored number (shortest repr), no rounding."""
    return Decimal(repr(float(x))) if not isinstance(x, str) else Decimal(x.replace(",", ""))


def pct_from_prop(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    return format((dec(x) * 100).normalize(), "f")


def count_str(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    d = dec(x)
    return format(d.normalize(), "f")


def read_xlsx(path):
    """Return (sheet title, {state: (est, lo, hi)}) for the 12+ columns of the any-SUD table."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for sn in wb.sheetnames:
        rows = list(wb[sn].iter_rows(values_only=True))
        if not rows or not rows[0] or not rows[0][0]:
            continue
        title = str(rows[0][0]).strip()
        if not TITLE_RE.search(title):
            continue
        hdr_i = next(i for i, r in enumerate(rows) if r and r[0] == "Order")
        hdr = [str(h or "") for h in rows[hdr_i]]
        assert hdr[1] == "State", hdr
        assert re.match(r"12(\+| or Older)\s*Estimate", hdr[2]) and "Lower" in hdr[3] and "Upper" in hdr[4], hdr
        notes = " ".join(str(r[0]) for r in rows[1:hdr_i] if r and r[0])
        out = {}
        for r in rows[hdr_i + 1:]:
            if r[1] is None:
                continue
            out[norm_state(r[1])] = (r[2], r[3], r[4])
        return title, notes, sn, out
    raise SystemExit(f"No any-SUD sheet in {path}")


class TableGrab(HTMLParser):
    """Collect tables as (caption, rows of cell text)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.cur, self.row, self.cell, self.cap, self.in_cap = [], None, None, None, "", False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.cur = {"caption": "", "rows": []}
        elif tag == "caption" and self.cur is not None:
            self.in_cap = True
        elif tag == "tr" and self.cur is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = ""
        elif tag == "br" and self.cell is not None:
            self.cell += " "

    def handle_endtag(self, tag):
        if tag == "table" and self.cur is not None:
            self.tables.append(self.cur)
            self.cur = None
        elif tag == "caption":
            self.in_cap = False
        elif tag == "tr" and self.row is not None and self.cur is not None:
            self.cur["rows"].append(self.row)
            self.row = None
        elif tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row.append(re.sub(r"\s+", " ", self.cell).strip())
            self.cell = None

    def handle_data(self, data):
        if self.in_cap and self.cur is not None:
            self.cur["caption"] += data
        elif self.cell is not None:
            self.cell += data


def read_html(path, want_counts):
    p = TableGrab()
    p.feed(path.read_text(encoding="latin-1"))
    kind = "Estimated Numbers" if want_counts else "Percentages, Annual Averages Based on"
    for t in p.tables:
        cap = re.sub(r"\s+", " ", t["caption"]).strip()
        if "Dependence or Abuse of Illicit Drugs or Alcohol in the Past Year" in cap and kind in cap \
                and "P Values" not in cap and "P\xa0Values" not in cap:
            hdr = t["rows"][0]
            assert hdr[0] == "State" and hdr[1].startswith("12+") and "Confidence" in hdr[2], hdr
            out = {}
            for r in t["rows"][1:]:
                if len(r) < 3:
                    continue
                m = re.match(r"\(\s*([\d,\.]+)\s*[-–‐]\s*([\d,\.]+)\s*\)", r[2].replace("\xa0", " "))
                assert m, r
                out[norm_state(r[0])] = (r[1].replace(",", ""), m.group(1).replace(",", ""), m.group(2).replace(",", ""))
            return cap, out
    raise SystemExit(f"No table in {path}")


def main():
    rows = []
    # Windows from published tables
    for window, ((pk, pp), (ck, cp)) in TABLES.items():
        if pk == "xlsx":
            ptitle, pnotes, psheet, pct = read_xlsx(RAW / pp)
            pct = {s: tuple(pct_from_prop(v) for v in vals) for s, vals in pct.items()}
            # sanity: values were proportions
            assert float(pct["United States"][0]) < 100
            psrc = f"{pp} [{psheet}]"
        else:
            ptitle, pct = read_html(RAW / pp, want_counts=False)
            pnotes = "DSM-IV"  # HTML table footnote: "based on definitions found in the 4th edition" (DSM-IV)
            pct = {s: vals for s, vals in pct.items()}
            psrc = f"{pp} [{ptitle.split(' ')[0]} {ptitle.split(' ')[1]}]"
        if ck == "xlsx":
            ctitle, _, csheet, cnt = read_xlsx(RAW / cp)
            cnt = {s: tuple(count_str(v) for v in vals) for s, vals in cnt.items()}
            csrc = f"{cp} [{csheet}]"
        else:
            ctitle, cnt = read_html(RAW / cp, want_counts=True)
            csrc = f"{cp} [Table 20]"
        # DSM edition comes from the table's own NOTE text
        if "5th edition" in pnotes:
            dsm = "5"
        elif "4th edition" in pnotes or "DSM-IV" in pnotes:
            dsm = "IV"
        else:
            raise SystemExit(f"Cannot tell DSM edition for {window}")
        # measure name = the table title up to ", by Age Group" / ": Among"
        mname = re.split(r",? by Age Group|: Among", re.sub(r"^Table [A-Z]?\.?\d+\.?\s*[\u2013-]?\s*", "", ptitle))[0].strip()
        missing = KEEP - set(pct) | KEEP - set(cnt)
        assert not missing, (window, missing)
        for s in sorted(KEEP, key=lambda x: (x != "United States", x)):
            p, c = pct[s], cnt[s]
            rows.append(dict(window=window, end_year=int(window[-4:]), state=s,
                             pct=p[0], pct_lo=p[1], pct_hi=p[2],
                             count_thousands=c[0], count_lo=c[1], count_hi=c[2],
                             measure_name=mname, dsm=dsm, source_file=f"pct: {psrc}; count: {csrc}"))

    # Windows only in SAMHSA's SAS dataset
    d = pd.read_sas(RAW / SAS_9919, encoding="latin1")
    d.columns = [c.lower() for c in d.columns]
    d = d[(d.outcome == "ABODILAL") & (d.agegrp == 0) & d.pyearnm.isin(SAS_WINDOWS)]
    for _, r in d.iterrows():
        s = norm_state(r.stname)
        if s not in KEEP:
            continue
        rows.append(dict(window=r.pyearnm, end_year=int(r.pyearnm[-4:]), state=s,
                         pct=pct_from_prop(r.bsae), pct_lo=pct_from_prop(r.low_sae), pct_hi=pct_from_prop(r.up_sae),
                         count_thousands=count_str(r.est_total), count_lo=count_str(r.low_total),
                         count_hi=count_str(r.up_total), measure_name=DSM4_NAME, dsm="IV",
                         source_file=f"{SAS_9919} [OUTCOME=ABODILAL, AGEGRP=0]"))

    rows.sort(key=lambda r: (r["end_year"], r["state"] != "United States", r["state"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} rows, {len({r['window'] for r in rows})} windows)")


if __name__ == "__main__":
    main()
