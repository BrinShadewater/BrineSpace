from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;root=P.parents[1]
e=json.loads((P/'continue-evidence.json').read_text());v=json.loads((P/'continue-validation.json').read_text())
assert e['failures']==0 and v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
cases=[]
for case in range(6):
    rows=[r for r in e['records'] if r['case']==case and r['resumed']]
    assert rows and any(r['stage']=='observation_rise' for r in rows)
    cases.append({'case':case,'mode':rows[0]['mode'],'restoredStage':rows[0]['stage'],'tabletExitPose':rows[0]['tabletExitPose'],'completedRise':True})
block=f'''## James seated tablet fresh-scene Continue — October 1, 2026

Six actual disk checkpoints now restore into fresh main scenes: partial draw,
held reading and interrupted held-to-stow, bare/helmet, reachable q0 South sofa.
Normal core release roster retained; no free-building/disabled-failure flags.
{e['checks']}native checks/zero failures, {e['captures']}source-change captures. Actual save
capture/problem/write/read/restore_staged, exact actor snapshot/playback/visual
clock/source RGBA and paused stability, then normal60Hz-stepped NPC update through
stow/rise. Interrupted exit restores its retained held source/tablet_exit_pose;
texture slot -1 still denotes a valid held texture outside the exit pool.
Original six-case run timed out during its final case with no reported failures;
archived without acceptance. Two bounded three-case gear lanes completed instead,
with separate scratch profiles/terminal reports; combined counts below retain
their full declared scope and do not treat timeout as a passing result.
Engine0/no timeout/scratch APPDATA/strict owner unchangedtrue. No runtime/art/scale/
grade change required. Six before/after/first-five restored source changes/final-six
rise pose boards reviewed. GIFs reconstruct source intervals; not continuous
60Hz video, autonomous travel, title-button navigation or all-rotation/cardinal
acceptance. Existing12-case power-loss evidence remains separate.

Lesson: snapshot admission cannot certify persistence. Write the real checkpoint,
read it into a new main scene, retarget run_save_path to scratch, compare the
actual rendered source including dynamic retained held frames, and resume the
controller through the next activity boundary. Preserve room contact separately
from source pixels and saved playback clocks. Full James animation/master/art/
perspective/material consistency goal active; other cardinal/furniture/gear/travel
contexts and cross-family polish/owner acceptance remain open. Handoff:
character/james-seated-read-phases-v1/HANDOFF.md.

'''
def atomic(p,data):
    tmp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data);os.replace(tmp,p)
paths=[root/'docs/CURRENT_STATUS.md',root/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(paths):
    original=p.read_bytes();payload=block.encode('utf8');assert payload not in original;atomic(p,payload+original if i==0 else original+b'\n\n'+payload)
handoff=P/'HANDOFF.md';atomic(handoff,handoff.read_bytes()+b'\n\n'+block.encode('utf8'))
selection=P/'selection.json';s=json.loads(selection.read_text())
s['powerLossInterruptions']={'cases':12,'checks':1866,'evidence':'interrupt-evidence.json','visualReview':'All12 native interruption pose boards reviewed; current source RGBA preserved.'}
s['freshSceneContinue']={'cases':cases,'checks':e['checks'],'captures':e['captures'],'evidence':'continue-evidence.json','profileGuard':v,'visualReview':'Six before/after/first-five restored source-change/final-six rise pose boards reviewed. Owner pending.'}
s['remaining']=['Other cardinal/furniture/rotation/gear/travel controller contexts','Chronological master/perspective/material and cross-family polish','Full library owner acceptance and requested export checks']
atomic(selection,(json.dumps(s,indent=2)+'\n').encode('utf8'))
print(json.dumps({'checks':e['checks'],'captures':e['captures'],'freshSceneCases':cases,'guidesUpdated':5}))
