"""One pooled case-surface grade in explicit polygons; glove/clasp/anatomy unchanged."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'whole-pose-join-v4/material-review';O=S/'case-review-v1';O.mkdir(exist_ok=True)
# Visually inspected native case bounds; sample only lid and right casing.
boxes=[(134,125,163,146),(134,125,162,145),(135,122,163,144),(136,126,165,148),(134,123,166,146),(134,126,163,147)]
claspboxes=[(146,130,157,141),(146,130,157,141),(147,127,158,138),(147,131,159,142),(146,128,159,140),(147,131,158,142)]
masterpath=R/'character/veld-cargo-turns-master-family-v1/north-east-candidate-v5/frames/bare/005.png';master=np.array(Image.open(masterpath).convert('RGBA'))
def region(a,box,clasp):
 x0,y0,x1,y1=box;mask=np.zeros(a.shape[:2],bool)
 mask[y0+1:y0+6,x0+2:x1-2]=True
 mask[y0+8:y1-2,x1-6:x1-1]=True
 cx0,cy0,cx1,cy1=clasp;mask[cy0:cy1,cx0:cx1]=False
 mask[136:160,125:157]=False
 rgb=a[:,:,:3].astype(float)
 return mask&(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)&(rgb.mean(2)>20)&(rgb.mean(2)<130)
inputs=[np.array(Image.open(S/f'{i:03}.png').convert('RGBA')) for i in range(6)]
masks=[region(a,box,clasp) for a,box,clasp in zip(inputs,boxes,claspboxes)]
mastermask=region(master,(135,119,161,141),(143,123,154,135))
q=[5,20,40,60,80,95];pooled=np.concatenate([a[m,:3].mean(1) for a,m in zip(inputs,masks)])
knots=np.quantile(pooled,np.array(q)/100);targets=np.quantile(master[mastermask,:3].mean(1),np.array(q)/100)
# Apply the same monotonic brightness ratio to each case. Preserve RGB hue/detail.
assert np.all(np.diff(knots)>0) and np.all(np.diff(targets)>=0)
frames=[];checks=0;rows=[];board=Image.new('RGB',(1792,790),'#202a30');d=ImageDraw.Draw(board)
d.text((8,8),'CASE SURFACE STUDY: ONE pooled master curve; exact alpha/glove/clasp/outside-mask preservation.',fill='white')
items=[('Repaired held master',Image.fromarray(master))]
for i,(a,mask,clasp) in enumerate(zip(inputs,masks,claspboxes)):
 out=a.copy();rgb=a[:,:,:3].astype(float);lum=rgb[mask].mean(1);new=np.interp(lum,knots,targets)
 out[mask,:3]=(rgb[mask]*(new/np.maximum(lum,1))[:,None]).clip(0,255).astype('uint8')
 assert np.array_equal(out[:,:,3],a[:,:,3]);checks+=1
 assert np.array_equal(out[~mask],a[~mask]);checks+=1
 cx0,cy0,cx1,cy1=clasp;assert np.array_equal(out[cy0:cy1,cx0:cx1],a[cy0:cy1,cx0:cx1]);checks+=1
 # Glove and cuff are entirely excluded: only upper lid/right case surfaces.
 assert not mask[136:160,125:157].any();checks+=1
 f=Image.fromarray(out);f.save(O/f'{i:03}.png');frames.append(f);items.append((f'Case-graded phase{i}',f))
 rows.append({'phase':i,'caseBounds':boxes[i],'claspProtected':clasp,'changedMaskPixels':int(mask.sum()),'sourceSHA256':hashlib.sha256((S/f'{i:03}.png').read_bytes()).hexdigest(),'outputSHA256':hashlib.sha256((O/f'{i:03}.png').read_bytes()).hexdigest(),'meanBefore':float(lum.mean()),'meanAfter':float(out[mask,:3].mean())})
for i,(name,f) in enumerate(items):
 d.text((i*256+5,32),name,fill='white');board.paste(f,(i*256,40),f)
 detail=f.crop((125,112,185,160)).resize((240,192),Image.Resampling.NEAREST);board.paste(detail,(i*256+8,330),detail)
 if i:
  a=inputs[i-1].copy();a[masks[i-1],:3]=[0,220,200]
  overlay=Image.fromarray(a).crop((125,112,185,160)).resize((240,192),Image.Resampling.NEAREST);board.paste(overlay,(i*256+8,565),overlay)
  d.text((i*256+8,538),'Teal: exact permitted mask',fill='white')
board.save(O/'case-master-comparison.png')
preview=[]
for f in frames:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);preview.append(bg)
preview[0].save(O/'cycle.png',save_all=True,append_images=preview[1:],duration=140,loop=0,disposal=0,blend=0)
decoded=Image.open(O/'cycle.png');assert decoded.n_frames==6;checks+=1
for i,f in enumerate(preview):
 decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));checks+=1
 assert decoded.info['duration']==140;checks+=1
(O/'review-evidence.json').write_text(json.dumps({'scope':'Source case grade candidate only, no geometry edits/helmet/native/cadence/normal acceptance.','onePooledCurve':True,'quantiles':q,'sourceLuminanceKnots':knots.tolist(),'masterLuminanceTargets':targets.tolist(),'master':masterpath.relative_to(R).as_posix(),'masterSHA256':hashlib.sha256(masterpath.read_bytes()).hexdigest(),'checks':checks,'failures':0,'rows':rows,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld East carry case review</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}button{font:inherit;margin-right:12px;padding:8px 14px}output{margin-left:12px}</style><h1>Veld East carry — case consistency</h1><p>Shared case tone; body motion and final materials remain under review.</p><div><button id="toggle">Pause</button><button id="previous">Previous pose</button><button id="next">Next pose</button><output id="phase">Pose 1 / 6</output></div><img id="pose" class="motion" src="000.png"><img src="case-master-comparison.png"><script>
const pose=document.getElementById('pose'),phase=document.getElementById('phase'),toggle=document.getElementById('toggle');
const frames=Array.from({length:6},(_,i)=>{const im=new Image();im.src=String(i).padStart(3,'0')+'.png';return im});
let playing=true,elapsed=0,last=performance.now(),index=0;
function show(i){index=i;pose.src=frames[i].src;phase.textContent='Pose '+(i+1)+' / 6';phase.dataset.phase=i;phase.dataset.elapsed=elapsed.toFixed(1)}
function paused(){playing=false;toggle.textContent='Play'}
toggle.onclick=()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';last=performance.now()};
document.getElementById('next').onclick=()=>{paused();elapsed=((index+1)%6)*140;show((index+1)%6)};
document.getElementById('previous').onclick=()=>{paused();elapsed=((index+5)%6)*140;show((index+5)%6)};
function tick(t){const dt=Math.max(0,t-last);if(playing){elapsed=(elapsed+dt)%840;show(Math.floor(elapsed/140))}last=t;requestAnimationFrame(tick)}
requestAnimationFrame(tick);
</script>''',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'knots':knots.tolist(),'targets':targets.tolist(),'maskPixels':[r['changedMaskPixels'] for r in rows],'meansAfter':[r['meanAfter'] for r in rows]}))
