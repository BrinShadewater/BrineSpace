from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((R/'output/veld-carry-east-start-master-v2/validation.json').read_text(encoding='utf-8'));assert v['passed']
for n in ['execution-start-v2.json','registration.json','native-review-evidence.json']:
 d=json.loads((P/n).read_text(encoding='utf-8'));d['visualReview']='Raw corrected fourpose source,8paired exports and4chronological boards/all48source-native pairs seen. Head proxy28 vs canonical26/27 closer than rejected30/31; compact case and continuous wholebody steps. Whole-body horizontal registration avoids planted-boot centroid drift. Material/grip/stride geometry/cadence/world travel remain polish.'
 (P/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld East whole-body carry start/stop sources — October 2, 2026

Staged veld-carry-east-start-master-v1 adds finite320ms fourpose carry-start-east
and exact reversed carry-stop-east, both gears. First held and final carry0 are
exact whole accepted East master family aliases; existing sixpose840ms carry row
unchanged. Builtin raw v1 exec86df3a3e rejected larger heads/case; raw v2 exec
ebe5994d-90f0-4711-8eb0-674aa4d3a7e1 corrects entire body source, prompt/refhashes
retained. One first-standing148ruler .2375601926163724; no body strips/per-pose
height forcing. Intermediate head width28 vs canonical26/27 (v1 30/31).
Wholebody translations align canonical head axis125 and opaque boot floor224;
centering moving planted-boot span had shifted torso and was corrected. Natural
leg swing retained. Same West material recipe/protected case-glove box; original
East34x38 shell at unchanged scale/grade, body outside head region exact.
52buildchecks0. Actual standalone player317checks0/48native samples5.81s;41frozen
inputs stable, scratchAPPDATA/2931owner files unchanged. All48pairs in4boards and
raw/8exports seen;48native APNG decode checks exact. Fourfinite browser completions
and paused helmet firststep seen/saved. Nativeviewer400ms repeats are resets, not
320ms authored loop. First passing test interval retained before correcting the
comparison label and explicit whole resource paths; v2 is current evidence.

No normal sources/controllers changed. New clips not automatically used by
production carry transition selector. Next real-route start/stop clock, travel
acceleration/deceleration and phase-aware gait0 joins; West/other directions also
need starts/stops. Head/material/grip/foot contact and continuous cadence remain
polish. Full North idle, case ownership/checkpoint, coordinated safety/Continue,
South/cardinal/furniture/swimming and full-library consistency remain. Goal active.
Lesson: shrinking equipment by whole source edit is preferable to body masking;
wholeframe pivot registration must not shift torso with alternating planted feet.
Exact endpoints and standalone clock checks do not prove locomotion in a room.
Handoff: character/veld-carry-east-start-master-v1/HANDOFF.md.

'''
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-east-start.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 now=p.stat();assert (st.st_size,st.st_mtime_ns)==(now.st_size,now.st_mtime_ns)
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld East first carrying step

## Objective and acceptance
Full Veld master-matched library plus cross-library consistency/polish, active.
This is staged source/player progress; real motion/lifecycle remains required.

## Accepted decisions and constraints
Whole body/one148standing ruler, exact master held and gait0 endpoints, unchanged
existing carry row. Same grade/rigid original East helmet. No torso/leg strips.
Scratch APPDATA and preserve owner saves/concurrent work/normal selections.

## Current state
This folder retains two raw sheets/prompts/execution/refhashes, rejected-v1 record,
wholeframe registration/build, paired4pose start/stop manifests/APNGs and unchanged
carry aliases, nativeboards/evidence/browsercontrols. New standalone test+UID/runner.
No actor override or production selector adoption for new clips yet.

## Verification
52build0;317standalone0/48native samples5.81s/41inputs stable.48native pairs in
4boards reviewed,48APNG decoded snapshots exact. Fourfinite browser completions,
helmet smallstep seen/saved. ScratchAPPDATA/2931owner files unchanged. First passing
test interval preserved; current v2 corrects display label/full resource references.

## Next action
Real-route simulation clock/travel acceleration and phase-aware joins before using
these clips. West/cardinal start/stop needs equivalent whole sources; don't mirror
asymmetric equipment. Material/grip/foot contact and continuous native cadence
remain polish. North fullidle, independent prop lifecycle, guarded safety/Continue,
South/cardinal/furniture/swimming/fullset consistency still in full goal.
''',encoding='utf-8')
print('Recorded first-step source/player milestone and five maintained references.')
