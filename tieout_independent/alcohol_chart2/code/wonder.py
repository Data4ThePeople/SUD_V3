import sys, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
tmpl, out = sys.argv[1], sys.argv[2]
root = ET.parse(tmpl).getroot()
params = {}
for p in root.findall('parameter'):
    params[p.find('name').text] = [v.text or '' for v in p.findall('value')]
# my query: group by year, filter alcohol-induced, age-adjusted
params['B_1'] = ['D76.V1-level1']; params['B_2'] = ['*None*']
params['F_D76.V25'] = ['A']; params['I_D76.V25'] = ['A (Alcohol-induced causes)']
params['V_D76.V25'] = ['']
params['F_D76.V1'] = ['2002','2003','2018','2019']
params['V_D76.V1'] = ['']
params['O_V25_fmode'] = ['freg']; params['O_ucd']=['D76.V25']
params['V_D76.V22'] = ['*All*']; params['F_D76.V9']=['*All*']
params['O_aar'] = ['aar_std']; params['O_aar_pop'] = ['0000']
params['O_age'] = ['D76.V5']; params['V_D76.V5'] = ['*All*']; params['V_D76.V52'] = ['*All*']
params['O_precision'] = ['3']
params['M_1'] = ['D76.M1']; params['M_2'] = ['D76.M2']; params['M_3'] = ['D76.M3']; params['M_4']=['D76.M4']
params['accept_datause_restrictions'] = ['true']
params.pop('dataset_vintage',None); params['dataset_label']=['Underlying Cause of Death, 1999-2020']
xml = "<request-parameters>" + "".join(
    "<parameter><name>%s</name>%s</parameter>" % (k, "".join("<value>%s</value>" % v for v in vs)) for k, vs in params.items()) + "</request-parameters>"
data = urllib.parse.urlencode({'request_xml': xml, 'accept_datause_restrictions': 'true'}).encode()
req = urllib.request.Request('https://wonder.cdc.gov/controller/datarequest/D76', data=data, headers={})
try:
    resp = urllib.request.urlopen(req, timeout=300).read()
except urllib.error.HTTPError as e:
    resp = e.read(); print("HTTP", e.code)
open(out, 'wb').write(resp)
print(resp[:300])
