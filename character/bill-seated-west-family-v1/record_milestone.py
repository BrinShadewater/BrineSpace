from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
T=P.parent/'bill-reading-entry-west-v1'
native=ROOT/'output/bill-seated-west-selected-renderer-v1'
entry=ROOT/'output/bill-reading-entry-west-candidate-native-v1'
reports=[json.loads((folder/'validation.json').read_text()) for folder in [native,entry]]
assert all(r['passed'] and not r['realProfileChanges'] for r in reports)
for folder in [P,T]:assert json.loads((folder/'verification.json').read_text())['passed']
note='''
Bill west seated family selected — September 30, 2026.
12gear states/72refs: sit/rise,breathing/reading,tablet entry/exit. New tablet
source exec-742f8633-06e2-498e-af49-af5245df6192 has four independent interiors,
exact paired seated/reading joins,fixed ruler[.235,.276],density1.24 and native
west helmet/protected body.40package/103native entry checks PASS11.65sec.
Selected family90package/320native checks PASS11.13sec without injection:all72
pixels,shared plane,dry poses,finite holds and eight paired exact joins.
Full-size/native82 source and normal-family boards reviewed.2,914 owner non-log
profile files unchanged in both scratch runs. Normal loader/registry changed;
actor behavior unchanged. All four seated source families are now selected.
Live east/west furniture/activity,NPC interruption/checkpoint support remain
unproved;reading snapshots retain north/south restriction. Next audit remaining
selected life/rest coverage and compare cardinal seated material/proportion/
pacing together,then complete remaining families/actual journeys/full-set polish.
Lesson: keep exact pose joins and source rulers while separating source coverage,
normal renderer selection and real activity/restore evidence. Full goal active.
Handoff: character/bill-seated-west-family-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill west seated renderer selection — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
common=[ROOT/'scripts/grid_canvas.gd',ROOT/'character/ACTIVE_ASSETS.json']
for folder,report,checks,out,scope in [(T,reports[1],{'package':40,'native':103},entry,'candidate source/player;selected normal family evidence is separate'),(P,reports[0],{'package':90,'native':320},native,'normal renderer/source selection;no actor/furniture/restore proof')]:
    files=[folder/'bare-manifest.json',folder/'helmet-manifest.json',folder/'build.py',folder/'verification.json',folder/'FAMILY_HANDOFF.md',out/'validation.json',out/'loaded-water-carry.png']+common
    if folder==T:files += [T/'sources/entry-v1.png',T/'sources/prompt-entry.txt',T/'source-rulers.json',T/'registration.json',ROOT/'tests/test_bill_reading_entry_west_candidates.gd']
    else:files += [P/'source-bindings.json',ROOT/'tests/test_bill_seated_west_selected_renderer.gd']
    (folder/('candidate-evidence.json' if folder==T else 'selected-renderer-evidence.json')).write_text(json.dumps({'scope':scope,'checks':checks,'native':report,'sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded west tablet sources and selected renderer milestone')
