"""Record reviewed Command architecture and catalog precedence lesson."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/command-owner-v2'
card=ROOT/'assets/command-directional-v1/cards/command_center.png'
shutil.copyfile(ROOT/'output/command-owner-repair-2026-09-12/riser-corrected/command_center-q0.png',card)
record={'status':'native-four-orientation-reviewed','source_sha256':hashlib.sha256((pack/'riser.png').read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'native':'output/command-owner-repair-2026-09-12/riser-corrected','remaining':['independent table and comms overhead/inward conversion','wall-bank source camera review'],'owner_acceptance':None}
(pack/'riser-review.json').write_text(json.dumps(record,indent=2)+'\n')
p=ROOT/'assets/room-risers-v2/registrations.json';data=json.loads(p.read_text());data['command_center']['stage']='Native four-orientation palette and seam review complete';p.write_text(json.dumps(data,indent=2)+'\n')
note='\n\nCommand riser precedence lesson (September 12): catalog files merge with Dictionary.merge default overwrite=false. A duplicate room ID in a later file does not override its existing entry. Locate and update the authoritative first registration; preserve the previous entry as provenance. A passing card-binding test cannot prove the new source was selected. Compare native imagery before claiming palette integration.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Command riser precedence lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Command matching wall reviewed - September 12, 2026\n\nCommand architecture now matches charcoal/red consoles. Native q0-q3 palette/seams reviewed and card refreshed. Independent table/comms overhead and inward facing remain open. See docs/COMMAND_OWNER_ASSET_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
