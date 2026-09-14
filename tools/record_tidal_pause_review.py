"""Record only a verified native pause result, preserving concurrent documents."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
result=json.loads((ROOT/'output/tidal-owner-repair-2026-09-12/station-pause/result.json').read_text())
assert result['failures']==0 and len(result['samples'])==4
assert all(s['operating'] and s['pixels_equal'] and s['paused_clock']>s['clock_before_run'] for s in result['samples'])
path=ROOT/'assets/rooms/tidal-condenser/pack/equipment-review.json'
record=json.loads(path.read_text())
record['status']='integrated-native-static-operating-retained-pause-reviewed'
record['retained']='equipment-states direct and retained RGB identical, 24 samples'
record['pause']='output/tidal-owner-repair-2026-09-12/station-pause/result.json'
record['remaining']=[]
path.write_text(json.dumps(record,indent=2)+'\n')
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Tidal owner asset repair verified - September 12, 2026\n\nOverhead wall family, matching riser and independent pump/monitor integrated. Native four-direction, operating, retained parity and real station pause checks pass. Next asset review: Command Center. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export or owner acceptance.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
note='\n\nTidal station-state lesson (September 12): a comms dialog can legitimately hold pause and invalidate an art fixture resume sample. Dismiss the dialog and disable automatic comms polling in the isolated fixture, then prove real clock advancement before testing pause. Check both renderer clock and native pixels; fixed-clock parity alone does not establish paused station behavior. New rotated art also requires matching visual bounds for containment and retained culling.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Tidal station-state lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
