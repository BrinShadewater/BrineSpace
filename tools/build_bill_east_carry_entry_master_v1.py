from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,copy,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-carry-entry-master-v1';c=json.loads((D/'contract.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/p)==h for p,h in c['protected'].items())
F=D/'frames';F.mkdir(exist_ok=True);old=[];frames=[];records=[]
def bounds(im):return im.getchannel('A').point(lambda a:255 if a>127 else 0).getbbox()
for slot,path in enumerate(c['originalState']['frameFiles']):
 original=Image.open(R/path.replace('res://','')).convert('RGBA');old.append(original);dst=F/f'{slot:03}.png'
 if slot==0:im=Image.open(R/c['pickup']).convert('RGBA');origin=c['pickup'];rec={'slot':slot,'wholeAlias':origin}
 elif slot in [4,5]:im=Image.open(R/c['carry']).convert('RGBA');origin=c['carry'];rec={'slot':slot,'wholeAlias':origin}
 else:
  P=D/f'pose-{slot:03}';receipt=json.loads((P/'receipt.json').read_text());raw=P/'raw.png'
  if not raw.exists():shutil.copy2(receipt['generatedPath'],raw)
  rawim=Image.open(raw).convert('RGBA');assert rawim.width==rawim.height
  im=rawim.resize((256,256),Image.Resampling.LANCZOS);b=bounds(im);a=bounds(original);dy=a[3]-b[3]
  packed=Image.new('RGBA',(256,256));packed.alpha_composite(im,(0,dy));im=packed
  rec={'slot':slot,'rawSize':list(rawim.size),'heightDelta':b[3]-b[1]-a[3]+a[1],'wholeY':dy,'soleDelta':bounds(im)[3]-a[3],'rawSHA256':sha(raw),'preparedPromptSHA256':sha(P/'prompt.txt'),'references':json.loads((P/'references.json').read_text()),'receipt':receipt}
  assert abs(rec['heightDelta'])<=3 and rec['soleDelta']==0,rec
 im.save(dst);frames.append(im);rec['frameSHA256']=sha(dst);records.append(rec)
state=copy.deepcopy(c['originalState']);state['frameFiles']=[f'res://character/bill-east-carry-entry-master-v1/frames/{i:03}.png' for i in range(6)]
m=json.loads((R/c['originalManifest']).read_text());m.update(name='Bill East carry entry matched to master',status='provisional_unselected',states=[state]);(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
movies=[]
def movie(name,images,times,rate):
 p=D/f'{name}-{rate}.png';expected=[]
 for im,t in zip(images,times):
  if expected and expected[-1][0].tobytes()==im.tobytes():expected[-1][1]+=t*rate
  else:expected.append([im,t*rate])
 images[0].save(p,save_all=True,append_images=images[1:],duration=[t*rate for t in times],loop=0,disposal=0,blend=0)
 decoded=Image.open(p);assert decoded.n_frames==len(expected)
 for i,(im,t) in enumerate(expected):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==t
 movies.append({'file':p.name,'slots':len(images),'decoded':decoded.n_frames,'durationMs':sum(times)*rate})
for rate in [1,4]:
 movie('previous',old,state['frameDurationsMs'],rate);movie('candidate',frames,state['frameDurationsMs'],rate)
 cm=json.loads((R/'character/bill-east-carry-master-v1/manifest.json').read_text());cs=cm['states'][0];gait=[Image.open(R/p.replace('res://','')).convert('RGBA') for p in cs['frameFiles']]
 # Clock resumes at .104 seconds, so this source preview starts with the remaining1ms of gait0.
 movie('pickup-entry-carry',[frames[0]]+frames+gait*2,[400]+state['frameDurationsMs']+[1]+cs['frameDurationsMs'][1:]+cs['frameDurationsMs'],rate)
board=Image.new('RGBA',(1536,560),'#17252d');draw=ImageDraw.Draw(board)
for i in range(6):
 for row,(label,im) in enumerate([('Previous',old[i]),('Matched',frames[i])]):
  x=i*256;y=row*280;draw.text((x+8,y+8),f'{label} / {i}',fill='white');board.alpha_composite(im,(x,y+20))
board.save(D/'comparison.png')
review={'records':records,'protectedInputs':c['protected'],'movies':movies,'sourceSlots':6,'newWholeSources':3,'exactPickupEndpoint':True,'exactCarryEndpoints':[4,5],'normalAdmission':False,'visualReviewed':False,'nativeTested':False,'processing':'Uniform square-to256 LANCZOS; whole Y registration only. No stretching, stamping, local grade or invented intermediate artwork.'};(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill East carry entry</title><style>body{background:#17252d;color:#dbe5e9;font:17px system-ui;margin:24px}img{max-width:100%}.row{display:flex;gap:40px}.sprite{height:256px;width:256px}button{padding:10px}</style><h1>Bill East: pickup into carrying</h1><p>Three whole intermediate poses now match the matte suit and warmer face. The first frame is exactly the repaired pickup endpoint; the last two exactly reuse the repaired carry pose. Original six-frame,320ms entry retained.</p><button id="speed">Quarter speed</button><div class="row">'''
for name in ['previous','candidate','pickup-entry-carry']:html+=f'<div><p>{name}</p><img class="sprite motion" data-name="{name}" src="{name}-1.png"></div>'
html+='''</div><img src="comparison.png"><p>Source-motion preview, stationary gait. Normal selection unchanged; other carry turns still need matching.</p><script>let slow=false;document.querySelector('#speed').onclick=()=>{slow=!slow;document.querySelectorAll('.motion').forEach(im=>im.src=im.dataset.name+'-'+(slow?4:1)+'.png');document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'}</script>''';(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'records':[{k:r[k] for k in ['slot','heightDelta','wholeY','soleDelta'] if k in r} for r in records],'movies':movies}))
