"""Preserve refined wall evidence and component-specific review lesson."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
note = '\n\nConstruction material refinement (September 12): a casing repaint can leave bright reflection bands on rollers and spools. Name those residual components explicitly in a second edit and preserve rib/winding readability. The refined wall passed four native views; a newly generated floor atlas is still a candidate. Never treat an untouched-looking drone row in a generated atlas as pixel-identical or replace it without verification.\n'
for path in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md', Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction material refinement (September 12)' not in path.read_text(encoding='utf-8'):
        with path.open('a', encoding='utf-8') as out:
            out.write(note)
path = ROOT/'assets/rooms/construction-drone-bay/material/build.json'
data = json.loads(path.read_text())
data['status'] = 'refined wall native-reviewed; floor equipment remains open'
data['remaining'] = ['independent floor equipment material repair']
path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
path = ROOT/'docs/CURRENT_STATUS.md'
data = path.read_bytes().replace(b'Roller/spool sheen and independent floor equipment remain open;', b'Roller/spool refinement now passes native review; independent floor equipment remains open;', 1)
path.write_bytes(data)
print('Refinement evidence and shared lesson recorded.')
