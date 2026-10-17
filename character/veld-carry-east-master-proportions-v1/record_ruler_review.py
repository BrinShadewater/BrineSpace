from pathlib import Path
import hashlib,json,os,time
P=Path(__file__).resolve().parent;R=P.parents[1]
refs=[R/'character/veld-cargo-turns-master-family-v1/corrected-east-held-density-reference.png',P/'five-phase-geometry-guide.png']
raw=P/'raw-v11.png'
(P/'references-unified-v11.json').write_text(json.dumps([{'path':r.relative_to(R).as_posix(),'sha256':hashlib.sha256(r.read_bytes()).hexdigest()} for r in refs],indent=2)+'\n',encoding='utf-8')
(P/'execution-unified-v11.json').write_text(json.dumps({'tool':'builtin image_gen','generatedSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-1404e3e3-ea11-4a6b-b005-030365e729b7.png','workspaceSource':raw.relative_to(R).as_posix(),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':'prompt-unified-v11.txt','references':'references-unified-v11.json','status':'rejected_full_gait_retained_common_body_study','review':'Six complete figures/compact head widths28/28/28/27/28/28, one first148scale .2360446571, crown source range48-49/floor674-677. Uniform body scale and grade improve, but opposing-contact/support assignment remains repeated/unclear; last cell tightly bounded at image right. All18 original/selected/study presentations inspected. No accepted gait, helmet, native or normal selection.'},indent=2)+'\n',encoding='utf-8')
names=['near-support-v1-density-guide.png','raw-far-swing-v10.png','raw-opposite-contact-v5.png','raw-passing-v8.png','raw-swing-v9.png']
(P/'five-phase-geometry-guide-provenance.json').write_text(json.dumps({'scope':'GEOMETRY ONLY comparison collage. Individually fitted to330x650 inside360x700 cells; not common anatomy scale or animation frames.','script':'prepare_pose_guide.py','sources':[{'path':(P/n).relative_to(R).as_posix(),'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in names],'nearSupportCrop':{'source':'raw-v1.png','box':[365,26,684,686]},'sha256':hashlib.sha256((P/'five-phase-geometry-guide.png').read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
block='''## Veld East carry common-anatomy review — October 2, 2026

East source study adds review_anatomical_ruler.py: manual raw crown/cylinder-bottom
landmarks define a common65.209px upper-body span; each whole source rigidly scales
to this span and registers its opaque physical boot floor224. No per-pose height
normalization, torso/leg stretching or anatomy pasting. Seven columns/21whole,
upper-body and leg views plus seven raw landmark plates inspected. Independent
sources produce11.685px crown spread, exposing disproportion/bounce hidden by
earlier equal-height comparisons. This diagnostic is not accepted motion.

New far-swingV10 source correctly advances far shin/boot behind near plated support
leg, but lower-body proportions differ at common ruler; geometry guide only.
Raw/prompt/ref hashes/execution retained. Five-phase geometry-only collage retains
source lineage/fit recipe. Unified six-figureV11 uses canonical identity plus guide;
one first148scale .2360446571 gives head proxies28/28/28/27/28/28, raw crown48-49
and foot bounds674-677. All18 original/selected/study presentations inspected.
Body/case consistency improves, but opposite-contact/support pattern still repeats
or is unclear; rightmost source margin too tight. V11 rejects full gait.

Lesson: stable crown/torso/case cannot certify alternating support-side geometry;
geometry and shared anatomical scale are separate visual requirements. Use the
successful individual opposing-contact reference for targeted complete-pose repair
of unified atlas, preserving shared anatomy rather than mixing differently sized
independent bodies. Built-in image editing supports at most five local references;
use a documented geometry-only collage when needed, not unrecorded source merges.
extract_study.py now has version-specific output directories; V2 was regenerated
from retained raw after initial V11 call wrote its diagnostic folder, then V11
rebuilt in its own folder. Source raw/provenance unchanged. No native run or normal
adoption. Next repair exact opposing-contact and passing/swing support assignments,
review six-phase gait/shared grade/helmet/native, then cargo actions/South/North,
actual world/controller/ownership/Continue and full-library consistency polish.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  old=path.read_bytes();source=old.decode('utf-8-sig')
  if block.splitlines()[0] in source:break
  tmp=path.with_name(path.name+'.veld-ruler.tmp');tmp.write_text(block+source,encoding='utf-8')
  if path.read_bytes()!=old:tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action')
 source=source[:start]+'''## Common-anatomy continuation
Manual crown/cylinder-bottom source landmarks set65.209px anatomical span with
physical opaque foot floor224; seven columns/21whole-detail+sevenraw landmark
plates inspected. Independent poses vary11.685px in registered crown: mixed-source
body bounce/proportion fails. V10 far shin advances behind near planted leg, useful
geometry only. V11 unified six-source body improves scale/grade/head/case consistency
(crowns48-49, floors674-677, heads27-28), but repeats/unclear opposing support pattern
and tight last margin. Full gait rejected. Both raws/prompts/ref hashes/execution,
documented geometry collage, common-ruler study/APNG and V11source comparisons kept.
extract_study version-output fixed; V2 diagnostic restored from raw, V11separate.
No package/native/normal selection. Five maintained references record the lesson.

## Next action
Target complete opposing-contact/passing poses in unified V11 using successful
individual geometry references; preserve common anatomy/head/case. Review all six
support/occlusion phases, floor/root/grade, then paired helmet/native. East actions,
South/North cargo matching, actual controller/room/ownership/interruptions/Continue,
guarded adoption and full-library consistency polish remain incomplete.
'''
 path.write_text(source,encoding='utf-8')
print(json.dumps({'newSourceProvenance':1,'geometryLineage':1,'maintainedReferences':5,'handoffs':2,'scope':'diagnostic source review only'}))
