"""Illustrated polish review with native before/after captures and persistent notes."""
import html,json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/room-style-polish-2026-09-08'
PACK=ROOT/'assets/room-style-polish-v1'
rows=json.loads((PACK/'generation.json').read_text())
runtime=json.loads((OUT/'catalog/runtime.json').read_text())
blocks=[]
summaries={
    'mycelium-cultivation-wall':'Grey-green casing, quieter tray edges and a clearer separation between fungi, nutrient plumbing and service panels.',
    'crew-hab-berth-wall':'Warm cream casing and dark wood backing bring the berths closer to the existing habitation furniture.',
    'research-analysis-wall':'Cream composite, restrained blue accents and recessed rear service panels match the laboratory equipment.',
    'clone-growth-wall':'Warm ivory and teal replace the generic green cabinet while keeping the culture vessels focal.',
    'quarantine-specimen-wall':'Charcoal casing and sparse burgundy fittings connect the specimen bank to the containment room.',
    'medical-treatment-wall':'Cream and teal equipment surrounds the warm treatment pad, with more restrained rear panel detail.',
    'xeno-containment-wall':'Warm grey composite and muted safety details match the established xenobiology equipment.',
    'bio-culture-wall':'Cream, olive and teal separate the cabinet, sample mats and laboratory instruments.',
    'emergency-isolation-wall':'Charcoal housing and limited orange fittings bring the chamber back into the engineering palette.',
    'crew-lounge-built-in':'Warmer wood, cream end cabinets and fabric detail match the room’s existing lounge furniture.',
    'radio-signal-wall':'Dark slate and muted burgundy fittings match the communications equipment.',
    'maintenance-repair-wall':'Charcoal casing, restrained orange accents and recessed service details match the maintenance tools.'
}
sheet=Image.new('RGB',(1760,((len(rows)+1)//2)*270),'#233438')
for n,row in enumerate(rows):
    identity=row['id']; name=identity.replace('-',' ').title()
    comp='comparisons/'+identity+'.png'
    with Image.open(OUT/comp) as image: sheet.paste(image,(n%2*880,n//2*270))
    host=next((room for room in runtime if any(p['id']=='full_wall_'+identity and p['side_view']=='south' for v in room['views'] for p in v['props'])),None)
    host_html=''
    if host:
        q=next(v['quarter'] for v in host['views'] if any(p['id']=='full_wall_'+identity and p['side_view']=='south' for p in v['props']))
        host_html=f'<details><summary>In {html.escape(host["name"])} · {q*90}°</summary><div class="pair"><figure><img loading="lazy" src="../studio-owner-notes-2026-09-08/catalog/images/{host["id"]}-q{q}.png"><figcaption>Before</figcaption></figure><figure><img loading="lazy" src="catalog/images/{host["id"]}-q{q}.png"><figcaption>Polished</figcaption></figure></div></details>'
    else: host_html='<p>Available as a south-facing tray variant; current default layout uses another mounting wall.</p>'
    blocks.append(f'<article data-search="{html.escape(name+" "+row["department"])}"><h2>{html.escape(name)}</h2><p>{html.escape(row["department"])}</p><a href="{comp}"><img loading="lazy" src="{comp}" alt="{html.escape(name)} before and after at runtime scale"></a><p>{html.escape(summaries[identity])}</p>{host_html}<textarea data-note="style:{identity}" placeholder="Your polish notes…"></textarea></article>')
sheet.save(OUT/'comparison-sheet.jpg',quality=95)
style='''*{box-sizing:border-box}body{margin:0;background:#10282c;color:#dfe8dd;font:16px/1.5 system-ui}main{max-width:1400px;margin:auto;padding:28px}h1{font-size:34px}a{color:#b0dfcd}.toolbar{position:sticky;top:0;background:#10282cf5;display:flex;flex-wrap:wrap;gap:12px;padding:12px 0;z-index:2}input,button,textarea{font:inherit;color:inherit;background:#203b3f;border:1px solid #69877e;padding:10px;border-radius:5px}input{flex:1}button{cursor:pointer}article,section{background:#1b3438;border:1px solid #47615e;padding:20px;margin:22px 0;border-radius:8px}article[hidden]{display:none}img{max-width:100%;display:block}article>a img{width:100%}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}summary{cursor:pointer;padding:10px 0}textarea{width:100%;min-height:90px;margin-top:12px}.doors{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.doors img{width:100%}@media(max-width:650px){main{padding:12px}.pair{grid-template-columns:1fr}}'''
js=r'''const key='brinespace-room-review-2026-09-08';let saved={};try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch{}for(const t of document.querySelectorAll('textarea')){t.value=saved[t.dataset.note]||'';t.oninput=()=>{saved[t.dataset.note]=t.value;localStorage.setItem(key,JSON.stringify(saved))}}document.querySelector('#search').oninput=e=>{for(const a of document.querySelectorAll('article'))a.hidden=!a.dataset.search.toLowerCase().includes(e.target.value.toLowerCase())};document.querySelector('#export').onclick=()=>{let text='# BrineSpace polish notes\n\n';for(const [id,note]of Object.entries(saved))if(note.trim())text+='## '+id+'\n'+note+'\n\n';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'text/markdown'}));a.download='brinespace-polish-notes.md';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};'''
    # raw JS above already preserves escaped newline sequences.
doors=''.join(f'<figure><a href="studio-final/door-{phase}.png"><img src="studio-final/door-{phase}.png"></a><figcaption>{phase.title()}</figcaption></figure>' for phase in ['closed','half','open'])
doc=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · Room style polish</title><style>{style}</style><main><h1>Room style polish</h1><p>Twelve south-facing banks now follow the approved Tidal material quality while retaining department colors, their inward-facing silhouettes and room scale. Compare the actual registered art beside Bill, then expand a room to see it installed.</p><p><a href="catalog/index.html">Full illustrated list: all 47 rooms and orientations</a> · <a href="../studio-owner-notes-2026-09-08/index.html#saved">Your preserved layout review</a></p><div class="toolbar"><input id="search" aria-label="Filter polished artwork" placeholder="Filter by room or department"><button id="export">Export notes</button></div><section><h2>Riser door finish</h2><p>Recessed leaves, rubber-like seals and a subdued threshold. Painted panel insets reuse the surrounding hull material and retract with the leaves.</p><div class="doors">{doors}</div><textarea data-note="style:riser-door" placeholder="Door finish notes…"></textarea></section>{''.join(blocks)}<p>Previous art is preserved. Source, frame and native checks are recorded with the assets; your visual notes remain the final style review.</p></main><script>{js}</script></html>'''
(OUT/'index.html').write_text(doc,encoding='utf-8')
links=re.findall(r'(?:src|href)="([^"]+)"',doc)
assert all((OUT/s.split('#')[0]).exists() for s in links if not s.startswith('#'))
(OUT/'gallery-check.js').write_text(js)
print(f'Polish gallery: {len(rows)} comparisons and {len(links)} verified local links')
