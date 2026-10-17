from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,copy,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'character/krusher-animation-package-v9';O.mkdir(exist_ok=True)
for name in ['packs','frames','references']:(O/name).mkdir(exist_ok=True)
progress=json.load(open(P/'candidate-bank-index.json'));index={'identity':{'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','bodyFamily':'James utility suit','accent':'#527C80'},'status':'complete revised animation asset candidate; owner review pending','candidatePacks':{'bare':[],'helmet':[]},'states':{},'files':{}};checks=0;slots=0
for gear in ['bare','helmet']:
 selected={}
 for path in progress['candidatePacks'][gear]:
  m=R/path[6:];data=json.load(open(m))
  for state in data['states']:selected[state['id']]=(m,data,state)
 groups={}
 for key,(m,data,state) in selected.items():groups.setdefault(m,[]).append((key,data,state))
 for number,(m,rows) in enumerate(groups.items()):
  data=copy.deepcopy(rows[0][1]);data['states']=[];out=O/'packs'/f'{gear}-{number:02d}.json'
  for key,_,state in rows:
   item=copy.deepcopy(state);item['frameFiles']=[];inputs=[]
   for path in state['frameFiles']:
    src=R/path[6:] if path.startswith('res://') else m.parent/path
    content=src.read_bytes();digest=hashlib.sha256(content).hexdigest();dst=O/'frames'/(digest+'.png')
    if not dst.exists():dst.write_bytes(content)
    assert dst.read_bytes()==content;checks+=1;slots+=1
    item['frameFiles'].append('../frames/'+dst.name);inputs.append(src.relative_to(R).as_posix())
    index['files']['frames/'+dst.name]={'sha256':digest,'bytes':len(content)}
   data['states'].append(item);index['states'][gear+':'+key]={'manifest':'packs/'+out.name,'sourceManifest':m.relative_to(R).as_posix(),'sourceFrames':inputs}
  out.write_text(json.dumps(data,indent=2)+'\n');index['candidatePacks'][gear].append('res://'+out.relative_to(R).as_posix())
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
sheet=Image.new('RGBA',(1600,1030),'#272b2e');d=ImageDraw.Draw(sheet)
d.text((28,18),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');d.text((28,54),'AI & Robotics / James utility suit / matte muted cyan #527C80',font=font,fill='#b9d0d2')
reference=[]
for row,gear in enumerate(['bare','helmet']):
 for col,direction in enumerate(['south','east','north','west']):
  q=index['states'][gear+':idle-'+direction];m=O/q['manifest'];data=json.load(open(m));state=next(s for s in data['states'] if s['id']=='idle-'+direction);source=m.parent/state['frameFiles'][0];im=Image.open(source).convert('RGBA');xy=(col*400+16,row*445+118)
  sheet.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),xy);d.text((xy[0]+10,xy[1]-30),direction.upper()+' / '+gear.upper(),font=font,fill='white')
  reference.append({'gear':gear,'direction':direction,'frame':source.resolve().relative_to(O.resolve()).as_posix(),'canvas':[data['frameWidth'],data['frameHeight']],'pivot':data['pivot'],'standingHeight':data['standingHeight'],'displayScale':2})
d.text((28,990),'Canonical idle views / 2x nearest / standing ruler 148 source pixels / preserve per-pack pivots',font=font,fill='#b9d0d2');sheet.save(O/'references/character-sheet.png')
index['references']=reference
# Browser viewer uses actual authored PNG dimensions and registered pivot; no body-fit resize.
html="""<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher Dom animations</title><style>body{background:#272b2e;color:#dbe5e7;font:18px sans-serif;margin:24px}canvas{background:#30383d;image-rendering:pixelated;max-width:100%}select,button{font:inherit;margin:8px}img{max-width:100%}</style><h1>Krusher Dom</h1><p>System Administrator / AI &amp; Robotics / James utility suit / matte muted cyan</p><img src="references/character-sheet.png"><p>Complete revised asset candidate; owner review remains. Frame holds use original clocks. Gaits here replay by time; station movement uses distance.</p><select id="gear"><option>bare</option><option>helmet</option></select><select id="state"></select><button id="play">Pause</button><p id="info"></p><canvas id="view" width="640" height="960"></canvas><script src="library.js"></script><script>
const g=document.querySelector('#gear'),s=document.querySelector('#state'),c=document.querySelector('#view'),ctx=c.getContext('2d'),info=document.querySelector('#info');let imgs=[],record=null,epoch=performance.now(),running=true,paused=0;
function options(){s.replaceChildren();for(const key of Object.keys(LIBRARY[g.value]).sort()){const o=document.createElement('option');o.value=o.textContent=key;s.append(o)}s.value='idle-south';load()}
function load(){record=LIBRARY[g.value][s.value];imgs=record.files.map(p=>{const im=new Image();im.src=p;return im});epoch=performance.now();paused=0}
g.onchange=options;s.onchange=load;document.querySelector('#play').onclick=()=>{if(running)paused=performance.now()-epoch;else epoch=performance.now()-paused;running=!running;document.querySelector('#play').textContent=running?'Pause':'Play'};
function draw(now){if(record){const total=record.durations.reduce((a,b)=>a+b,0);let elapsed=running?now-epoch:paused;if(record.loop)elapsed%=total;else elapsed=Math.min(elapsed,total-0.001);let i=0;while(i<record.durations.length-1&&elapsed>=record.durations[i]){elapsed-=record.durations[i++]}ctx.clearRect(0,0,c.width,c.height);ctx.imageSmoothingEnabled=false;const im=imgs[i],x=320-record.pivot[0]*2,y=560-record.pivot[1]*2;if(im.complete)ctx.drawImage(im,x,y,record.width*2,record.height*2);ctx.strokeStyle='#527c80';ctx.beginPath();ctx.moveTo(300,560);ctx.lineTo(340,560);ctx.stroke();info.textContent=g.value+' / '+s.value+' / pose '+i+' / '+record.width+' x '+record.height+' / pivot '+record.pivot.join(', ')+' / ruler 148 / 2x nearest preview'}requestAnimationFrame(draw)}options();requestAnimationFrame(draw);
</script>"""
library={gear:{} for gear in ['bare','helmet']}
for full,q in index['states'].items():
 gear,key=full.split(':',1);m=O/q['manifest'];data=json.load(open(m));state=next(s for s in data['states'] if s['id']==key)
 library[gear][key]={'files':[(m.parent/f).resolve().relative_to(O.resolve()).as_posix() for f in state['frameFiles']],'durations':state['frameDurationsMs'],'loop':state.get('loop',False),'width':data['frameWidth'],'height':data['frameHeight'],'pivot':data['pivot']}
(O/'library.js').write_text('const LIBRARY='+json.dumps(library)+';\n');(O/'index.html').write_text(html)
(O/'package.json').write_text(json.dumps(index,indent=2)+'\n')
(O/'README.md').write_text('# Krusher Dom animation package\n\nSystem Administrator / AI & Robotics. James utility suit with matte muted cyan #527C80.\n\n338 bare and 248 helmet states, preserving original source pose clocks, canvas, pivot, ruler, filters and state metadata. Packs retain their individual render profiles; merge the ordered whole paths from package.json, and load helmet packs into diving-helmet. Every PNG lives inside this folder. Open index.html for a searchable local animation viewer and current James-body character sheet. Rebuild with ../krusher-style-neck-v1/build_package.py.\n\nRevised source coverage is complete. Normal roster integration and owner visual acceptance remain separate. Provenance maps original files in package.json. Historical Bill-body reference sheets are superseded by references/character-sheet.png for this package.\n')
print(json.dumps({'checks':checks,'sourceSlots':slots,'states':len(index['states']),'uniquePNG':len(index['files']),'package':str(O)}))



