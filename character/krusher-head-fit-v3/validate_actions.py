from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,sys
from scipy.ndimage import binary_dilation,label
R=Path.cwd();C=R/'character/krusher-james-canonical-v6'
def arr(p):return np.array(Image.open(p).convert('RGBA'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for family in sys.argv[1:] or ['repair','torch','seated']:
 P=R/f'character/krusher-{family}-family-v3';OLD=R/f'character/krusher-{family}-family-v1';checks=0;errors=[];contacts=[];joins=[]
 def check(ok,msg):
  global checks
  checks+=1
  if not ok:errors.append(msg)
 records=json.loads((P/'revision.json').read_text())['records']
 for q in records:
  a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;detail=q['details'];tag=q['output']
  check(sha(R/q['source'][6:])==q['sourceHash'],'input hash '+tag);check(sha(P/q['output'])==q['outputHash'],'output hash '+tag);check(a.shape==b.shape,'canvas '+tag);check(np.array_equal(a[~mask],b[~mask]),'original body outside head '+tag);check(np.array_equal(a[150:],b[150:]),'original lower legs '+tag)
  if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'original helmet alpha '+tag)
  if 'headSource' not in detail:continue
  hp=R/detail['headSource'][6:];check(sha(hp)==detail['headHash'],'head source hash '+tag)
  if q['gear']!='bare':continue
  head=arr(hp);x,y=detail['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>180;check(np.array_equal(b[opaque],layer[opaque]),'complete bare head exact '+tag)
  body=(b[:,:,3]>180)&~opaque;lower=opaque.copy();lower[:y+head.shape[0]*2//3]=False;edge=int((binary_dilation(lower)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));check(edge>0,'neck contact '+tag);check(joined,'head silhouette connected '+tag);contacts.append({'output':tag,'state':q['state'],'frame':q['frame'],'edge':edge,'joined':joined})
 actions={'repair':['kneel','stand'],'torch':['torch-draw','torch-stow'],'seated':['sit-down','sit-rise']}[family]
 for g in ['bare','helmet']:
  check((P/(g+'-manifest.json')).read_bytes()==(OLD/(g+'-manifest.json')).read_bytes(),'manifest exact '+g);m=json.loads((P/(g+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};cm=json.loads((C/(g+'-manifest.json')).read_text())
  for s in m['states']:check(all((P/f).is_file() for f in s['frameFiles']),'all slots '+s['id'])
  for d in ['south','east','north','west']:
   idle=next(s for s in cm['states'] if s['id']=='idle-'+d);expected=np.zeros((m['frameHeight'],m['frameWidth'],4),dtype='uint8');expected[:184,:184]=arr(C/idle['frameFiles'][0])
   for action,i in [(actions[0],0),(actions[1],-1)]:check(np.array_equal(arr(P/states[action+'-'+d]['frameFiles'][i]),expected),'canonical join '+g+d+action);joins.append([g,d,action,i])
 report={'checks':checks,'errors':errors,'contacts':contacts,'exactCanonicalJoins':joins,'scope':'All unique outputs, body mask conservation, original helmet alpha and full bare head source bytes/topology/collar contact; exact original manifest bytes and16standing endpoints. Technical checks do not certify likeness or station contact.'};(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'family':family,'checks':checks,'errors':len(errors),'examples':errors[:10],'bareContacts':len(contacts)}))
 # Every revised drawing, collar/shoulder context included at 3x nearest.
 qs=[q for q in records if q['changedPixels']];review=P/'review/source';review.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),15)
 for start in range(0,len(qs),48):
  chunk=qs[start:start+48];board=Image.new('RGB',(1440,35+((len(chunk)+7)//8)*180),'#252b2e');draw=ImageDraw.Draw(board);draw.text((10,5),family.upper()+' / ALL REVISED HEAD AND COLLAR CONTEXTS',font=font,fill='white')
  for j,q in enumerate(chunk):
   im=Image.open(P/q['output']).convert('RGBA');ys,xs=np.where(np.array(Image.open(P/q['mask']))>0);cx=int((xs.min()+xs.max())//2);cy=int((ys.min()+ys.max())//2);box=(cx-28,cy-24,cx+28,cy+28);crop=im.crop(box).resize((168,156),Image.Resampling.NEAREST);x=j%8*180;y=25+j//8*180;board.paste(crop,(x,y),crop);draw.text((x,y+156),q['gear'][0]+' '+q['state']+' '+str(q['frame']),font=font,fill='white')
  board.save(review/f'heads-{start//48:02d}.png')
 (review/'index.json').write_text(json.dumps({'changedDrawings':len(qs),'pages':(len(qs)+47)//48,'records':qs},indent=2)+'\n')
 if errors:raise SystemExit(1)
