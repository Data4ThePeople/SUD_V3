import sys, openpyxl
fn,sn=sys.argv[1],sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 10
ws=openpyxl.load_workbook(fn,read_only=True)[sn]
for i,row in enumerate(ws.iter_rows(values_only=True)):
    if i>=n: break
    print([x for x in row][:9])
