"""Pair actual submitted native captures with unmodified source and master poses."""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
O=R/'output/veld-south-read-interrupt-selected-v1'
data=json.loads((O/'records.json').read_text(encoding='utf-8'))
bound={}; boards=[]; traces=[]
def bind(path):
    bound[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
def registered(source):
    im=Image.open(source).convert('RGBA')
    if im.size==(184,184):
        # Selected locomotion's p92,172 and furniture's p128,224 share H148.
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(36,52));im=canvas
    assert im.size==(256,256)
    return im
for case in data['futures']:
    name=case['name']; gear=name.split('-')[0]
    files=sorted(O.glob(name+'-reference-future-*-source.png'),key=lambda p:int(re.search(r'future-(\d+)-',p.name)[1]))
    columns=len(files)+2
    board=Image.new('RGB',(columns*180,328),'#202a30'); d=ImageDraw.Draw(board)
    for col,index in enumerate([0,5]):
        source=R/f'character/veld-seated-south-coherent-v1/frames/{gear}/sit-down-south/{index:03}.png'
        bind(source); im=Image.open(source).convert('RGBA')
        board.paste(im.resize((128,128),Image.Resampling.LANCZOS),(col*180+26,20),im.resize((128,128),Image.Resampling.LANCZOS))
        d.text((col*180+5,5),'Standing master' if index==0 else 'Seated body',fill='white')
    frames=[]
    for col,source in enumerate(files,2):
        tick=int(re.search(r'future-(\d+)-',source.name)[1]); native=source.with_name(source.name.replace('-source.png','-room.png'))
        bind(source);bind(native)
        full=registered(source)
        replay=P/'replay-frames'/source.name;replay.parent.mkdir(exist_ok=True);full.save(replay)
        im=full.resize((128,128),Image.Resampling.LANCZOS)
        board.paste(im,(col*180+26,20),im)
        # Fixed real sofa bounds: no pose-dependent recentering.
        crop=Image.open(native).convert('RGB').crop((490,286,660,391))
        board.paste(crop,(col*180+5,190))
        d.text((col*180+5,5),f'{tick/120:.3f}s / '+case['reference'][tick]['stage'].removeprefix('observation_'),fill='white')
        frames.append({'tick':tick,'path':'replay-frames/'+source.name})
    d.text((5,308),name+' | source at H74; actual native sofa crop | world paused, actor stepped',fill='white')
    path=P/(name+'-board.png');board.save(path);boards.append(path.name)
    traces.append({'name':name,'frames':frames,'duration':(len(case['reference'])-1)/120})
for filename in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    bind(O/filename)
page='''<!doctype html><meta charset="utf-8"><title>Veld South reader interruptions</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}button,select{font:inherit;padding:8px}canvas{background:#26353d}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — South sofa interruption review</h1><p>Normally selected artwork. Power loss and suspension checked at all fourteen reading positions in both equipment versions. Six distinct incoming poses per version compared through ordinary disk save and fresh-scene continuation. The replay below shows exact submitted sources at one-third speed; boards pair them with actual sofa captures and the standing/seated body references.</p><select id="case"></select> <button id="play">Replay</button><p id="status"></p><canvas width="256" height="256" id="pose"></canvas><div id="boards"></div><p>Prescribed default sofa contact and stepped actor updates. Natural whole-world scheduling, other layouts, South seated falls and final owner motion acceptance remain open.</p><script>const tracks=TRACKS,boards=BOARDS;const select=document.querySelector('#case');tracks.forEach((t,i)=>{let o=document.createElement('option');o.value=i;o.textContent=t.name;select.append(o)});document.querySelector('#boards').innerHTML=boards.map(p=>`<p><img src="${p}"></p>`).join('');let images={},start=performance.now();function reset(){start=performance.now()}select.onchange=reset;document.querySelector('#play').onclick=reset;Promise.all(tracks.flatMap(t=>t.frames).map(f=>new Promise((yes,no)=>{const im=new Image();im.onload=()=>{images[f.path]=im;yes()};im.onerror=no;im.src=f.path}))).then(()=>{function draw(now){let t=tracks[Number(select.value)],sec=Math.min(t.duration,(now-start)/3000),f=t.frames[0];for(let v of t.frames)if(v.tick/120<=sec)f=v;let c=document.querySelector('#pose').getContext('2d');c.clearRect(0,0,256,256);c.drawImage(images[f.path],0,0);document.querySelector('#status').textContent=t.name+' — '+sec.toFixed(3)+'s';requestAnimationFrame(draw)}requestAnimationFrame(draw)})</script>'''
(P/'review.html').write_text(page.replace('TRACKS',json.dumps(traces)).replace('BOARDS',json.dumps(boards)),encoding='utf-8')
(P/'review-evidence.json').write_text(json.dumps({'scope':data['scope'],'boards':boards,'futureCases':len(traces),'nativeSourcePairs':sum(len(t['frames']) for t in traces),'bindings':bound,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'boards':len(boards),'nativeSourcePairs':sum(len(t['frames']) for t in traces),'boundFiles':len(bound)}))
