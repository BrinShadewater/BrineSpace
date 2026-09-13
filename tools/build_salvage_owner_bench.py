"""Preserve source, key explicit magenta and prepare exact directional turns."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
pack = root / 'assets/salvage-owner-v2'
source = pack / 'bench-raw.png'
im = Image.open(source).convert('RGBA')
a = np.array(im)
rgb = a[:,:,:3].astype(int)
mask = (rgb[:,:,0] - rgb[:,:,1] > 35) & (rgb[:,:,2] - rgb[:,:,1] > 35)
a[mask] = 0
clean = Image.fromarray(a)
crop = clean.getbbox()
clean = clean.crop(crop)
turns = [clean, clean.transpose(Image.Transpose.ROTATE_270),
         clean.transpose(Image.Transpose.ROTATE_180), clean.transpose(Image.Transpose.ROTATE_90)]
for q, turn in enumerate(turns):
    turn.save(pack / f'bench-q{q}.png')
record = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'source_size': im.size, 'crop': crop, 'clean_size': clean.size,
          'key': 'R-G>35 and B-G>35, including dark magenta edge contamination and handle apertures',
          'stage': 'cleaned candidate, not selected',
          'review': 'Low overhead work surface and inward vise; source still needs native material/scale review.'}
(pack / 'bench-review.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))

# Preserve the selected tote's registered silhouette and handle openings.
reg = json.loads((root / 'rooms/full-wall-v1/registrations/side-salvage-tote-south.json').read_text())
tote = Image.open(root / reg['source'].removeprefix('res://')).convert('RGBA')
mask_image = Image.new('L', tote.size)
draw = ImageDraw.Draw(mask_image)
for polygon in reg['pieces']:
    draw.polygon([tuple(p) for p in polygon], fill=255)
tote.putalpha(mask_image)
tote = tote.crop(tote.getbbox())
for q, turn in enumerate([tote, tote.transpose(Image.Transpose.ROTATE_270), tote.transpose(Image.Transpose.ROTATE_180), tote.transpose(Image.Transpose.ROTATE_90)]):
    turn.save(pack / f'tote-q{q}.png')
