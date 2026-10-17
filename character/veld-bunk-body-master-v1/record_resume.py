from pathlib import Path
import hashlib,json,re

P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-resume-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==8
checks=int(re.search(r'VELD BUNK BODY RESUME: (\d+) checks,0 failures', (O/'native.log').read_text()).group(1))
captures=len(list(O.glob('*-room.png')))
note=f'''## Veld bunk future motion after fresh Continue — October 1, 2026

Staged complete master-body pair now compares 64 ordinary actor.update(.02)
steps before saving against the same 1.28s after actual disk read and fresh main
scene RunSave.restore_staged. Eight prescribed phases: lower/held/rise/supported
death, both gears. Exact original actor/player/visual clock restored and checked
before writing; reference progress never becomes the checkpoint starting state.
Whole source RGBA hashes, physical foot, stage/state/gear, needs, timer, offset,
depth and clock match at every step. Native room position/depth matches at every
captured source change and terminal tick. Includes lower-to-rest and rise-to-idle
joins; supported death starts inside exact live entrance before finite release.
Rising fixture also re-enters sleep through the ordinary chooser; both traces
match, but this prescribed-needs station does not certify natural rest cadence.
This is deterministic actor-only advancement with scene processing paused,
not full station unpause or fresh-process/title Continue. Rotation0 prescribed
clear station remains separate from prior actual door-connected approach proof.

{checks}checks/0failures, engine0/{report['seconds']}s, {captures}actual room and
{captures}exact source captures. Eight paired future native/source boards visually
reviewed at original canvas/pivot; body, matte head/helmet, support and terminal
standing match.184standing source padded at36,52 into256x272 preserves the same
128,224pivot without resizing. {report['realProfileFileCount']}owner non-log files unchanged with
scratch APPDATA. {report['targetedInputCount']}targeted source/manifest/controller/test
file hashes identical before/after interval; other engine dependencies not frozen.
No production/art/normal manifest selection changes. New paired UID test and
runner: tests/test_veld_bunk_body_resume.gd/tools/run_veld_bunk_body_resume.py.
Evidence/review: character/veld-bunk-body-master-v1/resume-evidence.json.

Lesson: saved-pose equality cannot establish future motion. Rewind reference actor,
playback and visual clocks exactly before real disk write, then compare the same
ordinary updates across fresh restoration and actual rendered contact joins.
Keep whole-world cadence and source/timing/contact evidence distinct. Remaining
room-removal/fire/gear interruption contexts, partial/seated death sources,
broader rotations, normal paired body installation and full-family/master polish.
Full Veld goal active/incomplete; owner visual acceptance remains open.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
    old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff=P/'HANDOFF.md';old=handoff.read_text()
old=old.replace('fourth covers actual chooser/approach.', 'fourth covers actual chooser/approach; fifth covers future fresh Continue.')
old=old.replace('After-run bindings only; dependencies not frozen across launch.', f'New future Continue: {checks}checks,8fresh scenes,512resumed20ms updates;\n{captures}native/source presentations. Lower/rest and rise/standing joins retain exact\npixels/contact/clocks/needs. Targeted{report["targetedInputCount"]}inputs frozen across the\n{report["seconds"]}s clean interval; broader dependencies not frozen. Eight boards reviewed.')
old=old.replace('Verify future motion after fresh Continue, remaining interrupts (room removal,', 'Verify remaining interrupts (room removal,')
handoff.write_text(old)
files=[R/'tests/test_veld_bunk_body_resume.gd',R/'tests/test_veld_bunk_body_resume.gd.uid',R/'tools/run_veld_bunk_body_resume.py',O/'validation.json',O/'records.json',O/'native.log',O/'inputs-before.json',O/'inputs-after.json']+list(P.glob('native-resume-*.png'))
(P/'resume-evidence.json').write_text(json.dumps({'validation':report,'checks':checks,'freshSceneDiskCases':8,'futureStepsPerCase':64,'dt':.02,'referenceSteps':512,'resumedSteps':512,'roomCaptures':captures,'sourceCaptures':captures,'visualReview':'Eight paired future-motion native/source boards inspected','scope':'Actor-only ordinary updates, prescribed rotation0 station; not full-world/fresh-process/title Continue','normalManifestSelection':False,'files':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
html=P/'index.html';old=html.read_text();links='<p>Motion after loading: '+ ' · '.join(f'<a href="native-resume-{r["name"]}.png">{r["name"]}</a>' for r in records)+'</p>'
if links not in old:html.write_text(old+'\n'+links)
print(f'{checks}checks;{captures}native/source captures; five maintained lesson records and concise handoff updated')
