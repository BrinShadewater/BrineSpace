"""Actual source-change captures plus replay of saved native source/root traces."""
from pathlib import Path
import json,re,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-partial-fall-north-native-v1'
assert json.loads((O/'validation.json').read_text())['passed']
records=json.loads((O/'records.json').read_text());assets=P/'replay-frames';assets.mkdir(exist_ok=True)
tracks=[];count=0
def vec(s):return [float(v) for v in s.strip('()').split(',')]
for record in records:
 slots=[s['tick'] for s in record['reference'] if 'rendered' in s]
 board=Image.new('RGB',(1040,(len(slots)+1)*280),'#202a30');draw=ImageDraw.Draw(board)
 master_path=R/('character/veld-shared-helmet-v1/frames/idle-north/000.png' if record['name'].startswith('helmet') else 'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png')
 master=Image.open(master_path).convert('RGBA')
 for col in range(2):board.paste(master,(col*520+296,60),master);draw.text((col*520+8,12),'North standing master / original pixels / H148',fill='white')
 for slot_row,tick in enumerate(slots):
  row=slot_row+1
  for col,side in enumerate(['reference','resumed']):
   name=f"{record['name']}-{side}-tick-{tick:02d}"
   room=Image.open(O/f'{name}-room.png').convert('RGB').crop((255,280,515,530))
   board.paste(room,(col*520,row*280+30));draw.text((col*520+8,row*280+8),f'{side} / {(tick+1)*20}ms after saved clock',fill='white')
   source=Image.open(O/f'{name}-source.png').convert('RGBA');board.paste(source,(col*520+260,row*280+8),source);count+=1
   dest=assets/(record[side][tick]['pixels']+'.png')
   if not dest.exists():shutil.copy2(O/f'{name}-source.png',dest)
 board.save(P/f"native-fall-{record['name']}.png")
 tracks.append({'name':record['name'],'reference':[{'pixels':s['pixels'],'offset':vec(s['offset']),'clock':s['clock'],'depth':s['depth']} for s in record['reference']],'resumed':[{'pixels':s['pixels'],'offset':vec(s['offset']),'clock':s['clock'],'depth':s['depth']} for s in record['resumed']]})
(P/'replay-traces.json').write_text(json.dumps(tracks,separators=(',',':'))+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Veld Partial North lounge fall — saved continuation</title><style>body{background:#202a30;color:#e1e7eb;font:17px system-ui;margin:26px}a{color:#afd6da}img{max-width:100%}.row{display:flex;gap:18px;flex-wrap:wrap}canvas{background:#26353d}select,button,input{font:inherit;margin:10px}p{max-width:85ch}</style><h1>Partial North lounge fall — saved continuation</h1><p>Actual death API, exact incoming partial lowering/rising pose, registered chair-to-floor progression. Eight saves loaded into fresh main scenes. Source and saved-root replay below uses the captured 150-step traces; this is not a recording of continuous world gameplay. Playback is slowed to one-third speed.</p><label>Case <select id="case"></select></label><button id="play">Pause</button><label>Step <input id="step" type="range" min="0" max="149" value="0"></label><span id="status">Loading…</span><div class="row"><div><p>Uninterrupted reference</p><canvas id="reference" width="360" height="400"></canvas></div><div><p>Loaded continuation</p><canvas id="resumed" width="360" height="400"></canvas></div></div><p>35 targeted inputs unchanged during the native run; scratch profile preserved all 2,931 owner files. Normal fall selection remains staged. This verifies prescribed rotation-0 mortality and future actor updates; natural hazard cadence, other partial seating poses and wider room contexts remain open.</p><h2>Actual room captures beside exact submitted sources and masters</h2><div id="boards"></div><p><a href="./?v=source-contact-v1">Source/master preview</a> · <a href="HANDOFF.md">Handoff</a></p><script>
const selector=document.querySelector('#case'),range=document.querySelector('#step'),play=document.querySelector('#play'),status=document.querySelector('#status');let running=true,last=performance.now(),elapsed=0,tracks=[],images={};
play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};selector.onchange=()=>{elapsed=0;range.value=0};range.oninput=()=>{running=false;play.textContent='Play';elapsed=Number(range.value)*60};
fetch('replay-traces.json').then(r=>r.json()).then(async data=>{tracks=data;for(const t of tracks){const opt=document.createElement('option');opt.textContent=t.name;selector.append(opt);const im=document.createElement('img');im.src='native-fall-'+t.name+'.png';im.alt=t.name+' paired actual room/source/master review';document.querySelector('#boards').append(im)}const ids=[...new Set(tracks.flatMap(t=>t.reference.map(s=>s.pixels)))];await Promise.all(ids.map(id=>new Promise((yes,no)=>{const im=new Image();im.onload=()=>{images[id]=im;yes()};im.onerror=no;im.src='replay-frames/'+id+'.png'})));function draw(now){if(running)elapsed+=now-last;last=now;const i=Math.floor(elapsed/60)%150;range.value=i;const t=tracks[selector.selectedIndex];for(const side of ['reference','resumed']){const sample=t[side][i],c=document.querySelector('#'+side).getContext('2d');c.clearRect(0,0,360,400);c.drawImage(images[sample.pixels],52+sample.offset[0]*148/65.28,70+sample.offset[1]*148/65.28)}status.textContent='Step '+i+' / '+((i+1)*20)+'ms after saved clock';requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>status.textContent='Preview load failed: '+e.message);
</script>'''
(P/'resume-review.html').write_text(html,encoding='utf-8')
print(f'{len(records)} paired native future boards;{count} room/source presentations;{len(list(assets.glob("*.png")))} exact replay source images')
