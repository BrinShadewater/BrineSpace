from pathlib import Path

import json
from PIL import Image

R=Path(__file__).resolve().parent

m=json.loads((R/'manifest.json').read_text())
if (R/'native-review/frame-023.png').exists():
    native=[Image.open(R/f'native-review/frame-{i:03}.png') for i in range(24)]
    native[0].save(R/'native-review/playback.webp',save_all=True,append_images=native[1:],duration=[38,37]*12,loop=0,lossless=True)

sections=[]

for s in m['states']:

    sid=s['id']

    label={'idle-south':'Idle / front','idle-east':'New idle / facing right','walk-east':'Walk / facing right','interact-east':'Sample inspection'}[sid]

    sections.append(f'''<section><h2>{label}</h2><div class="pair"><article><h3>Previous v3</h3><img src="preview/{sid}-old.webp"></article><article><h3>Revised v4</h3><img src="preview/{sid}-new.webp"></article></div><div class="small"><img src="preview/{sid}-old.webp"><img src="preview/{sid}-new.webp"></div><p>Lower pair: approximately 45 px standing height.</p><details><summary>Step through revised frames</summary><div class="frames">'''+''.join(f'<figure><img src="{p}"><figcaption>{i+1}</figcaption></figure>' for i,p in enumerate(s['frameFiles']))+'</div></details></section>')

html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld: brightness, size and walk revision</title><style>body{margin:0;background:#192127;color:#e1e6e3;font:16px system-ui}main{max-width:1100px;margin:auto;padding:24px}p{color:#bdcbcc;line-height:1.5}a{color:#b8dce9}section{border:1px solid #52626b;padding:18px;margin:20px 0;background:#263139}.pair,.small{display:grid;grid-template-columns:1fr 1fr;text-align:center;align-items:end}.pair img{width:276px;height:276px;image-rendering:pixelated}.small img{width:56px;height:56px;justify-self:center}.small{margin-top:20px}h3{font-size:16px}.contact{width:100%}.frames{display:flex;overflow:auto}.frames figure{margin:4px}.frames img{width:184px;height:184px}summary{cursor:pointer}</style><main><p>BRINESPACE / VELD REFINEMENT</p><h1>Right-facing idle and native playback</h1><p>Skin, blue cloth and graphite now follow the locked colour ramps, with shading preserved. A new right-facing idle fills the stop/walk coverage gap. For that new clip, the left example is the previous front idle. Previous v3 is on the left; v4 is on the right.</p><p>The walk retains alternating legs and counter-swing while lowering the lifted knees. V3 passed 85 native playback checks; two flat-foot segments drifted less than two source pixels. V4 passes 97 native checks; playback is included below. These candidates are not installed in the game. The targeted colour masks preserve geometry. Hair, ivory, steel highlights and instruments still need a complete material audit before installation.</p>'''+''.join(sections)+'''<h2>Native Godot playback</h2><img class="contact" src="native-review/playback.webp" alt="Native sprite-player playback"><p><a href="native-review/checks.json">Native checks</a>  /  <a href="../veld-animation-pilot-v3/native-review/contact-audit.json">Planted-foot measurements</a></p><h2>All revised frames</h2><a href="contact-sheet.png"><img class="contact" src="contact-sheet.png" alt="Revised frame contact sheet"></a><p><a href="brightness-checks.json">Brightness measurements</a> · <a href="manifest.json">Manifest</a> · <a href="../crew-turnarounds-v4/">Selected design</a></p></main></html>'''

(R/'index.html').write_text(html,encoding='utf-8')

