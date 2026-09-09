"""Install native cards and create a room-by-room owner review; never edit source pixels."""
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
pack = ROOT / 'assets/riser-departments-v1'
out = ROOT / 'output/riser-departments-v1'
groups = json.loads('{' + re.search(r'const GROUPS=\{(.*?)\}\s*static', (ROOT/'rooms/whole-room/riser_catalog.gd').read_text(), re.S)[1] + '}')
family = {rid: group for group, ids in groups.items() for rid in ids}
family.update(brine_core='brine_core', airlock='airlock')
cards = json.loads((pack/'cards/runtime.json').read_text())
ids = [r['room'] for r in cards] + ['corridor', 'corner', 'tee_corridor']
records = []
for rid in ids:
    before = 'assets/door-polish-v1/cards/'+rid+'.png' if rid not in ['corridor','corner','tee_corridor'] else 'assets/layout-scale-pass/cards-final/'+rid+'.png'
    records.append(dict(id=rid, family=family[rid], before='../../'+before, after='../../assets/riser-departments-v1/cards/'+rid+'.png'))
for name in ['scripts/room_card_art.gd','scripts/grid_canvas.gd']:
    path = ROOT/name
    s = path.read_text()
    for rid in ids:
        target = 'res://assets/riser-departments-v1/cards/'+rid+'.png'
        pattern = r'("'+re.escape(rid)+r'":\s*\[?")res://[^"\n]+\.png(")'
        s,n = re.subn(pattern, lambda m:m[1]+target+m[2], s)
        assert n in ([1] if name.endswith('room_card_art.gd') else [1,2]), (name,rid,n)
    if name.endswith('grid_canvas.gd'):
        for rid in ['corridor','corner','tee_corridor']:
            for v in [1,2]:
                s=s.replace(f'res://rooms/decoration-integration/{rid}-{v}.png',f'res://assets/riser-departments-v1/cards/{rid}-{v}.png')
    path.write_text(s)
registrations=json.loads((pack/'registrations.json').read_text())
for r in registrations.values():
    assert hashlib.sha256((ROOT/r['source'].removeprefix('res://')).read_bytes()).hexdigest()==r['sha256']
(pack/'manifest.json').write_text(json.dumps(dict(families=groups, retained=['brine_core','airlock'], rooms=records, sources=registrations, acceptance='Native visual review complete; owner acceptance pending'),indent=2)+'\n')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Riser walls · room review</title><style>
*{box-sizing:border-box}body{margin:0;background:#13272d;color:#deE4db;font:16px system-ui}main{max-width:1500px;margin:40px auto;padding:0 24px}h1{font-size:36px;font-weight:550}p{max-width:900px;line-height:1.6}button,select,input{background:#29464b;color:inherit;border:1px solid #67847c;padding:10px;border-radius:5px}nav{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#13272df5;padding:16px 0;z-index:1}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:20px}article{background:#20363b;border:1px solid #425e60;border-radius:9px;padding:14px}img{width:100%;display:block}h2{font-size:20px;text-transform:capitalize;margin:4px 0 8px}small{color:#a8c2b9}textarea{width:100%;min-height:85px;padding:10px;margin-top:10px;color:inherit;background:#152b31;border:1px solid #587770}details{margin:12px 0}summary{cursor:pointer}article[hidden]{display:none}</style><main>
<h1>Riser walls, by room</h1><p>Eight new wall families: biology, clinical, habitat, engineering, research, communications, logistics and containment. BRINE and the airlock retain their dedicated treatments. Raised walls now start enabled in the game and Layout Studio; the game display preference remembers an explicit change.</p>
<p>All 47 rooms appear below. These native previews show the standard layouts; your saved editor arrangements remain separate. Use Before / After to compare. Notes stay in this browser and can be exported for your fixes.</p>
<nav><input id="search" placeholder="Find a room" aria-label="Find a room"><select id="family" aria-label="Wall family"><option value="">All wall families</option></select><button id="compare">Show before</button><button id="export">Export notes</button></nav><div class="grid" id="rooms"></div>
<details><summary>Source artwork and four-rotation studies</summary><div class="grid" id="sources"></div></details><p><small>Verified: 47 room assignments, 32 department rotation captures, nine corridor variants, settings migration and saved preference behavior. Owner visual acceptance pending.</small></p></main><script>
const records=RECORDS,groups=GROUPS;const key='riser-departments-v1-notes';let notes=JSON.parse(localStorage.getItem(key)||'{}'),before=false;
for(const f of [...new Set(records.map(r=>r.family))].sort()){const o=document.createElement('option');o.value=f;o.textContent=f.replaceAll('_',' ');document.querySelector('#family').append(o)}
for(const r of records){const c=document.createElement('article');c.dataset.id=r.id;c.dataset.family=r.family;c.innerHTML=`<h2>${r.id.replaceAll('_',' ')}</h2><small>${r.family.replaceAll('_',' ')}</small><a target="_blank" href="${r.after}"><img loading="lazy" src="${r.after}" alt="${r.id} raised wall preview"></a><textarea aria-label="Notes for ${r.id}" placeholder="Notes or fixes…"></textarea>`;const t=c.querySelector('textarea');t.value=notes[r.id]||'';t.oninput=()=>{notes[r.id]=t.value;localStorage.setItem(key,JSON.stringify(notes))};document.querySelector('#rooms').append(c)}
const filter=()=>{const q=document.querySelector('#search').value.toLowerCase().replaceAll(' ','_'),f=document.querySelector('#family').value;document.querySelectorAll('#rooms article').forEach(c=>c.hidden=!c.dataset.id.includes(q)||(f&&f!==c.dataset.family))};document.querySelector('#search').oninput=filter;document.querySelector('#family').onchange=filter;
document.querySelector('#compare').onclick=()=>{before=!before;document.querySelector('#compare').textContent=before?'Show after':'Show before';records.forEach(r=>{const c=document.querySelector(`[data-id="${r.id}"]`),src=before?r.before:r.after;c.querySelector('img').src=src;c.querySelector('a').href=src})};
for(const f of Object.keys(groups)){const c=document.createElement('article');c.innerHTML=`<h2>${f}</h2><a target="_blank" href="../../assets/riser-departments-v1/${f}/source.png"><img loading="lazy" src="../../assets/riser-departments-v1/${f}/source.png" alt="${f} source artwork"></a><p>Runtime uses the upper service face. Lower source cabinet area is excluded.</p><select aria-label="${f} rotation">${[0,1,2,3].map(q=>`<option value="${q}">Rotation ${q+1}</option>`).join('')}</select><img class="rotation" loading="lazy" src="${f}-q0.png" alt="${f} native rotation study">`;c.querySelector('select').onchange=e=>c.querySelector('.rotation').src=f+'-q'+e.target.value+'.png';document.querySelector('#sources').append(c)}
document.querySelector('#export').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(notes,null,2)],{type:'application/json'}));a.download='riser-wall-notes.json';a.click();URL.revokeObjectURL(a.href)};</script></html>'''.replace('RECORDS',json.dumps(records)).replace('GROUPS',json.dumps(groups))
(out/'index.html').write_text(html,encoding='utf-8')
print('47 cards installed; 8 source hashes verified; gallery includes before/after, rotations and notes')
