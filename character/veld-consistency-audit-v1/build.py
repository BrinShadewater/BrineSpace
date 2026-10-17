"""Read-only comparison of Veld's current selections and staged fitting v13."""
import hashlib,json,re
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
HERE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
selected={'bare':{},'helmet':{}}; manifests=[]
def load(path,variant):
    data=read(path);manifests.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
    for state in data['states']:
        files=[path.parent/f for f in state['frameFiles']]
        selected[variant][state['id']]={'files':files,'pivot':data['pivot'],'manifest':path.relative_to(ROOT).as_posix(),'selection':'retained' if 'dr-veld-v2' in str(path) else 'revised_installed','durations':state['frameDurationsMs']}
catalog=read(ROOT/'character/dr-veld-v2/catalog.json')
for variant,key in [('bare','body'),('helmet','equipment')]:
    for entry in catalog[key]:load(ROOT/'character/dr-veld-v2'/entry,variant)
loader=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
block=loader.split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
for line in block.splitlines():
    m=re.search(r'"res://([^"]+manifest.json)"',line)
    if m:load(ROOT/m[1],'helmet' if 'load_equipment_manifest' in line else 'bare')
candidate=read(ROOT/'character/veld-helmet-fitting-east-v1/manifest.json')
candidate_frames=[ROOT/'character/veld-helmet-fitting-east-v1'/f for f in candidate['states'][0]['frameFiles']]
inventory={};checked=0
for variant,rows in selected.items():
    inventory[variant]={}
    for key,row in rows.items():
        hashes=[]
        for p in row['files']:
            with Image.open(p) as im:im.verify()
            hashes.append(sha(p));checked+=1
        inventory[variant][key]={**{k:v for k,v in row.items() if k!='files'},'files':[p.relative_to(ROOT).as_posix() for p in row['files']],'hashes':hashes}
def aligned(path,pivot,size=(224,232),anchor=(112,208)):
    im=Image.open(path).convert('RGBA');out=Image.new('RGBA',size)
    out.alpha_composite(im,(round(anchor[0]-pivot[0]),round(anchor[1]-pivot[1])))
    return out
def card(draw,sheet,x,y,path,pivot,label,w=160,h=194,large=False):
    im=aligned(path,pivot,(320,400),(160,250)) if not large else aligned(path,pivot)
    if large:small=im
    else:small=im.resize((128,160),Image.Resampling.LANCZOS)
    sheet.paste(small,(x+(w-small.width)//2,y+30),small)
    draw.text((x+3,y+3),label[:26],fill='white')
pages=[]
for variant in selected:
    for selection in ['revised_installed','retained']:
        rows=[(key,row) for key,row in selected[variant].items() if row['selection']==selection]
        for offset in range(0,len(rows),24):
            chunk=rows[offset:offset+24]
            sheet=Image.new('RGB',(160*8,194*6),'#202a30');d=ImageDraw.Draw(sheet)
            for j,(key,row) in enumerate(chunk):
                for k,index in enumerate([0,len(row['files'])//2]):
                    n=j*2+k;card(d,sheet,(n%8)*160,(n//8)*194,row['files'][index],row['pivot'],f'{key} [{index}]')
            name=f'{variant}-{selection}-{offset//24+1}.png';sheet.save(HERE/name);pages.append((f'{variant} / {selection} / {offset//24+1}',name))
# A large east comparison reveals density and silhouette changes hidden by averages.
items=[]
for variant in ['bare','helmet']:
    for key in ['idle-east','walk-east','interact-east','kneel-east','repair-east','stand-east']:
        if key in selected[variant]:
            row=selected[variant][key];i=0 if key.startswith('idle') else len(row['files'])//2
            items.append((variant+' '+key,row['files'][i],row['pivot']))
items +=[(f'staged fit {i}',p,candidate['pivot']) for i,p in enumerate(candidate_frames)]
sheet=Image.new('RGB',(224*5,262*4),'#202a30');d=ImageDraw.Draw(sheet)
for j,(label,p,pivot) in enumerate(items):card(d,sheet,(j%5)*224,(j//5)*262,p,pivot,label,224,262,True)
sheet.save(HERE/'east-reference-and-candidate.png')
# Selected walk/action playback in all directions, without touching runtime art.
gifs=[]
for variant in ['bare','helmet']:
    for direction in ['east','west','south','north']:
        frames=[];durations=[]
        for key in [f'idle-{direction}',f'walk-{direction}',f'interact-{direction}',f'kneel-{direction}',f'repair-{direction}',f'stand-{direction}',f'idle-{direction}']:
            row=selected[variant][key]
            indices=[0] if key.startswith('idle') else range(len(row['files']))
            for i in indices:
                im=aligned(row['files'][i],row['pivot']);bg=Image.new('RGB',im.size,'#202a30');bg.paste(im,mask=im);frames.append(bg)
                durations.append(650 if key.startswith('idle') else round(row['durations'][i]))
        name=f'{variant}-{direction}.gif';frames[0].save(HERE/name,save_all=True,append_images=frames[1:],duration=durations,loop=0);gifs.append((variant+' '+direction,name))
report={'scope':'Current catalog + explicit loader overrides; derived runtime joins omitted. All selected PNGs decoded/hashed, first/middle contact samples per state; eight directional core sequences packaged for visual review. Staged v13 compared separately.','loader_sha256':sha(ROOT/'scripts/grid_canvas.gd'),'manifests':manifests,'selected':inventory,'frame_references_checked':checked,'counts':{v:{s:sum(r['selection']==s for r in rows.values()) for s in ['revised_installed','retained']} for v,rows in selected.items()},'candidate_status':'staged; owner consistency concern; not installed'}
(HERE/'inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Veld consistency audit</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{max-width:100%;margin:12px 0}a{color:#8cc6e7}section{border-top:1px solid #57616b;padding:16px 0}</style><h1>Veld consistency audit</h1><p>Current installed selections are the reference. The fitting candidate remains staged. Contact sheets show first and middle samples, not every pose or a certification of the retained library.</p><h2>East: selected references and staged fitting</h2><img src="east-reference-and-candidate.png"><p><a href="FINDINGS.md">Findings and next step</a> / <a href="inventory.json">Exact selection inventory</a></p><h2>Current core animations</h2>'
for label,name in gifs:html+=f'<section><h3>{label}</h3><img src="{name}" height="232"><img src="{name}" height="128"><img src="{name}" height="85"></section>'
html+='<h2>Whole-library contact samples</h2>'
for label,name in pages:html+=f'<section><h3>{label}</h3><a href="{name}"><img src="{name}" loading="lazy"></a></section>'
summary='<p><strong>Finding: v13 has drifted beyond color.</strong> Its smoother face/hair, darker flatter cloth and harder helmet highlights differ from selected idle/walk. Older retained actions also vary. The next fitting revision should start from the accepted east identity and helmet source.</p><p>340 selected states / 2,932 frame references checked. Contact samples inspected; full-library motion acceptance remains open.</p>'
html=html.replace('<h2>East: selected references and staged fitting</h2>',summary+'<h2>East: selected references and staged fitting</h2>')
(HERE/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'counts':report['counts'],'frame_references_checked':checked,'contact_sheets':len(pages),'directional_sequences':len(gifs)}))
