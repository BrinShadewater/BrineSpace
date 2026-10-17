from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
coverage=json.loads((R/'character/james-locker-continue-v1/runtime-coverage.json').read_bytes());inputs={};records=[];clips=[];images={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(mode,key):
 f=R/coverage[mode][key]['path'];inputs[f.relative_to(R).as_posix()]=sha(f);m=json.loads(f.read_bytes());s=next(s for s in m['states'] if s['id']==key)
 assert m['standingHeight']==148
 out=[]
 for i,rel in enumerate(s['frameFiles']):
  p=R/rel.removeprefix('res://') if rel.startswith('res://') else (f.parent/rel).resolve();inputs[p.relative_to(R).as_posix()]=sha(p)
  im=Image.open(p).convert('RGBA');plane=Image.new('RGBA',(512,512));plane.alpha_composite(im,(256-round(m['pivot'][0]),256-round(m['pivot'][1])));out.append(plane)
  records.append({'mode':mode,'key':key,'index':i,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'pivot':m['pivot'],'size':im.size,'standingHeight':m['standingHeight'],'durationMs':s['frameDurationsMs'][i]})
 return m,s,out
for d in ['north','west']:
 for action in ['tread','swim-start','swim','swim-stop']+(['death-water'] if d=='west' else []):
  key=action+'-'+d;frames={};durations=None
  board=Image.new('RGB',(6*256,2*330),'#303b40');draw=ImageDraw.Draw(board)
  for row,mode in enumerate(['body','equipment']):
   m,s,ims=load(mode,key);images[(mode,key)]=ims
   if durations is None:durations=s['frameDurationsMs']
   else:assert durations==s['frameDurationsMs']
   files=[]
   for i,im in enumerate(ims):
    crop=im.crop((128,150,384,450));f=P/f'{mode}-{key}-{i:03d}.png';crop.save(f);files.append(f.name)
    board.paste(crop,(i*256,row*330+25),crop);draw.text((i*256+4,row*330+4),mode+' '+key+' '+str(i),fill='white')
   frames[mode]=files
  assert len(frames['body'])<=6
  board.save(P/(key+'-all-poses.png'))
  clips.append({'key':key,'frames':frames,'durationsMs':durations,'cycleMs':sum(durations),'finite':action in ['swim-start','swim-stop','death-water']})
masters={}
for d in ['north','west']:
 for mode in ['body','equipment']:
  m,s,ims=load(mode,'idle-'+d);im=ims[0];out=Image.new('RGBA',(512,512));out.alpha_composite(im,(0,144));f=P/f'{mode}-master-{d}.png';out.crop((128,150,384,450)).save(f);masters[mode+'-'+d]=f.name
# Compare full alpha/RGBA in the shared anchor plane, not cropped silhouettes.
joins=[]
for mode in ['body','equipment']:
 for d in ['north','west']:
  for label,a,b in [('start->swim',images[mode,'swim-start-'+d][-1],images[mode,'swim-'+d][0]),('swim->stop',images[mode,'swim-'+d][0],images[mode,'swim-stop-'+d][0])]+([('swim->death',images[mode,'swim-west'][0],images[mode,'death-water-west'][0])] if d=='west' else []):
   joins.append({'mode':mode,'direction':d,'join':label,'registeredRGBAExact':a.tobytes()==b.tobytes()})
inputs['scripts/grid_canvas.gd']=sha(R/'scripts/grid_canvas.gd')
(P/'source-inputs-before.json').write_text(json.dumps(inputs,indent=2)+'\n')
data={'clips':clips,'masters':masters};(P/'playback.json').write_text(json.dumps(data,indent=2)+'\n')
(P/'pose-evidence.json').write_text(json.dumps({'records':records,'joins':joins,'sourceReferences':len(records),'scope':'Every selected North/West tread/start/swim/stop and West water-death source pose, both gears; original manifest durations and declared148 ruler/pivots. Source playback only, not native route or mortality video. Standing masters shown separately, no per-pose rescale.'},indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>James water motion and masters</title><style>body{background:#303b40;color:#eef3f4;font:16px system-ui;margin:20px}button,select{font:inherit;padding:6px}main{display:flex;gap:18px}figure{margin:6px;text-align:center}img{width:256px;height:300px;object-fit:contain}.small img{width:142px;height:166px}p{max-width:1050px}output{display:block;margin:10px}</style><h2>James water motion and masters</h2><p>Original source timing and scale. Water anchors remain fixed; standing masters are separate references. Both gears use the same body ruler.</p><select id="clip" aria-label="Animation"></select> <button id="toggle">Pause</button> <button id="restart">Restart</button><output id="clock"></output><main><figure><figcaption>Bare motion</figcaption><img id="body"></figure><figure><figcaption>Helmet motion</figcaption><img id="equipment"></figure><figure><figcaption>Bare master</figcaption><img id="bm"></figure><figure><figcaption>Helmet master</figcaption><img id="hm"></figure></main><main class="small"><figure><figcaption>82px ruler · bare</figcaption><img id="bs"></figure><figure><figcaption>82px ruler · helmet</figcaption><img id="hs"></figure></main><p>Finite clips hold their last pose for two seconds before replaying. Loop clips replay directly. This view does not simulate travel, depth, mortality or room lighting.</p><script>fetch('playback.json').then(r=>r.json()).then(data=>{const select=document.querySelector('#clip');data.clips.forEach((c,i)=>select.add(new Option(c.key,i)));let paused=false,t=0,last=performance.now();document.querySelector('#toggle').onclick=()=>{paused=!paused;document.querySelector('#toggle').textContent=paused?'Play':'Pause'};document.querySelector('#restart').onclick=()=>{t=0};select.onchange=()=>{t=0};const set=(id,src)=>{document.getElementById(id).src=src};function paint(now){if(!paused)t+=now-last;last=now;const c=data.clips[+select.value],time=t%(c.cycleMs+(c.finite?2000:0));let sum=0,index=c.durationsMs.length-1;for(let i=0;i<c.durationsMs.length;i++){sum+=c.durationsMs[i];if(time<sum){index=i;break}}set('body',c.frames.body[index]);set('equipment',c.frames.equipment[index]);set('bs',c.frames.body[index]);set('hs',c.frames.equipment[index]);const d=c.key.endsWith('north')?'north':'west';set('bm',data.masters['body-'+d]);set('hm',data.masters['equipment-'+d]);document.querySelector('#clock').textContent=c.key+' · '+(time/1000).toFixed(2)+'s · pose '+index+' / '+c.durationsMs.length+' · '+(paused?'paused':'playing');requestAnimationFrame(paint)}requestAnimationFrame(paint)});</script>'''
(P/'index.html').write_text(html,encoding='utf-8')
after={f:sha(R/f) for f in inputs};assert inputs==after;(P/'source-inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
print(json.dumps({'clips':len(clips),'references':len(records),'inputsUnchanged':len(inputs),'joins':joins}))
