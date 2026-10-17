"""Consolidate reviewed cardinal cargo loops without changing pixels or runtime."""
from pathlib import Path
import json,re,hashlib,shutil
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
selected={'bare':{},'helmet':{}}
installed=json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'))['actionOverrides'].get('veld-water-cargo')=='character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json'
def read(path,gear):
 p=R/path;m=json.loads(p.read_text())
 for s in m['states']:selected[gear][s['id']]=dict(manifest=path,files=[(p.parent/f).resolve() for f in s['frameFiles']])
catalog=json.loads((R/'character/dr-veld-v2/catalog.json').read_text())
for gear,key in [('bare','body'),('helmet','equipment')]:
 for p in catalog[key]:read('character/dr-veld-v2/'+p,gear)
branch=(R/'scripts/grid_canvas.gd').read_text().split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
for method,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',branch):read(path,'bare' if method=='load_manifest' else 'helmet')
baseline=json.loads((R/'character/veld-water-cargo-master-audit-v1/current-selection.json').read_text())
proof={};sources={};manifests={};checks=0
board=Image.new('RGBA',(1792,1600),'#202a30');draw=ImageDraw.Draw(board)
for gi,gear in enumerate(['bare','helmet']):
 states=[];profile=None
 for di,direction in enumerate(['east','west','north','south']):
  family=R/f'character/veld-swim-carry-{direction}-coherent-v1';mp=family/f'{gear}-manifest.json';m=json.loads(mp.read_text());state=m['states'][0].copy()
  profile=profile or {k:v for k,v in m.items() if k not in ['states','name','status']}
  assert all(m[k]==v for k,v in profile.items());checks+=1
  native=json.loads((family/'native-candidate-v1-checks.json').read_text());pack=json.loads((family/'packaging-checks.json').read_text())
  assert native['failures']==0 and native['engine_errors']==[] and native['real_profile_changed_files']==[] and pack['failures']==0;checks+=1
  current=selected[gear]['swim-carry-'+direction];old=baseline['records'][gear+'/'+direction]
  expected_manifest=f'character/veld-swim-carry-matrix-coherent-v1/{gear}-manifest.json' if installed else old['manifest']
  expected_hashes=[sha(family/f) for f in state['frameFiles']] if installed else old['hashes']
  assert current['manifest']==expected_manifest and [sha(p) for p in current['files']]==expected_hashes;checks+=1
  proof[gear+'/'+direction]=dict(manifest=current['manifest'],hashes=expected_hashes,selectedUnchanged=not installed,selectedInstalled=installed)
  files=[];row=(gi*4+di)*200
  for i,f in enumerate(state['frameFiles']):
   source=family/f;dest=H/f'frames/{gear}/swim-carry-{direction}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True)
   assert sha(source)==native['frameHashes'][f]==pack['frameHashes'][f];checks+=1
   shutil.copyfile(source,dest);assert sha(source)==sha(dest);checks+=1
   rel=dest.relative_to(H).as_posix();files.append(rel);sources[rel]=dict(source=source.relative_to(R).as_posix(),sha256=sha(source),nativeEvidence=(family/'native-candidate-v1-checks.json').relative_to(R).as_posix())
   board.alpha_composite(Image.open(dest).convert('RGBA'),(i*256,row-15));draw.text((i*256+4,row+5),f'{gear} {direction} cargo {i}',fill='white')
  master=selected[gear]['swim-'+direction]['files'][0];dest=H/f'masters/{gear}-{direction}.png';dest.parent.mkdir(exist_ok=True);shutil.copyfile(master,dest)
  sources[dest.relative_to(H).as_posix()]=dict(source=master.relative_to(R).as_posix(),sha256=sha(master),selectedMaster=True)
  board.alpha_composite(Image.open(dest).convert('RGBA'),(1536,row-15));draw.text((1540,row+5),'selected swim master',fill='white')
  state['frameFiles']=files;states.append(state)
 manifests[gear]={**profile,'name':'Veld coherent cardinal water cargo '+gear,'status':('installed_locally_pending_full_set_polish' if json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'))['actionOverrides'].get('veld-water-cargo')=='character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json' else 'staged_all_cardinals_pending_action_turn_world_joins'),'states':states}
 (H/f'{gear}-manifest.json').write_text(json.dumps(manifests[gear],indent=2)+'\n')
board.save(H/'family-master-comparison-v1.png')
(H/'family-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=installed,currentCargo=proof,loaderSha256=sha(R/'scripts/grid_canvas.gd'),sources=sources,scope='Fresh ordered selection trace, exact consolidation of48 currently native-checked cargo refs and8 selected masters; independent motion/world acceptance required'),indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Veld four-direction water cargo</title><style>body{background:#202a30;color:#e5ebed;font:16px sans-serif;margin:24px}a{color:#8cc6e7}canvas,img{max-width:100%;height:auto}button,select,input{margin:8px}</style><h1>Veld — four-direction water cargo</h1><p>All four independently authored views beside their selected swimming masters. Bare and helmet share one840ms clock. Fixed anatomical rulers, compact case and shared directional helmets. Staged; action/turn joins and complete world journeys remain.</p><button id="play">Pause</button><label>Frame <input id="phase" aria-label="Frame" type="range" min="0" max="5" value="0"></label><label>Speed <select id="speed"><option value="1">Full speed</option><option value="0.3333333333">One-third speed</option></select></label><label>Background <select id="bg"><option value="#202a30">Dark</option><option value="#a7afb2">Light</option></select></label><span id="clock"></span><canvas id="canvas" width="1280" height="700"></canvas><p><a href="family-master-comparison-v1.png">All48cargo phases and8masters at identical148ruler</a> · <a href="family-checks.json">Fresh selection and pixel provenance</a></p><script>const data=DATA;let phase=0,running=true,elapsed=0,last=performance.now();const ctx=canvas.getContext('2d'),images={};async function init(){for(const g of ['bare','helmet']){images[g]=[];for(const s of data[g].states){images[g].push(await Promise.all([...s.frameFiles,'masters/'+g+'-'+s.id.replace('swim-carry-','')+'.png'].map(url=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(im);im.src=url}))))}}requestAnimationFrame(tick)}function draw(){ctx.fillStyle=bg.value;ctx.fillRect(0,0,1280,700);ctx.fillStyle='#e5ebed';ctx.font='15px sans-serif';for(let d=0;d<4;d++){ctx.fillText(['east','west','north','south'][d],d*320+12,20);for(let g=0;g<2;g++){const gear=g?'helmet':'bare',y=g*340+20;for(const [slot,x] of [[phase,2],[6,160]]){ctx.drawImage(images[gear][d][slot],d*320+x,y,148,148);ctx.fillText(slot===6?'swim master':gear+' cargo',d*320+x+5,y+170)}for(const [slot,x] of [[phase,2],[6,160]])ctx.drawImage(images[gear][d][slot],d*320+x,y+190,82,82)}}clock.textContent='Phase '+(phase+1)+' /6 · '+Math.round(elapsed)+'ms /840ms';document.getElementById('phase').value=phase}function tick(t){if(running){elapsed=(elapsed+(t-last)*Number(speed.value))%840;phase=Math.floor(elapsed/140)}last=t;draw();requestAnimationFrame(tick)}play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};document.getElementById('phase').oninput=e=>{running=false;play.textContent='Play';phase=Number(e.target.value);elapsed=phase*140;draw()};init()</script>'''
if installed:html=html.replace('Staged; action/turn joins and complete world journeys remain.','Selected locally; native journeys and phase restores checked. Broader safety/traffic and full-set polish remain.')
(H/'index.html').write_text(html.replace('DATA',json.dumps(manifests)),encoding='utf-8')
print(f'{checks} consolidation/current-selection checks PASS;48cargo refs/8masters, runtime unchanged.')
