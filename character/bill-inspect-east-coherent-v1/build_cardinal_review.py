from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent
data={};bindings={};board=Image.new('RGB',(1024,768),(34,52,62));draw=ImageDraw.Draw(board)
for col,direction in enumerate(['east','south','west','north']):
    pack=ROOT/f'bill-inspect-{direction}-coherent-v1';data[direction]={}
    for row,gear in enumerate(['bare','helmet']):
        path=pack/(gear+'-manifest.json');m=json.loads(path.read_text());s=m['states'][0]
        assert m['pivot']==[128,224] and m['standingHeight']==148 and s['id']=='inspect-'+direction
        assert s['frameDurationsMs']==[160]*6 and s['loop']
        files=[pack/name for name in s['frameFiles']]
        assert files[0].read_bytes()==files[-1].read_bytes()
        data[direction][gear]=['../'+file.relative_to(ROOT).as_posix() for file in files]
        for file in [path]+files:bindings[file.relative_to(ROOT).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
        im=Image.open(files[0]);board.paste(im,(col*256,row*256),im)
        draw.text((col*256+10,row*256+12),direction+' '+gear,fill='white')
    r=json.loads((pack/'registration.json').read_text());master=ROOT/r['idleAuthority'];idle=Image.new('RGBA',(256,256));idle.paste(Image.open(master),(36,52));board.paste(idle,(col*256,512),idle)
    draw.text((col*256+10,524),direction+' selected idle',fill='white')
    data[direction]['master']='../'+master.relative_to(ROOT).as_posix();bindings[master.relative_to(ROOT).as_posix()]=hashlib.sha256(master.read_bytes()).hexdigest()
board.save(P/'cardinal-master-review.png')
(P/'cardinal-review-bindings.json').write_text(json.dumps({'scope':'eight staged states/48refs; current source comparison, no normal selection proof','sha256':bindings},indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill inspection cardinal review</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}canvas{display:block}p{max-width:85ch;color:#bdd0d2}</style><h1>Bill inspection — cardinal candidates</h1><p>Compare all four inspection loops against their selected idle masters. Top: inspection; bottom: idle. Reader draw/stow and normal activity integration remain pending. East/north crown range1px; west/south3px. This is a candidate comparison, not final full-set acceptance.</p><select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select><select id="size"><option selected>82</option><option>148</option><option>54</option></select><button id="play">Pause</button><button id="step">Next pose</button><span id="label"></span><canvas id="view" width="1000" height="620"></canvas><script>const data=DATA;let time=0,last=performance.now(),playing=true,manual=0;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};step.onclick=()=>{playing=false;manual=(manual+1)%6;play.textContent='Play'};const load=f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});Promise.all(Object.values(data).map(async d=>{d.images={};for(const g of ['bare','helmet'])d.images[g]=await Promise.all(d[g].map(load));d.idle=await load(d.master)})).then(()=>{function draw(now){if(playing)time+=now-last;last=now;const index=playing?Math.floor((time%960)/160):manual,c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,1000,620);Object.entries(data).forEach(([direction,d],j)=>{const x=125+j*250;c.fillStyle='#e6eff1';c.fillText(direction,x-25,30);c.drawImage(d.images[gear.value][index],x-128*scale,280-224*scale,256*scale,256*scale);c.drawImage(d.idle,x-92*scale,550-172*scale,184*scale,184*scale)});label.textContent=' pose '+(index+1)+'/6';requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'cardinal-review.html').write_text(html.replace('DATA',json.dumps(data)))
print('Bound eight staged inspection states/48refs and four selected idle masters')
