"""Register empty chamber insert while preserving the existing housing pixels."""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/cryo-layered-v1'

def build():
    original = Image.open(ROOT / 'assets/material-polish-cryo-recovery-v1/bill/wake-0.png').convert('RGBA')
    source = OUT / 'empty-closed-source.png'
    insert = Image.open(source).convert('RGBA').resize(original.size, Image.Resampling.LANCZOS)
    mask = Image.new('L', original.size)
    ImageDraw.Draw(mask).rounded_rectangle((116, 145, 299, 412), radius=14, fill=255)
    Image.composite(insert, original, mask).save(OUT / 'closed.png')
    (OUT / 'provenance.json').write_text(json.dumps({
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'canvas': [418,627], 'insert_bounds': [116,145,299,412],
        'method': 'Generated empty interior registered once; original housing preserved outside insert.',
        'prompt': 'Remove entire human occupant; reconstruct empty padded chamber behind blue glass; preserve supplied closed pod camera, framing and matte style; transparent exterior.',
        'characters': 'Live selected south idle/walk textures; no new character art.'
    }, indent=2)+'\n')
    print('Built registered empty closed chamber.')

if __name__ == '__main__':
    build()
