from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_dilation
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=R/'character/krusher-recovery-salvage-v1';C=R/'character/krusher-james-canonical-v6';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=read(P/'revision.json')['records'];checks=0;errors=[];contacts=[];joins=[]
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
for q in records:
 a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;detail=q['details'];tag=q['output'];v=q['state'].rsplit('-',1)[1];hh,ww=a.shape[:2];yy,xx=np.indices((hh,ww));check(sha(R/q['source'][6:])==q['sourceHash'],'source hash');check(sha(P/tag)==q['outputHash'],'output hash');check(a.shape==b.shape,'complete original canvas');check(np.array_equal(a[~mask],b[~mask]),'original whole body outside head '+tag)
 foreground=np.zeros_like(mask)
 if q['family']=='salvage':
  foreground=((xx>=158)&(yy>=133)&(yy<153)) if v=='east' else ((xx<=105)&(yy>=133)&(yy<153)) if v=='west' else ((yy<102)&(xx<128)) if v=='north' else yy>=157
  check(np.array_equal(a[foreground],b[foreground]),'whole original tool/hands/effect '+tag);lower=xx<90 if v=='east' else xx>=172 if v=='west' else yy>=160 if v=='north' else yy<104;check(np.array_equal(a[lower],b[lower]),'original swimming legs/boots '+tag)
 else:check(np.array_equal(a[180:],b[180:]),'original recovery feet/legs '+tag)
 if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'original shell alpha '+tag)
 if 'headSource' not in detail:continue
 hp=R/detail['headSource'][6:];check(sha(hp)==detail['headHash'],'complete head hash '+tag)
 if q['gear']=='helmet':continue
 head=arr(hp);x,y=detail['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=(layer[:,:,3]>180)&~foreground;check(np.array_equal(b[opaque],layer[opaque]),'full authored head/neck exact except source foreground '+tag);body=(b[:,:,3]>180)&~opaque;edge=int((binary_dilation(opaque)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));check(edge>0,'head/body contact '+tag);check(joined,'head connected to main body '+tag);contacts.append({'output':tag,'state':q['state'],'frame':q['frame'],'edge':edge,'joined':joined})
for family in ['recovery','salvage']:
 for g in ['bare','helmet']:
  name=f'{family}-{g}-manifest.json';check((P/name).read_bytes()==(OLD/name).read_bytes(),'whole original manifest byte exact '+name);m=read(P/name)
  for s in m['states']:
   check(all((P/f).is_file() for f in s['frameFiles']),'all original frame slots '+g+s['id'])
   if family=='recovery':
    v=s['id'].rsplit('-',1)[1];cm=read(C/(g+'-manifest.json'));idle=next(s for s in cm['states'] if s['id']=='idle-'+v);expected=Image.new('RGBA',(m['frameWidth'],m['frameHeight']));expected.alpha_composite(Image.open(C/idle['frameFiles'][0]).convert('RGBA'),(36,52));check(np.array_equal(arr(P/s['frameFiles'][-1]),np.array(expected)),'exact canonical recovery ending '+g+v);joins.append([g,v])
   else:check(np.array_equal(arr(P/s['frameFiles'][0]),arr(P/s['frameFiles'][-1])),'exact closed salvage cycle '+g+s['id'])
report={'checks':checks,'errors':errors,'bareContacts':contacts,'canonicalJoins':joins,'scope':'All86unique outputs and96source slots, mixed original root/canvas/pivots/timing flags via whole manifests, original whole body outside local head masks, full tools/hand effects and distant legs, original helmet alpha, complete authored head source and visible mainbody contacts,8exact canonical recovery joins/8closed salvage loops. Not physical station or owner acceptance.'};(P/'independent-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':len(errors),'examples':errors[:8],'badContacts':[q for q in contacts if not q['edge'] or not q['joined']],'bareContacts':len(contacts),'canonicalJoins':len(joins)}))
O=P/'review/source';O.mkdir(parents=True,exist_ok=True);rows=[q for q in records if q['changedPixels']];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),15)
for start in range(0,len(rows),36):
 chunk=rows[start:start+36];board=Image.new('RGB',(1440,35+((len(chunk)+7)//8)*180),'#252b2e');draw=ImageDraw.Draw(board);draw.text((10,5),'RECOVERY / SALVAGE / COMPLETE HEAD CONTEXTS',font=font,fill='white')
 for j,q in enumerate(chunk):
  ys,xs=np.where(np.array(Image.open(P/q['mask']))>0);cx=int((xs.min()+xs.max())//2);cy=int((ys.min()+ys.max())//2);crop=Image.open(P/q['output']).convert('RGBA').crop((cx-28,cy-24,cx+28,cy+28)).resize((168,156),Image.Resampling.NEAREST);x=j%8*180;y=25+j//8*180;board.paste(crop,(x,y),crop);draw.text((x,y+156),q['gear'][0]+' '+q['state']+' '+str(q['frame']),font=font,fill='white')
 board.save(O/f'heads-{start//36:02d}.png')
(O/'index.json').write_text(json.dumps({'changedDrawings':len(rows),'records':rows},indent=2)+'\n')
assert not errors
