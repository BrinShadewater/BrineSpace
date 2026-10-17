from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
world=json.loads((P/'world-review-evidence.json').read_text(encoding='utf-8'));assert world['validation']['passed']
world['visualReview']='Both native workshop boards reviewed: all7 unload poses, exact static idle and8/24/48unit departures per gear,22views. Progressive rise improves abrupt stand; deeper release dip/contact/material and open-stride first step remain polish. No uninterrupted cadence/lifecycle acceptance.'
(P/'world-review-evidence.json').write_text(json.dumps(world,indent=2)+'\n',encoding='utf-8')
block='''## Veld North whole-body rise-to-master transition — October 2, 2026

Staged cargo-north-master-family-v1/rise-join-v3 uses three whole authored recovery
poses between reused descent and exact original master standing/static idle. Raw
builtin imagegen9b5c77a1-34ea-4d15-8077-5affaeb11c54, prompt/refhashes retained;
original master authoritative, older action motion context only. Generated fourth
standing diagnostic retained, not used as endpoint. One final standing148ruler
.23604465709728867; new native body heights102/128/143, no body strips or per-pose
scale. Shared West recipe, fixed original33x35 helmet, protected body/alpha.
Seven poses70/90/100/60/65/65/70ms=520finite; pickup exact reversed frames AND holds.
Separate same33x24floor case appears behind body at release source3/.26s onward;
pickup source preview inverse; actual pickup ownership still unimplemented.
76buildchecks0; standalone457checks0/72samples6.24s/47inputs stable. All72source/
native pairs in4boards reviewed and72decode checks exact. Browser4finite completions,
helmet intermediate rise seen/saved, quarter-speed control verified.
Actual workshop5203checks0/102.35s/224inputs stable; scratchAPPDATA/2931owner files
unchanged. Both native boards22views seen:7poses+idle+3departures per gear. Exact
master terminal idle retained, prop fixed through8/24/48world-unit departure.
No normal source/controller/room change; authoring-only coordinated subclass.

Remaining: release dip/contact and suit-detail/material polish, first-step/stop,
full North idle breathing, independent case pickup/ownership/lifetime/checkpoint,
guarded needs/safety/medium/gear/death/Continue adoption. South/master cardinal,
furniture/swimming and full-library consistency remain; full goal active/incomplete.
Lesson: a correct master endpoint still needs whole authored recovery poses; retain
one standing ruler and reverse holds with pickup. Sampled pose/departure checks
do not prove uninterrupted motion or production prop lifecycle.
Handoff: character/veld-cargo-north-master-family-v1/rise-join-v3/HANDOFF.md.

'''
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-rise.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 now=p.stat();assert (st.st_size,st.st_mtime_ns)==(now.st_size,now.st_mtime_ns)
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld North recovery motion

## Objective and acceptance
Full master/style/perspective/proportion/grade-matched Veld library, then full-set
consistency/polish. Active/incomplete; this is a scoped staged recovery milestone.

## Accepted decisions and constraints
Original whole North master endpoint/static idle and one standing ruler. New whole
recovery sources, shared West recipe and unchanged rigid shell. Fixed separate
case after release. Preserve normal sources/controllers, owner saves/concurrent work.

## Current state
This folder: raw4pose sheet/prompt/execution/reference hashes, whole extraction,
build/registration, paired7pose actions/static idle and APNGs, independent floor
prop wrapper, browser/native/world boards/evidence. Two new fixtures with paired
UIDs and runners. Existing idle-join-v2 remains retained. Nothing normally adopted.

## Verification
76build0.457standalone0/72samples/all72pairs visually reviewed.5203world0/102.35s,
22worldviews seen, case fixed through8/24/48unit departure, exact terminal/idle.
47standalone/224worldinputs unchanged; scratchAPPDATA/2931owner files unchanged.
Four browser finite completions and helmet intermediate seen/saved. This is sampled
pose/route/departure evidence, not full uninterrupted cadence or lifecycle.

## Next action
Genuine whole first-step/stop and full North idle breathing. Release dip/contact/
material polish still pending. Then independent case pickup/lifetime/checkpoint
and coordinated controller needs/safety/service/medium/gear/death/fresh Continue
before guarded normal adoption. South/cardinal/furniture/swimming/full-set polish
remain. Arrival hold in authoring subclass still skips ordinary actor update.
''',encoding='utf-8')
print('Recorded North recovery milestone and updated five maintained references.')
