import sys, openpyxl, re
for fn in sys.argv[1:]:
    wb=openpyxl.load_workbook(fn,read_only=True)
    for sn in wb.sheetnames:
        ws=wb[sn]
        for row in ws.iter_rows(min_row=1,max_row=8,values_only=True):
            t=" ".join(str(x) for x in row if x)
            if re.search(r"(?i)drug.*(disorder|dependence or abuse)|dependence or abuse of illicit|alcohol use disorder|substance use disorder",t):
                print(fn.split("/")[-1],sn,"|",t[:160]); break
