import sys, time, requests
sys.path.insert(0,'code')
import importlib.util
src=open('code/wonder_pull.py').read().split("time.sleep(16)\nrun(")[0]
exec(src)
def go(mod):
    p=base(); mod(p)
    time.sleep(16)
    r=requests.post('https://wonder.cdc.gov/controller/datarequest/D76',data={'request_xml':build(p),'accept_datause_restrictions':'true'},timeout=600)
    import re; m=re.search('<message>(.*?)</message>',r.text,re.S); print(r.status_code, m.group(1) if m else 'ok')
go(lambda p: None)
def m1(p): p['B_1']=['D76.V1-level1']; p['B_2']=['*None*']
go(m1)
