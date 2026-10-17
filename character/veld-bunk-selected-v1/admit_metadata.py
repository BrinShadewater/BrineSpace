"""Admission labels and registry additions after both frozen native intervals."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-selected-native-v1'
native=json.loads((O/'validation.json').read_text());assert native['passed']
continuation=json.loads((R/'output/veld-bunk-selected-continue-v1/validation.json').read_text());assert continuation['passed']
tested=json.loads((O/'inputs-after.json').read_text());changes=[]
folders=['veld-bunk-body-master-v1','veld-bunk-early-fall-v1']
old_status=['staged_whole_body_native_contact_pending','staged_source_only_native_entry_contact_pending']
installed='installed_locally_owner_motion_review_open'
loader=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
for folder,status in zip(folders,old_status):
 root=R/'character'/folder
 for gear in ['bare','helmet']:
  path=root/f'{gear}-manifest.json';rel=path.relative_to(R).as_posix();snapshot=P/f'{folder}-{gear}-tested-manifest.json'
  assert '"res://'+rel+'"' in loader
  raw=path.read_bytes();old=json.loads(raw)
  if old['status']==installed:raw=snapshot.read_bytes();old=json.loads(raw)
  assert hashlib.sha256(raw).hexdigest()==tested[rel] and old['status']==status
  if not snapshot.exists():snapshot.write_bytes(raw)
  new=dict(old);new['status']=installed;path.write_text(json.dumps(new,indent=2)+'\n')
  check=json.loads(path.read_bytes());assert {k:v for k,v in check.items() if k!='status'}=={k:v for k,v in old.items() if k!='status'}
  changes.append({'path':rel,'beforeSha256':hashlib.sha256(raw).hexdigest(),'afterSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'changedFields':['status']})
 builder=root/('build_bare.py' if folder==folders[0] else 'build.py');text=builder.read_text(encoding='utf-8')
 assert status in text or installed in text;builder.write_text(text.replace(status,installed),encoding='utf-8')
 validator=root/'validate.py';text=validator.read_text(encoding='utf-8')
 if "'normalSelection':False" in text:
  at=text.index('result=') if folder==folders[0] else text.index("(P/'package-checks.json').write_text")
  normal='''normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text(encoding='utf-8') for gear in ['bare','helmet'])
'''
  text=text[:at]+normal+text[at:];text=text.replace("'normalSelection':False","'normalSelection':normal_selection").replace('Source package only; native mortality and furniture contact pending','Source package checks; combined normal-loader contact/mortality/Continue evidence in ../veld-bunk-selected-v1')
  validator.write_text(text,encoding='utf-8')
 (root/'normal-selection.json').write_text(json.dumps({'normalSelection':True,'bareAndHelmet':True,'combinedEvidence':'../veld-bunk-selected-v1/native-evidence.json','scope':'Paired normal-loader East bunk; need-driven default route/rest, four-rotation prescribed supported death, early fall and fire/fresh-main-scene actor future. Prior dated staged evidence keeps original scope; natural whole-world hazard cadence/owner review open.'},indent=2)+'\n')
registry_path=R/'character/ACTIVE_ASSETS.json';raw=registry_path.read_bytes();registry=json.loads(raw)
snapshot=P/'ACTIVE_ASSETS-before-admission.json'
if not snapshot.exists():snapshot.write_bytes(raw)
additions=[]
for folder,key in zip(folders,['veld-east-bunk-whole-body-family','veld-east-bunk-early-fall-family']):
 for section,gear in [('actionOverrides','bare'),('equipmentActionOverrides','helmet')]:
  value=f'character/{folder}/{gear}-manifest.json';assert key not in registry[section] or registry[section][key]==value
  registry[section][key]=value;additions.append({'section':section,'key':key,'value':value})
  binding={'script':'scripts/grid_canvas.gd','contains':'res://'+value}
  if binding not in registry['bindings']:registry['bindings'].append(binding)
review='character/veld-bunk-selected-v1/review.html'
if review not in registry['reviews']:registry['reviews'].append(review)
temporary=R/'character/ACTIVE_ASSETS.veld-bunk-admission.tmp';temporary.write_text(json.dumps(registry,indent=2)+'\n')
assert registry_path.read_bytes()==raw,'Preserve concurrent registry edit';temporary.replace(registry_path)
check=json.loads(registry_path.read_bytes());previous=json.loads(raw)
for section in ['actionOverrides','equipmentActionOverrides']:assert all(check[section].get(k)==v for k,v in previous[section].items())
for key,value in previous.items():
 if key not in ['actionOverrides','equipmentActionOverrides','bindings','reviews']:assert check[key]==value
assert check['bindings'][:len(previous['bindings'])]==previous['bindings'] and check['reviews'][:len(previous['reviews'])]==previous['reviews']
allowed={x['path'] for x in changes}|{'character/ACTIVE_ASSETS.json'}
actual={p for p,h in tested.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h};assert actual==allowed
(P/'post-run-metadata.json').write_text(json.dumps({'passed':True,'manifestChanges':changes,'registryAdditions':additions,'allOtherFrozenInputsUnchanged':True,'sourcePNGsUnchanged':True,'otherRegistrySelectionsPreserved':True},indent=2)+'\n')
print('Four manifest status fields/paired registry entries updated; frozen PNGs and all other selections preserved')
