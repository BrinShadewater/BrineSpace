from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-cardinal-natural-v1'
data=json.loads((O/'journeys.json').read_text());v=json.loads((O/'validation.json').read_text());h=json.loads((R/'output/bill-carry-cardinal-player-v1/validation.json').read_text());assert v['passed'] and h['passed']
findings=[]
for j in data['journeys']:
 rec=j['records'];arrival=next(i for i,r in enumerate(rec) if r['stage']=='workshop_unload');before=rec[arrival-1];after=rec[arrival]
 findings.append({'helmet':j['helmet'],'unalteredRoute':j['generatedRoute'],'beforeArrival':before,'arrival':after,'observedDirections':sorted({r['direction'] for r in rec}),'observedTurnClips':sorted({r['clip'] for r in rec if r['clip']}),'unloadReached':j['unloadSeen'],'arrivalSnapUnresolved':before['direction']!='north' and after['direction']=='north'})
assert all(f['arrivalSnapUnresolved'] for f in findings)
(P/'review-assessment.json').write_text(json.dumps({'reviewedNativeBoards':['bare-natural-review.png','helmet-natural-review.png'],'native':v,'headless':h,'nativeSourceSamples':74,'findings':findings,'normalSelectionChanged':False,'goalComplete':False},indent=2)+'\n')
paths=[P/'carry_player.gd',P/'carry_actor.gd',R/'tests/test_bill_carry_cardinal_player_v1.gd',R/'tests/test_bill_carry_cardinal_natural_v1.gd']
for bank in ['bill-carry-east-gait-v3','bill-carry-start-east-v4','bill-carry-south-gait-v2','bill-carry-start-south-v1','bill-carry-west-gait-v2','bill-carry-start-west-v2','bill-carry-north-gait-v1','bill-carry-start-north-v1']:
 for gear in ['bare','helmet']:
  f=R/f'character/{bank}/{gear}-manifest.json';paths.append(f)
  for source in json.loads(f.read_text())['states'][0]['frameFiles']:paths.append(R/source.removeprefix('res://'))
(P/'input-hashes.json').write_text(json.dumps({f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
lesson='''
## Bill unified cardinal carry and natural workshop route — October 1, 2026

Staged `character/bill-carry-cardinal-runtime-v1` admits latest eight paired
source banks through explicit whole manifest paths: East gait3/start4, South
gait2/start1, West gait2/start2, North gait1/start1. One player selects each
direction's finite320ms entrance and late contact (.104 East/.139 elsewhere),
with direct pickup entry and completed-turn entry. One actor holds only the
first40ms standing row and existing planted carry turns; inherited needs,
navigation, service and emergency controller remain active. No source art,
grade/ruler/pivot, normal loader or Title Continue changes.

Headless271checks0failures/5.03s cover both gears, four direct entries/all6rows,
exact contact exit and next gait1, gear/backwards-clock/state cancellation,
all12quarter/half facing changes per gear turning before first step. This does
not certify physical routes or snapshots; start_motion is not yet in snapshots.

Native actual main/workshop test leaves generated waypoints, heading and arrival
unchanged; both gears follow [(7792,8416),(7760,8416)]. It passes2862checks0failures
/56.62s, collision/source submission/needs/unload completion. Source-clock replay
and74paired room/source views (37per gear) generated and both boards reviewed.
Actual native direction coverage East/West/North; actual turn East-West, then
West entrance and walk. South and other turns remain headless/prescribed evidence,
not natural physical coverage. Both intervals scratch APPDATA and all2931 owner
non-log files unchanged. No commit, release or save/room ownership changes.

Visual finding: arrival at7.583s forces original North unload directly from West
gait; last carry source and first unload source do not have a settling/yaw bridge.
Original unload then rises quickly; improved staged `bill-unload-north-rise-v1`
is not admitted here. Green service/source checks expose rather than solve this
visible jump. Preserve this natural before-repair interval. Next connect a
generalized arrival plan to the latest source banks, reverse the actual partial
entrance or settle the actual gait contact, turn to North, and use improved rise
within the original2s unloading budget. Reconcile earlier West stow bank bindings
before claiming adoption. Then interruption/snapshot/Continue and broader natural
route coverage; full Bill set and cross-family polish remain incomplete.

Lesson: combine directional source banks before certifying a sequence. Observe
the production-generated route and arrival, not only a chosen long lane. A
missing bridge at arrival can pass every geometry/service check; inspect the
actual adjacent submitted textures and retain the defect as scoped evidence.
'''
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+lesson)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+lesson)
status=R/'docs/CURRENT_STATUS.md';prior=status.read_text(encoding='utf-8');status.write_text(lesson.strip()+'\n\n'+prior,encoding='utf-8')
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Unified Bill carrying

## Objective and acceptance
Full master-matching Bill set then cross-family consistency/polish; incomplete.
This milestone combines current cardinal sources and reveals natural arrival.

## Accepted decisions and constraints
Directional masters, current paired banks, nominal148/pivot128224 and matte
material preserved. Reversible integration authorized, no gameplay/room/save
ownership change. Keep owner and other character work intact; scratch APPDATA.

## Current state
Staged carry_player/actor and UIDs admit all8gait/start profiles, direct pickup,
turn-first entry, finite bridge and correct late contact. Headless/native tests,
scoped runners,74source/native samples, replay, hashes and findings retained.
Pipeline/bible/maintained and installed skill lessons updated. Normal unmodified.

## Verification
271headless checks0fail/5.03s;2862native0fail/56.62s. Four direct entries and
12turns per gear headless, actual natural East-West turn/West walk/North unload
with unchanged generated route both gears, source/geometry/needs valid.
37native/source views per gear visually reviewed; all2931 owner files unchanged.

## Next action
Arrival jumps West gait→North unload at7.583s; current North unload rise is old.
Generalize stow to latest banks and actual submitted entry/gait source, then
connect staged North rise within original2s budget. Preserve before evidence.
Afterward natural-route/cancellation/gear/medium/hazard/snapshot/fresh Continue
coverage before normal adoption. start_motion snapshot currently missing.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');print('Recorded unified source integration, natural route evidence and unresolved arrival')
