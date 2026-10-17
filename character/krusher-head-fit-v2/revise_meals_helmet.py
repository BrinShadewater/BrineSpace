"""Head-fit-only revisions of the existing meal and equipment poses."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_dilation
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def locate(base,p):return R/p[6:] if p.startswith('res://') else base/p
def shifted(mask,dx,dy):
 out=np.zeros_like(mask);y,x=np.where(mask);nx,ny=x+dx,y+dy;v=(nx>=0)&(nx<mask.shape[1])&(ny>=0)&(ny<mask.shape[0]);out[ny[v],nx[v]]=True;return out
can=R/'character/krusher-james-canonical-v5';oldcan=R/'character/krusher-james-canonical-v4'
canonical={g:{s['id']:s for s in read(can/(g+'-manifest.json'))['states']} for g in ['bare','helmet']}
yy,xx=np.indices((256,256));font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
def padded(im):
 out=Image.new('RGBA',(256,256));out.alpha_composite(Image.fromarray(im),(36,52));return np.array(out)
def save(new,old,rel,out,mask,extra,proof):
 before=rgba(old/rel);assert np.array_equal(before[~mask],out[~mask])
 q=new/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q)
 m='head-fit-masks/'+rel.removeprefix('frames/').removeprefix('poses/');mp=new/m;mp.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(mp)
 proof.append({'source':'res://'+(old/rel).relative_to(R).as_posix(),'sourceHash':sha(old/rel),'output':rel,'outputHash':sha(q),'mask':m,'changedPixels':int(np.any(before!=out,axis=2).sum()),'details':extra})
def finish(new,old,manifests,proof,extra=None):
 for name in manifests:
  (new/name).write_text(json.dumps(read(old/name),indent=2)+'\n')
 (new/'revision.json').write_text(json.dumps({'errors':[],'records':proof,'scope':'Head fitting against existing Krusher poses. Unchanged source clocks/registration/root/state metadata; exact old body outside head masks. Staged candidate only.',**(extra or {})},indent=2)+'\n')
 native=new/'native';native.mkdir(exist_ok=True)
 (native/'review.gd').write_text((old/'native/review.gd').read_text().replace(old.name,new.name))
 (new/'run_native.py').write_text((old/'run_native.py').read_text().replace(old.name,new.name))
 print(json.dumps({'pack':new.name,'uniquePoses':len(proof),'changed':sum(q['changedPixels']>0 for q in proof),'errors':[]}))

# Meals: change bare side registration, and rebind sealed inspection substitutes
# to the corrected canonical tablet sequence. Existing food/hand masks remain.
old=R/'character/krusher-meal-family-v1';new=R/'character/krusher-meal-family-v2';new.mkdir(exist_ok=True);proof=[]
for q in read(old/'provenance.json')['records']:
 gear=q['gear'];d=q['state'].rsplit('-',1)[1];before=rgba(old/q['output']);out=before.copy();mask=np.zeros((256,256),bool);detail={'gear':gear,'state':q['state'],'frame':q['frame']}
 if gear=='helmet':
  row=canonical[gear]['interact-'+d];out=padded(rgba(locate(can,row['frameFiles'][q['canonicalTabletPose']])))
  mask=np.any(before!=out,axis=2);assert np.array_equal(before[:,:,3],out[:,:,3]);detail['canonicalTabletPose']=q['canonicalTabletPose']
 elif d in ['east','west']:
  original=rgba(R/q['source']);a=np.zeros_like(before);ox,oy=q['sourcePadding'];a[oy:oy+original.shape[0],ox:ox+original.shape[1]]=original
  head=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];axis=ax+head.width//2;bottom=ay+head.height;top=bottom-({'south':101,'east':100,'north':96,'west':100}[d]-76)
  oldmask=(xx>=axis-head.width//2-5)&(xx<axis+head.width//2+6)&(yy>=top-5)&(yy<bottom)
  collar=(yy>=bottom-5)&(a[:,:,3]>0)&((xx<axis-3) if d=='east' else (xx>axis+3))
  foreground=np.array(Image.open(old/q['foregroundMask']))>0;oldmask&=~collar&~foreground
  dx=-2 if d=='east' else 2;dy=2
  marking=np.any(a!=before,axis=2)&~oldmask&(before[:,:,3]>0)
  mask=(oldmask|shifted(oldmask,dx,dy))&~collar&~foreground&~marking
  layer=Image.new('RGBA',(256,256));layer.paste(head,(ax+dx,ay+dy));h=np.array(layer);out[mask]=h[mask]
  assert np.array_equal(before[foreground],out[foreground]);assert np.array_equal(before[141:],out[141:]);detail.update(oldPaste=[ax,ay],newPaste=[ax+dx,ay+dy],foregroundProtected=True)
 save(new,old,q['output'],out,mask,detail,proof)
finish(new,old,['bare-manifest.json','helmet-manifest.json'],proof)

# Equipment changes: retain raised hands, held helmet and shell, move existing
# bare side identity and enlarge only bounded visible face pixels inside helmet.
old=R/'character/krusher-helmet-transition-v1';new=R/'character/krusher-helmet-transition-v2';new.mkdir(exist_ok=True);proof=[];outputs={};m=read(old/'manifest.json');equip=m['states'][0]
head=Image.open(R/'character/krusher-bill-base-test-v2/sources/east-head-native.png').convert('RGBA')
for q in read(old/'provenance.json')['records']:
 i=q['pose'];rel=equip['frameFiles'][i];before=rgba(old/rel);a=rgba(R/q['source']);out=before.copy();mask=np.zeros((256,256),bool);detail={'pose':i}
 oldmask=np.array(Image.open(old/f'masks/{i:03}-head.png'))>0
 marking=np.array(Image.open(old/f'masks/{i:03}-marking.png'))>0
 if i in [0,11]:
  gear='bare' if i==0 else 'helmet';out=padded(rgba(locate(can,canonical[gear]['idle-east']['frameFiles'][0])));mask=np.any(out!=before,axis=2);detail['canonicalEndpoint']=gear
 elif q['faceBox'] is None:
  ax,ay=q['headPaste'];dx=-2;dy=2;bottom=ay+head.height
  bounds={1:(108,70,140,100),2:(107,70,137,101),3:(108,70,136,101),4:(106,70,132,102)}[i];axis=round((bounds[0]+bounds[2])/2)
  collar=(yy>=bounds[3]-5)&(xx<axis-3)&(a[:,:,3]>0)
  mask=(oldmask|shifted(oldmask,dx,dy))&~collar&~marking
  layer=Image.new('RGBA',(256,256));layer.paste(head,(ax+dx,ay+dy));out[mask]=np.array(layer)[mask];detail.update(oldPaste=[ax,ay],newPaste=[ax+dx,ay+dy])
 else:
  x0,y0,x1,y1=q['faceBox'];box=[x0-1,y0-3,x1+1,y1]
  rgb=a[:,:,:3].astype(float);cool=(a[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
  mask=binary_dilation(oldmask,iterations=2)&(xx>=box[0])&(xx<box[2])&(yy>=box[1])&(yy<box[3])&(a[:,:,3]>0)&~marking&~cool
  if i==5:mask&=xx>=120 # Raised hand/held shell remain in front of partial face.
  fit=head.crop((8,5,head.width,head.height)).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
  layer=Image.new('RGBA',(256,256));layer.paste(fit,(box[0],box[1]));h=np.array(layer);mask&=h[:,:,3]>60;out[mask,:3]=h[mask,:3]
  assert np.array_equal(before[:,:,3],out[:,:,3]);detail.update(oldFaceBox=q['faceBox'],newFaceBox=box)
 assert np.array_equal(before[138:],out[138:]);save(new,old,rel,out,mask,detail,proof);outputs[i]=out
for s in m['states']:
 for rel,i in zip(s['frameFiles'],s['sourcePoseIndices']):
  path=new/rel;path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(outputs[i]).save(path)
finish(new,old,['manifest.json'],proof,{'reversal':'Exact same revised fitting poses in original sourcePoseIndices order for removal.'})

# Indexed service returns share the exact meal source poses or standing endpoint.
# Pitched South and North sources already have correct registration and stay exact.
old=R/'character/krusher-meal-service-v1';new=R/'character/krusher-meal-service-v2';new.mkdir(exist_ok=True);proof=[];replacement={}
mealold=R/'character/krusher-meal-family-v1';mealnew=R/'character/krusher-meal-family-v2'
for q in read(mealnew/'revision.json')['records']:
 if q['details']['gear']=='bare':replacement[rgba(R/q['source'][6:]).tobytes()]=rgba(mealnew/q['output'])
for d in ['south','east','north','west']:
 cm=read(oldcan/'bare-manifest.json');s=next(s for s in cm['states'] if s['id']=='idle-'+d)
 replacement[padded(rgba(locate(oldcan,s['frameFiles'][0]))).tobytes()]=padded(rgba(locate(can,canonical['bare']['idle-'+d]['frameFiles'][0])))
for q in read(old/'provenance.json')['records']:
 before=rgba(old/q['output']);out=replacement.get(before.tobytes(),before).copy();mask=np.any(before!=out,axis=2)
 save(new,old,q['output'],out,mask,{'method':'Exact corrected shared meal/standing pose' if before.tobytes() in replacement else 'Unchanged pitched South or North identity'},proof)
finish(new,old,['bare-manifest.json'],proof)

# Compact full source boards preserve source order, allowing contact/occlusion review.
for name,manifest in [('krusher-meal-family-v2','bare-manifest.json'),('krusher-meal-family-v2','helmet-manifest.json'),('krusher-helmet-transition-v2','manifest.json'),('krusher-meal-service-v2','bare-manifest.json')]:
 P=R/'character'/name;qs=read(P/'revision.json')['records']
 if name=='krusher-meal-family-v2':qs=[q for q in qs if q['details']['gear']==manifest.split('-')[0]]
 board=Image.new('RGB',(1536,60+((len(qs)+5)//6)*280),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),name+' / '+manifest,font=font,fill='white')
 for j,q in enumerate(qs):
  im=Image.open(P/q['output']).convert('RGBA');x=j%6*256;y=50+j//6*280;board.paste(im,(x,y),im);draw.text((x+8,y+250),str(j),font=font,fill='#bed2d3')
 board.save(P/(manifest.replace('.json','')+'-head-fit-sheet.png'))
