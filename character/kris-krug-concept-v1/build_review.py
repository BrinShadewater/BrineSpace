"""Deterministic scale illustration and provenance; source artwork stays intact."""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
revision = len(sys.argv) > 1 and sys.argv[1] == 'v2'
sheet_name = 'concept-02-no-hat-unique-suit.png' if revision else 'concept-01.png'
sheet = Image.open(ROOT / sheet_name).convert('RGB')
front = sheet.crop((545, 266, 803, 831)).resize((68, 148), Image.Resampling.NEAREST)
krusher = Image.open(REPO / 'character/krusher-concept-v1/concept-04-krusher-dom.png').convert('RGB')
krusher = krusher.crop((548, 274, 803, 824)).resize((69, 148), Image.Resampling.NEAREST)
bill = Image.open(REPO / 'character/crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png').convert('RGBA')
box = bill.getbbox()
bill = bill.crop(box)
# Current selected pack declares 148px standing height; retain native density.
board = Image.new('RGB', (800, 590), '#25292c')
draw = ImageDraw.Draw(board)
draw.text((20, 16), 'KRIS KRUG - CONCEPT SCALE REVIEW', fill='white')
draw.text((20, 38), '148px standing ruler; concept crops, not runtime frames.', fill='#b9c3c9')
for x, name, sprite in [(85, 'Bill: selected sprite', bill), (340, 'Krusher: concept', krusher), (600, 'Kris: concept', front)]:
    board.paste(sprite, (x, 78), sprite if sprite.mode == 'RGBA' else None)
    draw.text((x - 40, 250), name, fill='white')
draw.line((20, 226, 780, 226), fill='#627780')
draw.text((20, 291), 'Historical room capture + opaque Kris inset (static composite).', fill='#b9c3c9')
room = Image.open(REPO / 'character/dr-veld-v1/qa/native/crew-together-crop.png').convert('RGB')
room = room.crop((120, 110, 380, 345))
room.paste(front.resize((34, 74), Image.Resampling.NEAREST), (207, 100))
board.paste(room, (25, 325))
draw.text((310, 360), 'Room inset illustrates size only.', fill='white')
draw.text((310, 384), 'Grey concept background remains visible.', fill='#b9c3c9')
draw.text((310, 408), 'No runtime, motion or occlusion acceptance.', fill='#b9c3c9')
board.save(ROOT / ('scale-review-v2.png' if revision else 'scale-review.png'))
refs = [
    Path('C:/Users/Alex/.codex/codex-remote-attachments/01a10108-0cea-7ee1-8d89-586acd3a735c/18A42E78-05F7-4BBA-B1E7-22EBA103E6B4/1-Photo-1.jpg'),
    Path('C:/Users/Alex/.codex/codex-remote-attachments/01a10108-0cea-7ee1-8d89-586acd3a735c/18A42E78-05F7-4BBA-B1E7-22EBA103E6B4/2-Photo-2.jpg'),
    ROOT / 'concept-01.png' if revision else REPO / 'character/krusher-concept-v1/concept-04-krusher-dom.png',
]
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
provenance = {
    'tool': 'built-in image_gen',
    'generated_source': 'C:/Users/Alex/.codex/generated_images/01a10108-0cea-7ee1-8d89-586acd3a735c/exec-bad9782b-1dd7-488a-b7b8-04c50dfaa3c5.png',
    'references': [{'path': str(p), 'sha256': digest(p)} for p in refs],
    'concept_sha256': digest(ROOT / sheet_name),
    'prompt_file': 'revision-02-prompt.txt' if revision else 'prompt.txt',
    'status': 'First concept; role and visual owner acceptance pending; no runtime integration',
}
if revision:
    provenance['generated_source'] = sys.argv[2]
(ROOT / ('provenance-v2.json' if revision else 'provenance.json')).write_text(json.dumps(provenance, indent=2), encoding='utf-8')
print('Saved scale review and provenance; source image unchanged.')
