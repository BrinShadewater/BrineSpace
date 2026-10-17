from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-v2';OUT=BASE/'supplemental/cargo-matched-v1';OUT.mkdir(exist_ok=True);catalog=BASE/'catalog.json';before=json.loads(catalog.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def selected(cat):
 result={}
 for rel in cat['body']:
  mp=(BASE/rel).resolve();data=json.loads(mp.read_text())
  for state in data['states']:
   result[state['id']]={'entry':{k:v for k,v in state.items() if k!='frameFiles'},'frames':[sha(ROOT/f.removeprefix('res://')) if f.startswith('res://') else sha((mp.parent/f).resolve()) for f in state['frameFiles']]}
 return result
prior=selected(before);source_list=json.loads((ROOT/'character/marsh-water-transition-material-v1/combined07-cross-review/manifest-list.json').read_text())['manifests'];names=['loaded-water-loops-turns','dry-turns','held-pickup-unload','carry-east','carry-west','carry-north','carry-south','water-pickup-drain'];receipts=[];after=json.loads(json.dumps(before));expected=set();copies=[]
for rel,name in zip(source_list,names):
 mp=ROOT/rel;data=json.loads(mp.read_text());out=OUT/name;out.mkdir(exist_ok=True);mapped={}
 for state in data['states']:
  expected.add(state['id']);new=[]
  for f in state['frameFiles']:
   src=ROOT/f.removeprefix('res://') if f.startswith('res://') else (mp.parent/f).resolve()
   if src not in mapped:
    dst=out/f'frame-{len(mapped):03}.png';assert not dst.exists();shutil.copy2(src,dst);assert sha(src)==sha(dst);mapped[src]=dst;copies.append({'source':src.relative_to(ROOT).as_posix(),'path':dst.relative_to(ROOT).as_posix(),'sha256':sha(dst)})
   new.append('res://'+mapped[src].relative_to(ROOT).as_posix())
  state['frameFiles']=new
 data['normalAdmission']=True;data['fullGoalComplete']=False;data['revision']=data.get('revision','marsh-cargo')+'-selected-normal-v1';dest=out/'manifest.json';dest.write_text(json.dumps(data,indent=2)+'\n')
 copied=json.loads(dest.read_text());original=json.loads(mp.read_text())
 for a,b in zip(original['states'],copied['states']):assert {k:v for k,v in a.items() if k!='frameFiles'}=={k:v for k,v in b.items() if k!='frameFiles'}
 for k,v in original.items():
  if k not in ['states','normalAdmission','fullGoalComplete','revision']:assert copied[k]==v
 path=dest.relative_to(BASE).as_posix();assert path not in after['body'];after['body'].append(path);receipts.append({'sourceManifest':rel,'sourceManifestSha256':sha(mp),'normalManifest':dest.relative_to(ROOT).as_posix(),'normalManifestSha256':sha(dest),'stateIds':[s['id'] for s in data['states']]})
post=selected(after);changed=[k for k in prior if prior[k]!=post[k]];assert set(changed)==expected and len(expected)==48 and set(prior)==set(post)
r={'catalogBefore':before,'catalogBeforeSha256':sha(catalog),'manifests':receipts,'wholeFrameCopies':copies,'changedStateIds':sorted(changed),'normalSelectedStateCount':len(post),'unchangedOtherStates':len(post)-48,'normalAdmission':True,'fullGoalComplete':False,'scope':'Coherent whole-source48state cargo family, per-manifest geometry/timing/stride retained; source admission during ongoing consistency/contact/cadence polish. No actor/gameplay behavior changed.'};catalog.write_text(json.dumps(after,indent=2)+'\n');r['catalogAfterSha256']=sha(catalog);(OUT/'admission.json').write_text(json.dumps(r,indent=2)+'\n');(OUT/'selection.json').write_text(json.dumps({'manifests':[q['normalManifest'] for q in receipts],'stateCount':48,'slots':272,'normalAdmission':True,'fullGoalComplete':False},indent=2)+'\n');print(f'48states admitted;{len(copies)}whole PNG copies;{len(post)}normal states/{len(post)-48}unchanged;8pack metadata preserved')
