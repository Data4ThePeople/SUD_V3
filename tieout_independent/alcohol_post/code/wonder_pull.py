"""Pull D76 (1999-2020) alcohol-induced deaths from the CDC WONDER API."""
import sys, re, requests, xml.etree.ElementTree as ET, time
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
EX = Path('/Users/ericpachman/PycharmProjects/SUD_V3/data/raw/wonder_api/D76_Example2-req.xml')

def base():
    root = ET.parse(EX).getroot()
    p = {}
    for par in root.findall('parameter'):
        n = par.find('name').text
        vals = [v.text or '' for v in par.findall('value')]
        p[n] = vals
    return p

def build(p):
    out = ['<request-parameters>']
    for k, vals in p.items():
        out.append('<parameter><name>%s</name>' % k)
        for v in vals:
            v = v.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            out.append('<value>%s</value>' % v)
        out.append('</parameter>')
    out.append('</request-parameters>')
    return ''.join(out)

def run(name, groups, aar):
    p = base()
    for i in range(1,6):
        p['B_%d'%i] = [groups[i-1] if i-1 < len(groups) else '*None*']
    p['O_aar'] = ['aar_std' if aar else 'aar_none']
    p['O_aar_pop'] = ['0000']
    p['O_title'] = [name]
    p['O_precision'] = ['3']
    p['O_age'] = ['D76.V5']   # ten-year age groups
    p['V_D76.V22'] = ['*All*']
    p['O_ucd'] = ['D76.V25-level1']
    p['V_D76.V1'] = ['*All*']
    p['V_D76.V9'] = ['']
    p['V_D76.V5'] = ['*All*']
    xml = build(p)
    r = requests.post('https://wonder.cdc.gov/controller/datarequest/D76',
                      data={'request_xml': xml, 'accept_datause_restrictions': 'true'}, timeout=600)
    (HERE/'raw'/f'{name}.xml').write_text(r.text)
    print(name, r.status_code, len(r.text))

time.sleep(16)
run('d76_year_cause_aar', ['D76.V1-level1', 'D76.V25-level1'], True)
time.sleep(20)
run('d76_year_age_cause', ['D76.V1-level1', 'D76.V5', 'D76.V25-level1'], False)
