"""Review four authored key poses without substituting holds for a full walk loop."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,ast
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';K=P/'keypose-review-v1';K.mkdir(exist_ok=False);F=K/'frames';F.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slots=[0,12,24,36];inputs={};records=[];images={};before={}
for slot in slots:
 D=P/(f'stride-{slot:03}-v2' if slot==24 else f'stride-{slot:03}-v1');receipt=json.loads((D/'provenance.json').read_text(encoding='utf-8'));raw=D/f'raw-{slot:03}.png'
 assert sha(raw)==receipt['rawSha256'] and sha(D/'prompt.txt')==receipt['promptSha256']
 assert all(sha(Path(r['source']))==r['sourceSha256'] and sha(Path(r['path']))==r['sha256'] for r in receipt['references'])
 for path in [raw,D/'prompt.txt',D/'provenance.json']:inputs[str(path)]=sha(path)
 array=np.asarray(Image.open(raw).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)).copy()
 if slot==24:
  assert not array[0,:,3].any();shifted=np.zeros_like(array);shifted[:-1]=array[1:]
  assert np.array_equal(shifted[:-1],array[1:]) and np.count_nonzero(shifted[:,:,3])==np.count_nonzero(array[:,:,3]);array=shifted
 im=Image.fromarray(array);dst=F/f'{slot:03}.png';im.save(dst);images[slot]=im
 oldpath=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png';old=Image.open(oldpath).convert('RGBA');before[slot]=old;inputs[str(oldpath)]=sha(oldpath)
 def bounds(pixels):
  y,x=np.where(pixels[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
 nb,ob=bounds(array),bounds(np.asarray(old));a=array[:,:,3]>127;b=np.asarray(old)[:,:,3]>127
 records.append(dict(slot=slot,bounds=nb,selectedBounds=ob,boundsDelta=[x-y for x,y in zip(nb,ob)],heightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]),soleDelta=nb[3]-ob[3],silhouetteIoU=float(np.count_nonzero(a&b)/np.count_nonzero(a|b)),wholeShiftY=-1 if slot==24 else 0,frameSha256=sha(dst),generationId=receipt['generationId']))
manifestpath=R/'character/bill-walk-east-material-v1/manifest.json';manifest=json.loads(manifestpath.read_text(encoding='utf-8'));state=next(s for s in manifest['states'] if s['id']=='walk-east');selectedInputs={str(manifestpath):sha(manifestpath)}
for resource in state['frameFiles']:
 path=R/resource.removeprefix('res://');selectedInputs[str(path)]=sha(path)
assert len(state['frameFiles'])==48
master=Image.open(P/'original-master.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);board=Image.new('RGB',(1600,1120),'#17252d');draw=ImageDraw.Draw(board)
for row,(label,bank) in enumerate([('Selected',before),('Authored key pose',images)]):
 for col,slot in enumerate(slots+[None]):
  im=master if slot is None else bank[slot];x=col*320;y=row*560;draw.text((x+10,y+10),'Original master' if slot is None else f'{label} {slot}',fill='white');body=im.resize((320,320),Image.Resampling.NEAREST);board.paste(body,(x,y+35),body);head=im.crop((100,66,160,126)).resize((192,192),Image.Resampling.NEAREST);board.paste(head,(x+64,y+365),head)
board.save(K/'whole-master-comparison.png')
density=Image.new('RGB',(1600,900),'#17252d');draw=ImageDraw.Draw(density)
for row,height in enumerate([148,82,54,27]):
 scale=height/148
 for col,slot in enumerate(slots):
  x=col*400;y=row*225;draw.text((x+8,y+8),f'pose{slot} H{height}: selected / new',fill='white');draw.line((x+20,y+205,x+380,y+205),fill='#819b98')
  for center,im in [(100,before[slot]),(280,images[slot])]:
   view=im.resize((round(256*scale),round(256*scale)),Image.Resampling.LANCZOS);density.paste(view,(round(x+center-128*scale),round(y+205-224*scale)),view)
density.save(K/'density-comparison.png')
report=dict(status='provisional_four_keyposes',sourceCoverage='Four of48 preferred whole authored poses; five generation units including superseded original24. No complete manifest/loop or admission.',records=records,inputs=inputs,selectedInputs=selectedInputs,normalAdmission=False,nativeTested=False,visualReviewed=False,scope='Original phase shapes/heights and source contacts compared separately from master identity/material review. Whole canvas y-1 at24 only, exact surviving RGBA/no alpha discarded. Other poses unchanged whole packing. Static key poses do not prove neighbors/seam/full48cadence.')
(K/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'poses':len(records),'selectedInputs':len(selectedInputs),'boundsDeltas':[r['boundsDelta'] for r in records],'heightDeltas':[r['heightDelta'] for r in records],'soleDeltas':[r['soleDelta'] for r in records]}))
