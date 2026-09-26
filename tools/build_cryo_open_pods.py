"""Rebuild empty human pods; preserve the selected exit's visible housing and lid."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / 'character/cryo-open-study-2026-09-23'
OUT = ROOT / 'assets/material-polish-cryo-open-v1'
# Union of the three exit occupants, with a small margin for their outlines.
REPAIR = [(108,250),(307,250),(307,608),(108,608)]

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    source = STUDY / 'empty-open-source01.png'
    fill = Image.open(source).convert('RGBA').resize((418,627), Image.Resampling.LANCZOS)
    mask = Image.new('L', (418,627))
    painter = ImageDraw.Draw(mask)
    # Blend only the unoccupied margin; all former character pixels are replaced.
    for inset in range(13):
        painter.rectangle((108+inset,250+inset,307-inset,608-inset), fill=round(255*inset/12))
    results=[]
    for actor in ['bill','veld','branforth']:
        original = ROOT / f'assets/material-polish-cryo-recovery-v1/{actor}/wake-5.png'
        before = Image.open(original).convert('RGBA')
        assert before.size == fill.size
        after = Image.composite(fill,before,mask)
        path = OUT / f'{actor}.png'
        after.save(path)
        results.append({'actor':actor,'exit_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
                        'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (STUDY/'build.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'canvas':[418,627],'repair_polygon':REPAIR,'blend_margin':12,'outputs':results},indent=2)+'\n')
    print('Built three 418x627 empty-open pods; pixels outside occupant repair unchanged.')

if __name__ == '__main__':
    build()
