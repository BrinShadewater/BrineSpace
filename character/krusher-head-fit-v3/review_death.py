from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from scipy.ndimage import binary_dilation,label
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-death-family-v2';OLD=R/'character/krusher-death-family-v1';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
contacts=[];errors=[];checks=0
records=read(P/'revision.json')['records']
for q in records:
 a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;assert sha(R/q['source'][6:])==q['sourceHash'] and sha(P/q['output'])==q['outputHash'];assert np.array_equal(a[~mask],b[~mask]);checks+=3
 d=q['details']
 if d.get('originalShellRestored'):
  old=next(t for t in read(OLD/'provenance.json')['records'] if t['output']==q['output']);original=arr(R/old['source']);shell=mask.copy();ap=d['observedVisorAperture']
  if ap:
   x0,y0,x1,y1=ap;shell[y0:y1,x0:x1]=False
  assert np.array_equal(b[shell],original[shell]);checks+=1
 if 'sharedCompletePose' in d:assert np.array_equal(b,arr(R/d['sharedCompletePose'][6:]));checks+=1
 if q['gear']=='helmet':assert np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
 if q['gear']!='bare' or 'headSource' not in d:continue
 head=arr(R/d['headSource'][6:]);assert sha(R/d['headSource'][6:])==d['headHash'];checks+=1;x,y=d['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head
 assert np.array_equal(b[layer[:,:,3]>180],layer[layer[:,:,3]>180]);checks+=1
 opaque=(layer[:,:,3]>180)&np.all(layer==b,2);body=(b[:,:,3]>180)&~opaque;lower=opaque.copy();lower[:y+head.shape[0]*2//3]=False;edge=int((binary_dilation(lower)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));checks+=2
 attachment='lower-neck'
 if 'rigidSource' in d:
  source=Image.open(R/d['rigidSource'][6:]).convert('RGBA');assert sha(R/d['rigidSource'][6:])==d['rigidSourceHash'];assert np.array_equal(head,np.array(source.rotate(d['rotationDegrees'],resample=Image.Resampling.NEAREST,expand=True)));checks+=2
  ring=np.array(source)[:,:,3]>180;ring[:-4]=False;ring=Image.fromarray(ring.astype('uint8')*255).rotate(d['rotationDegrees'],resample=Image.Resampling.NEAREST,expand=True);region=np.zeros(body.shape,bool);region[y:y+ring.height,x:x+ring.width]=np.array(ring)>0;edge=int((binary_dilation(region)&body).sum());attachment='authored-neck-end-rigid-rotation'
 if q['state']=='death-water-south' and q['frame']>=3:
  # In this overhead prone view the original back collar contacts the nape
  # behind the head crown; the projected chin does not meet the chest below.
  back=opaque.copy();back[y+head.shape[0]//3:]=False
  edge=int((binary_dilation(back)&body).sum());attachment='observed-overhead-back-collar'
 row={'state':q['state'],'frame':q['frame'],'view':q['view'],'output':q['output'],'edge':edge,'attachment':attachment,'joined':joined,'foregroundClippedPixels':d.get('foregroundClippedPixels',0)};contacts.append(row)
 if edge==0 or not joined:errors.append(row)
for f in ['ground','water']:
 for g in ['bare','helmet']:assert (P/f'{f}-{g}-manifest.json').read_bytes()==(OLD/f'{f}-{g}-manifest.json').read_bytes();checks+=1
(P/'independent-validation.json').write_text(json.dumps({'checks':checks,'errors':errors,'contacts':contacts,'scope':'Original whole manifests, unchanged body outside recorded masks, exact shared corrected endpoints, helmet alpha and complete authored bare source contact.'},indent=2)+'\n')
out=P/'review/source';out.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),16)
changed=[q for q in records if q['changedPixels']]
for page in range((len(changed)+39)//40):
 board=Image.new('RGBA',(1250,1440),'#252b2e');draw=ImageDraw.Draw(board)
 for slot,q in enumerate(changed[page*40:page*40+40]):
  old=next(t for t in read(OLD/'provenance.json')['records'] if t['output']==q['output']);x0,y0,x1,y1=old['headBox'];im=Image.open(P/q['output']).convert('RGBA').crop((x0-23,y0-25,x1+23,y1+24));im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);x=(slot%5)*250;y=(slot//5)*180;board.alpha_composite(im,(x+10,y+27));draw.text((x+5,y+2),q['gear']+' '+q['view']+' '+str(q['frame']),font=font,fill='white');draw.text((x+5,y+158),q['state'].removeprefix('swim-'),font=font,fill='#bed2d3')
 board.save(out/f'heads-{page:02d}.png')
print(json.dumps({'checks':checks,'bareContacts':len(contacts),'errors':errors,'sourcePages':(len(changed)+39)//40}))
