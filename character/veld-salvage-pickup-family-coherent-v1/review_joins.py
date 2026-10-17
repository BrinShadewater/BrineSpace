"""Display every possible cosmetic work exit beside finite pickup entry."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent
for gear in ['bare','helmet']:
    m=json.loads((H/f'{gear}-manifest.json').read_text(encoding='utf-8'));by={s['id']:s for s in m['states']}
    board=Image.new('RGBA',(1536,1200),'#202a30');d=ImageDraw.Draw(board)
    for row,direction in enumerate(['east','west','north','south']):
        work=by['salvage-'+direction];pick=by['swim-pickup-'+direction]
        for i,f in enumerate(work['frameFiles']):
            a=Image.open(H/f).convert('RGBA');b=Image.open(H/pick['frameFiles'][0]).convert('RGBA')
            for im,x in [(a,0),(b,128)]:
                thumb=im.resize((128,128),Image.Resampling.BILINEAR);board.alpha_composite(thumb,(i*256+x,row*300+30))
            # Native scale paired with a crop that retains the entire action pose.
            d.text((i*256+4,row*300+8),f'{direction} work{i} -> pickup0',fill='white')
            for im,x in [(a,0),(b,128)]:board.alpha_composite(im.resize((82,82),Image.Resampling.BILINEAR),(i*256+x,row*300+180))
    board.save(H/f'{gear}-work-exit-comparison-v1.png')
html='''<!doctype html><meta charset="utf-8"><title>Veld underwater sample family</title><style>body{background:#202a30;color:#e5ebed;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8cc6e7}</style><h1>Veld — sample work and pickup family</h1><p>All four independently authored directions, bare and helmet. Staged; controller timelines and arbitrary work exits under review. Runtime unchanged.</p><p>Each pair shows work phase0–5 on the left and pickup entry on the right, at identical canvas and native rulers.</p><h2>Bare work exits</h2><img src="bare-work-exit-comparison-v1.png"><h2>Helmet work exits</h2><img src="helmet-work-exit-comparison-v1.png"><p><a href="bare-family-contact-v1.png">All bare action poses</a> · <a href="helmet-family-contact-v1.png">All helmet action poses</a> · <a href="family-checks.json">Exact source checks</a></p>'''
(H/'index.html').write_text(html,encoding='utf-8')
