"""Build actual normal-loader source/master/native comparisons by completed suite."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,shutil,sys,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-selected-native-v1'
available='--available' in sys.argv
report=json.loads((O/('progress.json' if available else 'validation.json')).read_text())
if not available:assert report['passed'];report=report['suites']
completed={s['label']:s for s in report if s['passed']};boards=[];presentations=0;tracks=[]
continue_out=R/'output/veld-bunk-selected-continue-v1/validation.json'
if continue_out.exists():
 continuation=json.loads(continue_out.read_text())
 if continuation['passed']:completed['continue']={'output':'veld-bunk-selected-continue-v1'}
if not available:assert 'continue' in completed
assets=P/'replay-frames';assets.mkdir(exist_ok=True)
def pad(im):
 im=im.convert('RGBA');assert im.size in [(184,184),(256,272)]
 if im.size==(184,184):
  result=Image.new('RGBA',(256,272));result.alpha_composite(im,(36,52));im=result
 return im
def master(gear):
 path=R/('character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png' if gear=='helmet' else 'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png')
 return pad(Image.open(path)).resize((128,136),Image.Resampling.LANCZOS)
def source(board,path,x,y):
 im=pad(Image.open(path)).resize((128,136),Image.Resampling.LANCZOS);board.paste(im,(x,y),im)
def room(board,path,x,y,box=(330,330,590,580)):
 global presentations
 im=Image.open(path).convert('RGB').crop(box).resize((128,123),Image.Resampling.NEAREST);board.paste(im,(x,y));presentations+=1
def save(board,name):board.save(P/name);boards.append(name)
def vec(s):return [float(x) for x in s.strip('()').split(',')]
if 'approach' in completed:
 out=R/'output'/completed['approach']['output'];records=json.loads((out/'records.json').read_text())
 assert len(records)==2
 for record in records:
  gear=record['gear'];count=record['captures'];cols=6
  board=Image.new('RGB',(cols*128,170+math.ceil(count/cols)*300),'#202a30');draw=ImageDraw.Draw(board);im=master(gear);board.paste(im,(0,25),im)
  draw.text((140,30),f'{gear}: normal need choice / route / whole bunk cycle',fill='white');draw.text((140,55),'East master / same half-scale anatomical ruler',fill='white')
  for i in range(count):
   x=i%cols*128;y=170+i//cols*300;name=f'{gear}-pose-{i:02}'
   draw.text((x+3,y+2),f'Actual capture {i+1}',fill='white');source(board,out/f'{name}-source.png',x,y+20)
   room(board,out/f'{name}-room.png',x,y+164,(260,330,520,580) if i==0 else (330,330,590,580))
  save(board,f'approach-{gear}-normal-review.png')
if 'partial' in completed:
 out=R/'output'/completed['partial']['output'];records=json.loads((out/'records.json').read_text());assert len(records)==80
 for rotation in range(4):
  for gear in ['bare','helmet']:
   selected=[r for r in records if r['rotation']==rotation and r['gear']==gear and r['native']]
   rows=[(r,[s for s in r['samples'] if 'slot' in s]) for r in selected]
   cols=1+max(len(samples) for _,samples in rows)
   board=Image.new('RGB',(cols*128,len(rows)*320+28),'#202a30');draw=ImageDraw.Draw(board)
   for row,(record,samples) in enumerate(rows):
    y=row*320+28;im=master(gear);board.paste(im,(0,y+26),im);draw.text((4,y+2),f'r{rotation} {gear} master',fill='white')
    for col,sample in enumerate(samples):
     x=(col+1)*128;name=f'{record["name"]}-slot-{sample["slot"]:02}'
     draw.text((x+3,y+2),f'{sample["elapsed"]:.2f}s',fill='white');source(board,out/f'{name}-source.png',x,y+26);room(board,out/f'{name}-room.png',x,y+176)
    draw.text((4,y+190),record['stage'],fill='white');draw.text((4,y+209),f'progress {record["progress"]}',fill='white')
   save(board,f'partial-r{rotation}-{gear}-normal-review.png')
for label in ['settle','early','fire','continue']:
 if label not in completed:continue
 out=R/'output'/completed[label]['output'];records=json.loads((out/'records.json').read_text())
 for gear in ['bare','helmet']:
  selected=[r for r in records if r['name'].startswith(gear)]
  rows=[(r,[s for s in r['reference'] if 'rendered' in s]) for r in selected]
  cols=1+max(len(samples) for _,samples in rows)
  board=Image.new('RGB',(cols*128,len(rows)*320+28),'#202a30');draw=ImageDraw.Draw(board)
  for row,(record,samples) in enumerate(rows):
   y=row*320+28;im=master(gear);board.paste(im,(0,y+26),im);draw.text((4,y+2),gear+' master',fill='white');draw.text((4,y+190),record['name'].removeprefix(gear+'-'),fill='white')
   for col,sample in enumerate(samples):
    tick=sample['tick'];x=(col+1)*128;name=f'{record["name"]}-reference-tick-{tick:02}'
    draw.text((x+3,y+2),f'{(tick+1)*20}ms',fill='white');source(board,out/f'{name}-source.png',x,y+26);room(board,out/f'{name}-room.png',x,y+176)
    destination=assets/(sample['pixels']+'.png')
    if not destination.exists():pad(Image.open(out/f'{name}-source.png')).save(destination)
   tracks.append({'name':label+'/'+record['name'],'reference':[{'pixels':s['pixels'],'offset':vec(s['offset']),'foot':vec(s['foot']),'clock':s['clock'],'depth':s['depth']} for s in record['reference']],'resumed':[{'pixels':s['pixels'],'offset':vec(s['offset']),'foot':vec(s['foot']),'clock':s['clock'],'depth':s['depth']} for s in record['resumed']]})
  save(board,f'{label}-{gear}-normal-review.png')
missing={s['pixels'] for track in tracks for side in ['reference','resumed'] for s in track[side] if not (assets/(s['pixels']+'.png')).exists()}
binding_path=P/'replay-walk-bindings.json'
walking_bindings=json.loads(binding_path.read_text())['bindings'] if binding_path.exists() else []
for binding in walking_bindings:
 original=Image.open(R/binding['source']).convert('RGBA')
 assert hashlib.sha256(original.tobytes()).hexdigest()==binding['nativePixelSha256']
 assert pad(original).tobytes()==Image.open(assets/(binding['nativePixelSha256']+'.png')).convert('RGBA').tobytes()
# The fire fixture captures the first walk and refuge, while recording every
# intermediate pixel hash. Bind uncaptured walking frames to the selected bank.
for root in [R/'character/crew-runtime-matte-v1/veld/frames',R/'character/veld-shared-helmet-v1/frames']:
 for folder in root.glob('walk*'):
  for path in folder.glob('*.png'):
   im=Image.open(path).convert('RGBA');pixels=hashlib.sha256(im.tobytes()).hexdigest()
   if pixels in missing:
    pad(im).save(assets/(pixels+'.png'));missing.remove(pixels)
    walking_bindings.append({'nativePixelSha256':pixels,'source':path.relative_to(R).as_posix(),'sourceFileSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'originalCanvas':list(im.size)})
assert not missing,('Unresolved exact replay sources',len(missing))
binding_path.write_text(json.dumps({'bindings':walking_bindings,'scope':'Current normally selected locomotion PNG pixels match the native recorded hash at each uncaptured walking step; these source files were not frozen in the earlier native interval. Fixed padding only.'},indent=2)+'\n')
(P/'review-evidence.json').write_text(json.dumps({'completedSuites':list(completed),'boards':boards,'futureReplayCases':len(tracks),'nativePresentations':presentations,'missingReplaySources':0,'supplementalWalkingPixelBindings':len(walking_bindings),'scope':'Actual normal need-choice route/rest and prescribed partial mortality/fire phases; paired source/native captured clocks beside fixed master ruler, not continuous world video'},indent=2)+'\n')
(P/'replay-traces.json').write_text(json.dumps(tracks,separators=(',',':'))+'\n')
gallery=''.join(f'<img src="{b}" alt="{b}">' for b in boards)
html='''<!doctype html><meta charset="utf-8"><title>Veld normally selected bunk sequences</title><style>body{background:#202a30;color:#e1e7eb;font:17px system-ui;margin:26px}a{color:#afd6da}img{max-width:100%}canvas{background:#26353d}select,button,input{font:inherit;margin:10px}.row{display:flex;gap:18px;flex-wrap:wrap}p{max-width:85ch}</style><h1>Veld bunk sequences — normal selection</h1><p>Both gear versions use the production loader. Actual need-driven approach and rest, four-rotation supported partial falls, early floor falls, supported fall continuation and fire-rise/refuge continuation. Boards pair submitted sources with matching native room captures and the East master at one anatomical ruler. Prescribed hazard phases and stepped actor traces remain separate from natural whole-world hazard cadence.</p><label>Case <select id="case"></select></label><button id="play">Pause</button><label>Step <input id="step" type="range" min="0" max="149" value="0"></label><span id="status">Loading…</span><div class="row"><div><p>Uninterrupted reference</p><canvas id="reference" width="520" height="430"></canvas></div><div><p>Fresh-scene loaded future</p><canvas id="resumed" width="520" height="430"></canvas></div></div><p>Replay reconstructs exact saved source, foot and visual-offset samples at one-third speed. This is not a continuous native world recording. Fire refuge movement can leave this fixed replay canvas; the native boards preserve the room captures.</p><h2>Actual native/source/master comparisons</h2>'''+gallery+'''<p><a href="HANDOFF.md">Handoff and remaining work</a></p><script>
const selector=document.querySelector('#case'),range=document.querySelector('#step'),play=document.querySelector('#play'),status=document.querySelector('#status');let running=true,last=performance.now(),elapsed=0,tracks=[],images={};
play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};selector.onchange=()=>{elapsed=0;range.value=0;range.max=tracks[selector.selectedIndex].reference.length-1};range.oninput=()=>{running=false;play.textContent='Play';elapsed=Number(range.value)*60};
fetch('replay-traces.json').then(r=>r.json()).then(async data=>{tracks=data;for(const t of tracks){const opt=document.createElement('option');opt.textContent=t.name;selector.append(opt)}if(!tracks.length){status.textContent='Future suites still running';return}range.max=tracks[0].reference.length-1;const ids=[...new Set(tracks.flatMap(t=>t.reference.map(s=>s.pixels)))];await Promise.all(ids.map(id=>new Promise((yes,no)=>{const im=new Image();im.onload=()=>{images[id]=im;yes()};im.onerror=no;im.src='replay-frames/'+id+'.png'})));function draw(now){if(running)elapsed+=now-last;last=now;const t=tracks[selector.selectedIndex],i=Math.floor(elapsed/60)%t.reference.length;range.value=i;const foot=t.reference[0].foot;for(const side of ['reference','resumed']){const sample=t[side][i],c=document.querySelector('#'+side).getContext('2d');c.clearRect(0,0,520,430);c.drawImage(images[sample.pixels],132+(sample.offset[0]+sample.foot[0]-foot[0])*148/65.28,80+(sample.offset[1]+sample.foot[1]-foot[1])*148/65.28)}status.textContent='Step '+i+' / '+((i+1)*20)+'ms after saved clock';requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>status.textContent='Preview load failed: '+e.message);
</script>'''
(P/'review.html').write_text(html,encoding='utf-8')
print(f'{len(completed)} completed normal suites/{len(boards)} boards/{presentations} native presentations/{len(tracks)} replay cases')
