"""Record scoped actual cargo evidence, whole-source correction and West guides."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-carry-material-v1';S=BASE/'sources'
MARKER='## Marsh East carry03 native crate polish and West guides — October 2, 2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'contact-07.request.json').read_text());assert sha(S/'contact-07.prompt.txt')==r['promptSha256'] and sha(S/'contact-07.raw.png')==r['rawSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
reports=[]
for n,review,count in [('02','actor-review-v1',102),('03','actor-review-v2',115)]:
    audit=ROOT/f'output/marsh-animation-audit/east-carry-actor-{n}-2026-10-02';report=json.loads((audit/'report.json').read_text());reports.append(report)
    assert report['checks']==523 and report['failures']==0 and len(report['captures'])==6 and len(report['samples'])==95 and report['actorRestores']==4 and report['wraps']==2
    assert (audit/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (audit/'native.log').read_text()
    for name,total in [('inputs',count),('owner',2931)]:
        before=json.loads((audit/f'{name}-before.json').read_text());assert before==json.loads((audit/f'{name}-after.json').read_text()) and len(before)==total
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allSixViewsInspected':True,'viewCount':6,'pairedBoardsInspected':2,'findings':'Selected idle plus four opposite cargo poses and final paused carry seen as exact source/native pairs. Body/head and same single-latch crate projection closer in corrected03; narrower far-contact crate in02 prompted full-source07 correction. Remaining grade/registration/continuous contact and family joins provisional.','limits':'Held crops/illustrative180ms poses, not realtime film, full scene or complete pickup/carry/unload. No full RunSave or TitleContinue evidence in this fixture.'}
    (BASE/review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    subprocess.run([sys.executable,str(ROOT/f'tools/publish_marsh_east_carry{n}_actor.py')],check=True,stdout=subprocess.DEVNULL)
assert reports[0]['samples']==reports[1]['samples']
assert [(c['foot'],c['position']) for c in reports[0]['captures']]==[(c['foot'],c['position']) for c in reports[1]['captures']]
for i in [0,1,3]:assert sha(BASE/f'candidate-02/{i:03}.png')==sha(BASE/f'candidate-03/{i:03}.png')
a=json.loads((BASE/'candidate-03/assembly.json').read_text());a.update(visualReviewed=True,nativeReviewed=True,normalAdmission=False,findings='Whole far-contact07 preserves opposite thighs and enlarges inset-panel/single-right-latch crate toward far05. Four-pose cargo concept/projection now closer; three other source PNGs unchanged. Native03 six pairs seen and523 checks pass. Head/body/camera/grade and physical moving contact/full-family joins remain provisional.',remaining='West carry source/native, carry-turn and held joins, independent normal saves/visible Continues, full-set cross-reference consistency/polish.');(BASE/'candidate-03/assembly.json').write_text(json.dumps(a,indent=2)+'\n')
W=ROOT/'character/marsh-west-carry-material-v1/sources';g=json.loads((W/'guide-provenance.json').read_text());req=json.loads((W/'carry-01.request.json').read_text());assert req['status']=='frozen before generation';assert sha(W/'carry-01.prompt.txt')==req['promptSha256']
for q in g['primarySourceFrames']+g['guideSourceFrames']+g['guideArtifacts']+[g['originalOwnMaster']]+req['orderedReferences']+req['guideToolDependencies']:assert sha(ROOT/q['path'])==q['sha256']
(W/'guide-review.json').write_text(json.dumps({'allEightCompleteGuideFramesInspected':True,'singleIdleAndOppositeGuideInspected':True,'originalOwnMasterInspected':True,'normalAdmission':False,'fullGoalComplete':False,'selectedIdleOccupiedSize':[31,147],'findings':'Own West bare visible temple, implant hidden on far side, genuine ankle hardware and fitted31x147 selected adult side body. Old crate/body/head remain motion/cargo-only; old combined extents86x147/61x149/67x148/66x148 are not anatomical calibration. Four figures plus neutral frozen with own selected idle,opposite whole stances,old cargo guide,own original. No mirrored East artwork.','generationStarted':False},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
lesson='''

## Marsh East carry03 native crate polish and West guides — October 2, 2026

East carry02 actual normal factory/controller/main/grid/player workshop_carry
fixture completed:523checks,6 exact held source/native views,95 controlled20ms
samples,four actor/player restores+pause holds,two wraps,0failures/engine errors,
exit0.102 bounded inputs stable DURING interval;2931 owner nonlog files unchanged
under scratch APPDATA. All six pairs/two boards seen. Native view confirms narrower
far-contact crate despite concept/latch consistency. Source/native parity proves
what the renderer uses; it does not prove art coherence. Correct full source next.

Contact07 exec-a022b5f8-98d9-4aef-a929-f145d7770f79 frozen exact prompt/four
ordered refs:whole contact04 stance,whole far05 cargo,selected idle PRIMARY,own
original East. Raw retained with ID/original/SHA; two complete alpha128 figures,
one neutral147 scale .1781818181818182:92x146,ruler38x147. Opposite thighs/front
far flat boot preserved; inset-panel/single-right-latch crate widened toward far05.
Raw/packed/neutral/used whole guides inspected. No mirror,patch,recolour,per-pose
or crate-width body fitting. Whole source correction keeps connected arm support.
Candidate03 replaces only complete slot2;other three PNGs exact02 unchanged,
four decoded APNG frames exact.184p92/172H148/four180ms/stride.0827027027027027.
Body/camera/grade and rigid-crate projection closer, remaining registration/physical
moving contact/full family joins provisional; not full-set acceptance.

East carry03 identical actual workshop fixture also523/6/95/4restores/2wraps/
0fail/engine0/exit0;115 bounded inputs stable DURING interval,2931 owner nonlog
files unchanged.95 full sample dictionaries and six capture root/position pairs
exact02. All six new source/native pairs/two boards seen. Both actual normal
Marsh.move rate46,run excluded,positiveX168clear furnished route. Dedicated site
fixture free room only;global normal free-build/failure flags false,not paid-build
proof. Samples cover87.4world units,not complete pickup/carry/unload or arrival.
Held180ms APNG illustration not continuous film/contact or full-scene acceptance.
No full RunSave/visible TitleContinue or carry-turn/held joins proven here.

Publication03 initially reused actor-review-v1 directory. AFTER its native interval,
publisher output renamed actor-review-v2 and both reviews republished from retained
separate02/03 audits. Runtime,source PNGs,fixtures/native interval inputs unchanged;
115 freeze proves interval equality,not all current publication helper hashes.
Give each review revision a distinct directory to retain earlier visual evidence.

West own guides frozen/inspected:eight unchanged complete selected idle0/1,walk0/3
and old carry0..3;single selected idle31x147,own bare visible temple/far-side implant,
authentic ankle hardware/elevated West camera. Old cargo combined extents86x147/
61x149/67x148/66x148 not body calibration. Own original/selected/whole opposite
stance/cargo guides seen. Frozen carry01 asks four alternating supported cargo
poses+neutral147,one consistent single-LEFT-latch own crate. Generation NOT STARTED.
No West native/source acceptance. Never mirror East asymmetry into West.

East03 staged/unselected,normal catalog unchanged. Full goal active/incomplete.
Next West frozen whole cargo generation/source review,then its actual own native
carry;carry-turn/held joins,independent normal full saves/visible Continues,full
cross-family consistency/polish remain. No live process or job handle.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(MARKER in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_EAST_CARRY03_NATIVE_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh East carry03 / West guides

## Objective and acceptance
Full master-matched animation set and cross-family consistency/polish active and
incomplete. East carry03 staged and reviewed on actual workshop-carry actor;
unselected. West own reference guides reviewed and carry01 frozen,not generated.
No live process/tool handle; native sessions60068/88781 terminal exit0.

## Decisions and constraints
Primary selected adult bodies/camera/grade; complete authored poses and one neutral
calibration per source,whole translations only,no clipping/mirror/limb/crate patch.
East visible implant;West bare visible temple/implant hidden far side. Cargo width
is not body calibration. Runtime cadence/184p92/172H148 unchanged. Every Godot test
isolated scratch APPDATA,owner fingerprints before/after. No gameplay/catalog edit.

## Current state and changed files
East02/03 native fixture/preparer/publisher/fingerprint tools and paired UIDs;
contact07 prepare/build raw/prompt/ordered refs/provenance/packed figure+ruler;
candidate03 assembler/four unchanged complete source PNGs,manifest/APNG/comparison.
actor-review-v1 retains02;actor-review-v2 retains03;both assessments/verification.
West guide/request preparers,sources/whole guide provenance/frozen carry01 prompt.
Pipeline,bible,current status,master-repair maintained/installed mirrors appended.

## Verification and scope
Each East actual fixture523checks,6 exact source/native pairs,95controlled20ms
samples,4 actor/player restores+pause holds,2wraps,0failures/engine errors,exit0.
102 bounded inputs02 and115inputs03 equal during each interval;2931 owner nonlog
files unchanged each.95 full sample dictionaries and6 capture roots equal across
both. All12 held pairs/fourboards inspected. Contact07 scale.1781818181818182,
92x146/ruler38x147,opposite leg anatomy kept,crate enlarged. Three other source
PNGs unchanged from02,APNG4exact. Whole source and cycle comparisons seen.
Publication03 review directory corrected after native terminal; native freeze
proves interval equality,not current publisher helper hash. Both reviews retained.
Held views are not continuous contact/full scene,normal full save/TitleContinue,
complete pickup/carry/unload or turn/held join acceptance. East03 remains staged.

## Remaining work and next action
Generate West carry01 exact frozen prompt/four ordered own refs from sources
request JSON;all refs inspected. Preserve raw ID/original/SHA immediately;inspect
opposite leg support,crate projection,adult body/camera/grade before packing one
neutral147 scale. No West generation started. Stage own negative-X native route
after coherent complete cycle. Then carry-turn/held joins,independent normal
full saves/visible TitleContinue and full-set consistency/polish. Keep goal active.
''',encoding='utf-8')
print('Recorded two actual East carry intervals and whole-source crate correction; West request frozen; skill mirrors equal; goal incomplete.')
