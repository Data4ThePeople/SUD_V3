# usage: titles.py RAWDIR file1 file2 ...
import sys, openpyxl
R=sys.argv[1]
for fn in sys.argv[2:]:
    wb=openpyxl.load_workbook(R+"/"+fn,read_only=True)
    for ws in wb.worksheets:
        for r in ws.iter_rows(min_row=1,max_row=3,values_only=True):
            t=" ".join(str(x) for x in r if x)
            if "lcohol" in t: print(fn,"|",ws.title,"|",t[:200]); break
