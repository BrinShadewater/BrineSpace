"""Build a review page from native production captures, never mock room renders."""

from pathlib import Path

import json

R=Path(__file__).resolve().parents[1]

O=R/'assets/architecture-rollout-2026-09-26'

rooms=json.loads((R/'rooms/full-wall-v1/editor-catalog.json').read_text())

cards=''.join(f'<article><h2>{r["room"].replace("_"," ").title()}</h2><img loading="lazy" data-room="{r["room"]}" src="review/{r["room"]}-q0.png" alt="Native room capture"></article>' for r in rooms)

page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · Installed walls and doors</title><style>body{margin:0;background:#16242b;color:#dbddd4;font:16px/1.5 system-ui}header,section,nav{max-width:1300px;margin:auto;padding:24px}h1{font-size:32px}h2{font-size:20px}p{color:#b4bdbb}a{color:#d9b37b}select,button{font:inherit;padding:8px;background:#283b42;color:white;border:1px solid #657473;border-radius:5px}.grid{max-width:1400px;margin:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;padding:24px}article{background:#203139;padding:12px;border:1px solid #3a4b51}article img{width:100%;image-rendering:pixelated}.wide{max-width:100%;image-rendering:pixelated}nav{position:sticky;top:0;background:#16242bf2}input{width:260px}small{color:#aab7b5}</style><header><small>BRINESPACE / PRODUCTION ARCHITECTURE / SEPTEMBER 26</small><h1>Installed walls, doors and hatch motion</h1><p>75 rooms · 300 native views · nine door families. The 28 additions inherit matching wall families. Saved material choices remain available.</p><p>These captures use the production renderers. Integration checks pass; this is ready for your visual review. <a href="../new-room-props-2026-09-26/furnished.html">Furnished additions with Bill for scale</a> · <a href="../animation-polish-2026-09-26/">Latest animation inventory and BRINE polish</a>.</p></header><section><h2>Department door movement</h2><label>Opening <input id="door" type="range" min="0" max="18" value="0"></label><p><img id="door-image" class="wide" src="motion/doors-00.png" alt="Nine door families, raised and low views"></p><p>19 sampled poses. The frame stays fixed while rigid leaves retract.</p><h2>Airlock in the live game</h2><label>Wall <select id="wall"><option value="0">North</option><option value="1">East</option><option value="2">South</option><option value="3">West</option></select></label> <label>State <select id="state"><option value="dry">Dry / sealed exterior</option><option value="flooding">Flooding</option><option value="opening_outer">Hatch opening</option><option value="exterior">Open to ocean</option><option value="sealing_departed">Sealing departure</option><option value="sealed_exterior">Awaiting return</option><option value="draining">Draining</option></select></label><p><img id="airlock" class="wide" src="live/airlock-q0-dry.png" alt="Native gameplay airlock capture"></p><p>Right-hinged outward swing, driven by the existing pressure cycle. These are captured states, not continuous video.</p></section><nav><label>Room rotation <select id="rotation"><option value="0">0°</option><option value="1">90°</option><option value="2">180°</option><option value="3">270°</option></select></label></nav><main class="grid">'''+cards+'''</main><script>const $=id=>document.getElementById(id);$('door').oninput=()=>$('door-image').src='motion/doors-'+$('door').value.padStart(2,'0')+'.png';function airlock(){$('airlock').src='live/airlock-q'+$('wall').value+'-'+$('state').value+'.png'}$('wall').onchange=airlock;$('state').onchange=airlock;$('rotation').onchange=()=>document.querySelectorAll('[data-room]').forEach(im=>im.src='review/'+im.dataset.room+'-q'+$('rotation').value+'.png');</script></html>'''

(O/'index.html').write_text(page,encoding='utf-8')

print('Architecture gallery: 75 rooms, 300 views, 28 airlock states, 19 door poses.')

