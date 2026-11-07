"""Compare unchanged source banks at one pivot, including unmodified handoffs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-family-review-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
banks=[('idle-east','bill-east-idle-master-motion-v1'),('walk-east','bill-east-walk-master-full-v1'),('interact-east','bill-east-reach-adjacent-motion-v2'),('run-east','bill-east-run-master-v2'),('carry-east','bill-east-carry-master-v1'),('weld-east','bill-east-torch-master-v1')]
audit=json.loads((R/'character/bill-east-interact-master-consistency-v1/native/corrected-source-audit.json').read_text())['selected']['bare']
sources={};protected={};pictures={};movies=[]
for key,manifest in [(k,f'character/{b}/manifest.json') for k,b in banks]+[(k,audit[k]['manifest']) for k in ['pickup-east','unload-east','torch-draw-east','torch-stow-east']]:
 p=R/manifest;m=json.loads(p.read_text());s=next(s for s in m['states'] if s['id']==key);frames=[];files=[]
 protected[manifest]=sha(p)
 for name in s['frameFiles']:
  path=(R/name.removeprefix('res://')) if name.startswith('res://') else p.parent/name
  files.append(path.relative_to(R).as_posix());protected[files[-1]]=sha(path)
  im=Image.open(path).convert('RGBA');canvas=Image.new('RGBA',(256,256))
  offset=(round(128-m['pivot'][0]),round(224-m['pivot'][1]));canvas.alpha_composite(im,offset);frames.append(canvas)
 sources[key]=dict(manifest=manifest,files=files,durations=s['frameDurationsMs'],loop=s['loop'],pivot=m['pivot'],standingHeight=m['standingHeight'],candidate=key in dict(banks))
 pictures[key]=frames
 for rate in [1,4]:
  out=D/f'{key}-{rate}.png';frames[0].save(out,save_all=True,append_images=frames[1:],duration=[t*rate for t in s['frameDurationsMs']],loop=0,disposal=0,blend=0)
  decoded=Image.open(out)
  # Some unchanged consecutive input frames may be losslessly coalesced by Pillow.
  cursor=0;expected=[(im.tobytes(),t*rate) for im,t in zip(frames,s['frameDurationsMs'])]
  for n in range(decoded.n_frames):
   decoded.seek(n);pixels=decoded.convert('RGBA').tobytes();duration=decoded.info['duration'];used=0
   while cursor<len(expected) and used<duration:
    assert pixels==expected[cursor][0];used+=expected[cursor][1];cursor+=1
   assert used==duration
  assert cursor==len(expected)
  movies.append(dict(file=out.name,sourceFrames=len(frames),decodedFrames=decoded.n_frames,duration=sum(s['frameDurationsMs'])*rate,sha256=sha(out)))
for name,keys in [('family-comparison.png',[k for k,b in banks]),('handoff-comparison.png',['pickup-east','unload-east','torch-draw-east','torch-stow-east'])]:
 board=Image.new('RGBA',(256*len(keys),825),'#17252d');draw=ImageDraw.Draw(board)
 for col,key in enumerate(keys):
  frames=pictures[key]
  for row,slot in enumerate([0,len(frames)//2,len(frames)-1]):
   draw.text((col*256+8,row*275+8),f'{key}: {slot} / {len(frames)}',fill='white');board.alpha_composite(frames[slot],(col*256,row*275+18))
 board.save(D/name)
idle=pictures['idle-east'];pairs=[]
for key,b in banks[1:]:
 frames=idle+pictures[key]+idle;times=sources['idle-east']['durations']+sources[key]['durations']+sources['idle-east']['durations']
 out=D/f'join-{key}.png';frames[0].save(out,save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0);pairs.append(out.name)
review=dict(sources=sources,protectedInputs=protected,movies=movies,normalAdmission=False,nativeTested=False,visualReviewed=False,scope='Unchanged six repaired East banks and four currently selected handoff clips. Preview padding only to pivot128224/H148; no resampling or recolouring. Idle/action/idle comparisons are direct source boundaries, not authored pickup/tool or physical navigation lifecycles.')
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
cards=''.join(f'<figure><figcaption>{k}'+(' · repaired' if s['candidate'] else ' · existing handoff')+f'</figcaption><img class="sprite" data-key="{k}" src="{k}-1.png"></figure>' for k,s in sources.items())
html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Bill East family consistency</title><style>body{background:#17252d;color:#dbe5e9;font:16px system-ui;margin:24px}p{max-width:1000px;line-height:1.5}.row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}figure{background:#20313b;padding:12px;margin:0}img{max-width:100%}.sprite{width:100%;height:auto}button{padding:10px;margin:8px;color:#dbe5e9;background:#34515f;border:0}</style><h1>Bill East: family consistency</h1><p>Six repaired animation banks beside the existing pickup, unload and torch handoffs. All sources retain their original pixels, timing and size. Review version; normal game selection is unchanged.</p><button id="speed">Quarter speed</button><div class="row">'''+cards+'''</div><h2>Repaired family: first, middle and last poses</h2><img src="family-comparison.png"><h2>Existing handoffs: first, middle and last poses</h2><img src="handoff-comparison.png"><h2>Direct idle / action / idle boundaries</h2><p>These comparisons show material and size continuity. Cargo and tools appear directly; they do not replace pickup, unload or tool draw/stow.</p><div class="row">'''+''.join(f'<figure><figcaption>{n.removeprefix("join-").removesuffix(".png")}</figcaption><img class="sprite" src="{n}"></figure>' for n in pairs)+'''</div><script>let slow=false;document.querySelector('#speed').onclick=()=>{slow=!slow;for(let image of document.querySelectorAll('[data-key]'))image.src=image.dataset.key+'-'+(slow?4:1)+'.png';document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'};</script></html>'''
html=html.replace('.sprite{width:100%;height:auto}', '.sprite{width:100%;height:200px;object-fit:contain}')
(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(banks=len(sources),frames=sum(len(x) for x in pictures.values()),protectedInputs=len(protected),reviewMovies=len(movies),newArt=0)))
