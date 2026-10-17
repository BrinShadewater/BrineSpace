from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import json,hashlib,numpy as np,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;C=R/'character/krusher-james-canonical-v7'
read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for family in sys.argv[1:] or ['repair','torch','seated']:
 P=R/f'character/krusher-{family}-family-v4';OLD=R/f'character/krusher-{family}-family-v3';records=read(P/'revision.json')['records'];checks=0;errors=[];contacts=[];oldPortraitPixels=0
 def check(ok,msg):
  global checks
  checks+=1
  if not ok:errors.append(msg)
 for q in records:
  tag=q['gear']+' '+q['state']+' '+str(q['frame']);src=R/q['source'][6:];out=P/q['output'];a=arr(src);b=arr(out);mask=np.array(Image.open(P/q['mask']).convert('L'))>0
  check(sha(src)==q['sourceHash'],'source hash '+tag);check(sha(out)==q['outputHash'],'output hash '+tag);check(a.shape==b.shape,'canvas '+tag);check(np.array_equal(a[~mask],b[~mask]),'protected body and shell '+tag)
  if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'original shell alpha '+tag)
  d=q['details']
  if 'headSource' not in d:continue
  hp=R/d['headSource'][6:];head=Image.open(hp).convert('RGBA');check(sha(hp)==d['headHash'],'source head hash '+tag);layer=Image.new('RGBA',(b.shape[1],b.shape[0]));layer.paste(head,tuple(d['paste']));h=np.array(layer)
  if q['gear']=='bare':
   visible=(h[:,:,3]>180)&np.all(h==b,axis=2)
   vlabs,_=label(visible,np.ones((3,3)));vs=np.bincount(vlabs.ravel());vs[0]=0;main=vlabs==int(vs.argmax())
   labs,_=label(b[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());detached=int((main&(labs!=body)).sum())
   check(detached==0,'primary head detached '+tag);check(int(main.sum())>int((h[:,:,3]>180).sum())*.60,'face excessively occluded '+tag)
   contacts.append({'state':q['state'],'frame':q['frame'],'detachedPrimaryHeadPixels':detached,'visibleHeadPixels':int(visible.sum()),'registrationOffset':d['neckRegistrationOffset']})
  else:
   yy,xx=np.indices(b.shape[:2]);lining=arr(R/d['liningSource'][6:]);expected=lining[(yy-d['paste'][1])%32,(xx-d['paste'][0])%32,:3].copy();opaque=h[:,:,3]>0;expected[opaque]=h[opaque,:3];wrong=int((mask&np.any(b[:,:,:3]!=expected,axis=2)).sum());oldPortraitPixels+=wrong;check(wrong==0,'non-v4 portrait pixels inside aperture '+tag)
 actions={'repair':['kneel','stand'],'torch':['torch-draw','torch-stow'],'seated':['sit-down','sit-rise']}[family];refs=0;states=0
 for g in ['bare','helmet']:
  check((P/(g+'-manifest.json')).read_bytes()==(OLD/(g+'-manifest.json')).read_bytes(),'all metadata unchanged '+g);m=read(P/(g+'-manifest.json'));sm={s['id']:s for s in m['states']};cm=read(C/(g+'-manifest.json'));states+=len(sm)
  for s in m['states']:
   refs+=len(s['frameFiles']);check(all((P/f).is_file() for f in s['frameFiles']),'all frame slots '+g+' '+s['id'])
  for direction in ['south','east','north','west']:
   idle=next(s for s in cm['states'] if s['id']=='idle-'+direction);expected=np.zeros((m['frameHeight'],m['frameWidth'],4),dtype='uint8');expected[:184,:184]=arr(C/idle['frameFiles'][0])
   for action,i in [(actions[0],0),(actions[1],-1)]:check(np.array_equal(arr(P/sm[action+'-'+direction]['frameFiles'][i]),expected),'canonical idle endpoint '+g+' '+direction+' '+action)
 report={'checks':checks,'errors':errors,'states':states,'frameReferences':refs,'uniqueOutputs':len(records),'primaryHeadContactRecords':contacts,'oldPortraitPixelsInsideRevisedApertures':oldPortraitPixels,'scope':'Every unique source/output hash and protected pixel, full manifest/profile/clock preservation, every reference, all bare primary head contacts, all helmet face/lining pixels, and all16canonical endpoints. Offline source validation; station and owner acceptance remain separate.'};(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','states','frameReferences','uniqueOutputs','oldPortraitPixelsInsideRevisedApertures']}|{'errors':len(errors),'examples':errors[:8]}))
 if errors:raise SystemExit(1)
