"""Publish a local review page through the existing riser gallery server."""
from pathlib import Path
import shutil

PACK=Path(__file__).resolve().parent
OUT=PACK.parent/'room-risers-expansion-v1/special-north'
OUT.mkdir(exist_ok=True)
sections=[]
for key,title,description in [
    ('survey_probe_bay','Survey Probe Bay','Matching steel reinforcement, pressure lines and a muted teal accumulator connect the wall to the existing launcher. Two ocean windows flank the assembly.'),
    ('airlock','Diving Airlock','Steel pressure manifolds and reinforced plating match the functional hatch, with an ocean window on either side.')]:
    shutil.copy2(PACK/'masters'/f'{key}.png',OUT/f'{key}-master.png')
    shutil.copy2(PACK/'prompts'/f'{key}.txt',OUT/f'{key}-prompt.txt')
    for q in range(4):shutil.copy2(PACK/'review'/f'{key}-q{q}.png',OUT/f'{key}-q{q}.png')
    sections.append(f'<article><h2>{title}</h2><p>{description}</p><img class="wall" src="{key}-master.png" alt="{title} wall source"><img class="room" src="{key}-q0.png" alt="{title} assembled north view"><details><summary>Other rotations and prompt</summary><a href="{key}-prompt.txt">Exact generation prompt</a><div class="rotations">'+''.join(f'<img src="{key}-q{q}.png" alt="{title} rotation {q}">' for q in range(1,4))+'</div></details></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · Special north walls</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#131e24;color:#e4e2d8;font:16px/1.5 system-ui}header,main{max-width:1200px;margin:auto;padding:24px}header{padding-top:40px}h1{margin:8px 0}p{color:#b4c1c1}a{color:#d8b778}main{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{background:#1b2a31;border:1px solid #384a52;border-radius:8px;padding:18px}h2{margin:0}.wall{width:100%;background:#26343b}.room{display:block;width:100%;image-rendering:pixelated}.rotations{display:grid;grid-template-columns:repeat(3,1fr)}.rotations img{width:100%}summary{cursor:pointer;margin:12px 0}@media(max-width:800px){main{grid-template-columns:1fr}}
</style><header><a href="../">← All riser walls</a><h1>Built around the machinery.</h1><p>Two special north walls. Existing launcher and working hatch retained; separate ocean windows on the left and right. Native views below; owner visual review pending.</p></header><main>'''+''.join(sections)+'</main></html>'
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Special north wall gallery ready.')
