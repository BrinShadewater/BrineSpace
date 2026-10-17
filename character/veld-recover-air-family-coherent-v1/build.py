"""Consolidate independent directional recovery sources without regrading frames."""
from pathlib import Path
import json,hashlib,copy
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
DIRS=['east','west','north','south']
def main():
 packs={};bindings={};checks=0
 registry=json.loads((ROOT/'character/ACTIVE_ASSETS.json').read_text())
 installed=registry.get('actionOverrides',{}).get('veld-dry-recovery-family')==f'character/{P.name}/bare-manifest.json' and registry.get('equipmentActionOverrides',{}).get('veld-dry-recovery-family')==f'character/{P.name}/helmet-manifest.json'
 board=Image.new('RGB',(1536,280*8),'#23313a');d=ImageDraw.Draw(board)
 for gi,gear in enumerate(['bare','helmet']):
  states=[]
  for di,direction in enumerate(DIRS):
   src=P.parent/f'veld-recover-air-{direction}-coherent-v1';name='manifest.json' if gear=='bare' else 'helmet-manifest.json';m=json.loads((src/name).read_text());s=copy.deepcopy(m['states'][0]);refs=[]
   assert s['id']==f'recover-air-{direction}' and s['frameDurationsMs']==[500]*6 and not s['loop'];checks+=1
   for i,file in enumerate(s['frameFiles']):
    f=src/file;path=f.relative_to(ROOT).as_posix();refs.append('res://'+path);bindings[path]=hashlib.sha256(f.read_bytes()).hexdigest()
    im=Image.open(f).convert('RGBA');assert im.size==(256,256);checks+=1
    y=(gi*4+di)*280;board.paste(im,(i*256,y),im);d.text((i*256+4,y+4),f'{gear} {direction} {i}',fill='white')
   s['frameFiles']=refs;states.append(s)
  m.update(name='Veld independent dry recovery family '+gear,status='installed_locally_pending_full_set_polish' if installed else 'staged_candidate',states=states)
  (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
  packs[gear]=copy.deepcopy(states)
  for s in packs[gear]:s['frameFiles']=['../'+f.removeprefix('res://character/') for f in s['frameFiles']]
 board.save(P/'family-contact.png')
 (P/'source-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
 (P/'family-checks.json').write_text(json.dumps({'passed':True,'checks':checks,'states':8,'references':48,'scope':'consolidation dimensions,finite3smetadata,sourcehashbindings;individual candidate/native evidence separate'},indent=2)+'\n')
 html='''<!doctype html><meta charset="utf-8"><title>Veld dry recovery family</title><style>body{background:#23313a;color:#edf2f4;font:16px system-ui;margin:24px}p{max-width:78ch}button,select{font:inherit;padding:8px}canvas{display:block}a{color:#9ad4e8}</style><h1>Veld — dry breathing recovery family</h1><p>Four independently authored views, bare and helmet. Exact selected idle at entry and exit, planted boots, shared source ruler per direction and master-matched materials. Three-second finite recovery. Staged: real low-air journeys, restores, clearance and runtime selection remain.</p><select id="direction"><option>east</option><option>west</option><option>north</option><option>south</option></select> <select id="gear"><option>bare</option><option>helmet</option></select> <button id="play">Pause</button> <button id="step">Next pose</button> <span id="status"></span><canvas id="view" width="720" height="480"></canvas><p><a href="family-contact.png">All48frames</a></p><script>const packs=DATA;let running=true,t=0,last=performance.now(),slot=0;function selected(){return packs[gear.value].find(s=>s.id==='recover-air-'+direction.value)}play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};step.onclick=()=>{running=false;play.textContent='Play';slot=(slot+1)%6};gear.onchange=direction.onchange=()=>{t=0;slot=0};Promise.all(Object.values(packs).flat().map(async s=>{s.images=await Promise.all(s.frameFiles.map(f=>new Promise((yes,no)=>{let im=new Image;im.onload=()=>yes(im);im.onerror=no;im.src=f})))})).then(()=>{function draw(now){if(running)t+=now-last;last=now;if(running)slot=Math.min(5,Math.floor((t%3600)/500));let c=view.getContext('2d');c.fillStyle='#23313a';c.fillRect(0,0,720,240);c.fillStyle='#dce4e5';c.fillRect(0,240,720,240);for(let row=0;row<2;row++){let x=20;for(let h of [148,82,54]){let scale=h/148;c.drawImage(selected().images[slot],x,230+row*240-224*scale,256*scale,256*scale);x+=256*scale+20}}status.textContent='Frame '+slot+' / 5';requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
 if installed:html=html.replace('Staged: real low-air journeys, restores, clearance and runtime selection remain.','Selected locally. Real low-air/restore checks cover the family; full-set motion, helmet pitch and broader contextual polish remain.')
 (P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
 print(f'{checks} consolidation checks PASS;8states/48 source references;no pixel rewrite')
if __name__=='__main__':main()
