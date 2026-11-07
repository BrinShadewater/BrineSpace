"""Record real dispatched route scope and visible mixed-family join findings."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';O=B/'east-loop-02-world-review';A=ROOT/'output/marsh-animation-audit/loaded-swim-east-world-05-2026-10-02'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(A/'report.json');v=read(O/'verification.json')
assert (v['checks'],v['failures'],v['sourceNativePairs'],v['samples'],v['actorPlayerRestores'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(15137,0,48,3710,48,647,2931)
assert set(r['eastSlots'])==set(r['pickupSlots'])==set(range(6)) and set(r['unloadSlots'])==set(range(4)) and set(r['drainSlots'])==set(range(5))
assert set(r['turns'])=={'swim-carry-turn-west-east','swim-carry-turn-east-north'}
assert len(v['endpointChecks'])==4 and not any(c['sameAsNewEastLoop0'] for c in v['endpointChecks'])
for q in v['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
for suffix,checks,failures in [('02',36009,5),('03',13223,30),('04',15137,1)]:
    audit=ROOT/f'output/marsh-animation-audit/loaded-swim-east-world-{suffix}-2026-10-02'
    old=read(audit/'report.json');assert (old['checks'],old['failures'])==(checks,failures)
    assert (audit/'fixture-original.gd').is_file() and (audit/'preparer-original.py').is_file()
    assert read(audit/'owner-before.json')==read(audit/'owner-after.json')
(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'all48SourceNativePairsInspected':True,'pairedBoardsInspected':6,'findings':'Staged East loop renders clearly in actual seabed return route. Same four figures across six timing holds. Correct one-right-edge case latch differs visibly from older turn endpoint hardware; old WestEast last / newEast0 / old EastNorth first switch pose/body/case rendering. Source equality exposes four linked East endpoints still old: East pickup last, WestEast turn last, EastNorth turn first and East drain first. Actual q2 pickup West and drain South only, so East pickup/drain mismatches are source-audit findings, not observed q2 gameplay. Complete route success does not approve those joins. Head/body breadth, grade and registration remain provisional.','next':'Whole other loaded-swim cardinal sources (West own LEFT temple/case edge, then North/South); then linked whole turn/pickup/drain families with exact shared selected endpoints, complete route and save/Continue evidence before normal admission.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_loaded_swim_world05.py')],check=True,stdout=subprocess.DEVNULL)
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh loaded-swim East actual dispatched route and mixed joins — October 2, 2026'
lesson='''

## Marsh loaded-swim East actual dispatched route and mixed joins — October 2, 2026

Actual normal q2 dispatch with free authored airlock/site fixture, normal global
cost/failure flags, automatic route and exact main/controller/Cycle/grid/player:
15137 checks, zero failures/errors, exit0. All12 expedition phases complete dry/
alive, one site unit extracted and one cargo delivery credited only after unload.
3710 controlled20ms samples,48 exact-source/native pairs and48 actor/player
restores + actual paused outer-process holds. Six East timing slots alias four
authored02 figures; all6 pickup,4 unload,5 drain poses and actual WestEast/EastNorth
water cargo turns observed. All48pairs/six boards inspected. Only East loaded-swim
loop privately overridden; other clips remained old normal catalogue artwork.
647bounded inputs stable DURING interval,2931owner non-log files unchanged under
scratchAPPDATA. No normal catalogue/runtime art selection changed. Metadata/review
artifacts after interval are not a claim of that exact current freeze.

Native rendering shows candidateEast clearly on actual seabed, but mixed old/new
turn joins visibly switch body/pose/case hardware. Four linked source endpoints
still alias the OLD East loop0, not candidate02: East pickup last, WestEast turn
last, EastNorth turn first, East drain first. In q2, pickup isWest anddrain isSouth;
East pickup/drain mismatch is source-audit evidence only, not witnessed in q2.
Actual route uses oldWestEast8 -> newEast0 and newEast3 -> oldEastNorth0. Keep all
four cardinal loaded-swim endpoint sources coherent before reauthoring linked
whole turn/pickup/drain families; endpoint-only pixel swaps cannot prove intermediate
body/case consistency. Do not admit isolatedEast art because controller tests pass.
Neutral width+3, head/body/grade and physical registration/contact remain open.

Retained failed fixture runs (not gameplay regressions): world02 used direct
actor.update, bypassing main's expedition orchestration; 36009checks/5failures,
9000samples stuck inapproach,0captures. Main updates expeditions with advance_needs
plus CrewExpedition.advance instead of normal actor.update. world03 corrected
dispatch but called internal _update_test_walker during pause: that worker has NO
pause guard. It advanced the trip during every capture pause;13223checks/30failures,
29captures,3260samples. Use actual outer _process while paused, not an internal
worker, to verify game pause. world04 then completed behavior/restores but incorrectly
expected4 timing indices instead of6;15137checks/1failure. Player creates distinct
textures per slot even when paths alias the same four drawings. world05 corrected
coverage semantics and passed. Original fixture/preparer copies and all first
reports/logs remain; owner profiles unchanged in every interval. Per-frame route/
next waypoint/chamber/battery diagnostics retained, rather than weakening behavior
or changing gameplay to make a fixture pass.

Next whole West loaded-swim loop (own bare LEFT temple and LEFT case edge), then
North/South endpoints; rebuild linked turns/pickup/drain consistently. Broader
route rotations, helmet, fullRunSave/fresh visibleTitleContinue, continuous motion
and physical contact remain separate gates. Drycargo normal admission/grounded
arrival pivot and remaining fullMarsh families remain required. Full master-matched
set and all-family consistency/polish active/incomplete. No live job at milestone.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_LOADED_SWIM_WORLD05_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh loaded-swim actual world route

## Objective and acceptance
Full master-matched Marsh set and all-family consistency/polish active/incomplete.
East loaded-swim02 staged; linked older water family not yet coherent/admitted.

## Accepted decisions and constraints
Whole sources and own directional identity, one neutral scale, no mirrors/patches/
per-part fitting. Automatic expedition route, real main/Cycle/grid/player and normal
cost/failure flags in authored free airlock/site fixture. Scratch APPDATA required.
Keep failed evidence; do not fix gameplay to compensate for a fixture mistake.

## Current state
Added world02 prepare, .gd/.uid fixture, fingerprint, world05 publish/record helpers.
character/marsh-loaded-swim-material-v1/east-loop-02-world-review holds48 pairs/six
reviewed boards and exact endpoint checks. Pipeline/bible/status/skill mirrors updated.
Normal catalogue/runtime unchanged. No live job. Older drycargo milestone still open.

## Verification
15137 checks/0failures/errors/exit0; one completed q2 normal dispatched expedition,
12phases,3710samples,48source-native pairs,48actor/player restores+paused _process.
All6 East timing slots (4drawings),6pickup,4unload,5drain holds and2cargo turns.
647bounded inputs/2931ownerfiles stable per interval. All48pairs seen. Four East
linked endpoints still old; actual turn joins visibly switch body/pose/case hardware.
East pickup/drain mismatch source-audit only; q2 actual pickupWest/drainSouth.
Failed02/03/04 fixtures retained with original code: wrong actor updater, internal
worker pause bypass, then4drawings-versus6slot assertion.05 fixes fixture only.

## Next action
Author whole West loaded-swim loop, then North/South with own masters/case identity.
Rebuild linked whole turns/pickup/drain around coherent endpoints before selection.
More route rotations, helmet, fullsave/visibleContinue and physical joins remain.
Continue all remaining Marsh families and full cross-family consistency/polish.
''',encoding='utf-8')
print('Recorded one real water delivery:15137checks,48 reviewed pairs; mixed-family joins remain open.')
