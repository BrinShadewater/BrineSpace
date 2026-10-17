from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_dilation
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=R/'character/krusher-rest-family-v2';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();revision=read(P/'revision.json');checks=0;errors=[];contacts=[];joins=[];yy,xx=np.indices((256,256))
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
for q in revision['records']:
 a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;detail=q['details'];tag=q['output'];check(sha(R/q['source'][6:])==q['sourceHash'],'source hash');check(sha(P/tag)==q['outputHash'],'output hash');check(b.shape==(256,256,4),'canvas');check(np.array_equal(a[~mask],b[~mask]),'original body outside head '+tag)
 if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'original shell alpha '+tag)
 if 'headSource' not in detail:check(np.array_equal(a,b),'rear retained '+tag);continue
 hp=R/detail['headSource'][6:];check(sha(hp)==detail['headHash'],'authored head hash '+tag)
 if q['gear']=='helmet':continue
 head=arr(hp);x,y=detail['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>180;check(np.array_equal(b[opaque],layer[opaque]),'complete bare source exact '+tag)
 body=(b[:,:,3]>180)&~opaque;axis=np.array(detail['bodyAxis']);along=xx*axis[0]+yy*axis[1];lower=opaque&(along>along[opaque].max()-8);edge=int((binary_dilation(lower)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));contacts.append({'output':tag,'state':q['state'],'frame':q['frame'],'tilt':detail['tilt'],'edge':edge,'joined':joined});check(edge>0,'neck contact '+tag);check(joined,'head attached to main body '+tag)
for rel,source in revision['derivedSources'].items():
 check(sha(R/source['source'][6:])==source['sourceHash'],'rotated input hash');check(sha(P/rel)==source['outputHash'],'rotated output hash');expected=Image.open(R/source['source'][6:]).convert('RGBA').rotate(source['angle'],resample=Image.Resampling.NEAREST,expand=True);check(np.array_equal(arr(P/rel),np.array(expected)),'whole nearest rigid rotation, no anatomy edits')
for g in ['bare','helmet']:
 check((P/(g+'-manifest.json')).read_bytes()==(OLD/(g+'-manifest.json')).read_bytes(),'entire manifest byte exact '+g);m=read(P/(g+'-manifest.json'));states={s['id']:s for s in m['states']};check(m['pivot']==[128,224] and m['standingHeight']==148,'original ruler/pivot');check(all((P/f).is_file() for s in m['states'] for f in s['frameFiles']),'all frame slots')
 for d in ['east','north','south','west']:
  for left,right in [('lie-down','sleep'),('sleep','get-up')]:
   check(np.array_equal(arr(P/states[left+'-'+d]['frameFiles'][-1]),arr(P/states[right+'-'+d]['frameFiles'][0])),'exact rest join '+g+d+left);joins.append([g,d,left,right])
  check(states['lie-down-'+d]['frameFiles']==list(reversed(states['get-up-'+d]['frameFiles'])),'exact reverse references '+g+d)
 for left,right in [('bunk-enter-east','bunk-sleep-east'),('bunk-sleep-east','bunk-exit-east')]:check(np.array_equal(arr(P/states[left]['frameFiles'][-1]),arr(P/states[right]['frameFiles'][0])),'bunk join '+g);joins.append([g,left,right])
 check(states['bunk-enter-east']['frameFiles']==list(reversed(states['bunk-exit-east']['frameFiles'])),'bunk exact reverse '+g)
report={'checks':checks,'errors':errors,'bareContacts':contacts,'joins':joins,'scope':'All92unique outputs, original bodies outside local head masks and shell alpha, source hashes/full authored bare heads, neck/body topology, rigid nearest source rotations, full original manifest bytes,20exact rest joins and10reversed choreographies. Not furniture or owner acceptance.'};(P/'independent-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':len(errors),'examples':errors[:8],'badContacts':[q for q in contacts if not q['edge'] or not q['joined']],'bareContacts':len(contacts),'joins':len(joins)}))
# Every revised source pose gets a complete head/collar context at3x nearest.
rows=[q for q in revision['records'] if q['changedPixels']];O=P/'review/source';O.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),15)
for start in range(0,len(rows),36):
 chunk=rows[start:start+36];board=Image.new('RGB',(1440,35+((len(chunk)+7)//8)*180),'#252b2e');draw=ImageDraw.Draw(board);draw.text((10,5),'REST / COMPLETE HEAD AND COLLAR CONTEXTS',font=font,fill='white')
 for j,q in enumerate(chunk):
  ys,xs=np.where(np.array(Image.open(P/q['mask']))>0);cx=int((xs.min()+xs.max())//2);cy=int((ys.min()+ys.max())//2);crop=Image.open(P/q['output']).convert('RGBA').crop((cx-28,cy-24,cx+28,cy+28)).resize((168,156),Image.Resampling.NEAREST);x=j%8*180;y=25+j//8*180;board.paste(crop,(x,y),crop);draw.text((x,y+156),q['gear'][0]+' '+q['state']+' '+str(q['frame']),font=font,fill='white')
 board.save(O/f'heads-{start//36:02d}.png')
(O/'index.json').write_text(json.dumps({'changedDrawings':len(rows),'records':rows},indent=2)+'\n')
assert not errors
