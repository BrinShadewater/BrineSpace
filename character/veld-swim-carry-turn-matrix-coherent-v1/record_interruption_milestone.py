from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];O=R/'output/veld-expedition-interruptions-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((O/'validation.json').read_text());r=json.loads((H/'interruption-review-v1/report.json').read_text())
assert v['passed'] and not v['realProfileChanges'] and r['failures']==0 and len(r['journeys'])==4
normal=next(x for x in r['journeys'] if x['mode']=='delivery')
assert len(normal['restoredPhases'])==12 and len(normal['powerHeldPhases'])==8
assert all(len(x['gearGuardPhases'])==12 for x in r['journeys'])
assert r['checks']==12060
paths=[R/'tools/review_veld_expedition_interruptions_v1.gd',R/'tools/run_veld_expedition_interruptions_validation_v1.py',O/'native.log',O/'validation.json',H/'interruption-review-v1/report.json',R/'scripts/run_save.gd',R/'scripts/crew_expedition.gd',R/'scripts/airlock_cycle.gd',R/'scripts/airlock_service.gd',R/'scripts/bill_npc.gd',R/'scripts/crew_sprite_player.gd',R/'scripts/grid_canvas.gd',H/'candidate-clearance-profile-v1.json']
for row in r['journeys']:paths.extend(H/'interruption-review-v1'/c['file'] for c in row['captures'])
f=json.loads((H/'route-evidence-v1.json').read_text())['frameHashes'];assert all(sha(R/p)==h for p,h in f.items())
(H/'interruption-evidence-v1.json').write_text(json.dumps(dict(installed=False,checks=r['checks'],journeys=4,diskRestores=12,powerHolds=8,gearGuards=48,hashes={p.relative_to(R).as_posix():sha(p) for p in paths},frameHashes=f,validation=v,scope='Dedicated native full journeys with explicit candidates; exact phase-entry disk pose/route/action/chamber/simulation clock restores; eight chamber/station power holds,48 actual gear-request guards,work/pickup recalls and25s oxygen automatic recall. Not arbitrary mid-frame restore,all safety events,traffic or owner/full-set acceptance.'),indent=2)+'\n',encoding='utf-8')
title='Veld expedition phase restores and safety guards verified — September 30, 2026'
body='''Four actual native journeys pass 12,060 checks: 12 phase-entry disk restores preserve exact pixels, route/action clock, chamber clock and simulation clock; eight station/chamber power holds; 48 real gear-request guards; sampling/pickup recalls and automatic recall at 25s tank reserve. Exact extraction/credit rules and dry/alive return pass. Engine errors zero; 2,914 owner non-log files unchanged. Initial fixture incorrectly set breath reserve to60s (runtime max15s); rejected checkpoint intervals retained and fixture corrected, validator unchanged. [Handoff](../character/veld-swim-carry-turn-matrix-coherent-v1/INTERRUPTION_HANDOFF.md). Candidate art/profile still staged; normal-loader installation proof and broader traffic/safety/arbitrary-phase checks remain. Full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;old=p.read_bytes()
    if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Expedition phase checkpoint contracts — September 30, 2026

Read actual capacity validators before setting a fixture: crew breath reserve is
15s while helmet tank capacity is60s. A later needs tick can clamp bad setup and
hide it from return-only save tests. Report Save.last_error before reading a
checkpoint, since reads can reset it. Test real locker requests during expeditions;
do not force unsupported gear removal. Compare restored expedition routes/action
clock, chamber clock and simulation time alongside pixels and paused position.
Exercise power holds in station/chamber phases and both manual/oxygen recalls with
exact no-early-extraction and delivery rules. Phase-entry restores are not arbitrary
phase, all interruptions or traffic proof. Preserve failed intervals and update
fixtures rather than relaxing production validators. Evidence: Veld cargo matrix
INTERRUPTION_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if b'Expedition phase checkpoint contracts' not in p.read_bytes():
        with p.open('ab') as out:out.write(lesson.encode())
print('12,060 checks bound to12phase restores/8power holds/48gear guards; handoff and lessons recorded.')
