"""Record the reviewed partial Construction pass without claiming completion."""
import json
import shutil
from pathlib import Path
from build_clone_overhead_directions import sha

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/rooms/construction-drone-bay/material'
NOTE = '''

Construction repair lesson (September 12): retain directional `wall_contact`
metadata when replacing raster registrations. It controls actual mounting in
`full_wall_prop.gd`; correct source hashes and passing route/card tests did not
detect a south bank placed beside floor stations. Inspect fresh native captures
after the process finishes. Matte casing improvement also does not prove matte
rollers, spools or shared floor machinery; track those components separately.
'''

def main():
    capture = ROOT / 'output/construction-owner-repair-2026-09-12/refined-native/construction_drone_bay-q0.png'
    card = ROOT / 'assets/rooms/construction-drone-bay/cards/card.png'
    shutil.copyfile(capture, card)
    review = {'status': 'wall material repair reviewed; floor equipment remains open', 'native': 'output/construction-owner-repair-2026-09-12/refined-native',
              'directions_reviewed': [0, 1, 2, 3], 'card_sha256': sha(card),
              'regressions': {'path': 'output/test-runs/20260912-193727-headless', 'layouts': 176, 'side_variants': 20, 'cards': 47, 'result': 'PASS'},
              'remaining': ['independent floor equipment', 'drone redesign question'], 'owner_acceptance': None}
    (PACK / 'review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')
    paths = [ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             ROOT / 'skills/brinespace-room-pipeline/references/material-and-scale-review.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]
    for path in paths:
        if 'Construction repair lesson (September 12)' not in path.read_text(encoding='utf-8'):
            with path.open('a', encoding='utf-8') as out:
                out.write(NOTE)
    status = ROOT / 'docs/CURRENT_STATUS.md'
    prefix = b'## Construction material repair in progress - September 12, 2026\n\nFour overhead fabrication-bank directions now use a matte casing repaint. Native mounting reviewed after preserving wall_contact metadata. Roller/spool sheen and independent floor equipment remain open; this room is not complete. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.\n\n'
    if not status.read_bytes().startswith(prefix):
        status.write_bytes(prefix + status.read_bytes())

if __name__ == '__main__':
    main()
