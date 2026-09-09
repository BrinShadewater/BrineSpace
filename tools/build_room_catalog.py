"""Build an illustrated owner review from fresh native room captures."""
import hashlib, html, json, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from build_material_review_gallery import discover_records

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/room-catalog-2026-09-08'
def local(s): return ROOT/s.removeprefix('res://')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s): return html.escape(str(s),quote=True)
def href(p):
    import os
    return os.path.relpath(p,OUT).replace('\\','/')

def main():
    rooms=json.loads((OUT/'runtime.json').read_text())
    assert len({r['id'] for r in rooms})==len(rooms)
    rooms.sort(key=lambda r:(r['category'],r['name']))
    gd=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
    base=gd.split('var room_texture_paths := {')[1].split('\n}')[0]
    prior=dict(re.findall(r'"([\w]+)": "(res://[^\"]+)"',base))
    selected=dict(re.findall(r'"([\w]+)": "(res://[^\"]+)"',(ROOT/'scripts/room_card_art.gd').read_text(encoding='utf-8')))
    mismatch=[r['id'] for r in rooms if selected.get(r['id'])!=prior.get(r['id'])]
    items=[]
    for i,r in enumerate(rooms,1):
        r['number']=i
        for s in r['images']:
            with Image.open(local(s)) as im: assert im.size==(512,512); im.verify()
        images=''.join(f'<a href="{href(local(s))}" target="_blank"><img loading="lazy" src="{href(local(s))}" alt="{esc(r["name"])} orientation {q}"></a>' for q,s in enumerate(r['images']))
        items.append(f'<article data-search="{esc(r["name"]+" "+r["id"]+" "+r["category"])}"><h2>{i:02d} · {esc(r["name"])}</h2><p class="meta">{esc(r["category"])} · {esc(r["id"])}</p><div class="poses">{images}</div><p>{len(r["images"])} native view(s) · default layout · offline</p><details><summary>Installed renderer and furniture</summary><p>{esc(r["view"])}</p><p>{esc(", ".join(p["id"] for p in r["views"][0]["props"]) if r["views"] else "Three corridor shapes; default decoration variant shown.")}</p></details><textarea data-note="{r["id"]}" aria-label="Notes for {esc(r["name"])}" placeholder="Your notes or fixes…"></textarea></article>')
    candidates=[]
    runtime_text=[]
    for folder in ('rooms','scripts'):
        for p in (ROOT/folder).rglob('*'):
            if p.suffix in ('.gd','.json') and 'manifest' not in p.name:
                runtime_text.append((p,p.read_text(encoding='utf-8',errors='replace')))
    for path,d in discover_records(ROOT):
        export=local(d['export_path'])
        assert export.exists()
        refs=[p.relative_to(ROOT).as_posix() for p,t in runtime_text if d['export_path'] in t]
        findings=[]
        for k,v in d['review'].items():
            if isinstance(v,dict): findings+=v.get('findings',[])
        integration=d['review'].get('integration',{})
        stage=integration.get('stage','unrecorded') if isinstance(integration,dict) else str(integration)
        candidates.append({'id':d['asset_id'],'department':d.get('department',''),'export':d['export_path'],'record':path.relative_to(ROOT).as_posix(),'stage':stage,'references':refs,'hash_matches':sha(export)==d['export_sha256'],'findings':findings})
    candhtml=[]
    for c in candidates:
        candhtml.append(f'<article data-search="{esc(c["id"]+" "+c["department"])}"><h2>{esc(c["id"])}</h2><p class="meta">{esc(c["department"])}</p><a href="{href(local(c["export"]))}" target="_blank"><img class="candidate" loading="lazy" src="{href(local(c["export"]))}" alt="{esc(c["id"])}"></a><p>Recorded stage: {esc(c["stage"])} · {len(c["references"])} direct room/script references</p><details><summary>Review findings and evidence</summary><ul>{"".join("<li>"+esc(f)+"</li>" for f in c["findings"])}</ul><a href="{href(local(c["record"]))}">Source review record</a></details><textarea data-note="asset:{c["id"]}" aria-label="Notes for {esc(c["id"])}" placeholder="Placement or art notes…"></textarea></article>')
    registrations=[]
    for p in sorted((ROOT/'rooms/full-wall-v1/registrations').glob('*.json')):
        d=json.loads(p.read_text(encoding='utf-8'))
        if 'source' not in d or 'sha256' not in d: continue
        src=local(d['source'])
        registrations.append({'registration':p.relative_to(ROOT).as_posix(),'source':d['source'],'hash_matches':src.exists() and sha(src)==d['sha256']})
    (OUT/'registration-audit.json').write_text(json.dumps(registrations,indent=2)+'\n',encoding='utf-8')
    audit={'rooms':len(rooms),'native_images':sum(len(r['images']) for r in rooms),'current_card_grid_mismatches':mismatch,'registrations_checked':len(registrations),'registration_hash_mismatches':sum(not r['hash_matches'] for r in registrations),'standardized_candidates':candidates,'scope':'Native default room layouts, offline stills; excludes personal layouts, animation and crew-route acceptance. Standardized candidate records are a subset of historical source versions.'}
    (OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    style='''*{box-sizing:border-box}body{margin:0;background:#10282c;color:#e1e7df;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:30px}h1{font-size:36px;margin-bottom:4px}h2{font-size:20px}a{color:#abdccc}header{max-width:1050px}.toolbar{position:sticky;top:0;padding:14px 0;background:#10282cf5;z-index:2;display:flex;gap:12px;flex-wrap:wrap}input,button,textarea{font:inherit;color:inherit;background:#203b3f;border:1px solid #77928b;padding:10px;border-radius:5px}input{flex:1;min-width:220px}button{cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:20px}article{background:#1b3438;border:1px solid #47615e;padding:18px;border-radius:8px;min-width:0}article[hidden]{display:none}.meta{color:#b9c6a7}.poses{display:grid;grid-template-columns:repeat(2,1fr);background:#344a4b}.poses>a:first-child{grid-column:1/-1}.poses img{width:100%;display:block;image-rendering:pixelated}.poses>a:only-child{max-width:512px;margin:auto}.candidate{width:100%;height:220px;object-fit:contain;background:#435554}textarea{width:100%;min-height:90px;margin-top:15px}details{overflow-wrap:anywhere}summary{cursor:pointer}#message{color:#c9d99e}@media(max-width:500px){main{padding:12px}.grid{grid-template-columns:1fr}}@media print{.toolbar,textarea,details{display:none}article{break-inside:avoid}}'''
    js='''const key='brinespace-room-review-2026-09-08';let saved={};try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}for(const t of document.querySelectorAll('textarea')){t.value=saved[t.dataset.note]||'';t.addEventListener('input',()=>{saved[t.dataset.note]=t.value;try{localStorage.setItem(key,JSON.stringify(saved));document.querySelector('#message').textContent='Notes saved in this browser. Export a copy to send back.'}catch(e){document.querySelector('#message').textContent='Browser storage unavailable. Export your notes before closing.'}})}document.querySelector('#search').addEventListener('input',e=>{for(const a of document.querySelectorAll('article'))a.hidden=!a.dataset.search.toLowerCase().includes(e.target.value.toLowerCase())});document.querySelector('#export').onclick=()=>{let text='# BrineSpace room art notes\\n\\n';for(const [id,note]of Object.entries(saved))if(note.trim())text+='## '+id+'\\n'+note+'\\n\\n';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'text/markdown'}));a.download='brinespace-art-notes.md';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};'''
    doc=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · Full room art review</title><style>{style}</style><main><header><h1>BrineSpace room art review</h1><p>47 room types · fresh native Godot captures · September 8, 2026</p><p>Each room shows its current installed furniture and available orientations. Click an image for the full 512-pixel capture. These are offline stills with default layouts; animation, connected doors and saved personal arrangements are not shown.</p><p>The newer standalone props follow the room list. Some need furniture relocation or shorter sections before installation. Their review records retain the fit findings.</p><a href="#candidates">Jump to standalone props</a> · <a href="contact-sheet.jpg">All rooms at a glance</a></header><div class="toolbar"><input id="search" type="search" aria-label="Find room, asset or department" placeholder="Find room, asset or department"><button id="export">Export my notes</button></div><p id="message">Notes stay in this browser. Export a copy when ready to send feedback.</p><section class="grid">{"".join(items)}</section><h1 id="candidates">Standalone prop review ({len(candidates)})</h1><p>Standardized recent art records. Preview sizes are fitted for browsing, not a shared world scale. This does not count discarded source iterations as additional assets.</p><section class="grid">{"".join(candhtml)}</section></main><script>{js}</script></html>'
    (OUT/'index.html').write_text(doc,encoding='utf-8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    sheet=Image.new('RGB',(6*260,((len(rooms)+5)//6)*292),(22,42,46)); draw=ImageDraw.Draw(sheet)
    for n,r in enumerate(rooms):
        im=Image.open(local(r['images'][0])).convert('RGBA');im.thumbnail((252,252))
        x=(n%6)*260;y=(n//6)*292
        sheet.paste(im,(x+(260-im.width)//2,y),im)
        label=f'{n+1:02d} {r["name"]}'
        size=20
        while draw.textlength(label,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size))>250: size-=1
        draw.text((x+5,y+254),label,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size),fill=(230,233,215))
    sheet.save(OUT/'contact-sheet.jpg',quality=92)
    links=re.findall(r'(?:src|href)="([^"]+)"',doc)
    missing=[s for s in links if not s.startswith('#') and not (OUT/s).exists()]
    assert not missing,missing
    print(f'{len(links)} local image/evidence links resolve')
    print(json.dumps({k:v for k,v in audit.items() if k!='standardized_candidates'},indent=2))
    print(f'{len(candidates)} candidates; {sum(bool(c["references"]) for c in candidates)} with direct references; {sum(not c["hash_matches"] for c in candidates)} stale hashes')

if __name__=='__main__':
    import sys
    if len(sys.argv)>1: OUT=ROOT/sys.argv[1]
    main()
