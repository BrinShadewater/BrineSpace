"""Record source-workspace Salvage evidence and the verified cleanup lesson."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
result=json.loads((root/'output/salvage-owner-repair-2026-09-12/station-pause/result.json').read_text())
assert result['failures']==0 and len(result['samples'])==4
def append(path,text):
    data=path.read_bytes(); addition=text.encode()
    if addition not in data:path.write_bytes(data+addition)
append(root/'docs/SALVAGE_OWNER_ASSET_REPAIR_2026-09-12.md','''

Verified source checkpoint: fresh `alpha-native` q0 confirms the magenta fringe
is gone; four-direction furnishing state contact reviewed for contained powered
lamp and inward access. Direct/retained RGB match, powered clock samples match,
off/on differ, and all six existing-canvas transition rows match direct references.
Actual station pause fixture passes all four orientations with operating state,
advancing running clock and frozen paused clock/pixels (`station-pause/result.json`).
Selected card refreshed from cleaned native q0. Tests: 176 layouts previously
passed; 20 side variants and 47 card identities pass `20260912-212525-headless`.
No export or owner acceptance. Older library alternatives remain historical;
this checkpoint covers the selected live bench/tote and four default layouts.
Next owner asset queue item: Galley, including large mess-hall tables.
''')
lesson='''

Salvage overhead conversion lesson (September 12): chroma-key edge pixels can be
much darker than the flat background. Native-scale review caught a magenta seam
missed by absolute brightness thresholds. For this source, red and blue dominance
over green removed the fringe while preserving neutral metal. Preserve raw art,
record the source-specific rule, and verify the cleaned result against the actual
room floor. Rotate source art, prop bounds and source-local effect anchors together;
remove obsolete fixed-camera layout overrides only for the affected prop fields.
'''
for path in [root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:append(path,lesson)
p=root/'assets/salvage-owner-v2/bench-review.json'
d=json.loads(p.read_text());d['stage']='selected live; native, state and station pause verified';d['evidence']='docs/SALVAGE_OWNER_ASSET_REPAIR_2026-09-12.md';p.write_text(json.dumps(d,indent=2)+'\n')
p=root/'docs/CURRENT_STATUS.md'
prefix=b'## Salvage owner asset repair verified - September 12, 2026\r\n\r\nOverhead bench and tote rotate through four default layouts. Native alpha, retained power transitions and actual station pause verified; selected card refreshed. See docs/SALVAGE_OWNER_ASSET_REPAIR_2026-09-12.md. Next: Galley and mess-hall tables. No export or owner acceptance.\r\n\r\n'
data=p.read_bytes()
if prefix not in data:p.write_bytes(prefix+data)
print('Recorded Salvage source checkpoint, card evidence and bible/skill lesson.')
