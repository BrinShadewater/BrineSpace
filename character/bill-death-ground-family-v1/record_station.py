from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-station-candidate-v1'
assert not (P/'lowered-entry-evidence.json').exists(), 'Historical recorder cannot overwrite lowered-entry evidence.'
r=json.loads((OUT/'validation.json').read_text());review=json.loads((P/'station-review.json').read_text());assert r['returnCode']==0 and '101 checks,0 failures' in (OUT/'native.log').read_text() and len(review['joins'])==16
summary=f'''Bill dry-collapse actual station/interruption audit — October 1, 2026.
Owner galley layout copied into scratch profile. Actual geometry/rebuild/standing
clearance at servicecounter112,160 and separate aisle point; four fixture-controlled
directions x two gears, last kneel/death entry/held terminal:48 native captures.
Existing RoomFlooding.kill path and actual station layered renderer used; death
holds original foot. Facing/kneeling forced for audit, not chosen galley activity.
101 native fixture checks0failures{r['seconds']}s; explicit scratch profile logged,
fresh capture. Overall validation FALSE: owner guard detected{r['realProfileChanges']}
among{r['realProfileFileCount']:,} non-log files. Evidence retained, no retry/owner restoration.
Report filename carries live project process371472; do not attribute those writes
to this scratch fixture or certify owner isolation from a green art-check count.
Hash-bound counter and aisle boards reviewed at unchanged native crop scale.
VERIFIED VISUAL DEFECT: all candidate deaths enter exact upright idle even after
kneeling, visibly lifting head/body first.16 measured crown-rise proxies recorded;
these are alpha extents, not anatomical/physical acceptance measurements.
North-facing corpse overlaps the counter at its actual service anchor; no full
physical clearance certification. Candidates remain staged; don't select merely
because prior459 mortality/save or261 family-pixel checks passed.
Next repair lowered-action death entry with persisted initial phase/pose and
prove interruption/save continuation; resolve actual placement/occlusion without
editing owner room geometry. Then normal selection/fresh Continue and wider
cross-action joins. Generic rest, meals/inspection and full-set polish remain.
No gameplay/controller/reward/normal binding/owner layouts changed this milestone.
Lesson: exact standing entry is only valid for upright callers. Inspect actual
pre-action/entry/terminal joins in the room renderer; native technical success
and clear standing anchor do not certify collapse anatomy or furniture clearance.
Full objective stays active.
'''
old=(P/'HANDOFF.md').read_text(encoding='utf-8');(P/'HANDOFF.md').write_text('# Current station defects — October 1, 2026\n\n'+summary+'\n## Earlier mortality evidence\n\n'+old,encoding='utf-8')
paths=[P/'HANDOFF.md',P/'station-review.json',P/'station-review.html',P/'station-counter-review.png',P/'station-aisle-review.png',P/'prepare_station.py',P/'build_station_review.py',ROOT/'tests/test_bill_death_ground_station_candidates.gd',ROOT/'tests/test_bill_death_ground_station_candidates.gd.uid',ROOT/'tools/run_bill_death_ground_station_candidate_validation.py']+[OUT/name for name in ['validation.json','native.log','contacts.json','profile-before.json','profile-after.json']]
e={'status':'staged_defects_found','nativeArtChecks':101,'overallPassed':r['passed'],'native':r,'visualDefects':['upright death entry raises kneeling caller','north corpse/counter overlap'],'captureBindings':review['sha256'],'scope':'actual galley two contacts and forced four-facing kneel interruption; defect evidence, not clearance acceptance','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'station-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill dry-collapse station join defects — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded real station join defects and strict failed profile guard; candidates remain staged')
