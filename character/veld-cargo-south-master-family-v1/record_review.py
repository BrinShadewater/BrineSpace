from pathlib import Path
import json, os, shutil, time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-south-master-family-v3'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
e=json.loads((P/'native-review-evidence.json').read_text(encoding='utf-8'))
b=json.loads((P/'browser-review.json').read_text(encoding='utf-8'))
assert v['passed'] and e['sourceNativePairs']==72 and e['decodedNativeFramesExact']==72
assert len(b['completions'])==4 and all(x['state']['completion']=='Pose 7 / 7 - complete' for x in b['completions'])
review=('Raw v4 whole source and four chronological native/source boards, all72 pairs, '
        'and full helmet release008 reviewed at47/93/148display sizes. Small heads22-23, '
        'original35x39shell, coherent whole-body lowering/rise. Descent147/119/94 improves '
        'v3 147/137/93 jump. Separate foreground case visible at112199. Four finite browser '
        'completions and paused helmet release pose4 screenshot inspected. Original idle '
        'material remains visibly darker; case/grip/clasp matching and continuous in-room '
        'cadence/contact need polish. No normal selector/controller/save/ownership acceptance.')
for name in ['registration.json','native-review-evidence.json','execution-unload-v4.json']:
 d=json.loads((P/name).read_text(encoding='utf-8'));d['visualReview']=review
 (P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
for name,decision in [('execution-unload-v1.json','Oversized heads25-27 versus canonical23; superseded by whole source v2.'),('execution-unload-v2.json','Head corrected22-23; recovery93 to130 gap superseded by v3 whole recovery poses.'),('execution-unload-v3.json','Recovery111/130 improved. Lowering137 to93 gap superseded by v4 whole second pose119. Retained lowering-study-v3 package; final selection is v4.')]:
 d=json.loads((P/name).read_text(encoding='utf-8'));d['selectionDecision']=decision
 (P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld South master pickup/unload: smoother descent and visible case — October 2, 2026

Staged character/veld-cargo-south-master-family-v1 now contains seven whole-body
pickup/unload poses, exact canonical held entry and exact original bare idle end.
Selected builtin whole-source edit v4 04456277-79b9-4259-8335-49ae8f2f4e91 lowers
the second coherent pose to119 native pixels: descent147/119/94 replaces147/137/93.
Recovery93/111/130/148 remains naturally proportioned. All four raw sheets, exact
prompts/executions/reference hashes and rejected/study packages retained. Sourcev1
heads25-27 rejected; v2 corrected22-23; v3 corrected recovery spacing; v4 descent.

One first-standing148 ruler .26287744227353466, whole-body boot-floor registration,
no per-pose scaling or anatomy strips. Head widths22-23; original35x39South helmet
unchanged scale/grade, bounded fit preserves body outside head region. Shared West
material recipe and protected case/grip areas; alpha and protected pixels exact.
Seven holds70/90/100/60/65/65/70 total520ms; pickup exactly reverses bodies/holds.
Existing840ms carry and exact held aliases remain. Original idle is selected South
breathing frame0 translated36/52 whole-body into256canvas, no endpoint retone.

Independent33x24floor case at112199, bottom223 versus bootfloor224, draws in front
after release. North's behind-body layer rule obscured the case in South nativev1
despite passing tests; depth study corrected placement/order before nativev2.
Final nativev3 after lowering repair:463checks0/72presentations6.48s/63inputs
unchanged; scratchAPPDATA/all2931owner non-log files unchanged. Build95checks0.
All72native/source pairs in4boards plus fullhelmetrelease008 reviewed at47/93/148;
72native APNG frames decodeexact. Browser all4gear/action finite completions and
pausedhelmetrelease pose4 reviewed/saved; tab32 retained. Earlier intervals retained.

Visual acceptance is scoped: source motion improved and foreground case visible.
Original idle remains visibly darker than authored intermediates; pooled material
matching, case/clasp/grip shape, actual room contact/depth and continuous cadence
remain polish. Static idle alias is not a complete idle animation. No normal runtime
selection/controller, real South route, prop ownership/lifetime/departure, checkpoint
or menu Continue adoption. Full master-matched Veld goal remains active/incomplete.

Lessons: compare pose-to-pose height spacing before timed playback, repair a coherent
whole source pose rather than forcing pose heights. Prop depth rules depend on view;
a passing texture/player check can hide a floor case. Review native foreground and
master endpoint material joins explicitly. Next: South idle material join and actual
room case handoff, remaining phase/cardinal transitions, guarded normal integration,
Continue/ownership, full idle/furniture/swimming, then whole-library consistency.
Handoff: character/veld-cargo-south-master-family-v1/HANDOFF.md.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in paths:
 with p.open('rb') as src:
  if src.read(120).startswith(block.encode('utf-8')[:120]):continue
 st=p.stat();tmp=p.with_name(p.name+'.veld-south-cargo.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:
  dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 for attempt in range(20):
  assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==19:raise
   time.sleep(.5)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: South master cargo actions

## Objective and acceptance
Complete the full master-matched Veld animation set, maintain pipeline/skill/bible,
then cross-library consistency/polish. Goal active/incomplete. This milestone proves
staged South pickup/unload source and standalone finite playback only.

## Accepted decisions and constraints
Original identity and exact held/original idle endpoints; one148standing ruler,
coherent whole-body authored poses and correct asymmetric hip gear. Original35x39
South shell unchanged. Shared grade/protected hardware, independent foreground
case112199. No procedural anatomy/mirroring. Always scratch APPDATA for Godot.

## Current state
This folder has4raw sheets/prompts/executions, reference bindings, extraction/build,
seven paired body poses, manifests/APNGs/finite page, native/browser reviews and
retained rejected/study packages. Selected rawv4 lowers second figure to119 between
147standing/94crouch; recovery93/111/130/148. New test+UID pair in tests and runner
in tools; final interval output/veld-cargo-south-master-family-v3. Five maintained
references updated. Normal runtime selectors and controller remain unchanged.

## Verification
95build0;463native0/72presentations6.48s/63inputs unchanged; all2931owner non-log
files unchanged. All72native/source pairs/four boards and fullhelmetrelease008
reviewed;72native previews decodeexact. Fourbrowser finite completions and paused
helmetrelease pose4 screenshot inspected. Case foreground fixes visual obscuring
seen in passing nativev1. Head22-23 and original shell preserved. Original idle
endpoint remains visibly darker; material/contact/grip joins need polish.

## Next action
Match South intermediate materials to original idle authority and review actual
room case contact/handoff. Finish remaining gait phases/cardinals and complete
idle/furniture/swimming coverage. Guard normal selector/controller/Continue and
case ownership/lifetime integration. Full continuous in-room cadence, safety
interruptions and whole-library visual consistency remain unproven.
''',encoding='utf-8')
print('Recorded South cargo source/native/browser milestone and pose/depth lessons in five maintained references.')
