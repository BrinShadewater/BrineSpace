from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-settle-resume-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==4
log=(O/'native.log').read_text();checks=int(re.search(r'VELD BUNK SETTLE RESUME: (\d+) checks,0 failures',log).group(1))
captures=len(list(O.glob('*-room.png')))
note=f"""## Veld partial bunk death full Continue motion — October 1, 2026

New native full checkpoint test covers actual RoomFlooding.kill from two prescribed
supported partial poses (lowering progress .51 and rising progress .81), both
bare and sealed gear. Existing Bill pod is paid/restored by the fixture and wakes
through actual CryoRecovery/roster logic so ordinary run save eligibility remains
valid after Veld mortality. No forced run resurrection/free-build/failure bypass.
Candidate manifests injected in every fresh scene; normal art selection unchanged.

{checks} checks, zero failures/{report['seconds']}s, engine terminal zero/clean log.
Four actual disk writes/reads and fresh main-scene restore_staged operations;
150 uninterrupted plus 150 restored ordinary actor updates per case (20ms each,
three seconds), 1200 total future steps. Exact source pixel hashes, physical foot,
visual clock, furniture offset/depth, needs, stage/state/dead/gear compared every
step; actual room submission position/depth at each source change and terminal.
Paused initial source and exact incoming hold preserved; terminal corpse remains
at rest-local-foot on the mattress, living navigation cleared. {captures} native
room captures plus {captures} exact source images; four paired boards reviewed.
Twenty authored PNGs unchanged; no art/grade/scale/production edits this interval.

Owner {report['realProfileFileCount']} non-log files unchanged with scratch APPDATA.
{report['targetedInputCount']} targeted source/test/manifest/production inputs match
before/after; broader engine dependencies not frozen. Paired UID retained for
new test_veld_bunk_body_settle_resume.gd; runner, board builder and evidence saved.
Initial test-only endpoint check wrongly included the transient 16px lift; that
failed interval retained. Corrected to independent authored terminal rest anchor,
without altering production contact or pixels.

Lesson: same-clock actor restore does not establish future full Continue. Check
an actual eligible world checkpoint, fresh scene and future exact sources/contact
against uninterrupted playback, including the finite resting endpoint. Keep
prescribed pose/API mortality distinct from naturally triggered whole-world
hazards. Actor-only update with frozen main loop does not prove world hazard cadence,
new process/title Continue, all room rotations, early falls or owner acceptance.
Fire-rise fresh Continue, early bunk/lounged fall artwork, whole-world hazard cadence,
normal paired body installation and full-set master/polish remain open. Goal active.
"""
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
h=P/'HANDOFF.md';old=h.read_text()
old=old.replace('New partial recipe lacks full RunSave/fresh-scene/future restoration proof.','New partial recipe now has four full RunSave/fresh-scene/future restores.')
old=old.replace('Fresh full-save Continue for fire rise and partial death, then early bunk/lounged','Fresh full-save Continue for fire rise, then early bunk/lounged')
if f'{checks}native partial full Continue' not in old:old=old.replace('## Verification\n','## Verification\n'+f'{checks}native partial full Continue checks0fail/{report["seconds"]}s;4fresh disk restores,\n1200future actor steps;{captures}native/source captures,4paired boards reviewed.\nOwner{report["realProfileFileCount"]}files unchanged;{report["targetedInputCount"]}targeted inputs frozen.\n')
h.write_text(old)
files=[O/n for n in ['native.log','records.json','validation.json','inputs-before.json','inputs-after.json']]+[R/'tests/test_veld_bunk_body_settle_resume.gd',R/'tests/test_veld_bunk_body_settle_resume.gd.uid',R/'tools/run_veld_bunk_body_settle_resume.py']+list(P.glob('native-settle-resume-*.png'))+[P/'settle-resume-review.html',P/'review_settle_resume.py',P/'record_settle_resume.py',R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png',R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png']
(P/'settle-resume-evidence.json').write_text(json.dumps({'validation':report,'checks':checks,'fullDiskFreshSceneRestores':4,'futureActorSteps':1200,'nativeCaptures':captures,'sourceCaptures':captures,'normalArtSelection':False,'visualReview':'Four paired native/source future-motion boards','scope':'Prescribed rotation-zero phases, actual world kill API; actor-only future updates, not natural world hazard cadence','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
index=P/'index.html';link='<p><a href="settle-resume-review.html">Supported settling: full Continue motion check</a></p>'
old=index.read_text()
if link not in old:index.write_text(old+'\n'+link)
print(f'{checks}checks;{captures}captures;four fresh restores;five lesson records and handoff saved')
