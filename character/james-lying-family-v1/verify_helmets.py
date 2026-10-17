from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;checks=0;failures=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:failures.append(msg)
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
for d in ['east','south','west','north']:
 p=P.parent/('james-lying-'+d+'-v1');b=json.loads((p/'bare-manifest.json').read_text());h=json.loads((p/'helmet-manifest.json').read_text());reg=json.loads((p/'helmet-registration.json').read_text());by={s['id']:s for s in b['states']};arrays={}
 for st in h['states']:
  bs=by[st['id']]
  for field in ['frameDurationsMs','pivot','depthOffsets','waterKinds','waterPoses','facings','loop','restHeadOffset']:
   check(st.get(field)==bs.get(field),st['id']+' paired '+field)
  out=[]
  for j,f in enumerate(st['frameFiles']):
   a=rgba(p/f);bare=rgba(p/bs['frameFiles'][j]);i=st['provenance']['sourcePoses'][j];r=reg['tracking'][i];check(a.shape==bare.shape,st['id']+' paired canvas');check(r['fixedHeadScale']==reg['headScale'],st['id']+' one head scale')
   if i:
    mask=np.ones(a.shape[:2],bool);x0,y0,x1,y1=r['editRegion'];mask[y0:y1,x0:x1]=False;check(np.array_equal(a[mask],bare[mask]),st['id']+' exact body outside head region')
   check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),st['id']+' unclipped');out.append(a)
  arrays[st['id'].rsplit('-',1)[0]]=out
 for i in range(6):check(np.array_equal(arrays['get-up'][i],arrays['lie-down'][5-i]),d+' equipped reverse')
 check(np.array_equal(arrays['sleep'][0],arrays['lie-down'][5]) and np.array_equal(arrays['sleep'][0],arrays['sleep'][5]),d+' helmet sleep neutral joins')
 master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(p/'selected-helmet-master.png').convert('RGBA'),(36,52));check(np.array_equal(arrays['lie-down'][0],np.array(master)),d+' exact selected shell arrival')
 gif=[];dur=[]
 for st in h['states']:
  for j,f in enumerate(st['frameFiles']):
   board=Image.new('RGB',(1200,330),'#303b40');draw=ImageDraw.Draw(board);draw.text((10,8),'James '+d+' '+st['id'].rsplit('-',1)[0]+' | bare / helmet / 82px / 54px / 27px',fill='white');im=Image.open(p/f).convert('RGBA');bare=Image.open(p/by[st['id']]['frameFiles'][j]).convert('RGBA');board.paste(bare,(0,38),bare);board.paste(im,(270,38),im)
   for x,height in [(575,82),(830,54),(1035,27)]:sc=height/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.LANCZOS);board.paste(small,(x,282-round(224*sc)),small)
   gif.append(board);dur.append(int(st['frameDurationsMs'][j]))
 gif[0].save(p/'paired-review.gif',save_all=True,append_images=gif[1:],duration=dur,loop=0,disposal=2);gif[4].save(p/'paired-review-frame004.png')
report=dict(checks=checks,failures=failures,status='PASS' if not failures else 'FAIL',scope='Paired anatomy scale, immutable body outside head regions, joins and timings; no full continuous polish claim')
(P/'helmet-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(bool(failures))
