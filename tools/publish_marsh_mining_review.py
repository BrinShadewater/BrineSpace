"""Source-clock mining chains and sampled native full-trip witnesses."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
from publish_marsh_gesture_review import selected,save_webp
from publish_marsh_remaining_review import registered,panel
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-underwater-mining-v1'
OUT=BASE/'review'
EVIDENCE=ROOT/'output/marsh-mining-2026-10-15'

def retime(values,total):
    edges=[0];s=0
    for v in values:s+=v;edges.append(round(s/sum(values)*total))
    return [edges[i+1]-edges[i] for i in range(len(values))]

def main():
    OUT.mkdir(exist_ok=True);d=selected();cards=[]
    for direction in ['south','north','east','west']:
        frames=[];durations=[]
        parts=[('swim-',1,None),('water-salvage-enter-',1,400),('water-mine-draw-',1,600),('water-mine-',6,3880),('water-mine-stow-',1,600),('swim-pickup-',1,520),('swim-carry-',2,None)]
        for family,repeats,total in parts:
            record=d[family+direction];s=record[2]
            images=[panel(registered(record,i)) for i in range(len(s['frameFiles']))]*repeats
            times=s['frameDurationsMs']*repeats
            frames.extend(images);durations.extend(retime(times,total) if total else [round(t) for t in times])
        save_webp(frames,durations,OUT/(direction+'-chain.webp'))
        cards.append(f'<article><h3>{direction.title()}</h3><img src="{direction}-chain.webp" alt="{direction} mining sequence"><p>Brake → draw → six drilling cycles → stow → pickup → loaded swim.</p></article>')
    report=json.loads((EVIDENCE/'native/report.json').read_text());assert report['failures']==0 and len(report['journeys'])==4
    native=[];facing_set=set()
    for j in report['journeys']:
        frames=[];q=j['rotation']
        for c in j['captures']:
            im=Image.open(EVIDENCE/'native'/c['file']).convert('RGB');canvas=Image.new('RGB',(600,512),'#26333c');canvas.paste(im,(0,32))
            ImageDraw.Draw(canvas).text((8,8),c['phase']+' | '+c['key']+' | hold '+str(c['slot']),fill='white');frames.append(canvas)
        save_webp(frames,[200]*len(frames),OUT/f'native-q{q}.webp')
        mine=next(c for c in j['captures'] if c['key'].startswith('water-mine-') and c['key'].count('-')==2 and c['slot']==1)
        facing_set.add(mine['direction'])
        Image.open(EVIDENCE/'native'/mine['file']).save(OUT/f'native-q{q}-mining.png')
        native.append(f'<article><h3>Rotation {q} · {mine["direction"]} mining</h3><img class="native" src="native-q{q}.webp" alt="Sampled complete mineral trip"><p>All 12 expedition phases; one load extracted; two metal delivered. Mid-lift, mining, loaded-return and drainage disk restores checked.</p><a href="native-q{q}-mining.png">Full-size mining crop</a></article>')
    assert facing_set=={'north','east','south','west'}
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Marsh · underwater mining</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1480px;padding:0 20px}p{line-height:1.6;max-width:1100px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}article{background:#26333c;padding:12px;border-radius:10px}img{width:350px;max-width:100%;image-rendering:pixelated}.native{width:600px}a{color:#a7d6cc}button{padding:10px 16px;background:#b2d4cc;border:0;border-radius:5px;cursor:pointer}</style><h1>Marsh · underwater mining</h1><p>Four independently authored facings with a compact extraction drill. The north-facing tool sits in front of his body and is mostly hidden by the correct rear view. Right-temple hardware remains on the correct side. Accepted salvage, swimming and cargo artwork is retained.</p><button id="motion">Pause previews</button><h2>Mining action at source and station scale</h2><p>Source chains use the actual mining service timing: 400 ms braking, 600 ms draw, six pressure/recoil cycles over 3.88 s, then 600 ms stowing before the existing pickup. The complete work interval remains 5.48 s. Swim loops before/after are review context; replay is separate from an actual delivery.</p><section>'''+''.join(cards)+'''</section><h2>Four actual full mining trips</h2><p>These native witnesses sample unique selected holds and phase changes. Each sample is held for 200 ms for inspection; they do not depict continuous real-time trip cadence. Routes and resource rules are production paths on prescribed station/deposit fixtures. North's final approach is routed around one fixture corridor. Existing work positions outside the deposits are retained.</p><section>'''+''.join(native)+f'''</section><p>{report['checks']:,} native checks / zero failures. Each journey reaches all draw, drill and stow holds, six pickup poses, five loaded drainage poses and four unload poses, with exact extraction and delivery credit. Pause, airlock power loss and actual saved-game restores pass.</p><p><a href="../../../docs/MARSH_UNDERWATER_MINING_2026-10-15.md">Evidence and handoff</a> · <a href="../../marsh-water-actions-v1/review/index.html">Accepted water transitions and salvage</a></p><script>let paused=false;document.querySelector('#motion').onclick=()=>{{paused=!paused;document.querySelectorAll('section img').forEach(img=>{{if(!img.complete||!img.naturalWidth)return;if(paused){{img.dataset.loop=img.src;const c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;c.getContext('2d').drawImage(img,0,0);img.src=c.toDataURL();}}else if(img.dataset.loop)img.src=img.dataset.loop;}});document.querySelector('#motion').textContent=paused?'Play previews':'Pause previews';}};</script></html>'''
    (OUT/'index.html').write_text(page,encoding='utf-8')
    for path in OUT.glob('*.webp'):
        with Image.open(path) as im:
            for i in range(im.n_frames):im.seek(i);im.load()
    for link in re.findall(r'(?:src|href)="([^"]+)"',page):
        if link.endswith(('.webp','.png')):assert (OUT/link).is_file()
    (EVIDENCE/'review-script.js').write_text(re.search(r'<script>(.*?)</script>',page,re.S)[1])
    (OUT/'publication.json').write_text(json.dumps({'states':len(d),'holds':sum(len(r[2]['frameFiles']) for r in d.values()),'newStates':12,'newHolds':52,'nativeChecks':report['checks'],'nativeJourneys':4,'facings':sorted(facing_set),'nativeSamples':sum(len(j['captures']) for j in report['journeys'])},indent=2)+'\n')
    print('4 source chains +4 sampled full mining trips decode; all4 native mining facings; local image links resolve')
if __name__=='__main__':main()
