"""Build a manifest-driven review; no generated art or inferred coverage."""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parent
packs = {}
for path in sorted((ROOT / 'pilot').glob('*/manifest.json')) + sorted((ROOT / 'locker').glob('*/manifest.json')):
    data = json.loads(path.read_text())
    clip = path.parent.name
    actor = clip.split('-', 1)[0]
    for state in data['states']:
        packs.setdefault(actor, {})[state['id']] = {
            **state, 'pivot': data.get('pivot', [46, 86]),
            'urls': [str(path.parent.relative_to(ROOT) / f).replace('\\', '/') for f in state['frameFiles']],
        }
crew = {'bill':'major-bill-v2','veld':'dr-veld-v1','branforth':'chief-engineer-branforth-v1'}
dry_paths = sorted((ROOT/'equipment/dry').glob('*/manifest.json'))
for path in dry_paths:
    actor, clip = path.parent.name.split('-', 1)
    source_path = ROOT.parent/crew[actor]/'final/manifest.json'
    source = json.loads(source_path.read_text())
    state = next(s for s in source['states'] if s['id'] == clip)
    packs.setdefault(actor, {})[clip] = {
        **state, 'pivot':source['pivot'],
        'urls':[os.path.relpath((source_path.parent/f).resolve(), ROOT).replace('\\', '/') for f in state['frameFiles']],
    }
equipment = {}
for path in sorted((ROOT / 'equipment/fitting').glob('*/manifest.json')) + dry_paths:
    data = json.loads(path.read_text())
    actor = path.parent.name.split('-', 1)[0]
    for state in data['states']:
        base = packs[actor][state['id']]
        assert state['frameDurationsMs'] == base['frameDurationsMs'] and state['loop'] == base['loop']
        assert data['pivot'] == base['pivot'] and len(state['frameFiles']) == len(base['urls'])
        equipment.setdefault(actor, {})[state['id']] = {**state, 'pivot':data['pivot'], 'urls':[str(path.parent.relative_to(ROOT) / f).replace('\\', '/') for f in state['frameFiles']]}
for actor in crew:
    for direction in ['east','west','south','north']:
        if direction=='north' and actor=='veld': continue
        revision = ROOT/'revisions'/f"{actor}-swim-{direction}-{'v3' if actor == 'branforth' and direction == 'north' else 'v2'}"
        for target, path in [(packs,revision/'manifest.json'),(equipment,revision/'helmet/manifest.json')]:
            data=json.loads(path.read_text(encoding='utf-8'))
            for state in data['states']:
                target[actor][state['id']]={**state,'pivot':data['pivot'],'urls':[(path.parent.relative_to(ROOT)/f).as_posix() for f in state['frameFiles']]}

for target,path in [(packs,ROOT/'revisions/veld-tread-south-v2/manifest.json'),(equipment,ROOT/'revisions/veld-tread-south-v2/helmet/manifest.json')]:
    data=json.loads(path.read_text(encoding='utf-8'))
    for state in data['states']:
        target['veld'][state['id']]={**state,'pivot':data['pivot'],'urls':[(path.parent.relative_to(ROOT)/f).as_posix() for f in state['frameFiles']]}

template = '''<!doctype html><meta charset="utf-8"><title>Crew water animation review</title>
<style>body{background:#10191f;color:#d7dfe3;font:16px system-ui;margin:24px}button,select,input{font:inherit;margin:8px;padding:6px}main{display:flex;gap:20px;flex-wrap:wrap}article{background:#1d2931;padding:16px}canvas{image-rendering:pixelated;background:#263740}p{max-width:900px}small{display:block;max-width:290px;color:#b9c8d1}label{white-space:nowrap}</style>
<h1>Crew water animation review</h1><p>Production pilots. Use the shared clock to compare pose registration and apparent scale. Missing clips stay visibly missing. This page checks isolated artwork; it does not demonstrate flooded-room behavior, collision, locker interactions or station integration.</p>
<label>Clip <select id="clip"></select></label><label>Scale <select id="scale"><option value="1">1×</option><option value="2" selected>2×</option><option value="3">3×</option></select></label>
<button id="pause">Pause</button><button id="restart">Restart</button><label>Phase <input id="phase" type="range" min="0" max="5" value="0"></label><label><input id="anchors" type="checkbox" checked>Show anchor</label>
<label><input id="helmet" type="checkbox">Diving helmet fitting</label><main></main><p id="status"></p>
<script>
const packs=PACK_DATA, equipment=EQUIPMENT_DATA, coverage=COVERAGE_DATA;
const names={bill:'Major Bill',veld:'Dr. Veld',branforth:'Chief Engineer Branforth'};
const clip=document.querySelector('#clip'), scale=document.querySelector('#scale'), phase=document.querySelector('#phase');
const keys=[...new Set(Object.values(packs).flatMap(p=>Object.keys(p)))].sort();
for(const state of ['swim','tread'])for(const dir of ['north','south','east','west'])if(!keys.includes(state+'-'+dir))keys.push(state+'-'+dir);
for(const key of keys)clip.add(new Option(key,key));clip.value='swim-south';
const cards={};for(const actor of Object.keys(names)){const el=document.createElement('article');el.innerHTML='<h2>'+names[actor]+'</h2><canvas width="276" height="276"></canvas><small></small>';document.querySelector('main').append(el);cards[actor]={canvas:el.querySelector('canvas'),label:el.querySelector('small')};}
const images={};for(const actor of Object.values({...packs,...Object.fromEntries(Object.entries(equipment).map(([k,v])=>[k+"-helmet",v]))}))for(const pack of Object.values(actor))for(const url of pack.urls){const im=new Image();im.src=url;images[url]=im;}
let running=true, elapsed=0, previous=null;
document.querySelector('#pause').onclick=()=>{running=!running;document.querySelector('#pause').textContent=running?'Pause':'Play';};
document.querySelector('#restart').onclick=()=>{elapsed=0;phase.value=0;};
clip.onchange=()=>{elapsed=0;phase.value=0;};
function referencePack(){return Object.values(packs).map(p=>p[clip.value]).find(Boolean);}
function frameAt(pack,time){const total=pack.frameDurationsMs.reduce((a,b)=>a+b,0);let t=pack.loop?time%total:Math.min(time,total);for(let n=0;n<pack.urls.length;n++){if(t<pack.frameDurationsMs[n])return n;t-=pack.frameDurationsMs[n];}return pack.urls.length-1;}
phase.oninput=()=>{running=false;document.querySelector('#pause').textContent='Play';const pack=referencePack();if(pack)elapsed=pack.frameDurationsMs.slice(0,Number(phase.value)).reduce((a,b)=>a+b,0);};
function draw(now){if(running&&previous!==null)elapsed+=Math.max(0,Math.min(now-previous,100));previous=now;
 const reference=referencePack();if(reference){phase.max=reference.urls.length-1;phase.value=frameAt(reference,elapsed);}
 for(const [actor,card] of Object.entries(cards)){const ctx=card.canvas.getContext('2d');ctx.clearRect(0,0,card.canvas.width,card.canvas.height);ctx.imageSmoothingEnabled=false;const helmet=document.querySelector("#helmet").checked;const pack=(helmet?equipment:packs)[actor]?.[clip.value];
  if(!pack){card.label.textContent='MISSING — no packaged animation';continue;}
  const i=frameAt(pack,elapsed);
  const s=Number(scale.value), [px,py]=pack.pivot, im=images[pack.urls[i]];const anchorY=16+Math.max(...Object.values(packs).map(p=>p[clip.value]?.pivot[1]||0))*s;const height=Math.max(360,anchorY+(im.naturalHeight-py)*s+16);if(card.canvas.width!==360||card.canvas.height!==height){card.canvas.width=360;card.canvas.height=height;}ctx.imageSmoothingEnabled=false;const x=180-px*s,y=anchorY-py*s;if(im.complete&&im.naturalWidth)ctx.drawImage(im,x,y,im.naturalWidth*s,im.naturalHeight*s);
  if(document.querySelector('#anchors').checked){ctx.strokeStyle='#72d5cf';ctx.beginPath();ctx.moveTo(174,anchorY);ctx.lineTo(186,anchorY);ctx.moveTo(180,anchorY-6);ctx.lineTo(180,anchorY+6);ctx.stroke();}
  const dir=clip.value.split('-').at(-1),state=clip.value.slice(0,-dir.length-1),entry=coverage.entries.find(e=>e.character===actor&&e.state===state&&e.direction===dir);
  card.label.textContent='Pose '+(i+1)+' / '+pack.urls.length+' · pivot '+pack.pivot.join(',')+' · '+(pack.loop?'loop':'one-shot, terminal hold')+' · '+(helmet?'Helmet fitting pilot; no locker integration':(entry?.visualReview||'Review pending'));
 }requestAnimationFrame(draw);}
requestAnimationFrame(draw);
</script>'''
(ROOT / 'review.html').write_text(template.replace('PACK_DATA', json.dumps(packs)).replace('EQUIPMENT_DATA', json.dumps(equipment)).replace('COVERAGE_DATA', (ROOT/'coverage.json').read_text()), encoding='utf-8')
print(f'Review built: {sum(map(len, packs.values()))} packaged clips for {len(packs)} crew')
