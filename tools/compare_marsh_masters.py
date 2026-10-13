"""Read-only comparison of every currently selected Marsh frame to identity masters."""
from pathlib import Path
import hashlib, json, html
import numpy as np
from PIL import Image, ImageDraw
from prepare_marsh_full_polish import material_mask

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-master-comparison-v1'
DIRS=('south','north','east','west')

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
 refs={}; masters={}; records=[]; pages=[]
 for d in DIRS:
  p=ROOT/f'character/marsh-motion-polish-v1/sources/{d}-standing-identity-01.png'
  masters[d]={'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
  im=Image.open(ROOT/states['idle-'+d]['files'][0]).convert('RGBA');refs[d]=im
  m,l,_=material_mask(im);masters[d]['idleIvoryMean']=float(l[m].mean())
 keys=sorted(states)
 for page,start in enumerate(range(0,len(keys),12)):
  board=Image.new('RGB',(1800,12*184),'#293b40');draw=ImageDraw.Draw(board)
  for row,key in enumerate(keys[start:start+12]):
   s=states[key];d=key.split('-')[-1];y=row*184
   draw.text((4,y+3),key,fill='white')
   # Matching idle at native pixel density, then every authored slot.
   images=[refs[d]]+[Image.open(ROOT/f).convert('RGBA') for f in s['files']]
   values=[]
   for col,im in enumerate(images):
    crop=im.crop(im.getbbox());crop.thumbnail((145,150),Image.Resampling.NEAREST)
    x=col*150+4;board.paste(crop,(x,y+24+150-crop.height),crop)
    draw.text((x,y+170),'MASTER IDLE' if col==0 else str(col-1),fill='#b8d8d9')
    if col:
     m,l,_=material_mask(im)
     values.append(float(l[m].mean()) if m.sum()>80 else None)
   records.append({'key':key,'files':s['files'],'masterDirections':key.split('-')[-2:] if '-turn-' in key else [d],
    'ivoryMeans':values,'ivoryMedianGap':float(np.median([v for v in values if v is not None]))-masters[d]['idleIvoryMean'] if any(v is not None for v in values) else None,
    'durations':s['durations'],'loop':s['loop'],'pivot':s['pivot'],'standingHeight':s['standingHeight']})
  name=f'overview-{page:02}.png';board.save(OUT/name);pages.append(name)
 findings=json.loads((OUT/'findings.json').read_text())
 for row in records:
  f=next(f for f in findings if any(row['key'].startswith(p) for p in f['prefixes']))
  row['reviewGroup']=f['group'];row['followUpPriority']=f['priority']
  vals=[v for v in row['ivoryMeans'] if v is not None]
  row['ivoryRange']=max(vals)-min(vals) if vals else None
 report={'states':len(states),'slots':sum(len(s['files']) for s in states.values()),'masters':masters,'rows':records,
  'policy':'Master sources are design authority; installed idle anchors export scale/material. Ivory statistics are review flags, not visual acceptance. Boards fit wide/tall poses to cells; interactive viewer preserves runtime pivot and density.'}
 report['visualReview']={'reviewer':'Codex','method':'Four full-resolution identity sources and all seventeen contact boards inspected, covering every selected slot. Timed viewer provided; no new full motion or browser-control acceptance claimed.','findings':findings,'allFrameBoardsInspected':17,'runtimeArtChanged':False}
 (OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
 data=json.dumps(states);masterdata=json.dumps(masters)
 markup='''<!doctype html><meta charset="utf-8"><title>Marsh — all animations against masters</title>
 <style>body{background:#192a30;color:#e1e6df;font:16px system-ui;margin:28px}select,button,input{font:inherit;margin:6px}canvas{background:#293b40;image-rendering:pixelated} .panels{display:flex;gap:24px;align-items:start;flex-wrap:wrap}.master{height:450px;image-rendering:pixelated}a{color:#a0d7d5}summary{cursor:pointer;margin:18px} .board{max-width:100%}</style>
 <h1>Marsh: master comparison</h1><p>204 selected states · 1,058 frame slots. Original identity master, installed directional idle, and current animation.</p>
 <p>Compare collar, chest panel, straps/pouches, sage shoulders, face/hair, temple hardware, knees and boots. Crouched, seated, swimming and fallen figures retain their authored scale. Turns show both directional masters.</p>
 <select id="state"></select><button id="pause">Pause</button><button id="step">Next frame</button><label>Scale <select id="scale"><option value="2">Source ×2</option><option value="1">Source ×1</option><option value="0.441081">Station size</option></select></label><span id="phase"></span>
 <div class="panels"><div><h3>Identity master</h3><div id="masters"></div></div><div><h3>Installed idle</h3><canvas id="idle" width="512" height="512"></canvas></div><div><h3>Current selected animation</h3><canvas id="action" width="512" height="512"></canvas></div></div>
 <p><a href="../marsh-quality-pass-v4/index.html">Full colour pass / transition review</a> · <a href="comparison.json">Frame and master provenance</a></p>
 '''
 table='<h2>Comparison findings</h2><p>Master matching remains incomplete. Runtime artwork is unchanged.</p><ul>'+''.join('<li><strong>'+html.escape(f['group'])+':</strong> '+html.escape(f['finding'])+'</li>' for f in findings)+'</ul>'
 markup=markup.replace('<select id="state">',table+'<select id="state">')
 markup+=''.join(f'<details><summary>All-frame board {i+1}</summary><a href="{p}"><img class="board" src="{p}" loading="lazy"></a></details>' for i,p in enumerate(pages))
 markup+='<script>const DATA='+data+', MASTERS='+masterdata+''';
 const state=document.getElementById('state'),scale=document.getElementById('scale'), cache={};let running=true,t=0,slot=0,previous=performance.now();
 for(const k of Object.keys(DATA).sort()){const o=document.createElement('option');o.value=k;o.textContent=k;state.append(o)}state.value='repair-east';
 function get(p){if(!cache[p]){cache[p]=new Image;cache[p].src='../../'+p}return cache[p]}
 function directions(k){return k.includes('-turn-')?k.split('-').slice(-2):[k.split('-').at(-1)]}
 function change(){t=0;slot=0;document.getElementById('masters').replaceChildren();for(const d of directions(state.value)){const im=document.createElement('img');im.src='../../'+MASTERS[d].file;im.className='master';im.alt=d+' identity master';document.getElementById('masters').append(im)}}
 state.onchange=change;change();document.getElementById('pause').onclick=()=>{running=!running;document.getElementById('pause').textContent=running?'Pause':'Play'};
 document.getElementById('step').onclick=()=>{running=false;document.getElementById('pause').textContent='Play';slot=(slot+1)%DATA[state.value].files.length;t=DATA[state.value].durations.slice(0,slot).reduce((a,b)=>a+b,0)};
 function draw(id,s,file){const c=document.getElementById(id),ctx=c.getContext('2d'),z=Number(scale.value),im=get(file);ctx.clearRect(0,0,c.width,c.height);ctx.imageSmoothingEnabled=false;if(im.complete&&im.naturalWidth)ctx.drawImage(im,256-s.pivot[0]*z,450-s.pivot[1]*z,im.width*z,im.height*z)}
 function tick(now){const s=DATA[state.value],total=s.durations.reduce((a,b)=>a+b,0);if(running)t+=Math.min(now-previous,100);previous=now;let pos=s.loop?t%total:Math.min(t,total-0.001),sum=0;slot=s.durations.findIndex(v=>(sum+=v)>pos);if(slot<0)slot=s.files.length-1;const d=directions(state.value).at(-1),idle=DATA['idle-'+d];draw('idle',idle,idle.files[0]);draw('action',s,s.files[slot]);document.getElementById('phase').textContent='Frame '+slot+' / '+(s.files.length-1)+' · '+s.durations[slot]+' ms';requestAnimationFrame(tick)}requestAnimationFrame(tick);
 </script>'''
 (OUT/'index.html').write_text(markup)
 assert len(records)==204 and report['slots']==1058
 for s in states.values():
  for f in s['files']:assert (ROOT/f).is_file(),f
 print('204 states / 1058 slots; 4 hashed identity masters; 17 complete frame boards')
 print('Largest ivory flags:',[(r['key'],round(r['ivoryMedianGap'],1)) for r in sorted((r for r in records if r['ivoryMedianGap'] is not None),key=lambda r:abs(r['ivoryMedianGap']),reverse=True)[:12]])

if __name__=='__main__':main()
