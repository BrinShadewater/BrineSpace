"""Freeze Veld's catalog and literal override selection; no runtime mutations."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
loader=ROOT/'scripts/grid_canvas.gd'
text=loader.read_text(encoding='utf-8')
branch=text.split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
catalog_path=ROOT/'character/dr-veld-v2/catalog.json'
catalog=json.loads(catalog_path.read_text()); selected={'bare':{},'helmet':{}}; order=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,variant):
    p=ROOT/path;m=json.loads(p.read_text());order.append({'variant':variant,'manifest':path,'sha256':sha(p)})
    for s in m['states']:
        files=[(ROOT/f.removeprefix('res://')).resolve() if f.startswith('res://') else (p.parent/f).resolve() for f in s['frameFiles']]
        selected[variant][s['id']]={'manifest':path,'pivot':m.get('pivot',[46,86]),'standingHeight':m.get('standingHeight',74),'frameCount':len(files),'durationMs':sum(s['frameDurationsMs']),'loop':s['loop'],'files':[f.relative_to(ROOT).as_posix() for f in files],'hashes':[sha(f) for f in files],'visual_master_review':'unproven_by_inventory'}
for variant,key in [('bare','body'),('helmet','equipment')]:
    for path in catalog[key]:load('character/dr-veld-v2/'+path,variant)
for match in re.finditer(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',branch):
    load(match[2],'bare' if match[1]=='load_manifest' else 'helmet')
failures=[]
for variant,states in selected.items():
    for state,data in states.items():
        for path in data['files']:
            with Image.open(ROOT/path) as im:
                if im.mode!='RGBA':failures.append({'path':path,'problem':'not RGBA'})
for variant,states in selected.items():
    # All sampled frames are aligned by declared pivot/standingHeight. No pose height normalization.
    ids=sorted(states)
    pages=[]
    for start in range(0,len(ids),12):
        subset=ids[start:start+12];out=Image.new('RGBA',(720,len(subset)*210),'#202a30');d=ImageDraw.Draw(out)
        for row,key in enumerate(subset):
            data=states[key];d.text((6,row*210+4),key,fill='white')
            for col,i in enumerate([0,len(data['files'])//2,len(data['files'])-1]):
                im=Image.open(ROOT/data['files'][i]).convert('RGBA');scale=148/data['standingHeight'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
                x=col*240+120-round(data['pivot'][0]*scale);y=row*210+195-round(data['pivot'][1]*scale)
                out.alpha_composite(im,(x,y));d.text((col*240+6,row*210+21),str(i),fill='#a3b7c2')
        name=f'{variant}-{start//12:02}.png';out.save(HERE/name);pages.append(name)
    selected[variant]['_pages']=pages
result={'scope':'catalog plus literal Veld overrides in current grid_canvas loader; inventory is not visual acceptance','loaderSha256':sha(loader),'catalogSha256':sha(catalog_path),'order':order,'selected':selected,'failures':failures,'staged_uninstalled':[],'master_identity_completion':False}
(HERE/'coverage.json').write_text(json.dumps(result,indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld full-set consistency inventory</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}a{color:#8cc6e7}img{max-width:100%}</style><h1>Veld selected full-set inventory</h1><p>First, middle and last slot per selected state, aligned by manifest pivot and standingHeight. These snapshots establish coverage and locate drift; they do not establish complete motion or visual acceptance. Master-derived cargo turns and coherent water locomotion/actions/distress/recovery plus cardinal wet death families are selected. Inherited dry rest/life/death still need renewed source and runtime review.</p>'
for variant,states in selected.items():
    html+=f'<h2>{variant}: {len(states)-1} states</h2>'
    for page in states['_pages']:html+=f'<p><img src="{page}"></p>'
(HERE/'index.html').write_text(html)
print(json.dumps({'states':{v:len(s)-1 for v,s in selected.items()},'selected_frames':sum(s['frameCount'] for states in selected.values() for k,s in states.items() if k!='_pages'),'failures':len(failures),'visual_acceptance':'unproven'}))
