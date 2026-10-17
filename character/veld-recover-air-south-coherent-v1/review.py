from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
def main():
 packs={k:json.loads((P/f).read_text())['states'][0] for k,f in [('bare','manifest.json'),('helmet','helmet-manifest.json')]}
 board=Image.new('RGB',(1536,660),'#23313a');d=ImageDraw.Draw(board)
 for row,(gear,s) in enumerate(packs.items()):
  for i,f in enumerate(s['frameFiles']):
   im=Image.open(P/f);board.paste(im,(i*256,row*330),im);small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(i*256+50,row*330+188),small);d.text((i*256+4,row*330+4),f'{gear} {i}',fill='white')
 board.save(P/'paired-contact.png')
 html='''<!doctype html><meta charset="utf-8"><title>Veld south recovery</title><style>body{background:#23313a;color:#edf2f4;font:16px system-ui;margin:24px}p{max-width:78ch}button,select{font:inherit;padding:8px}canvas{display:block}a{color:#9ad4e8}</style><h1>Veld — south breathing recovery</h1><p>Authored planted forward bend, one shared source ruler and material grade, exact selected idle at both ends. Native front helmet follows the head. Six poses, three seconds. Staged: native/controller/restore checks and other directions remain.</p><select id="gear"><option>bare</option><option>helmet</option></select> <button id="play">Pause</button> <button id="step">Next pose</button> <span id="status"></span><canvas id="view" width="720" height="480"></canvas><p><a href="paired-contact.png">All poses beside station-scale views</a></p><script>const packs=DATA;let running=true,t=0,last=performance.now(),slot=0;play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};step.onclick=()=>{running=false;play.textContent='Play';slot=(slot+1)%6};gear.onchange=()=>{t=0;slot=0};Promise.all(Object.values(packs).map(async s=>{s.images=await Promise.all(s.frameFiles.map(f=>new Promise((yes,no)=>{let im=new Image;im.onload=()=>yes(im);im.onerror=no;im.src=f})))})).then(()=>{function draw(now){if(running)t+=now-last;last=now;if(running)slot=Math.min(5,Math.floor((t%3600)/500));let c=view.getContext('2d');c.fillStyle='#23313a';c.fillRect(0,0,720,240);c.fillStyle='#dce4e5';c.fillRect(0,240,720,240);for(let row=0;row<2;row++){let x=20;for(let h of [148,82,54]){let scale=h/148;c.drawImage(packs[gear.value].images[slot],x,230+row*240-224*scale,256*scale,256*scale);x+=256*scale+20}}status.textContent='Frame '+slot+' / 5';requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
 (P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
if __name__=='__main__':main()
