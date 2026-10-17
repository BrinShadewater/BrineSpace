from pathlib import Path
import hashlib,json,os,time,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1]
specs=[
 ('passing-v15','exec-bc8b9696-f88a-4f26-863c-efebb52e4cae.png',['raw-passing-v8.png','unified-identity-pose-guide.png'],'rejected_foreground_planted_knee','Lifted rear boot present but large foreground knee plate belongs to planted leg; wrong supporting side.'),
 ('passing-v16','exec-c523abf3-39a2-41bb-9107-0109356e2f29.png',['raw-passing-v15.png'],'reviewed_near_bent_passing_geometry_join_study','Near foreground plated knee connects to bent rear shin/raised boot; far supporting knee partly hidden. Whole-pose common-ruler study only.'),
 ('far-swing-v17','exec-77517e39-28ef-4184-bcec-babe16fda6ed.png',['raw-far-swing-v10.png','unified-identity-pose-guide.png'],'rejected_floating_support_stance','Both legs spread rather than near supporting boot beneath hip; far-forward assignment not reproduced.'),
 ('far-swing-v18','exec-18fca577-a273-4358-a1b2-130d76bca76b.png',['raw-far-swing-v17.png'],'reviewed_far_forward_geometry_join_study','Near foreground planted boot under hip; far leg advances behind supporting knee. Ruler source crown43/cylinderbottom676 gives registeredcrown76.275 vsotherphases79.918-82.366; full gait/bounce/materials not accepted.'),
]
for name,generated,refs,status,review in specs:
 raw=P/f'raw-{name}.png'
 (P/f'references-{name}.json').write_text(json.dumps([{'path':(P/n).relative_to(R).as_posix(),'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in refs],indent=2)+'\n',encoding='utf-8')
 (P/f'execution-{name}.json').write_text(json.dumps({'tool':'builtin image_gen','generatedSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+generated,'workspaceSource':raw.relative_to(R).as_posix(),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':f'prompt-{name}.txt','references':f'references-{name}.json','status':status,'review':review,'scope':'Source authoring/rigid whole-pose diagnostics only. No paired helmet/native/normal admission.'},indent=2)+'\n',encoding='utf-8')
verification=[]
for n in ['index.html','cycle.png','comparison.png']:
 path=P/'whole-pose-join-v3'/n
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-carry-east-master-proportions-v1/whole-pose-join-v3/'+n) as response:
  payload=response.read();verification.append({'file':n,'status':response.status,'exactBytes':payload==path.read_bytes()})
assert all(v['status']==200 and v['exactBytes'] for v in verification)
(P/'whole-pose-join-v3/preview-verification.json').write_text(json.dumps({'files':verification,'continuousBrowserReview':False,'nativeReview':False},indent=2)+'\n',encoding='utf-8')
block='''## Veld East carry corrected passing/swing joins — October 2, 2026

PassingV15 repeats wrong foreground planted knee; targeted V16 joint/occlusion
edit attaches large near plate to rear bent foreground shin/airborne boot, far
supporting knee behind. Far-swingV17 generates floating spread stance; explicit
V18 support-position edit restores near boot under hip, far shin/boot advancing
behind near supporting knee. Four raws/prompts/ref hashes/executions retained.
V16/V18 reviewed as geometry/source studies only, not finished motion.

assemble_whole_pose_study.py now versions1/2/3. V2 substitutes completeV16 phase4;
V3 also substitutes completeV18 phase2, retains completeV14 phase3. Shared65.209px
crown-to-cylinder anatomy and physical opaque floor224, no fragments/stretch or
per-pose total-height normalization. Both six-column whole/upper/lower boards
inspected (36presentations). Six140ms APNG frames each exact decoded/840ms. V3
HTTP200/exactindex,cycle,comparison; continuous browser or native not claimed.

V3 native-sized coarse top20alpha head proxies27/27/26/28/26/27 and visible heights
143/144/148/142/145/144. Registered crown81.767/81.313/76.275/82.366/79.918/81.540,
range6.091px. Support-side progression clearer, but far swing rises too much versus
contact; torso/case/body cadence and shared neutral matte grade still provisional.
V16 source crown102/cylinderbottom689; V18crown43/cylinderbottom676. Raw V14 outline
margin concern and V11 last-cell tightness remain. No helmet/native/normal selection.

Lesson: specify the knee/shin/boot chain and anatomical occlusion, not only raised
boot silhouette. For failed floating poses, identify one supporting knee/shin/boot
under hip and advancing boot position explicitly. After geometry succeeds, common
anatomical registration may still expose vertical body/material discontinuity;
do not convert successful local corrections into full gait acceptance.
Next reduce phase2 body-rise at unchanged anatomy, check all6support/foot/hip/case
joins and unified master grade, then paired helmet/native/controller. Full East
actions/South/North/cargo ownership/interruptions/Continue and library polish open.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  old=path.read_bytes();source=old.decode('utf-8-sig')
  if block.splitlines()[0] in source:break
  tmp=path.with_name(path.name+'.veld-passing.tmp');tmp.write_text(block+source,encoding='utf-8')
  if path.read_bytes()!=old:tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action')
 source=source[:start]+'''## Passing/forward-swing join continuation
V15wrong plated supporting side rejected; V16explicit joint/occlusion repair gives
foreground bent trailing near leg. V17floating spread rejected; V18explicit near
support beneath hip/far forward boot behind corrects swing geometry. Four raw/
prompt/refhash/execution retained. JoinV2 replaces completephase4(V16); V3also
completephase2(V18) with priorwholeV14phase3. No body fragments/height forcing.
Two six-column whole/upper/lower boards inspected36views. Each APNG6exact140ms
decoded frames/840ms. V3preview3filesHTTP200/exact; no livecadence/native claim.
V3heads27/27/26/28/26/27; crownrange6.091px (phase2 high76.275 vscontact82.366).
Geometry improves, but body/case rise/grade/foot contact/cadence remain provisional.
V14edge/V11tightmargin concerns retained. Five maintained references updated.

## Next action
Reduce far-swingphase2 body rise through complete-pose knee/hip posture correction
at unchanged anatomy; inspect all6support/foot/hip/head/case/material joins and
shared master grade. Then paired helmet/native/controller. East actions/South/North
cargo matching, actual controller/room/ownership/interruptions/Continue, guarded
adoption and full-library consistency polish remain incomplete.
'''
 path.write_text(source,encoding='utf-8')
print(json.dumps({'sourceProvenanceRecords':4,'maintainedReferences':5,'handoffs':2,'httpExactFiles':3,'scope':'source studies, full objective incomplete'}))
