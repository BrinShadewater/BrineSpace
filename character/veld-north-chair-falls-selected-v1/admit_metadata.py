"""Update admission labels after the frozen normal-loader interval completes."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-chair-falls-selected-native-v1'
n=json.loads((O/'validation.json').read_text());assert n['passed']
before=json.loads((O/'inputs-after.json').read_text());evidence=[]
folders=['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1','veld-lounge-late-fall-north-v1','veld-lounge-early-fall-north-v1']
loader=(R/'scripts/grid_canvas.gd').read_text()
for folder in folders:
 root=R/'character'/folder
 for gear in ['bare','helmet']:
  path=root/f'{gear}-manifest.json';relative=path.relative_to(R).as_posix()
  assert '"res://'+relative+'"' in loader
  raw=path.read_bytes();old=json.loads(raw);new=dict(old)
  snapshot=P/f'{folder}-{gear}-tested-manifest.json'
  if old['status']=='installed_locally_owner_motion_review_open':
   assert snapshot.exists();raw=snapshot.read_bytes();old=json.loads(raw)
  assert hashlib.sha256(raw).hexdigest()==before[relative]
  assert old['status']=='staged_native_mortality_candidate'
  if not snapshot.exists():snapshot.write_bytes(raw)
  new['status']='installed_locally_owner_motion_review_open'
  path.write_text(json.dumps(new,indent=2)+'\n',encoding='utf-8')
  check=json.loads(path.read_bytes());assert {k:v for k,v in check.items() if k!='status'}=={k:v for k,v in old.items() if k!='status'}
  evidence.append({'path':relative,'beforeSha256':hashlib.sha256(raw).hexdigest(),'afterSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'changedFields':['status']})
 builder=root/'build.py';text=builder.read_text(encoding='utf-8')
 assert text.count("'status':'staged_native_mortality_candidate'")==1 or text.count("'status':'installed_locally_owner_motion_review_open'")==1
 builder.write_text(text.replace("'status':'staged_native_mortality_candidate'","'status':'installed_locally_owner_motion_review_open'"),encoding='utf-8')
 validator=root/'validate.py';text=validator.read_text(encoding='utf-8')
 if "'normalSelection':False" in text:
  at=text.index("(P/'package-checks.json').write_text")
  text=text[:at]+'''normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text() for gear in ['bare','helmet'])
'''+text[at:]
  text=text.replace("'normalSelection':False","'normalSelection':normal_selection").replace('North source artwork only; prescribed native chair audition recorded separately; production selector/mortality/Continue pending','North source artwork/package checks; combined normal-loader mortality/Continue evidence in ../veld-north-chair-falls-selected-v1')
  validator.write_text(text,encoding='utf-8')
 (root/'normal-selection.json').write_text(json.dumps({'normalSelection':True,'bareAndHelmet':True,'combinedNativeEvidence':'../veld-north-chair-falls-selected-v1/native-evidence.json','normalCases':28,'scope':'Normal-loader North chair falls; prescribed rotation0 mortality and disk/fresh-main-scene actor future. Prior dated staged evidence retains original scope; natural world/owner review open.'},indent=2)+'\n')
registry_path=R/'character/ACTIVE_ASSETS.json'
registry_raw=registry_path.read_bytes();registry=json.loads(registry_raw)
registry_snapshot=P/'ACTIVE_ASSETS-before-admission.json'
if not registry_snapshot.exists():registry_snapshot.write_bytes(registry_raw)
registry_changes=[]
for folder,label in zip(folders,['seated','partial','late','early']):
 key=f'veld-north-chair-fall-{label}'
 for section,gear in [('actionOverrides','bare'),('equipmentActionOverrides','helmet')]:
  value=f'character/{folder}/{gear}-manifest.json'
  assert key not in registry[section] or registry[section][key]==value
  registry[section][key]=value;registry_changes.append({'section':section,'key':key,'value':value})
  binding={'script':'scripts/grid_canvas.gd','contains':'res://'+value}
  if binding not in registry['bindings']:registry['bindings'].append(binding)
review_path='character/veld-north-chair-falls-selected-v1/resume-review.html'
if review_path not in registry['reviews']:registry['reviews'].append(review_path)
# Windows can retain a mapped reader that rejects truncation of this registry.
# Replace a complete sibling file atomically; a failed replace leaves it intact.
registry_candidate=R/'character/ACTIVE_ASSETS.veld-north-admission.tmp'
registry_candidate.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8')
assert registry_path.read_bytes()==registry_raw,'Concurrent registry edit; preserve it'
registry_candidate.replace(registry_path)
check=json.loads(registry_path.read_bytes());old=json.loads(registry_raw)
for section in ['actionOverrides','equipmentActionOverrides']:
 assert all(check[section].get(key)==value for key,value in old[section].items())
for key,value in old.items():
 if key not in ['actionOverrides','equipmentActionOverrides','bindings','reviews']:assert check[key]==value
assert check['bindings'][:len(old['bindings'])]==old['bindings'] and check['reviews'][:len(old['reviews'])]==old['reviews']
changes=[]
for relative,digest in before.items():
 if hashlib.sha256((R/relative).read_bytes()).hexdigest()!=digest:changes.append(relative)
assert sorted(changes)==sorted(x['path'] for x in evidence)
(P/'post-run-metadata.json').write_text(json.dumps({'passed':True,'metadataOnly':True,'changes':evidence,'allOtherFrozenInputsUnchanged':True,'sourcePNGsUnchanged':True,'registryAdditions':registry_changes,'otherRegistrySelectionsPreserved':True},indent=2)+'\n')
print(f'{len(evidence)}manifest status fields updated; all other frozen inputs exact')
