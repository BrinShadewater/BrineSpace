from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,b):
 old=p.read_bytes();tmp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(b)
 if p.read_bytes()!=old:raise RuntimeError('Concurrent edit '+str(p))
 os.replace(tmp,p)
g=read(P/'native-staged-behaviour-validation.json');assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
assert not any(x in (P/'native-staged-behaviour.log').read_text() for x in ['ERROR:','SCRIPT ERROR:'])
assert read(P/'package-verification.json')['failures']==0
old='james-west-water-death-polish-v1';new=P.name
p=R/'scripts/grid_canvas.gd';b=p.read_bytes();(P/'grid_canvas-before-install.gd.txt').write_bytes(b)
for mode in ['bare','helmet']:
 a=f'res://character/{old}/{mode}-manifest.json'.encode();c=f'res://character/{new}/{mode}-manifest.json'.encode();assert b.count(a)==1;b=b.replace(a,c)
atomic(p,b)
p=R/'character/ACTIVE_ASSETS.json';b=p.read_bytes();(P/'ACTIVE_ASSETS-before-install.json').write_bytes(b);m=json.loads(b)
for field,mode in [('actionOverrides','bare'),('equipmentActionOverrides','helmet')]:
 key='branforth-west-water-death-polish';assert m[field][key]==f'character/{old}/{mode}-manifest.json';m[field][key]=f'character/{new}/{mode}-manifest.json'
atomic(p,(json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode())
for mode in ['bare','helmet']:
 p=P/(mode+'-manifest.json');m=read(p);m['status']='installed_owner_review_pending';atomic(p,(json.dumps(m,indent=2)+'\n').encode())
(P/'selection.json').write_text(json.dumps({'status':'installed_owner_review_pending','runtimeInstalled':True,'fullSetComplete':False,'statesPerMode':1,'refsPerMode':6,'method':'Original native source-builder material curve; generated candidates unselected','pending':['Installed loader/mortality/disk restore','Owner and full-set consistency/journey review']},indent=2)+'\n')
print('Selected paired West water-death material correction; exact original alpha/anatomy/entry and finite clock.')
