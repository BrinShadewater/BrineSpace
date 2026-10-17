from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((p/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
validation=json.loads((p/'edge-study-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged']
evidence=json.loads((p/'native-evidence.json').read_bytes());assert evidence['failures']==0 and len(evidence['records'])==864
contract=json.loads((p/'source-contract.json').read_bytes());lookup={(x['mode'],x['direction'],x['slot']):x for x in contract['records']};records=[];banks={};paths={}
for row in evidence['records']:
 key=(row['mode'],row['direction'],row['slot']);item=lookup[key];old=Image.open(r/row['source'][6:]).convert('RGBA');new=Image.open(r/row['candidate'][6:]).convert('RGBA');a=np.array(old);b=np.array(new)
 assert a.shape==b.shape==(184,184,4)
 red,green,blue=a[:,:,:3].astype(int).transpose(2,0,1);alpha=a[:,:,3];solid=alpha>0;inside=solid.copy()
 for dy in [-1,0,1]:
  for dx in [-1,0,1]:
   if dy==dx==0:continue
   shifted=np.zeros_like(solid);y0=max(0,dy);y1=min(184,184+dy);x0=max(0,dx);x1=min(184,184+dx);shifted[y0:y1,x0:x1]=solid[y0-dy:y1-dy,x0-dx:x1-dx];inside &= shifted
 mask=solid&(10*green>13*red)&(10*green>13*blue)&(green>20)&((alpha<128)|~inside)
 if item['preserveEndpoint']:mask[:]=False
 assert int(mask.sum())==row['selectedPixels']
 assert np.array_equal(a[:,:,0],b[:,:,0]) and np.array_equal(a[:,:,2:],b[:,:,2:]) and np.array_equal(a[~mask],b[~mask])
 assert (b[:,:,1][mask]<=a[:,:,1][mask]).all()
 if item['preserveEndpoint']:assert np.array_equal(a,b)
 records.append(dict(**row,alphaRedBlueExact=True,outsideEdgeAdmissionExact=True,endpointExact=item['preserveEndpoint'],sourceSha256=sha(r/row['source'][6:]),candidateSha256=sha(r/row['candidate'][6:])))
 banks.setdefault((row['mode'],row['direction']),[]).append(new);paths[key]=row['candidate']
boardfiles=[]
for (mode,direction),frames in banks.items():
 for page in range((len(frames)+55)//56):
  board=Image.new('RGBA',(1472,1456),(48,59,63,255));draw=ImageDraw.Draw(board)
  for j,i in enumerate(range(page*56,min((page+1)*56,len(frames)))):
   at=((j%8)*184,(j//8)*208+24);board.alpha_composite(frames[i],at);draw.text((at[0]+3,at[1]-19),f'{mode} {direction} {i}',fill='white')
  f=p/f'{mode}-{direction}-cycle-{page}.png';board.convert('RGB').save(f);boardfiles.append(f.name)
for mode in ['bare','helmet']:
 source=r/'character/james-inspect-material-continuity-v1'/(mode+'-manifest.json');pack=json.loads(source.read_bytes())
 for state in pack['states']:
  parts=state['id'].split('-');direction=parts[-1]
  if parts[0] in ['inspect','interact'] and direction in ['south','north','west']:
   state['frameFiles']=[paths[(mode,direction,i)] for i in range(len(state['frameFiles']))]
  else:
   state['frameFiles']=[ref if ref.startswith('res://') else 'res://'+(source.parent/ref).resolve().relative_to(r).as_posix() for ref in state['frameFiles']]
 pack['name']='James three-direction edge-only native material '+mode;pack['status']='staged_full_cycle_review_pending'
 pack['edgeMaterialScope']='South/North/West inspect/interact edge green only; exact original alpha/R/B/outside mask/endpoints. Other state sources exact legacy refs; later selected V26East loader override must remain.'
 (p/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
 original=json.loads(source.read_bytes())
 assert all(original[k]==pack[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter'])
 for a,b in zip(original['states'],pack['states']):assert all(a[k]==b[k] for k in ['id','frameCount','frameDurationsMs','loop'])
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
report=dict(records=records,sourceFrames=864,originalAlphaRedBlueExact=True,outsideEdgeAdmissionExact=True,masterEndpointsExact=12,
 clockCountPivotRulerExact=True,frozenInputsStable=True,wholeRealProfileUnchanged=True,sourceBoards=boardfiles,visualReviewPending=True,sourceAcceptance=False,
 normalChanged=False,fullGoalComplete=False,scope='All864 paired edge-material candidate package checks. Numeric edge selector is not semantic segmentation; shared helmet edge green may change only if admitted.20? count authoritative boardfiles. Not normal/room/continuous-motion acceptance.')
report['scope']=report['scope'].replace('20? count authoritative boardfiles.','18 complete-cycle source boards prepared.')
(p/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(sourceFrames=864,sourceBoards=len(boardfiles),changedFrames=sum(x['changedPixels']>0 for x in records),endpointsExact=12,frozenInputsStable=True,lfsRasters=len(rasters),normalChanged=False)))
