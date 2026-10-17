from pathlib import Path
import json,re,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-emergency-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text())
fires=[r for r in records if 'samples' in r];cleared=[r for r in records if '-extinguished-' in r['name']]
assert len(fires)==22 and len(cleared)==6 and all(r['routePoints']>0 and r['movement']>0 and r['escapedCell']!='(21, 20)' for r in fires)
checks=int(re.search(r'EMERGENCY: (\d+) checks,0 failures',(O/'native.log').read_text()).group(1))
captures=len(list(O.glob('*-room.png')))
note=f'''## Veld supported bunk fire rise and refuge — October 1, 2026

Actual fire audit exposed immediate supported-to-walk snap. scripts/veld_npc.gd
now provides advance_fire_rise for its marked specialised dry bunk only;
scripts/fire_safety.gd invokes the optional actor hook before clearing stage.
Exact current lowering/held/rising pose starts a finite reverse rise, preserving
navigation foot/contact and standing master endpoint before ordinary refuge
routing. Remaining rise clock survives an extinguished fire; alarm clears only
after standing. Ordinary advance_needs still runs before fire dispatch. Actors
without the hook and unmarked Veld states retain existing fire behavior.
No new pose/grade/art/room/navigation data or normal manifest selection changes.

Staged paired body test:22actual fire cases (seven lower interiors,held,three
rise interiors x two gears),all22route and physically reach non-burning core
through original connected habitat door. Six fire-field clears mid-rise retain
source/contact/remaining clock and finish with needs advancing.22public direct
gear swaps select corresponding same supported pose/clock/position/depth;
actual locker-fitting action rejects during bunk stage. Direct setter evidence
does not certify an animated fitting action. Two actual crew-hab scrap attempts
are correctly blocked by resident-hab policy, preserving actor/room/Metal;
do not bypass removal policy to invent an animation emergency.

Final{checks}checks0failures/{report['seconds']}s engine0;45shared Room fire checks
0failures/headless engine0. {captures}actual native room captures and exact sources;
six fire-rise/refuge boards and six gear/extinguished boards inspected, same
source ruler/pivots/master entry and finish. Existing fire overlay obscures lying
body within flame; source board separately shows retained anatomy/materials.
Native evidence is not unobscured continuous whole-world simulation. Prescribed
phase/site/fire values with ordinary actor updates; not naturally ignited fire,
sprinkler-driven extinguishing, fresh emergency Continue or every room rotation.
Staged paired body remains unselected; normal actor fire hook is installed.

All{report['realProfileFileCount']}owner non-log files unchanged in scratch APPDATA.
{report['targetedInputCount']}targeted actor/fire/scrap/life/test/paired source and
manifest inputs identical before/after final interval; broader dependencies not
frozen. Initial45.06s/493checks110failures retained (actual snap); fixed51.24s/
2679pass retained before fuller evacuation/cleared-alarm proof. Latest evidence:
character/veld-bunk-body-master-v1/emergency-evidence.json. Paired UID test and
isolated runner: test_veld_bunk_body_emergency.gd/run_veld_bunk_body_emergency.py.

Lesson: emergency routing must account for supported anatomy, not just clear
activity flags. Advance the actor's authored finite rise while ordinary needs
continue, then use actual refuge routing; prove physical arrival, not merely a
nonempty path. Preserve remaining clock if hazard clears during the rise.
Separate direct appearance setters, fitting actions and real removal policy.
Remaining fresh emergency Continue/whole-world hazard cadence, partial/seated
death source families, broader rotation/silhouette review, normal paired body
selection and full-family/master polish. Full Veld goal active/incomplete.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
    old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff=P/'HANDOFF.md';old=handoff.read_text()
old=old.replace('fifth covers future fresh Continue.', 'fifth covers future fresh Continue; sixth covers supported fire rise/gear/scrap.')
old=old.replace('No room geometry, source artwork, clocks, grade, physical contact or normal', 'No room geometry, source artwork, grade, physical contact or normal')
old=old.replace('288.0s clean interval; broader dependencies not frozen. Eight boards reviewed.', f'288.0s clean interval; broader dependencies not frozen. Eight boards reviewed.\nFire: {checks}native/45shared checks0fail;22finite rises physically reach safe\ncore,6cleared alarms keep remaining rise,22direct gear swaps,2blocked scraps.\n{captures}native/source views;12boards reviewed;{report["seconds"]}s engine0, owner unchanged,\n28targeted inputs frozen. Veld-only fire rise hook before shared stage clearing;\nnormal paired art selection unchanged. Original snap and intermediate pass retained.')
old=old.replace('Verify remaining interrupts (room removal,\nfire/gear) and partial/seated death sources;', 'Verify fresh emergency Continue/whole-world hazard cadence and author partial/\nseated death sources;')
handoff.write_text(old)
files=[R/p for p in ['scripts/veld_npc.gd','scripts/veld_npc.gd.uid','scripts/fire_safety.gd','scripts/fire_safety.gd.uid','tests/test_veld_bunk_body_emergency.gd','tests/test_veld_bunk_body_emergency.gd.uid','tools/run_veld_bunk_body_emergency.py']]+[O/n for n in ['native.log','shared-fire-regression.log','validation.json','records.json','inputs-before.json','inputs-after.json']]+list(P.glob('native-emergency-*.png'))
(P/'emergency-evidence.json').write_text(json.dumps({'validation':report,'checks':checks,'sharedFireChecks':45,'fireCases':22,'physicalSafeRefugeArrivals':22,'clearedFireCases':6,'directGearSwapCases':22,'blockedScraps':2,'roomCaptures':captures,'sourceCaptures':captures,'visualReview':'12native/source boards inspected; flame occludes lying body so source view is separate','normalManifestSelection':False,'productionHook':'Veld marked dry bunk finite rise before fire route','bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
page=P/'emergency-review.html'
page.write_text('<meta charset="utf-8"><title>Veld bunk emergency return</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}a{color:#8cc6e7}img{max-width:100%}</style><h1>Veld — bunk emergency return</h1><p>Original supported pose rises to the standing master, then follows the actual door route to refuge. Playback below uses source clocks at one-third speed. Flames can obscure the resting body in the room captures.</p>'+''.join(f'<h2>{gear} / {phase}</h2><img src="emergency-{gear}-{phase}.gif"><p><a href="native-emergency-{gear}-{phase}.png">Actual room sequence and refuge</a> · <a href="native-emergency-contexts-{gear}-{phase}.png">Gear and cleared-fire joins</a></p>' for gear in ['bare','helmet'] for phase in ['lower-0.81','held','rise-0.9']))
html=P/'index.html';old=html.read_text();link='<p><a href="emergency-review.html">Bunk emergency rise and actual refuge</a></p>'
if link not in old:html.write_text(old+'\n'+link)
print(f'{checks}native+45shared checks;{captures}actual/source captures; five lesson records and concise handoff saved')
