from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-continue-v1'
result=json.loads((O/'validation.json').read_text());assert result['passed']
log=(O/'native.log').read_text();count=int(re.search(r'VELD BUNK BODY CONTINUE: (\d+) checks,0 failures',log)[1])
records=json.loads((O/'records.json').read_text());assert len(records)==8
note=f'''## Veld master bunk fresh-scene Continue — October 1, 2026

character/veld-bunk-body-master-v1 now has actual RunSave disk write/read and
eight fresh main-scene staged Continues: lowering, held, rising and supported
death, both gears. Prescribed interior poses/default habitation rotation0 and
candidate manifests injected in fresh fixture only. Exact whole RGBA source,
physical foot, stage/timer/gear, saved bunk/death recipe, native room position/depth
and paused visual clock preserved. Native{count}checks0failures/{result['seconds']}s,
engine0,16native before/after room captures plus16exact sources. All2931real
non-log owner files unchanged with scratch APPDATA. No artwork or production
script changes; normal selection remains unchanged. Native/source board reviewed.

Initial127.22s interval retained: all3bare live phases passed; held death ended
sole-named-survivor run and RunSave correctly rejected a new checkpoint. Revised
fixture supplies existing Bill ward as paid/restored (8Metal spent; repair work
is prescribed), then actual CryoRecovery wake, navigation landing and roster
logic creates survivor. No failure flags, run revival or invented roster. Real
baseline restores reset each gear/death case. This proves surviving-loop corpse
Continue, not saving after last-character expedition loss. Paused pose/source
verification does not establish future resumed motion, natural chooser/approach,
all-rotation Continue or owner acceptance. Earlier1306native all4rotation source
proof retains its original prescribed-clock/actor-file scope. After-run hashes
recorded; dependencies were not frozen across launch.

Lesson: keep checkpoint eligibility and mortality rules real. A last-character
death ends the loop; use actual recovered survivor and valid complete roster for
corpse checkpoint coverage. Do not force running=true or weaken save validation.
Next actual resumed activity, service interruptions, natural approach and partial
life death sources, then normal-loader integration/full-family/master polish.
Full Veld objective active/incomplete. Evidence: native-fresh-continue.png,
continue-evidence.json and HANDOFF.md in character/veld-bunk-body-master-v1.
'''
for i,p in enumerate([R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]):
    old=p.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:p.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff=P/'HANDOFF.md';old=handoff.read_text();addition='\n## Fresh-scene Continue follow-up — October 1\n\n'+note.split('\n\n',1)[1]
if '## Fresh-scene Continue follow-up' not in old:handoff.write_text(old+addition)
files=[R/'tests/test_veld_bunk_body_continue.gd',R/'tests/test_veld_bunk_body_continue.gd.uid',R/'tools/run_veld_bunk_body_continue.py',O/'native.log',O/'validation.json',O/'records.json',P/'native-fresh-continue.png',P/'bare-manifest.json',P/'helmet-manifest.json']+list((P/'frames').rglob('*.png'))
(P/'continue-evidence.json').write_text(json.dumps({'validation':result,'checks':count,'freshSceneRestores':8,'visualReview':'16 native/source before-after presentations reviewed; owner acceptance pending','scope':'fixture-only candidate paused checkpoints; not future resumed motion/natural approach/standard title selection','bindingsAfterRun':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
html=P/'index.html';old=html.read_text();link='<p><a href="native-fresh-continue.png">Fresh save/Continue — both gear versions and all four phases</a></p>'
if link not in old:html.write_text(old+'\n'+link)
print(f'{count}native checks; fresh Continue evidence/handoff and five lesson records saved')
