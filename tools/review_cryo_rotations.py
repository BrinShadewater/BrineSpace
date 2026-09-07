"""Assemble four native registered-room crops without resizing their pixels."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--source', default='output/cryo-state-v2')
parser.add_argument('--output', default='output/cryo-four-rotations-v1.png')
args = parser.parse_args()
target = (ROOT / args.output).resolve()
if not target.is_relative_to((ROOT / 'output').resolve()) or target.exists():
    raise SystemExit('Use a new review image within output/')
images = [Image.open(ROOT / args.source / f'room-q{q}.png').convert('RGB') for q in range(4)]
width, height = max(i.width for i in images), max(i.height for i in images)
sheet = Image.new('RGB', (2*(width+16), 2*(height+38)), '#142029')
draw = ImageDraw.Draw(sheet)
for q, image in enumerate(images):
    x, y = (q%2)*(width+16)+8, (q//2)*(height+38)+30
    sheet.paste(image, (x,y))
    draw.text((x,y-20), f'{q*90} degrees - native station crop', fill='#e4e9eb')
sheet.save(target)
