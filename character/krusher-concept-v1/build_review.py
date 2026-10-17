"""Deterministic concept crops/comparison only; does not author sprite artwork."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
sheet = Image.open(ROOT / 'concept-01.png').convert('RGB')
front = sheet.crop((548, 274, 803, 824))
front = front.resize((69, 148), Image.Resampling.NEAREST)
bill = Image.open(REPO / 'character/major-bill-v3/rotations/south.png').convert('RGBA')
veld = Image.open(REPO / 'character/dr-veld-v1/concept-01.png').convert('RGB')
veld = veld.crop((710, 298, 956, 816)).resize((70, 148), Image.Resampling.NEAREST)
board = Image.new('RGB', (800, 590), '#25292c')
draw = ImageDraw.Draw(board)
draw.text((20, 16), 'KRUSHER — CONCEPT SCALE REVIEW', fill='white')
draw.text((20, 38), '148px standing ruler; concept crops, not exported runtime frames.', fill='#b9c3c9')
for x, name, sprite in [(40, 'Bill: selected sprite', bill), (290, 'Veld: identity concept', veld), (550, 'Krusher: new concept', front)]:
    if name.startswith('Bill'):
        board.paste(sprite, (x + 30, 72), sprite)
    else:
        board.paste(sprite, (x + 70, 96))
    draw.text((x, 265), name, fill='white')
draw.text((20, 296), 'Historical room capture + opaque Krusher concept inset (static composite).', fill='#b9c3c9')
room = Image.open(REPO / 'character/dr-veld-v1/qa/native/crew-together-crop.png').convert('RGB')
room = room.crop((120, 110, 380, 345))
small = front.resize((34, 74), Image.Resampling.NEAREST)
room.paste(small, (207, 100))
board.paste(room, (25, 325))
draw.text((310, 360), 'Room inset is a scale illustration only.', fill='white')
draw.text((310, 384), 'Grey rectangle is retained concept background.', fill='#b9c3c9')
draw.text((310, 408), 'No runtime, alpha, motion or occlusion acceptance.', fill='#b9c3c9')
board.save(ROOT / 'scale-review.png')
print('Saved scale-review.png; source sheet unchanged.')
