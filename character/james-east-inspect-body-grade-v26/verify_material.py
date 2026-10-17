from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];source=r/'character/james-tablet-east-matte-v3';inputs=json.loads((p/'native-inputs.json').read_bytes())
assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preLaunchSha256'].items())
validation=json.loads((p/'material-bake-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged']
evidence=json.loads((p/'material-bake-evidence.json').read_bytes());assert evidence['complete'] and evidence['failures']==0
checks=[];records=[];banks={}
for mode in ('bare','helmet'):
 old=json.loads((source/(mode+'-manifest.json')).read_bytes());new=json.loads((p/(mode+'-manifest.json')).read_bytes())
 assert all(old[k]==new[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter'])
 for a,b in zip(old['states'],new['states']):assert all(a[k]==b[k] for k in ['id','frameCount','frameDurationsMs','loop'])
 os=next(s for s in old['states'] if s['id']=='inspect-east');ns=next(s for s in new['states'] if s['id']=='inspect-east');bank=[];oldbank=[]
 for i,(before,after) in enumerate(zip(os['frameFiles'],ns['frameFiles'])):
  im=Image.open(source/before).convert('RGBA');candidate=Image.open(p/after).convert('RGBA');a=np.array(im);b=np.array(candidate)
  rgb=a[:,:,:3].astype(float);red,green,blue=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2])
  mask=(a[:,:,3]>0)&(xx>=56)&(xx<110)&(yy>=24)&(yy<172)&(np.minimum(red,blue)-green>2)&(np.abs(red-blue)<20)&(rgb.mean(2)>16)
  if mode=='helmet':
   bare=np.array(Image.open(source/'candidate-frames/bare'/Path(before).name).convert('RGBA'));protected=np.any(a!=bare,2);mask &= ~protected
   assert np.array_equal(a[protected],b[protected])
  if i in [0,140]:mask[:]=False
  bad=np.any(a!=b,2)&~mask
  assert np.array_equal(a[:,:,3],b[:,:,3]) and not bad.any(), str((mode,i,[(int(x),int(y),a[y,x].tolist(),b[y,x].tolist()) for y,x in np.argwhere(bad)[:8]]))
  if i in [0,140]:assert np.array_equal(a,b)
  # All pixels beyond x110, including most tablet surface, remain exact.
  assert np.array_equal(a[:,110:],b[:,110:])
  records.append(dict(mode=mode,slot=i,changedPixels=int(np.any(a!=b,2).sum()),headChangedPixels=int(np.any(a[24:60]!=b[24:60],2).sum())))
  bank.append(candidate);oldbank.append(im)
 banks[mode]=bank
 for page in range(5):
  board=Image.new('RGBA',(1472,832),(48,59,63,255));draw=ImageDraw.Draw(board)
  for j,i in enumerate(range(page*32,min((page+1)*32,141))):
   at=((j%8)*184,(j//8)*208+24);board.alpha_composite(bank[i],at);draw.text((at[0]+3,at[1]-19),f'{mode} {i}',fill='white')
  board.convert('RGB').save(p/f'{mode}-cycle-{page}.png')
 indices=[0,35,60,70,80,105,140];board=Image.new('RGBA',(1288,624),(48,59,63,255));draw=ImageDraw.Draw(board)
 for col,i in enumerate(indices):
  for row,im in enumerate([bank[0],oldbank[i],bank[i]]):
   at=(col*184,row*208+24);board.alpha_composite(im,at);draw.text((at[0]+3,at[1]-19),['idle','selected '+str(i),'candidate '+str(i)][row],fill='white')
 board.convert('RGB').save(p/f'{mode}-comparison.png')
for i in range(141):assert np.array_equal(np.array(banks['bare'][i])[60:],np.array(banks['helmet'][i])[60:])
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
report=dict(records=records,sourceFrames=282,originalAlphaExact=True,outsideSelectorExact=True,helmetDifferenceExact=True,pairedBodyBelow60Exact=True,
 endpointsExact=True,clocksCountPivotRulerExact=True,frozenInputsStable=True,realProfileUnchanged=True,visualReviewPending=True,normalChanged=False,fullGoalComplete=False,
 scope='Native material candidate package checks only; bounded chroma selection is not semantic segmentation. All-cycle visual review and actual loader admission pending.')
(p/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(sourceFrames=282,changedFrames=sum(x['changedPixels']>0 for x in records),maxChangedPixels=max(x['changedPixels'] for x in records),frozenInputsStable=True,realProfileUnchanged=True,lfsRasters=len(rasters))))
