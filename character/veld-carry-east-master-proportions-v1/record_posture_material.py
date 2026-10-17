from pathlib import Path
import hashlib,json,os,time,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1]
specs=[('19','exec-caa89c2f-1b77-486c-aa1b-669cd03dbe59.png',['raw-far-swing-v18.png'],'rejected_posture_overshoot','Correct leg assignment but too low: sourcecrown120/cylinderbottom744, common-scale registeredcrown84.386 vsV18 76.275. Retained as posture guide, not gait.'),('20','exec-8649b786-035a-4b77-b949-b9558d60708b.png',['raw-far-swing-v19.png','raw-far-swing-v18.png'],'reviewed_reduced_rise_whole_pose_material_study','Preserved near support/far advancing occlusion. Sourcecrown42/cylinderbottom678 gives scale .1025299097, registeredcrown79.638; six-cycle common-ruler spread2.729 vsprior6.091. Raw requested coordinates not invariant; actual landmarks govern. Full cadence/case/material/native pending.')]
for version,generated,refs,status,review in specs:
 name='far-swing-v'+version;raw=P/f'raw-{name}.png'
 (P/f'references-{name}.json').write_text(json.dumps([{'path':(P/n).relative_to(R).as_posix(),'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in refs],indent=2)+'\n',encoding='utf-8')
 (P/f'execution-{name}.json').write_text(json.dumps({'tool':'builtin image_gen','generatedSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+generated,'workspaceSource':raw.relative_to(R).as_posix(),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':f'prompt-{name}.txt','references':f'references-{name}.json','status':status,'review':review,'scope':'Whole-pose source study only; no helmet/native/normal selection.'},indent=2)+'\n',encoding='utf-8')
O=P/'whole-pose-join-v4/material-review';evidence=json.loads((O/'review-evidence.json').read_text())
evidence['visualReview']='Eight whole/head-case/leg columns (24presentations) inspected against original East and repaired held master. Compact heads/suit detail retained, reduced crown rise, shared cloth/skin/hair grade closer across sources. Case/grip band intentionally unchanged and retains source material/detail differences; full cadence/helmet/native and final matte consistency not accepted.'
evidence['status']='reviewed_source_material_candidate_full_motion_pending'
verification=[]
for n in ['index.html','cycle.png','master-comparison.png']:
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-carry-east-master-proportions-v1/whole-pose-join-v4/material-review/'+n) as response:
  data=response.read();verification.append({'file':n,'status':response.status,'exactBytes':data==(O/n).read_bytes()})
assert all(v['status']==200 and v['exactBytes'] for v in verification)
evidence['previewVerification']=verification
(O/'review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
block='''## Veld East carry reduced rise and shared master grade — October 2, 2026

Whole far-swingV19 knee-flex edit lowers too much (registered crown84.386 vsprior
V18 76.275); preserved/rejected. V20 intermediate complete posture source preserves
near supporting/far advancing overlap; sourcecrown42/cylinderbottom678 sets scale
.1025299097/crown79.638. JoinV4 replaces only entirephase2 in priorV3, no anatomical
fragments/stretch/per-pose height forcing. Common65.209anatomical span/physical
opaque floor224 retained; crownspread drops6.091 to2.729px. Six whole/upper/leg
columns viewed18presentations. Raw/prompt/ref hashes/execution retained.

review_shared_material.py reuses unchanged West-original-derived pooled cloth
curve/fixed skin-hair offsets across all6frames, explicit head band and protected
whole110:160case/grip band.31checks0fail: alpha unchanged, protected band/outside
masks exact, six APNG frames exact decoded140ms/840ms. Comparison includes original
East plus repaired NEheld005; all8whole/head-case/leg columns viewed24presentations.
Head proxies27/27/26/28/26/27 remain compact. Shared cloth/head grade/detail nearer
masters; protected case/grip retains source material/detail differences and needs
own bounded master comparison. These are source checks, not native/motion proof.

Preview index/cycle/mastercomparison HTTP200/exactbytes. Continuous browser/native
cadence not claimed. Body/case/boot joins, matte highlights, source edge margins,
paired helmet and original loader/native/controller remain provisional/unselected.
Lesson: requested source-coordinate changes are not certified edit invariants;
compare actual anatomy/physical-foot landmarks after generation. Preserve segment
lengths by whole knee/hip posture changes, not height normalization, and verify
shared grading alpha/equipment protection separately from final visual acceptance.
Next bounded case/material alignment and continuous6phase review, then original
shared East helmet/paired package/native. Full Eastactions/South/North, cargo world/
ownership/interruptions/Continue and final library polish remain incomplete.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  old=path.read_bytes();source=old.decode('utf-8-sig')
  if block.splitlines()[0] in source:break
  tmp=path.with_name(path.name+'.veld-posture.tmp');tmp.write_text(block+source,encoding='utf-8')
  if path.read_bytes()!=old:tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action')
 source=source[:start]+'''## Reduced rise/shared material continuation
V19support-knee flexion overshoots low crown84.386; intermediate wholeV20 preserves
near support/far swing, sourcecrown42/cylinder678/.1025299097 gives crown79.638.
JoinV4 completephase2 reduces common-ruler six-crownspread6.091→2.729px. All18
whole/upper/leg presentations seen. Both raws/prompts/ref hashes/exec retained.
review_shared_material.py uses unchanged pooled master recipe, fixed skin/hair
offsets, protects entire110:160grip/case and alpha/outside masks.31checks0fail/6
exact decoded140msAPNGframes. OriginalEast+repairedNEheld005+6graded poses24whole/
headcase/leg views seen. Heads27/27/26/28/26/27. Case band/material source differences
remain; final matte/cadence/native/helmet/edge margins not accepted. Preview3files
HTTP200/exactbytes, no continuousbrowser/native claim. Five maintained refs updated.

## Next action
Bounded case/material master alignment and continuous six-phase support/foot/hip/
head/case cadence review, then original shared East helmet/paired package/native.
East actions/South/North cargo matching, actual controller/room/ownership/
interruptions/Continue, guarded adoption and full-library consistency polish open.
'''
 path.write_text(source,encoding='utf-8')
print(json.dumps({'newSourceProvenance':2,'materialChecks':31,'failures':0,'visualPresentations':42,'httpExactFiles':3,'maintainedReferences':5,'handoffs':2,'scope':'source candidates only; goal incomplete'}))
