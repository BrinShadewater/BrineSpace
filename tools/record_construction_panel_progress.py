"""Record the native-reviewed flat pallet and camera lesson."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
note='\n\nConstruction panel-storage lesson (September 12): an image edit anchored to tall upright plates retained their front faces despite overhead wording. A new low flat-storage companion produced an unambiguous top plane. Record this as a construction change, preserve the rejected elevation and both prompts, and fit inside the former maximum footprint. Point release catches toward room center and derive visual bounds from the same aspect-preserving rectangle used to draw. The live q2 pallet was inspected; other layouts omit this prop, so four room captures do not prove four pallet orientations.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction panel-storage lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f: f.write(note)
p=ROOT/'assets/rooms/construction-drone-bay/material/panel-review.json'
p.write_text(json.dumps({'status':'live q2 native-reviewed; other pallet placements not visually proven','native':'output/construction-owner-repair-2026-09-12/panel-native','observed':'five flat panel stacks and crosswise spare stack; release straps face right toward center','scope':'Construction only','remaining':['other floor machinery overhead/facing','other pallet placements','drone design decision'],'owner_acceptance':None},indent=2)+'\n')
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Construction panel pallet overhead companion - September 12, 2026\n\nThe tall glossy panel rack is replaced by a matte flat-storage pallet in Construction. Live q2 placement reviewed with inward catches and aspect-preserving bounds inside the old maximum size. Other floor equipment facing and alternate pallet placements remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix): p.write_bytes(prefix+p.read_bytes())
