"""Audit immutable wreck sources and document registered runtime compositions."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/environment/wrecked-rooms-v1'
KINDS = ['engineering','medical','habitation','hydroponics']
INTERIOR = [0.085,0.115,0.825,0.765]

def main():
    rows = []
    for kind in KINDS:
        row = {'id':kind,'footprint_cells':[1,1], 'canvas_pivot':[0.5,0.5],
               'runtime_width':'game.get_cell_size()', 'sources':{},
               'stripped_interior_normalized':INTERIOR,
               'hull_owner':'Original wreck texture at every uncleared stage',
               'state_sequence':['wreck','registered stripped interior','foundation clearing','cleared ground'],
               'visual_owner_approval':'pending'}
        for stage in ['wreck','stripped']:
            path = PACK / f'{kind}-{stage}-v1.png'
            im = Image.open(path)
            assert im.width == im.height, f'Square registration required: {path}'
            alpha = im.convert('RGBA').getchannel('A').histogram()
            if stage == 'wreck':
                assert alpha[0]>0, f'Transparent exterior required: {path}'
            else:
                previous = row['sources']['wreck']['native_size']
                assert [im.width,im.height] == previous, f'Source registration changed: {path}'
            row['sources'][stage] = {'file':path.name,'native_size':[im.width,im.height],
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'mode':im.mode,
                'transparent_pixels':alpha[0], 'partial_alpha_pixels':sum(alpha[1:255]),
                'processing':'none; original generation retained',
                'usage':'transparent whole-cell texture' if stage=='wreck' else 'opaque interior-only source; never render as a standalone full sprite'}
        rows.append(row)
    manifest = {'variants':rows, 'job_seconds_at_1x':18,
                'salvage_metal':dict(zip(KINDS,[12,8,6,10])),
                'timing_and_yields':'prototype values, not human balance acceptance',
                'native_evidence':'output/wrecked-rooms-v1/',
                'verification':'test_wreck_clearance.gd and playtest_wreck_rooms.gd'}
    (PACK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    cards=[]
    for kind in KINDS:
        cards.append(f'<article><h2>{kind.title()}</h2><div class="stages"><figure><div class="sprite"><img src="{kind}-wreck-v1.png" alt="{kind} wreck"></div><figcaption>Wreck · blocked</figcaption></figure><figure><div class="sprite"><img src="{kind}-wreck-v1.png" alt="Original outer hull"><img class="inside" src="{kind}-stripped-v1.png" alt="Salvaged interior"></div><figcaption>Stripped · still blocked</figcaption></figure></div></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BRINE / Wrecked rooms</title><style>body{font:16px system-ui;background:#081d25;color:#d4e5e1;margin:32px}h1{font-size:34px}p{max-width:900px;line-height:1.6;color:#91acae}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:24px}article{background:#132e37;padding:20px;border:1px solid #2e4d55;border-radius:8px}h2{margin:0 0 14px}.stages{display:flex;gap:12px}figure{margin:0;flex:1}.sprite{position:relative;aspect-ratio:1;background:#0b232c}.sprite img{position:absolute;width:100%;height:100%;object-fit:contain}.inside{clip-path:inset(11.5% 9% 12% 8.5%)}figcaption{margin-top:10px;color:#a8c7bf;font-size:14px}a{color:#77c6b4}@media(max-width:520px){main{grid-template-columns:1fr}}</style><h1>Wrecked rooms / four departments</h1><p>Each wreck occupies the same single grid cell as a standard room. The original transparent hull stays registered while equipment is stripped, then the final frame clears. These previews compose the interior source beneath the original perimeter, matching the game renderer.</p><p><a href="README.md">Gameplay and verification notes</a></p><main>'''+''.join(cards)+'</main></html>'
    (PACK/'index.html').write_text(page,encoding='utf-8')
    print('4 variants / 8 immutable source images: dimensions, full-wreck alpha and stripped registration verified')

if __name__=='__main__':
    main()
