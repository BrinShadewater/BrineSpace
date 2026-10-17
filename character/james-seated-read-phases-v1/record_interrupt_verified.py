from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;root=P.parents[1]
e=json.loads((P/'interrupt-evidence.json').read_text());v=json.loads((P/'interrupt-validation.json').read_text())
assert e['failures']==0 and v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
cases=[]
for case in range(12):
    rows=[r for r in e['records'] if r['case']==case and r['interrupted']]
    assert rows and rows[0]['beforeHash']==rows[0]['afterHash']
    assert any(r['stage']=='observation_read_exit' for r in rows) and any(r['stage']=='observation_rise' for r in rows)
    cases.append({'case':case,'mode':rows[0]['mode'],'triggerStage':rows[0]['triggerStage'],'triggerElapsed':rows[0]['triggerElapsed'],'sourcePreserved':True})
text=f'''## James seated tablet power-loss interruptions — October 1, 2026

Selected phase controller now exercised through twelve actual power-loss cases:
four partial-draw offsets (.03/.13/.29/.43s), two held offsets (.15/.75s), both
gears, reachable q0 South observation sofa. {e['checks']}native checks, zero failures,
{e['captures']}source-change captures. Current source RGBA hashes match exactly across
every interruption; real service loss clears goal, stows before rise, preserves
physical foot and earns no completion reward. Pre-interruption/interrupted snapshot
admission passes. Engine0/no timeout/scratch APPDATA/strict owner unchangedtrue.
All twelve native interruption boards reviewed; interval GIFs reconstruct source
changes, not continuous60Hz footage. No runtime/art/scale/grade changes required.

Earlier fixture failure retained under interrupt-fixture-before-clock-correction:
held reading uses its held timer rather than action_elapsed() (which returns -1),
and need growth must not be mistaken for a completion reward. Corrected fixture
records actual source hashes and tablet_exit_pose, including retained held texture
outside the exit pool. Lesson: compare rendered pixels across state changes,
rather than relying on a texture's slot number. Snapshot admission alone does not
prove fresh disk Continue. Fresh Continue, other contexts/rotations/cardinals and
full James consistency/owner acceptance remain open. Handoff:
character/james-seated-read-phases-v1/HANDOFF.md.

'''
def atomic(path,data):
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data);os.replace(tmp,path)
paths=[root/'docs/CURRENT_STATUS.md',root/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(paths):
    original=p.read_bytes();block=text.encode('utf8');assert block not in original
    atomic(p,block+original if i==0 else original+b'\n\n'+block)
handoff=P/'HANDOFF.md';atomic(handoff,handoff.read_bytes()+b'\n\n'+text.encode('utf8'))
(P/'interrupt-review-evidence.json').write_text(json.dumps({'checks':e['checks'],'captures':e['captures'],'cases':cases,'visualReview':'All12 native interruption boards reviewed by Codex; fixed furniture contact and draw/stow/rise ordering. Owner review pending.','limitations':'No fresh disk Continue, autonomous travel, other room rotations or East/West actual furniture contexts.'},indent=2))
print(json.dumps({'checks':e['checks'],'captures':e['captures'],'cases':len(cases),'guidesUpdated':5}))
