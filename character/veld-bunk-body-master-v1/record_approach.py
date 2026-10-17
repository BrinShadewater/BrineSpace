from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-approach-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==2
for r in records:
    assert r['entered'] and r['completed'] and r['finalWalkingCaptured']
    i=next(i for i,s in enumerate(r['samples']) if s['stage']=='life_lie')
    last=next(s for s in reversed(r['samples'][:i]) if s['state']=='walk')
    assert last['direction']=='east'
note=f'''## Veld natural bunk approach and East facing handoff — October 1, 2026

scripts/veld_npc.gd now overrides station_arrival_facing only for marked Veld
specialised bunk: East final clear approach matches exact East standing entry.
Other station types delegate inherited behavior. Shared chooser already checks
final segment facing, clearance, exact station contact and preserves route nodes.
No room geometry, source artwork, clocks, grade, physical contact or normal
manifest selection changes. New staged actual approach test uses normal selected
architect release position, high90fatigue and default room on vacant door-connected
side. Actual need chooser plans path; actor.update walks, dispatches activity,
completes full lower/rest/rise and reduces fatigue. No prescribed destination,
route, stage, station contact or activity timer during either case. Initial actor
snapshot resets released start for second equipment variant; gear/need fixture
is prescribed. Other crew/owner layouts and whole station simulation not certified.

Final9668checks0failures/{report['seconds']}s engine0, both gears;38actual native
room captures/38exact sources include final walking step and complete rest
sequence. Original ports/floor/service rules, valid snapshots and held activity
foot pass. Four paired native/source boards viewed using original184/p92,172
and256x272/p128,224 common ruler. Palette/hardware/stature retained at handoff.
All2931real non-log owner files unchanged with scratch APPDATA. After-run
bindings, not interval-frozen proof. No fresh Continue/future resumed proof in
this audit; previous169/3395checks retain separate scopes. Runner's historical
freshScreenshot field here measures fresh records.json; visual review is separate.

Initial42.63s failed interval retained: old rotation0 fixture below core has no
North door (crew_hab blueprint West/East/South); Veld correctly remains in core.
Move fixture to vacant original port-compatible side, never loosen navigation.
Next49.55s/9718pass showed actual final North walk then East bunk facing snap.
Seven-line actor hook fixes final-facing requirement;50.8s/9660pass retained.
Final49.56s adds actual pre-entry walking capture/guard and passes9668. Source
pixels unchanged. This is normal actor navigation behavior with staged bunk art,
not normal-loader installation/full-set acceptance or universal room clearance.

Lesson: source/contact and saved-pose checks do not prove accessible approach.
Check blueprint doors before testing a chooser. Match final travel facing to
the master entry using collision-checked route requirements; do not teleport,
rotate furniture or replace authored head designs to conceal a facing snap.
Next resumed fresh Continue, broader interrupts/partial life death sources and
normal-loader installation, then full-family/master polish. Full goal active.
Handoff/evidence: character/veld-bunk-body-master-v1.
'''
for i,p in enumerate([R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]):
    old=p.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:p.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
h=P/'HANDOFF.md';old=h.read_text()
if '## Natural approach follow-up' not in old:h.write_text(old+'\n## Natural approach follow-up\n\n'+note.split('\n\n',1)[1])
files=[R/'scripts/veld_npc.gd',R/'scripts/veld_npc.gd.uid',R/'tests/test_veld_bunk_body_approach.gd',R/'tests/test_veld_bunk_body_approach.gd.uid',R/'tools/run_veld_bunk_body_approach.py',O/'validation.json',O/'native.log',O/'records.json']+[P/n for n in ['native-approach-bare.png','native-approach-helmet.png','approach-source-bare.png','approach-source-helmet.png','bare-manifest.json','helmet-manifest.json']]+list((P/'frames').rglob('*.png'))
(P/'approach-evidence.json').write_text(json.dumps({'validation':report,'checks':9668,'actualChooserRouteActivityCases':2,'roomCaptures':38,'sourceCaptures':38,'actualFinalWalkingEast':True,'visualReview':'four paired native/source boards including final walking source reviewed','normalManifestSelection':False,'bindingsAfterRun':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
html=P/'index.html';old=html.read_text();link='<p><a href="native-approach-bare.png">Actual walk to the bunk and full rest</a> · <a href="native-approach-helmet.png">Helmet approach and rest</a> · <a href="approach-source-helmet.png">Same-size helmet handoff sources</a></p>'
if link not in old:html.write_text(old+'\n'+link)
print('Actual East walking handoff confirmed; approach evidence/handoff and five lesson records saved')
