# usage: wonder_api.py OUTFILE  -- national 2020 deaths by Drug/Alcohol induced cause x ICD-10 code (D76)
import sys, requests, time
p={"B_1":"D76.V25","B_2":"*None*","B_3":"*None*","B_4":"*None*","B_5":"*None*",
"M_1":"D76.M1","M_2":"D76.M2","M_3":"D76.M3",
"F_D76.V1":"2020","F_D76.V10":"*All*","F_D76.V2":"*All*","F_D76.V27":"*All*","F_D76.V9":"*All*",
"I_D76.V1":"2020","I_D76.V10":"*All* (The United States)","I_D76.V2":"*All* (All Causes of Death)","I_D76.V27":"*All* (The United States)","I_D76.V9":"*All* (The United States)",
"O_V10_fmode":"freg","O_V1_fmode":"freg","O_V27_fmode":"freg","O_V2_fmode":"freg","O_V9_fmode":"freg",
"O_aar":"aar_none","O_aar_pop":"0000","O_age":"D76.V5","O_javascript":"on","O_location":"D76.V9","O_precision":"1","O_rate_per":"100000","O_show_totals":"false","O_timeout":"300","O_title":"","O_ucd":"D76.V25","O_urban":"D76.V19",
"V_D76.V1":"","V_D76.V10":"","V_D76.V11":"*All*","V_D76.V12":"*All*","V_D76.V17":"*All*","V_D76.V19":"*All*","V_D76.V2":"","V_D76.V20":"*All*","V_D76.V21":"*All*","V_D76.V22":"*All*","V_D76.V23":"*All*","V_D76.V24":"*All*","V_D76.V25":"*All*","V_D76.V27":"","V_D76.V4":"*All*","V_D76.V5":["*All*"],"V_D76.V51":"*All*","V_D76.V52":"*All*","V_D76.V6":"00","V_D76.V7":"*All*","V_D76.V8":"*All*","V_D76.V9":"",
"action-Send":"Send","finder-stage-D76.V1":"codeset","finder-stage-D76.V10":"codeset","finder-stage-D76.V2":"codeset","finder-stage-D76.V27":"codeset","finder-stage-D76.V9":"codeset","stage":"request"}
x="<request-parameters>\n"
for k,v in p.items():
    vs=v if isinstance(v,list) else [v]
    x+="<parameter>\n<name>%s</name>\n%s</parameter>\n"%(k,"".join("<value>%s</value>\n"%s for s in vs))
x+="</request-parameters>"
x=x.replace("*All* (The United States)","*All* (The United States)")
UA={"User-Agent":"Mozilla/5.0 (Macintosh) (independent tie-out; connect@data4thepeople.com)"}
r=requests.post("https://wonder.cdc.gov/controller/datarequest/D76",data={"request_xml":x,"accept_datause_restrictions":"true"},headers=UA,timeout=300)
print(r.status_code,len(r.content)); open(sys.argv[1],"wb").write(r.content); time.sleep(1)
