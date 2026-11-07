"""Install nine native corridor cards and create the owner review gallery."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/corridor-wall-variants-v1'
out=ROOT/'output/corridor-wall-variants-v1'
records=json.loads((out/'review.json').read_text())
sources=json.loads((pack/'registrations.json').read_text())
for s in sources.values():assert hashlib.sha256((ROOT/s['source'].removeprefix('res://')).read_bytes()).hexdigest()==s['sha256']
for name in ['scripts/room_card_art.gd','scripts/grid_canvas.gd']:
    p=ROOT/name;s=p.read_text()
    for rid in ['corridor','corner','tee_corridor']:
        target='res://assets/corridor-wall-variants-v1/cards/'+rid+'.png'
        pattern=r'("'+rid+r'":\s*\[?")res://[^"\n]+\.png(")'
        s,n=re.subn(pattern,lambda m:m[1]+target+m[2],s)
        assert n==(1 if name.endswith('room_card_art.gd') else 2),(name,rid,n)
        for v in [1,2]:
            s=s.replace(f'res://assets/riser-departments-v1/cards/{rid}-{v}.png',f'res://assets/corridor-wall-variants-v1/cards/{rid}-{v}.png')
    p.write_text(s)
(pack/'manifest.json').write_text(json.dumps({'sources':sources,'variants':records,'integration':'Shared low hull and raised wall renderers, nine card variants, existing art_variant selection','geometry':'Existing authoritative corridor hulls and openings retained; angled faces and neighbor culling retained; north entry faces are windowless closed doors','review':'Native review complete; owner acceptance pending'},indent=2)+'\n')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Corridor & corner walls</title><style>
*{box-sizing:border-box}body{margin:0;background:#13282e;color:#dce4db;font:16px system-ui}main{max-width:1550px;margin:36px auto;padding:0 22px}h1{font-size:36px;font-weight:550}p{max-width:950px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px}article{border:1px solid #486361;background:#20373b;border-radius:8px;padding:14px}h2{text-transform:capitalize;font-size:21px}img{width:100%;display:block}button,select{background:#31534f;border:1px solid #6a8880;color:inherit;padding:10px;border-radius:5px}textarea{width:100%;min-height:80px;background:#162c31;color:inherit;border:1px solid #57726d;padding:10px}nav{display:flex;gap:12px;position:sticky;top:0;background:#13282efa;padding:14px 0;z-index:1}small{color:#aac2b9}details{margin:20px 0}summary{cursor:pointer}</style><main>
<h1>Corridor &amp; corner walls</h1><p>Six new wall designs: transit, utility and observation, each with a dedicated straight and turning-bay treatment. Corners and T-junctions share the turning-bay family. All three shapes have three variants, already connected to the game's existing art variation selection.</p><p>Review the walls in every rotation, switch between raised and low walls, and export your notes. The observation windows stay on upright wall faces; quiet structural panels cover the low hull. Floor drains, cables, pipes and legacy mounted overlays are removed. Windows are centered in the riser; exposed north-facing entries use a door and no windows. Artwork follows existing angled corners and doorway geometry.</p>
<nav><button id="height">Show low walls</button><button id="rotate">Rotate all</button><button id="export">Export notes</button></nav><section class="grid" id="grid"></section>
<details><summary>Six original source designs</summary><section class="grid" id="sources"></section></details><p><small>Native checks cover all 72 raised/low rotation views, source registration, fitting bounds and neighbor culling. Source illustrations are unchanged; runtime uses registered sections. Owner visual acceptance pending.</small></p></main><script>
const records=RECORDS,sources=SOURCES,key='corridor-wall-variants-v1-notes';let notes=JSON.parse(localStorage.getItem(key)||'{}'),raised=true;
for(const r of records){const id=r.id+'-'+r.number,c=document.createElement('article');c.dataset.id=id;c.innerHTML=`<h2>${r.id.replaceAll('_',' ')} · ${r.variant}</h2><select aria-label="Rotation for ${id}">${[0,1,2,3].map(q=>`<option value="${q}">Rotation ${q+1}</option>`).join('')}</select><a target="_blank"><img loading="lazy" alt="${id} native wall view"></a><textarea aria-label="Notes for ${id}" placeholder="Notes or fixes…"></textarea>`;let q=r.id==='corridor'?1:0;const select=c.querySelector('select');select.value=q;c.show=()=>{q=+select.value;const path=r.frames[q*2+(raised?0:1)];c.querySelector('img').src=path;c.querySelector('a').href=path};select.onchange=c.show;const note=c.querySelector('textarea');note.value=notes[id]||'';note.oninput=()=>{notes[id]=note.value;localStorage.setItem(key,JSON.stringify(notes))};c.show();document.querySelector('#grid').append(c)}
document.querySelector('#height').onclick=()=>{raised=!raised;document.querySelector('#height').textContent=raised?'Show low walls':'Show raised walls';document.querySelectorAll('#grid article').forEach(c=>c.show())};document.querySelector('#rotate').onclick=()=>document.querySelectorAll('#grid article').forEach(c=>{const s=c.querySelector('select');s.value=(+s.value+1)%4;c.show()});
for(const id of Object.keys(sources)){const c=document.createElement('article');c.innerHTML=`<h2>${id.replaceAll('-',' ')}</h2><a target="_blank" href="../../assets/corridor-wall-variants-v1/${id}/source.png"><img loading="lazy" src="../../assets/corridor-wall-variants-v1/${id}/source.png" alt="${id} source illustration"></a>`;document.querySelector('#sources').append(c)}
document.querySelector('#export').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(notes,null,2)],{type:'application/json'}));a.download='corridor-wall-notes.json';a.click();URL.revokeObjectURL(a.href)};</script></html>'''.replace('RECORDS',json.dumps(records)).replace('SOURCES',json.dumps(sources))
(out/'index.html').write_text(html,encoding='utf-8')
for r in records:
    for f in r['frames']:assert (out/f).is_file()
print('Nine cards installed, six source hashes verified, 72 review image links valid')
