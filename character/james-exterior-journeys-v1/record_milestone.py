from pathlib import Path
import json,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,data):
 before=path.read_bytes() if path.exists() else None
 tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
 assert (path.read_bytes() if path.exists() else None)==before
 tmp.replace(path)
v=json.loads((P/'native-expedition-validation.json').read_bytes());e=json.loads((P/'native-expedition-evidence.json').read_bytes());old=json.loads((P/'prior-work-pose-snap-native-expedition-evidence.json').read_bytes())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and e['failures']==0
assert not any(x in (P/'native-expedition.log').read_text(errors='replace') for x in ['ERROR:','SCRIPT ERROR:','WARNING:'])
assert len(e['journeys'])==6 and sum(x['restored'] for x in e['journeys'])==4
loaded=[x for x in e['journeys'] if x['mode']!='recall-outbound']
assert len(loaded)==5 and all(x['joins']=={'salvagePickup':True,'pickupCarry':True} for x in loaded)
assert sum(x.get('joins',{}).get('salvagePickup')==False for x in old['journeys'] if 'salvagePickup' in x.get('joins',{}))==5
turns=sorted({t for x in e['journeys'] for t in x['turns']})
selection={'status':'installed_runtime_clock_polish_owner_review_pending','newRaster':False,'checks':e['checks'],'actualJourneys':6,'airlockOrientations':4,'freshSceneLoadedTurnContinues':4,'exactExtractionPickupJoins':5,'exactPickupCarryJoins':5,'priorExtractionSnaps':5,'currentExtractionSnaps':0,'actualTurnKeys':turns,'pickupAndUnloadSlotsPerLoadedJourney':6,'realProfileUnchanged':True,'evidence':'native-expedition-evidence.json','scope':'Normal dispatch, native needs and airlock cycle, exterior work/pickup/cargo turns/re-entry/drain/unload; four loaded-turn fresh-scene actual disk Continues; outbound and loaded recalls. Dedicated normally generated station, one chosen site arrangement per rotation; selected James manifests.','remaining':['Owner motion review','Extraction-stage fresh-scene Continue and interrupted work staging','Different exterior paths/sites, crowded airlocks and power/death hazards','Full mortality and cross-family motion/master consistency']}
atomic(P/'selection.json',(json.dumps(selection,indent=2)+'\n').encode())
for name in ['james-water-cargo-family-v1','james-water-cargo-turn-family-v1']:
 path=P.parent/name/'selection.json';data=json.loads(path.read_bytes());data['fullExteriorJourneys']={'checks':e['checks'],'journeys':6,'freshSceneLoadedTurnContinues':4,'evidence':'../james-exterior-journeys-v1/native-expedition-evidence.json','scope':selection['scope']};data['next']='Different exterior sites/routes/crowded airlocks, work interruption/Continue and full motion/master polish';atomic(path,(json.dumps(data,indent=2)+'\n').encode())
title='James complete exterior delivery and salvage clock polish - September 30, 2026'
lesson=f"""
### {title}

A full delivery can pass while its visible work/pickup join still snaps. All six
actual James trips initially delivered correctly; stronger actual-boundary
checks found five extraction snaps across four airlock orientations and loaded
recall. The exterior work loop had used the global visual clock. James now reads
his saved expedition.elapsed, fitting six complete selected work gestures inside
the unchanged5.48s work budget. WORK_SECONDS names the existing shared duration;
manifest metadata supplies source duration. No new timer/save field, raster,
scale/grade or reward change. Actual current-frame joins, not neutral asset
endpoint equality alone, establish continuity.
{e['checks']} native checks pass/six normal dispatch trips, four actual loaded-turn
fresh-scene disk Continues. Five actual work/pickup and pickup/carry joins are
exact, all6 pickup/unload slots exercised per loaded journey, four half/four
quarter cargo-turn keys exercised. Outbound recall extracts/credits nothing;
loaded recall returns cargo exactly once, only after dry unloading. Scratch
profile unchanged. Representative actual station/exterior screenshots reviewed;
this is not all-path/traffic/hazard/full-motion acceptance. See
JAMES_EXTERIOR_JOURNEYS_HANDOFF_2026-09-30.md. Full James goal active.
"""
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 before=path.read_bytes()
 if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:
 section=f"""## {title}

Six complete actual James exterior trips pass{e['checks']} checks: four airlock
orientations, outbound empty recall and loaded recall. Four actual fresh-scene
loaded-turn disk Continues retain actor/clock/pause/exact pose. Stronger boundary
checks found five work-to-pickup snaps; saved extraction-timer-driven six complete
source cycles now remove allfive. Existing5.48s work/reward/oxygen rules unchanged,
master matte/scale/art unchanged. All6 pickup/unload slots and eight cargo turn
keys exercised; delivery credited only after dry unloading. Representative native
screenshots reviewed; real profile unchanged. Different sites/traffic/hazards,
mid-work Continue, full mortality and cross-family motion polish remain. Goal active.
[Handoff](JAMES_EXTERIOR_JOURNEYS_HANDOFF_2026-09-30.md).

"""
 atomic(path,section.encode()+before)
handoff=f"""# Project handoff

Updated:2026-09-30 - Project:Brine Space - Task:James full exterior journey/clock polish

## Objective and acceptance
Continue all James animations and master/style/perspective/scale/material/motion
consistency. Complete journey proof is a milestone, not full-set completion.
Installed_owner_review_pending; full goal active. No export/commit.

## Accepted decisions and constraints
Selected matte neutral masters, fixed source rulers/pivots, independent equipment
views, belt wrench/forward torch. No source art edits. Existing exterior survival,
work duration and dry-delivery credit rules preserved. Scratch profile isolation.

## Current state
scripts/crew_expedition.gd names existing5.48s as WORK_SECONDS.
scripts/branforth_npc.gd caches selected manifest work duration and uses saved
expedition.elapsed for six full gestures in that budget; no new saved clock.
character/james-exterior-journeys-v1/native-expedition.gd runs six real dispatch
journeys through native survival/cycle/controller/renderer; evidence/logs/captures
and selection retained. Prior same-scene proof and five actual source-join snaps
archived. Water cargo/turn selection records, pipeline/bible/both skills updated.

## Verification
{e['checks']} checks/0fail, six actual trips: four oriented complete deliveries,
one outbound empty recall and one loaded recall. Four fresh-scene actual disk
Continues mid loaded turn preserve actor/clock/pause/exact pixels; paused process
cannot advance them. Five actual extraction/pickup and pickup/carry joins exact,
previously five extraction snaps. All6 pickup/unload slots per loaded journey;
eight turn keys ({len(turns)} unique), including allfour half turns. Native normal
loader confirms236 selected source slots. Exactly one site unit extracted per
loaded journey; no inventory credit before complete dry unload; empty recall0.
Actual rendered source nonnull throughout. Exit0/no timeout/engine warnings;
owner profile unchanged. Representative work/carry/airlock/unload screenshots
reviewed at actual station context. No all-frame motion/traffic certification.

## Next action
Mid-work Continue/interrupted work staging, different exterior sites/routes,
crowded airlocks/power-loss/death and full mortality contexts. Other galley
facings/native indices/custom contacts and cross-family motion/master polish
remain. Do not mark the full goal complete from six trips or asset coverage.
"""
atomic(R/'docs/JAMES_EXTERIOR_JOURNEYS_HANDOFF_2026-09-30.md',handoff.encode())
print(f'Recorded James exterior milestone:{e["checks"]} checks/6 trips/4 fresh Continues; goal active')
