from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-lifecycle-v1'
result=json.loads((O/'validation.json').read_text());assert result['passed']
records=json.loads((O/'records.json').read_text())
masters={'bare':R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png','helmet':R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'}
for gear in masters:
    master=Image.open(masters[gear]).convert('RGBA')
    start=Image.open(O/f'{gear}-cycle-00-source.png').convert('RGBA')
    end=Image.open(O/f'{gear}-cycle-15-source.png').convert('RGBA')
    assert start.crop((36,52,220,236)).tobytes()==master.tobytes()
    assert end.tobytes()==master.tobytes()
note='''## Veld master bunk controller cycles and service interruptions — October 1, 2026

character/veld-bunk-body-master-v1 actual controller audit completes two14.12s
lower/rest/rise cycles from prescribed clear station, both gears, through ordinary
actor.update(.04).32actual service losses cover power removal/suspension at seven
entry interiors and held sleep. Interrupted rise starts from exact displayed
whole source and bed offset, keeps physical foot, remains snapshot-admissible
through updates and completes. No phase timer writes during resumed cycles or
returns. Native3395checks0failures/64.26s engine0;48actual room captures and48exact
source captures (32complete-cycle pose changes,16interruption before/after views).
All2931owner non-log files unchanged in scratch APPDATA. No production/artwork
or normal selection edits. Two native cycle boards and interruption board viewed.
Independent exact master entry/terminal RGBA joins confirmed in both gears.

Earlier61.85s passing interval retained. Small board crop initially misread as
bare-headed terminal; full archived/current native captures and independent
pixel comparison both prove exact equipped master, no helmet removal. Diagnostic
rerun adds actor state/equipment/action and whole RGBA hashes to all708ordinary
cycle samples. Initial2.99s diagnostic parse failure fixed by instance hashing;
logs/profile results retained. No invented production bug or artwork repair.
After-run dependency bindings only, not frozen-interval evidence. Original test
resource_path entries were empty for ImageTextures; diagnostic uses content hashes.

Scope: actual controller activity/service-return update, prescribed station in
default rotation0, fixture-only candidate library. Separate prior eight fresh
Continues verify saved paused poses; this audit is not future motion after Continue,
natural chooser/approach, room removal/fire/gear interruption or all-rotation
lifecycle proof. Owner acceptance and normal installation remain open.
Lesson: inspect full native captures and actual loaded RGBA before diagnosing
design drift from small crops. ImageTexture resource_path is not frame provenance;
record pixel content hashes and actual actor gear/state. Source-clock, controller
progress, room contact and checkpoint continuation remain separate requirements.
Next natural approach/resumed Continue and remaining interruptions/partial life
death sources, then normal-loader integration and full-set/master polish.
Full Veld objective active. Handoff/evidence/review in this candidate folder.
'''
for i,p in enumerate([R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]):
    old=p.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:p.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
h=P/'HANDOFF.md';old=h.read_text()
if '## Controller lifecycle follow-up' not in old:h.write_text(old+'\n## Controller lifecycle follow-up\n\n'+note.split('\n\n',1)[1])
files=[R/'tests/test_veld_bunk_body_lifecycle.gd',R/'tests/test_veld_bunk_body_lifecycle.gd.uid',R/'tools/run_veld_bunk_body_lifecycle.py',O/'native.log',O/'validation.json',O/'records.json']+list((P/'frames').rglob('*.png'))+[P/n for n in ['bare-manifest.json','helmet-manifest.json','native-cycle-bare.png','native-cycle-helmet.png','native-service-interruptions.png']]+list(masters.values())
(P/'lifecycle-evidence.json').write_text(json.dumps({'validation':result,'checks':3395,'serviceInterruptions':32,'controllerCycles':2,'cycleSamples':sum(len(r.get('cycle',[])) for r in records),'roomCaptures':48,'sourceCaptures':48,'exactMasterEntryAndTerminal':True,'visualReview':'both cycle boards and service board plus full equipped terminal inspected','normalSelection':False,'bindingsAfterRun':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
html=P/'index.html';old=html.read_text();link='<p><a href="native-cycle-bare.png">Actual complete cycle</a> · <a href="native-cycle-helmet.png">Actual helmet cycle</a> · <a href="native-service-interruptions.png">Power loss and suspension</a></p>'
if link not in old:html.write_text(old+'\n'+link)
print('Exact paired master joins confirmed; lifecycle evidence/handoff and five lesson records saved')
