"""Publish captured advancing frames with matched source/native display scale."""
from pathlib import Path
from PIL import Image
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-material-west-v6'
e=json.loads((P/'review.json').read_text(encoding='utf-8'));data=json.loads((O/'records.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['decodedCaptureIntervals']==380
banks={}
for gear in ['bare','helmet']:
    for phase,lo,hi in [('entry',60,105),('exit',410,460)]:
        rows=sorted([x for x in data['records'] if x['name'].startswith(gear+'-') and 'tick' in x and lo<=x['tick']<hi],key=lambda x:x['tick'])
        assert len(rows)==hi-lo
        group=[]
        for row in rows:
            raw=P/'captures'/f"{row['name']}-source.png";im=Image.open(raw).convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest();m=e['sourceRegistration'][key]
            assert tuple(m['size'])==im.size and m['standingHeight']==148
            room=P/'captures'/f"{row['name']}-room.png";assert room.is_file()
            group.append(dict(name=row['name'],tick=row['tick'],clock=row['clock'],foot=row['foot'],state=row['state'],materialWeight=row['materialWeight'],bridgeActive=row['bridgeActive'],pivot=m['pivot'],standingHeight=m['standingHeight'],size=list(im.size),decodedSourceSHA256=key))
        banks[gear+'-'+phase]=group
(P/'contact-player-data.json').write_text(json.dumps(banks,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Bill — West transition comparison</title>
<style>body{margin:24px;background:#182932;color:#edf1f2;font:16px system-ui}main{max-width:1100px;margin:auto}.pair{display:flex;gap:24px;flex-wrap:wrap}.pane{text-align:center}canvas{background:#14242c;width:400px;height:400px;max-width:100%}button,select{padding:8px 12px;margin-right:8px}input{width:min(840px,95%)}p{line-height:1.5}</style>
<main><h1>Bill — West transition comparison</h1><p>Bill pauses while pushing up from the floor, then resumes walking. Compare the original artwork with its appearance in the station at matching scale.</p><p><select id="gear"><option value="bare">Bare-headed</option><option value="helmet">Helmet</option></select><select id="phase"><option value="entry">Water entry</option><option value="exit">Water exit</option></select><select id="speed"><option value="1">Normal speed</option><option value="0.25">Quarter speed</option></select></p>
<div class="pair"><div class="pane"><h2>In the station</h2><canvas id="native" width="400" height="400"></canvas></div><div class="pane"><h2>Original artwork</h2><canvas id="source" width="400" height="400"></canvas></div></div>
<p><button id="play">Play</button><button id="prev">Previous frame</button><button id="next">Next frame</button></p><input id="scrub" type="range" min="0" max="44" value="0"><p id="label">Loading captures…</p><p>Station colour includes the water treatment. Each clip plays once. These captures support pose comparison; full movement, master consistency and save/resume acceptance remain under review.</p><h2>Early exit progression</h2><p>The supporting poses now stay in one place. The early height change, suit colour and detailed hand/knee contact still need polish.</p><p><a href="index.html" style="color:#b8d8dd">All captured poses and interruption comparisons</a></p></main>
<script>
let banks={},pictures={},playing=false,index=0,last=0,elapsed=0,ready=false;
const key=()=>document.getElementById('gear').value+'-'+document.getElementById('phase').value;
function pause(){playing=false;document.getElementById('play').textContent='Play'}
function draw(){if(!ready)return;const rows=banks[key()],r=rows[index],ims=pictures[r.name];const footX=255+(r.foot[0]-7680)*398/384,footY=287+(r.foot[1]-8064)*398/384;
const n=document.getElementById('native').getContext('2d');n.clearRect(0,0,400,400);n.imageSmoothingEnabled=false;n.drawImage(ims.room,Math.round(footX)-100,Math.round(footY)-130,200,200,0,0,400,400);
const s=document.getElementById('source').getContext('2d');s.clearRect(0,0,400,400);s.imageSmoothingEnabled=false;const ratio=65.28/r.standingHeight*398/384;s.drawImage(ims.source,2*(100-r.pivot[0]*ratio),2*(130-r.pivot[1]*ratio),2*r.size[0]*ratio,2*r.size[1]*ratio);
document.getElementById('scrub').max=rows.length-1;document.getElementById('scrub').value=index;document.getElementById('label').textContent=(document.getElementById('phase').value==='entry'?'Entry':'Exit')+' · frame '+(index+1)+' of '+rows.length+' · '+Math.round((r.clock-rows[0].clock)*1000)+' ms · '+(r.bridgeActive?'transition':r.state);}
function select(){pause();index=0;elapsed=0;draw()}
document.getElementById('gear').onchange=select;document.getElementById('phase').onchange=select;
document.getElementById('play').onclick=()=>{if(playing){pause();return}if(index>=banks[key()].length-1)index=0;elapsed=0;playing=true;document.getElementById('play').textContent='Pause';draw()};
document.getElementById('prev').onclick=()=>{pause();index=Math.max(0,index-1);draw()};document.getElementById('next').onclick=()=>{pause();index=Math.min(banks[key()].length-1,index+1);draw()};document.getElementById('scrub').oninput=e=>{pause();index=Number(e.target.value);draw()};
function animate(now){if(last&&playing&&ready){elapsed+=(now-last)*Number(document.getElementById('speed').value);const rows=banks[key()];while(index<rows.length-1){const interval=(rows[index+1].clock-rows[index].clock)*1000;if(elapsed<interval)break;elapsed-=interval;index++}if(index>=rows.length-1)pause();draw()}last=now;requestAnimationFrame(animate)}
const load=url=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=url});
fetch('contact-player-data.json').then(r=>r.json()).then(async data=>{banks=data;await Promise.all(Object.values(banks).flat().map(async r=>{const [room,source]=await Promise.all([load('captures/'+r.name+'-room.png'),load('captures/'+r.name+'-source.png')]);pictures[r.name]={room,source}}));ready=true;draw();requestAnimationFrame(animate)}).catch(()=>{document.getElementById('label').textContent='Could not load a capture.'});
</script></html>'''
(P/'contact-player.html').write_text(html,encoding='utf-8')
e['contactPlayer']=dict(file='contact-player.html',capturedPresentations=sum(len(x) for x in banks.values()),matchingDisplayScale=True,scope='Interactive captured60Hz source/native comparison, actual clock and physical root retained in data. Browser functionality and unpaused visual acceptance not asserted by publisher.')
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8')
if 'contact-player.html' not in html:html+='<p><a href="contact-player.html">Compare source and station captures at matching scale</a></p>'
(P/'index.html').write_text(html,encoding='utf-8')
print('Published190paired capture scrubber at matched scale, with actual clocks/root and exact source metadata.')
