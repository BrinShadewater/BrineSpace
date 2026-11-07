"""Freeze East04 cardinal selection and an exact-frame timed comparison viewer."""
from pathlib import Path
import hashlib,json,shutil,argparse
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-retained-gesture-material-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--east',default='east04-unselected');parser.add_argument('--west',default='west03-unselected');parser.add_argument('--north',default='north02-unselected');parser.add_argument('--south',default='south03-unselected');parser.add_argument('--output',default='cardinal02-unselected');args=parser.parse_args()
    out=BASE/args.output;out.mkdir(exist_ok=True)
    states=[];children=[];viewer={}
    for d,folder in [('east',args.east),('west',args.west),('north',args.north),('south',args.south)]:
        path=BASE/folder/'manifest.json';child=json.loads(path.read_text());states+=child['states'];children.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
        state=next(s for s in child['states'] if s['id']=='remove-helmet-'+d)
        files=[];sources=[]
        for i,sourcepath in enumerate(state['frameFiles']):
            source=ROOT/sourcepath.removeprefix('res://');target=out/f'{d}-{i:02}.png';shutil.copy2(source,target)
            assert sha(source)==sha(target);files.append(target.name);sources.append({'path':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
        viewer[d]={'files':files,'sources':sources,'durations':state['frameDurationsMs'],'loop':False,'pivot':[92,172],'standingHeight':148}
    manifest={'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'states':states,
              'scope':'Unselected cardinal retained generic gesture source repair; '+'/'.join([args.east,args.west,args.north,args.south])+'. No actual helmet implementation or enabled controller.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'source-selection.json').write_text(json.dumps({'children':children,'slots':48,'viewer':viewer,'normalAdmission':False,'fullGoalComplete':False},indent=2)+'\n')
    markup='''<!doctype html><meta charset="utf-8"><title>Marsh retained gesture — timed whole-source review</title>
<style>body{margin:18px;background:#17292e;color:#dbe3d8;font:14px system-ui}button{margin-right:8px;padding:6px 12px}#cards{display:grid;grid-template-columns:repeat(2,368px);gap:12px}canvas{display:block;background:#293b40;image-rendering:pixelated}.card h2{font-size:16px;margin:8px 0}.card p{margin:4px 0}a{color:#acd6d0}</style>
<h1>Marsh: staged retained gesture playback</h1><p>Exact whole sources · original six150ms holds · own idle alongside · no helmet/controller change.</p>
<button id="pause">Pause</button><button id="restart">Restart</button><button id="step">Next frame</button><span id="clock"></span>
<p>Each card: source1x above and station height65.28 below. Left: staged pose; right: exact own idle. A300ms idle gap separates900ms finite repeats.</p><div id="cards"></div>
<p>Source/player checks and this timed preview have limited scope. Live furniture/contact, full saves/Continue and full-set acceptance remain open.</p>
<script>const DATA=__DATA__;let running=true,time=0,slot=0,previous=performance.now(),advancingTicks=0;const cache={};
const cards=document.getElementById('cards');for(const [d,s] of Object.entries(DATA)){let c=document.createElement('section');c.className='card';c.innerHTML='<h2>'+d+'</h2><p id="label-'+d+'"></p><canvas id="source-'+d+'" width="368" height="205"></canvas><canvas id="station-'+d+'" width="368" height="100"></canvas>';cards.append(c);for(const p of s.files){if(!cache[p]){const im=new Image;im.src=p;cache[p]=im}}}
function draw(id,file,idle,z,anchorY){let c=document.getElementById(id),ctx=c.getContext('2d');ctx.clearRect(0,0,c.width,c.height);ctx.imageSmoothingEnabled=false;for(const [x,p] of [[92,file],[276,idle]]){let im=cache[p];if(im.complete&&im.naturalWidth)ctx.drawImage(im,x-92*z,anchorY-172*z,184*z,184*z)}}
function present(){let cycle=time%1200;slot=cycle>=900?5:Math.min(5,Math.floor(cycle/150));for(const [d,s] of Object.entries(DATA)){draw('source-'+d,s.files[slot],s.files[0],1,190);draw('station-'+d,s.files[slot],s.files[0],65.28/148,85);document.getElementById('label-'+d).textContent='slot'+slot+' / '+s.files[slot]+' / loaded '+s.files.every(p=>cache[p].complete&&cache[p].naturalWidth===184)}document.getElementById('clock').textContent='elapsed '+Math.floor(time)+'ms · slot'+slot+' · '+(running?'playing':'paused')+' · advancing ticks '+advancingTicks;document.body.dataset.slot=String(slot);document.body.dataset.elapsed=String(Math.floor(time));document.body.dataset.advancingTicks=String(advancingTicks)}
document.getElementById('pause').onclick=()=>{running=!running;document.getElementById('pause').textContent=running?'Pause':'Play';present()};document.getElementById('restart').onclick=()=>{time=0;present()};document.getElementById('step').onclick=()=>{running=false;document.getElementById('pause').textContent='Play';time=((slot+1)%6)*150+1;present()};
function tick(now){let dt=Math.max(0,Math.min(now-previous,100));previous=now;if(running){time+=dt;advancingTicks++}present();requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
    (out/'index.html').write_text(markup.replace('__DATA__',json.dumps(viewer)),encoding='utf-8')
    print(args.output+':8aliases/48slots,24exact copied viewer frames,900ms finite playback and300ms viewer gap')
if __name__=='__main__':main()
