from pathlib import Path
import json,hashlib,shutil,uuid,time,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_bytes());refs=set();packs=set()
for gear in ['bare','helmet']:
 for key in ['idle-west','walk-west','interact-west','kneel-west','repair-west','stand-west']:
  row=inv['resolved'][gear][key];refs.update(row['frameFiles']);packs.add(row['manifest'])
for name in refs:assert sha(R/name)==inv['sourceBindings'][name],name
for name in packs:assert sha(R/name)==inv['bindings'][name],name
for f in [R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json']:
 text=f.read_text();assert all(x not in text for x in ['west-sample-family-v2','west-kneel-anchor-v1','west-kneel-anchor-v2'])
measurements={};bindings={}
for folder in [P,P.with_name('west-kneel-anchor-v1'),P.with_name('west-kneel-anchor-v2')]:
 for f in folder.iterdir():
  if f.is_file() and f.suffix in ['.png','.mp4','.txt','.json']:bindings[f.relative_to(R).as_posix()]=sha(f)
for version in [1,2]:
 folder=P.with_name(f'west-kneel-anchor-v{version}');raw=Image.open(folder/'raw.png').convert('RGBA');native=raw.resize((256,256),Image.Resampling.LANCZOS)
 assert native.tobytes()==Image.open(folder/'native.png').convert('RGBA').tobytes()
 a=np.array(native);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];yy,xx=np.where(a[218:226,:133,3]>200)
 measurements[f'anchor-v{version}']={'rawSize':raw.size,'height':int(y.max()-y.min()+1),'top':top,'floor':int(y.max()),'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.min()+hx.max())/2),'visibleFrontGroundLeft':int(xx.min()) if len(xx) else None,'mapping':'Uniform whole raw canvas to256,generated alpha preserved; no pose scaling or registration rescue.'}
verdict={'status':'Rejected before helmet/native expansion','newWholeVideoTask':'448679751106893','estimatedVideoUSD':0.28,'billingVerified':False,'wholeNewVideoFramesReviewed':142,'wholeNewPoseKeysReviewed':2,'sourceReplayChecks':278,'selectedWestSourcesUnchanged':len(refs),'selectedWestManifestsUnchanged':len(packs),'newRuntimeSelection':False,'measurements':measurements,'reasons':{'video-v2':'Both legs fold under body instead of requested planted front boot; vial stays visible during start of rising and cyan prop/hand appearance varies. Original identity and standing finish substantially retained, but motion fix failed.','anchor-v1':'Head width27 is correct (earlier visual commentary corrected); boot placement too far left and floor218 instead of223.','anchor-v2':'Guide improves floor222 versus223 but head24 versus27 and upper-body density visibly shrinks; front groundleft101 versus107. Reject material/geometry tradeoff.'},'bindings':bindings,'scope':'Complete source review only; no new helmet variants, native tests, source omission, per-pose recenter/refloor or local body/prop rescue. No owner profile access.'}
(P/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
title='## Veld West sample refinement rejected — October 3, 2026'
note=title+f'''

User continuation focused on sample v1 foot shifts and vial enlargement. One
revised original-master Hailuo02 task448679751106893 succeeded (6s768square,
24fps; estimated USD0.28,billing unverified). Exact prompt/input and all142 source
slots preserved at character/veld-library-closeout-v1/west-sample-family-v2/.
All142 raw frames inspected and278 full APNG grouped pixel/hold checks pass.
Motion fix fails: both legs fold underneath instead of front sole remaining
planted, and vial remains visible into rising with cyan prop/hand variation.
Appearance/standing-endpoint success is not planted contact or stable props.

Changed approach before more video expansion: two whole empty-handed one-knee
key drawings preserved under west-kneel-anchor-v1/v2. V1 head27 matches master;
original visual comment about enlarged head corrected after measurement. V1
floor218 instead of223, front boot too far left. V2 used explicit technical
pose guide, improves floor222 but head24 versus27 and upper body density shrinks;
front ground bandleft101 versus107. All raw/generated alpha preserved with fixed
whole-canvas downsample only. Both rejected; neither becomes a video endpoint.
Exact prompts/references/raws and reproducible measurement review retained.

{len(refs)} selected West source files and{len(packs)} manifests match frozen installed
inventory. New folders absent from loader/ACTIVE. No normal/controller changes,
helmet expansion, native test, owner profile access, local anatomy/prop patch,
per-pose refloor/recenter or rejection-hiding source omission. Ground-band
measurements compare visible pixels only: knee pixels enter band in v2, so the
37px change is not a proved37px boot slide. Do not equate silhouette metric with
contact biomechanics. Handoff: west-sample-family-v2/HANDOFF.md.
Next prove a whole one-knee key that matches density and registration together,
then guide source motion from fixed endpoints; do not repeat freeform full-action
prompts or propagate these rejected poses. Existing v1 remains staged and still
needs contact/vial cleanup. Full Veld set remains incomplete.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: West foot/prop refinement

## Objective and acceptance
Resolve source v1 sample lowering/rising foot movement and vial growth while preserving original Veld identity, density and adjoining standing-family joins.

## Accepted decisions and constraints
Existing reversible generation authorization applies. Whole poses and original master; no source omission/local anatomy/prop patches/per-pose rescale/recenter/refloor rescue. Do not propagate an unproved key into more variants or motion.

## Current state
One Hailuo02 video task448679751106893, estimated USD0.28 (billing unverified), complete142-source slots saved here. Rejected: legs fold under instead of planted front sole; vial remains visible into rising/prop-hand variation. Two built-in whole kneel keys preserved beside this folder under west-kneel-anchor-v1/v2, including exact prompts/references/raws and technical joint guide. Neither used as a video endpoint. Prior source v1 remains staged; normal game unchanged.

## Verification
All142 new raw frames and both whole keys inspected;278 APNG pixel/hold checks. Free key head27 correct but floor218/front boot misplaced; guide key floor222/head24 versus master223/27, visibly shrunken upper body. Generated alpha and whole native mapping verified. Selected274 source files/four manifests unchanged; new folders absent loader/ACTIVE. No native tests warranted for rejected artwork; no owner profile access. Ground-band ranges include knees and do not independently establish boot contact.

## Next action
Prove a single whole kneeling reference with original density/materials and registered front sole before more motion. Then use exact standing/kneeling endpoints to constrain descent and separately review sample handling and rise. Do not issue another vague full-action video or resize/recenter these failed keys to manufacture a pass. Other library closeout and full controller/new-process Continue remain open.
''',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld West — contact refinement review</title><style>body{background:#202a30;color:#e8eded;font:16px system-ui;line-height:1.5;margin:24px}main{max-width:1100px;margin:auto}.row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}figure{margin:0;text-align:center}figure img{width:100%;max-width:320px}.wide{width:100%}a{color:#b7dae9}@media(max-width:440px){.row{grid-template-columns:1fr}}</style><main><h1>Veld West — contact refinement</h1><p>The new trial retains her appearance, but does not solve the foot and vial issues. It is rejected; the game assets are unchanged.</p><div class="row"><figure><img src="master-native.png" alt="Original West master"><figcaption>Original master</figcaption></figure><figure><img src="../west-sample-family-v1/complete-sample-source.png" alt="Previous complete sample sequence"><figcaption>Previous staged source</figcaption></figure><figure><img src="complete-sample-source.png" alt="Rejected complete revised sample sequence"><figcaption>Revised source — rejected</figcaption></figure></div><p>She folds both legs under herself and still holds the vial when rising. The static keys below also miss the required placement or proportions, so neither has been expanded into an animation.</p><img class="wide" src="../west-kneel-anchor-v2/comparison.png" alt="Original master, previous kneel, rejected free pose and rejected guided pose"><p><a href="HANDOFF.md">Review notes</a> · <a href="../west-standing-family-v1/">Standing family preview</a></p></main></html>''',encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent update prevented prepend: '+str(path))

parent=P.parent/'HANDOFF.md';text=parent.read_text(encoding='utf-8');section='\n## West contact refinement rejected\nOne revised full action video plus two whole kneel keys reviewed and rejected for contact/prop or placement/density failures. No normal changes. Source v1 remains staged. See west-sample-family-v2/HANDOFF.md.\n'
if '## West contact refinement rejected' not in text:parent.write_text(text+section,encoding='utf-8')
print('New144 source/key drawings reviewed; selected sources unchanged:',len(refs))
