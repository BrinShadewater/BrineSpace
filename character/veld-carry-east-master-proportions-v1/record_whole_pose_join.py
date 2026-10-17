from pathlib import Path
import hashlib,json,os,time
P=Path(__file__).resolve().parent;R=P.parents[1]
refs=[P/'raw-opposite-contact-v13.png',P/'unified-identity-pose-guide.png'];raw=P/'raw-opposite-contact-v14.png'
(P/'references-opposite-contact-v14.json').write_text(json.dumps([{'path':r.relative_to(R).as_posix(),'sha256':hashlib.sha256(r.read_bytes()).hexdigest()} for r in refs],indent=2)+'\n',encoding='utf-8')
(P/'execution-opposite-contact-v14.json').write_text(json.dumps({'tool':'builtin image_gen','generatedSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-30bf542e-245d-4887-b9f2-cdec754a08ee.png','workspaceSource':raw.relative_to(R).as_posix(),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':'prompt-opposite-contact-v14.txt','references':'references-opposite-contact-v14.json','status':'reviewed_correct_overlap_whole_pose_join_study','review':'Pouch removed, near foreground plated trailing thigh retained. Generator globally changes source size despite narrow edit instruction; actual anatomical ruler registration .09925269795 puts crown82.366, closer to V1contact80.628 than old V5contact85.307. Registered whole source only, no body fragments. Six-phase join remains failed/unaccepted support phases. Raw right edge40nonzero pixels, maxalpha116: outline margin concern retained.'},indent=2)+'\n',encoding='utf-8')
(P/'unified-identity-pose-guide-provenance.json').write_text(json.dumps({'source':'raw-v11.png','sourceSHA256':hashlib.sha256((P/'raw-v11.png').read_bytes()).hexdigest(),'crop':[1083,47,1435,676],'sha256':hashlib.sha256((P/'unified-identity-pose-guide.png').read_bytes()).hexdigest(),'role':'Complete identity/proportion guide only; its existing lower-body support pattern is failed.'},indent=2)+'\n',encoding='utf-8')
block='''## Veld East carry repaired opposing-contact whole-pose join — October 2, 2026

Targeted six-figureV12 edit fails: fourth boot changes but foreground plated knee
stays forward. Isolating one complete pose with explicit old geometry-only guide
and unifiedV11 identity crop yieldsV13 correct near plated trailing thigh/far
forward boot. V13 leaks an old hip pouch; V14 narrow equipment edit removes it,
retains correct overlap. All raw/prompts/ref hashes/execution/crop lineage saved.
V14 source globally changes scale despite narrow instruction; do not assume edit
invariants. Rigid anatomy registration uses crown111/cylinderbottom768 and scale
.09925269795, crown82.366 vsV1contact80.628 and previousV5contact85.307.

assemble_whole_pose_study.py registers five completeV11 figures with ONE atlas
crown48/cylinderbottom335 ruler (.2272091378), replaces only full phase3 withV14
at same65.209px anatomical span/opaque boot floor224. No torso/leg fragments,
stretching or per-pose height normalization. Six whole/upper/lower columns viewed
(18presentations); crown/case fit closer, opposing overlap clearer. Nine-column
anatomical review also seen (27whole/detail+9raw landmark plates). Other support
phases still repeat/unclear: full walk not accepted, no helmet/native/selection.

Six-frame840ms diagnostic APNG decodes exactly to six source-composite frames
with140ms holds. Local preview/index and cycle HTTP200/exactbytes; app open queued,
continuous browser motion not claimed. RawV14 right edge has40nonzero alpha pixels
max116, no opaque contact at edge; outline/margin review remains provisional.
Lesson: isolate one complete pose when atlas-wide edit ignores limb occlusion;
then check identity leakage and actual source scaling before whole-pose joining.
Next repair far-forward swing and far-support passing against their successful
geometry guides at unified anatomy, review complete cadence/shared grade/helmet,
then native/controller/cargo actions/South/North/Continue and cross-library polish.
Full objective incomplete; normal selections unchanged.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  old=path.read_bytes();source=old.decode('utf-8-sig')
  if block.splitlines()[0] in source:break
  tmp=path.with_name(path.name+'.veld-join.tmp');tmp.write_text(block+source,encoding='utf-8')
  if path.read_bytes()!=old:tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action')
 source=source[:start]+'''## Whole-pose opposing-contact join continuation
V12atlas edit fails overlap. IsolatedV13 correct plated near trailing leg but leaks
old pouch; V14 removes pouch, preserves overlapping pose, changes source scale.
Both source/provenance retained. Anatomical register gives V14crown82.366 closer
to V1contact80.628 vsoldV5 85.307. whole-pose-join-v1 replaces complete phase3 in
V11 via common65.209span/opaque floor224; no anatomical strips or height forcing.
Six columns/18whole-details and updated9ruler columns/27details+9raw plates viewed.
Six140ms APNG frames decode exact/840ms; local HTTP200/exactbytes/app queued only.
Other support-side phases still fail/unclear, material/margins/cadence not accepted.
V14right edge40nonzero/maxalpha116 means outline margin provisional. No native,
paired helmet, normal admission. Five maintained references updated with lesson.

## Next action
Isolate and repair complete far-forward swing and far-support passing with V10/V8
geometry-only guides plus unified identity, then join at common anatomy. Review
six-phase support/occlusion/root/cadence and grade before paired helmet/native.
East actions/South/North cargo matching, actual controller/room/ownership/
interruptions/Continue, guarded adoption and full-library polish remain incomplete.
'''
 path.write_text(source,encoding='utf-8')
print(json.dumps({'newProvenance':1,'identityCropLineage':1,'maintainedReferences':5,'handoffs':2,'wholePosePreview':'six decoded exact frames; no native/selection'}))
