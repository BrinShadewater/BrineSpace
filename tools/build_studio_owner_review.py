"""Build review landing page with native repairs and preserved owner layouts."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/studio-owner-notes-2026-09-08'
rows=json.loads((OUT/'saved-layouts/runtime.json').read_text())
cards=[]
for row in rows:
    images=''.join(f'<figure><a href="saved-layouts/images/{row["id"]}-q{q}.png"><img src="saved-layouts/images/{row["id"]}-q{q}.png"></a><figcaption>{q*90}°</figcaption></figure>' for q in range(len(row['images'])))
    cards.append(f'<section><h2>{html.escape(row["name"])} · saved layout</h2><div class="poses">{images}</div><textarea data-note="{row["id"]}" placeholder="Your notes or fixes…"></textarea></section>')
doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · Studio fixes</title><style>
*{box-sizing:border-box}body{background:#10282c;color:#e1e7df;font:16px/1.5 system-ui;margin:0}main{max-width:1500px;margin:auto;padding:28px}a{color:#b4e7d1}section{margin:28px 0;padding:20px;background:#1b3438;border:1px solid #47615e;border-radius:8px}img{max-width:100%;display:block}figure{margin:0}.poses{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.poses img{width:100%}textarea,button{font:inherit;color:inherit;background:#203b3f;border:1px solid #77928b;border-radius:5px;padding:12px}textarea{width:100%;min-height:90px;margin-top:12px}button{cursor:pointer}.nav{display:flex;gap:20px;flex-wrap:wrap}.wide{max-width:1100px}@media(max-width:750px){.poses{grid-template-columns:repeat(2,1fr)}}
</style><main><h1>Room Studio updates</h1><p>Rotate Room · Next Room · Save. Valid edits autosave across rotations. R cycles a selected asset's available views, or rotates the room with nothing selected; F flips selected art.</p><div class="nav"><a href="catalog/index.html">Full list: 47 rooms · 167 images · notes</a><a href="#saved">Your saved layouts</a><a href="#repairs">Material and cutout fixes</a><a href="#south">South-facing views</a><button id="export">Export notes</button></div><p>Your Research, Xeno and Biomass layout changes are preserved. These images use a read-only copy of your saved file. Default-room previews show the newly installed art; art you removed stays removed in your personal layouts.</p><section><h2>Studio controls</h2><img class="wide" src="studio-controls.png"></section><section><h2>North riser door</h2><p>The door spans the riser and its two leaves retract. The low north wall is hidden while its riser is visible.</p><div class="poses">'''
for phase in ['closed','half','open']:
    doc+=f'<figure><a href="door-{phase}.png"><img src="door-{phase}.png"></a><figcaption>{phase.capitalize()}</figcaption></figure>'
doc+='</div></section><h1 id="saved">Your saved layouts</h1>'+''.join(cards)
doc+='''<section id="repairs"><h2>Material and cutout fixes</h2><p>Mining and Ore Refinery have quieter matte materials. Mycelium, Crew Lounge and Maintenance cutout edges are tightened; crane openings are explicitly excluded.</p><img src="repairs-native.jpg"><textarea data-note="art-repairs" placeholder="Art repair notes…"></textarea></section><section id="south"><h2>Inward-facing south banks</h2><p>Twelve rear-facing sources added; ten are used on the south wall by current default layouts. Quarantine and Radio also have matching south views available in the tray. Earlier candidates that still faced outward were rejected.</p><img src="south-native.jpg"><textarea data-note="south-facing" placeholder="South-facing art notes…"></textarea></section><p><a href="catalog/index.html">Open all 47 rooms and the complete illustrated review list</a></p></main><script>
const key='brinespace-room-review-2026-09-08';let notes={};try{notes=JSON.parse(localStorage.getItem(key)||'{}')}catch{}document.querySelectorAll('textarea').forEach(t=>{t.value=notes[t.dataset.note]||'';t.oninput=()=>{notes[t.dataset.note]=t.value;localStorage.setItem(key,JSON.stringify(notes))}});document.querySelector('#export').onclick=()=>{let text='# BrineSpace room notes\n\n';for(const [id,note] of Object.entries(notes))if(note.trim())text+='## '+id+'\n'+note+'\n\n';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'text/markdown'}));a.download='brinespace-art-notes.md';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
</script></html>'''
# Keep JavaScript string newlines escaped in the generated HTML.
doc=doc.replace("notes\n\n'","notes\\n\\n'").replace("id+'\n'+note+'\n\n'","id+'\\n'+note+'\\n\\n'")
(OUT/'index.html').write_text(doc,encoding='utf-8')
import re
links=re.findall(r'(?:src|href)="([^"]+)"',doc)
assert all(s.startswith('#') or (OUT/s).exists() for s in links)
print(f'Review page: {len(rows)} saved-room previews; {len(links)} local links verified')
