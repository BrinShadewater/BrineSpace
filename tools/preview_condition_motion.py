"""Label native condition captures without resizing their physical pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'output/condition-motion-v1'
source = Image.open(OUT / 'conditions-q0.png').convert('RGB').crop((280, 115, 860, 585))
board = Image.new('RGB', (580, 502), '#09171d')
board.paste(source, (0, 32))
draw = ImageDraw.Draw(board)
font = ImageFont.load_default(size=13)
for i, label in enumerate(['Healthy', 'Unpowered', 'Leaking', 'Flooded', 'Repaired']):
    draw.text((74 + i * 108, 16), label, fill='#a9bab9', font=font, anchor='mm')
board.save(OUT / 'condition-comparison-v1.png')
print('Native five-state comparison; no physical-pixel resizing')
