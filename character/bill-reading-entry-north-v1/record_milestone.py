from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-reading-entry-north-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed']
note='''
Bill north tablet transitions staged — September 30, 2026.
Four gear states/24refs;43 package/103 native checks PASS11.03sec. Exact selected
north seat/new reading endpoint joins;480ms finite entry and reversed exit.
Fresh native82px paired board reviewed;all2,914 real non-logfiles unchanged.
Right-arm take-out corrected with generated local edit;only corrected cell1 is
selected. Edited alpha fringe inflated opaque contact despite timing/pixel checks
passing. Use near-opaque component segmentation, separately measured frozen source
ruler and the primary material curve; do not height-normalize individual poses.
Primary ruler[.214,.251], edit[.214,.2455]; boot translated after single resize.
Keep rear tablet in front of torso, naturally occluded; never switch the working
hand between stages just to expose the prop. Native visual review remains needed
after technical checks. Normal north family selection/controller/checkpoints remain
next;actual observation sofa retains south facing regardless of room rotation.
Handoff: character/bill-reading-entry-north-v1/HANDOFF.md. Full Bill goal active;
other life/rest families and full-set cross-reference/polish remain.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill north tablet transitions staged — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/entry-v1.png',P/'sources/entry-right-arm-v2.png',P/'sources/prompt-entry.txt',P/'sources/prompt-right-arm-v2.txt',P/'build.py',P/'correction.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'verification.json',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_reading_entry_north_candidates.gd']
data={'status':'staged_candidate','checks':{'package':43,'native':103},'native':report,'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'candidate source/player proof;normal north selection/controller/saved stages pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
print('Recorded north tablet transition source and alpha-contact lessons')
