"""Rebuild isolated compact-bunk endpoints; not a runtime catalog edit."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
for actor, revision, paste, head in [('veld', 'dr-veld-v2', (11, 48), (63, 210)), ('branforth', 'chief-engineer-branforth-v2', (9, 57), (55, 208))]:
    source = Image.open(ROOT / f'{actor}-source.png').convert('RGBA')
    canonical = Image.open(PROJECT / f'character/{revision}/frames/bare/sleep-east/000.png').convert('RGBA')
    scale = 0.16  # Same head/torso density as canonical; not total prone length.
    small = source.resize(tuple(round(x * scale) for x in source.size), Image.Resampling.NEAREST)
    alpha = small.getchannel('A').point(lambda x: 255 if x >= 128 else 0)
    palette = canonical.convert('RGB').quantize(colors=256)
    small = small.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    small.putalpha(alpha)
    result = Image.new('RGBA', (256, 256))
    result.alpha_composite(small, paste)
    result.save(ROOT / f'{actor}-compact-sleep-east.png')
    (ROOT / f'{actor}-recipe.json').write_text(json.dumps({
        'source_sha256': hashlib.sha256((ROOT / f'{actor}-source.png').read_bytes()).hexdigest(),
        'reference': f'character/{revision}/frames/bare/sleep-east/000.png',
        'authoring': f'built-in image generation; exact prompt in {actor}-prompt.txt',
        'scale': scale, 'paste': list(paste), 'canvas': [256, 256],
        'pivot': [128, 224], 'standingHeight': 148, 'head_anchor': list(head),
        'alpha': 'binary threshold 128', 'palette': 'canonical sleep-east 256 colors',
        'status': 'staged static endpoint; no runtime binding or motion acceptance'
    }, indent=2) + '\n')
