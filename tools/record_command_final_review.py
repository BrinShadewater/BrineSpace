"""Record Command owner repair after final native review and real pause checks."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/command-owner-v2'
result=json.loads((ROOT/'output/command-owner-repair-2026-09-12/final-station-pause/result.json').read_text())
assert result['failures']==0 and len(result['samples'])==4
card=ROOT/'assets/command-directional-v1/cards/command_center.png'
shutil.copyfile(ROOT/'output/command-owner-repair-2026-09-12/wall-alpha-native/command_center-q0.png',card)
(PACK/'final-review.json').write_text(json.dumps({'status':'owner-asset-notes-native-reviewed','static_native':'output/command-owner-repair-2026-09-12/wall-alpha-native','pause':'output/command-owner-repair-2026-09-12/final-station-pause','equipment_states':'output/command-owner-repair-2026-09-12/equipment-states','latest_checks':'output/test-runs/20260912-205605-headless','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'owner_acceptance':None,'export':None},indent=2)+'\n')
note='\n\nCommand wall alpha lesson (September 12): a camera edit can open a new background pocket inside an older clipping polygon. Preserve the raw edit and verify alpha in the native consumer. Border-only cleanup can miss isolated pockets; removing all neutral white was appropriate for these sources only because their equipment has no authored white surfaces. Do not generalize this threshold to clinical or pale-painted art.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Command wall alpha lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Command owner asset repair reviewed - September 12, 2026\n\nMatching charcoal/red wall, overhead inward table/systems/comms and wall antenna corrections integrated. Native alpha, state/retained and actual pause checks recorded; selected card refreshed. Next: Observation rotation and architectural portholes. See docs/COMMAND_OWNER_ASSET_REPAIR_2026-09-12.md. No export or owner acceptance.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
