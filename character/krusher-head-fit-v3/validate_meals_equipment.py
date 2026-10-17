from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_dilation,label
import numpy as np,json,hashlib
R=Path.cwd();C=R/'character/krusher-james-canonical-v6'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def pad(a):
 im=Image.new('RGBA',(256,256));im.alpha_composite(Image.fromarray(a),(36,52));return np.array(im)
idle={(g,s['id'][5:]):pad(arr(C/s['frameFiles'][0])) for g in ['bare','helmet'] for s in read(C/(g+'-manifest.json'))['states'] if s['id'].startswith('idle-')}
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for family,names in [('meal-family',['bare-manifest.json','helmet-manifest.json']),('helmet-transition',['manifest.json']),('meal-service',['bare-manifest.json'])]:
 OLD=R/f'character/krusher-{family}-v1';P=R/f'character/krusher-{family}-v3';checks=0;errors=[];joins=0;slots=0;contacts=[]
 def check(ok,why):
  global checks
  checks+=1
  if not ok:errors.append(why)
 for name in names:
  check((P/name).read_bytes()==(OLD/name).read_bytes(),'whole manifest bytes '+name);m=read(P/name)
  for s in m['states']:
   for f in s['frameFiles']:check(Image.open(P/f).size==(m['frameWidth'],m['frameHeight']),'source canvas '+f);slots+=1
   if family=='meal-family' and name=='helmet-manifest.json':
    d=s['id'].rsplit('-',1)[1]
    for f in [s['frameFiles'][0],s['frameFiles'][-1]]:check(np.array_equal(arr(P/f),idle['helmet',d]),'sealed idle join '+s['id']);joins+=1
   if family=='meal-service' and s['id'].startswith('meal-return-'):
    d=s['id'].rsplit('-',1)[1];check(np.array_equal(arr(P/s['frameFiles'][-1]),idle['bare',d]),'indexed return idle '+s['id']);joins+=1
 if family=='helmet-transition':
  m=read(P/'manifest.json');equip=m['states'][0]
  for s in m['states']:
   for f,i in zip(s['frameFiles'],s['sourcePoseIndices']):check(np.array_equal(arr(P/f),arr(P/equip['frameFiles'][i])),'exact reverse equipment '+f)
   for i,g in [(0,'bare'),(11,'helmet')]:check(np.array_equal(arr(P/s['frameFiles'][s['sourcePoseIndices'].index(i)]),idle[g,'east']),'equipment endpoint '+g);joins+=1
 qs=read(P/'revision.json')['records']
 for q in qs:
  a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;d=q['details'];tag=q['output'];check(sha(R/q['source'][6:])==q['sourceHash'],'source hash '+tag);check(sha(P/q['output'])==q['outputHash'],'output hash '+tag);check(np.array_equal(a[~mask],b[~mask]),'protected original body '+tag);check(np.array_equal(a[d['protectedFromRow']:],b[d['protectedFromRow']:]),'original lower body '+tag)
  if d.get('gear')=='helmet' or (family=='helmet-transition' and d['pose']>=5):check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet shell/foreground alpha '+tag)
  foreground=None
  if 'foregroundMask' in d:foreground=np.array(Image.open(R/d['foregroundMask'][6:]))>0;check(np.array_equal(a[foreground],b[foreground]),'food and raised hand foreground '+tag)
  if 'headSource' not in d:continue
  head=arr(R/d['headSource'][6:]);check(sha(R/d['headSource'][6:])==d['headHash'],'new authored head source '+tag)
  if 'paste' not in d:continue
  x,y=d['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>180
  if foreground is not None:opaque&=~foreground
  check(np.array_equal(b[opaque],layer[opaque]),'full visible identity exact '+tag);body=(b[:,:,3]>180)&~opaque;edge=int((binary_dilation(opaque)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));check(edge>0,'collar contact '+tag);check(joined,'head connected to body '+tag);contacts.append({'output':tag,'edge':edge,'joined':joined,'pitch':d.get('pitch'),'foregroundOccluded':foreground is not None})
 report={'checks':checks,'errors':errors,'slots':slots,'exactCanonicalJoins':joins,'bareContacts':contacts,'scope':'Original whole manifests, all output/source/authoring hashes, body conservation and food/hand foreground, original helmet alpha, visible source exactness and connected complete bare heads. Equipment exact reversal, canonical endpoints and80indexed returns. Not world-contact or owner acceptance.'};(P/'independent-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'family':family,'checks':checks,'errors':len(errors),'examples':errors[:8],'bareContacts':len(contacts),'slots':slots,'joins':joins}))
 review=P/'review/source';review.mkdir(parents=True,exist_ok=True)
 for start in range(0,len(qs),32):
  chunk=qs[start:start+32];board=Image.new('RGB',(1280,40+((len(chunk)+7)//8)*190),'#252b2e');draw=ImageDraw.Draw(board);draw.text((10,5),family.upper()+' / ALL HEAD AND COLLAR CONTEXTS',font=font,fill='white')
  for j,q in enumerate(chunk):
   im=Image.open(P/q['output']).convert('RGBA');mask=np.array(Image.open(P/q['mask']))>0
   if mask.any():ys,xs=np.where(mask);cx=int((xs.min()+xs.max())//2);cy=int((ys.min()+ys.max())//2)
   else:cx=128;cy=88
   crop=im.crop((cx-25,cy-25,cx+25,cy+30)).resize((150,165),Image.Resampling.NEAREST);x=j%8*160;y=30+j//8*190;board.paste(crop,(x,y),crop);draw.text((x,y+165),str(start+j)+' '+str(q['details'].get('state',q['details'].get('newSourceIndex',q['details'].get('pose','')))),font=font,fill='white')
  board.save(review/f'heads-{start//32:02}.png')
 (review/'index.json').write_text(json.dumps({'pages':(len(qs)+31)//32,'records':qs},indent=2)+'\n')
 if errors:raise SystemExit(1)
