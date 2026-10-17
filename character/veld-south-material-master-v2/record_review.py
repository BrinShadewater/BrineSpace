from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-south-material-master-v2'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));e=json.loads((P/'native-review-evidence.json').read_text(encoding='utf-8'));b=json.loads((P/'browser-review.json').read_text(encoding='utf-8'))
assert v['passed'] and e['sourceNativePairs']==176 and e['decodedNativeFramesExact']==176 and len(b['completions'])==10
review='Original authored identity compared against processed selected matte idle; selected idle is substantially darker. All10boards/176native-source pairs and full bare terminal015 reviewed. Candidate uses original authored South standing drawing at148ruler, no colour change to that drawing, and fixed head curves across other South poses. Exact family held/start/stop/pickup and start/gait joins. Existing equipped head/shell preserved on16poses; original35x39shell fitted on authored idle. Ten browser source completions and original bare terminal screenshot inspected. Hair/contrast/hardware still require cross-master polish; no turns/normal selector/controller/world/save/ownership acceptance.'
for name in ['registration.json','native-review-evidence.json']:
 d=json.loads((P/name).read_text(encoding='utf-8'));d['visualReview']=review;(P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
old=R/'character/veld-south-material-study-v1/registration.json';d=json.loads(old.read_text(encoding='utf-8'));d['selectionDecision']='Superseded for original-master colour fidelity by veld-south-material-master-v2. V1 matched the darker processed runtime idle; identity-versus-selected-grade-audit.png/json prove that target differs from original authored master. Keep old accepted normal runtime unchanged until broader integration evidence.';old.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld South colour authority corrected to original authored master — October 2, 2026

New staged character/veld-south-material-master-v2 supersedes the previous shared
material study for original-master fidelity. A direct148ruler comparison exposed
that selected crew-runtime-matte idle was already darker than the original authored
identity: diagnostic skin median156/105/76 versus218/125/84. V1's darker study moved
actions toward a processed derivative. Retained identity-versus-selected-grade-audit
in character/veld-south-material-study-v1 documents the correction. Accepted normal
runtime remains preserved; this is a staged candidate, not a reset of owner data.

Candidate standing endpoint is exact original-south-identity-reference.png at one
148standing ruler, whole-image placement and unchanged colour. master-reference.json
binds original723fb333 source, scale/offset/export. Other16South bodies retain source
geometry/alpha, poses/pivots/timings; shared fixed RGB head curves restore original
skin warmth without per-frame normalization. Existing cloth.93/offset0,1,2 and
neutral metal.82 treatment retained with pose-aware case/grip protection. Equipped
head/shell fitting boxes on16poses remain exact; original35x39South shell refitted
onto original authored idle. One static idle endpoint is not a complete idle clip.

Build68checks0. Native987checks0/176presentations9.01s/89inputs unchanged; scratch
APPDATA/all2931owner non-log files unchanged. Five actions/both gears retain520cargo,
320starts/stops and840gait; exact shared held and start/gait joins and exact original
authored idle endpoint verified. All10boards/176native-source pairs plus fullbare
terminal015 inspected at47/93/148;176native previews decodeexact. Browser10finite
completions and original bare terminal screenshot reviewed; tab34 retained. Walking
source page shows one cycle; native gait uses supplied-distance actual player.

Lesson: original authored master and accepted processed runtime are different
authorities. Inspect both before selecting a grade target; matching a dark derivative
can make numeric consistency improve while moving away from the requested master.
Retain prior studies/accepted runtime; record the target and its source explicitly.
Diagnostic skin medians do not establish complete face/hair/detail matching.

South turn matching not completed this turn: the authority audit changed the next
action. Hair/contrast/grip/clasp and all angular/cardinal joins still need visual
polish. Normal selectors/controller, actual route/contact/case lifecycle, checkpoint
and Continue unchanged/unverified. Next compare original cardinal masters/turns
against corrected candidate, finish full idle and phase/cardinal/furniture/swimming
coverage, guarded integration and whole-library consistency. Full Veld goal active.
Handoff: character/veld-south-material-master-v2/HANDOFF.md.

'''
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 with p.open('rb') as src:
  if src.read(120).startswith(block.encode('utf-8')[:120]):continue
 st=p.stat();tmp=p.with_name(p.name+'.veld-original-master-colour.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 for attempt in range(20):
  assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==19:raise
   time.sleep(.5)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Original South master palette

## Objective and acceptance
Complete full master-matched Veld animation set, maintain skill/pipeline/bible,
then whole-library consistency/polish. Active/incomplete. Scoped South correction.

## Accepted decisions and constraints
Original authored identity supplies colour authority/standing endpoint at one148
ruler. Processed selected matte idle is darker, retained as accepted legacy output.
Other16whole bodies preserve geometry/alpha/timings. Fixed shared material curves,
pose-aware case/grip protection. Existing equipped head boxes preserved; original
35x39South shell refitted on authored idle. Scratch APPDATA, no normal adoption.

## Current state
This folder: original-idle-master.png/master-reference.json, build/fixed recipe,
17paired frames/six manifests, ten native boards/APNGs, finite page/browser proof.
New tests/test_veld_south_material_master_v2.gd plus UID and isolated tools runner.
Output/veld-south-material-master-v2 has final evidence. Previous study v1 preserved
and annotated superseded for master colour fidelity; comparison audit there proves
original identity versus selected dark derivative. Five maintained refs updated.

## Verification
68build0;987native0/176presentations9.01s/89inputs unchanged;2931owner non-log files
unchanged. Five actions/both gears, exact held/start/stop/pickup and start/gait joins,
exact original authored idle alias. All176pairs/10boards/fullbareterminal015 viewed;
176native APNG samples decodeexact. Ten browser source completions and original
bare terminal screenshot inspected. Hair/contrast/case hardware remain polish.

## Next action
Original cardinal master/turn comparison before extending grade. South turns not
repaired this turn because authority audit exposed wrong grade target. Complete
idle/phase/cardinal/furniture/swimming coverage, actual room contact/prop lifecycle,
normal selector/controller/Continue and whole-library consistency remain. No full
natural cadence, integrated gameplay or full-set acceptance claimed.
''',encoding='utf-8')
print('Recorded original-master colour authority correction in five maintained references.')
