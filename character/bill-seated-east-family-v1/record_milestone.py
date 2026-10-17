from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-seated-east-selected-renderer-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed']
note='''
Bill east seated family selected in normal renderer — September 30, 2026.
12gear states/72refs: sitting/rising, breathing/reading and tablet entry/exit.
90package/320native checks PASS10.49sec; all loaded pixels, shared plane,
finite timing/holds and paired exact stage joins verified without injection.
Fresh native82px full-family board reviewed.2,914 owner non-logfiles unchanged.
Loader/registry select whole literal res paths; actor behavior remains unchanged.
Reading snapshots still support north/south only. Normal renderer evidence does
not establish live east furniture/activity, interruption or checkpoint support.
Next audit real directional furniture consumers, complete west seated sources
and other life/rest coverage, then full-set material/proportion/motion polish.
Full goal active. Handoff: character/bill-seated-east-family-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east seated renderer selection — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json',P/'verification.json',P/'build.py',P/'FAMILY_HANDOFF.md',ROOT/'scripts/grid_canvas.gd',ROOT/'tests/test_bill_seated_east_selected_renderer.gd',native/'validation.json',native/'loaded-water-carry.png']
(P/'selected-renderer-evidence.json').write_text(json.dumps({'scope':'normal renderer/source selection;no actor/furniture proof','checks':{'package':90,'native':320},'native':report,'sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded east selected-renderer evidence and handoff')
