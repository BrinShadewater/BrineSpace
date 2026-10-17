from pathlib import Path
import json,hashlib,re
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
freeze=json.loads((OUT/'selected-gait-freeze.json').read_text(encoding='utf-8'))
assert len(freeze)==98
for path,h in freeze.items():assert sha(ROOT/path)==h,path
master=Image.open(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png').convert('RGBA')
master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS)
mc=Image.new('RGBA',(256,256));mc.alpha_composite(master,(128-master.width//2,224-master.height))
bare_bank=json.loads((ROOT/'character/bill-walk-west-master-repair-v2/bank-assessment.json').read_text(encoding='utf-8'))
bare_studies={p['frame']:p['study'] for p in bare_bank['poses']}
records=[]
def mask(im):
 arr=np.array(im);lab,n=label(arr[:,:,3]>=180);counts=np.bincount(lab.ravel());return lab==int(counts[1:].argmax()+1)
def bounds(m,box):
 x,y,x1,y1=box;ys,xs=np.where(m[y:y1,x:x1]);return [int(xs.min()+x),int(ys.min()+y),int(xs.max()+x+1),int(ys.max()+y+1)]
for q in sorted(OUT.glob('generation-provenance-*-v*.json')):
 job=json.loads(q.read_text(encoding='utf-8'));assert job['status']=='completed'
 n=int(re.fullmatch(r'walk-(\d{3})-helmet-material-edit-v\d+.png',Path(job['savedPath']).name).group(1))
 assert sha(Path(job['savedPath']))==sha(Path(job['originalPath']))==job['sha256']
 assert sha(Path(job['promptFile']))==job['promptSha256']==job['submittedPromptSha256']
 for ref in job['references']:assert sha(Path(ref['path']))==ref['sha256']
 if job.get('candidateDisposition','').startswith('rejected'):continue
 old=Image.open(ROOT/f'character/bill-walk-west-material-v1/frames/helmet/walk-west/{n:03}.png').convert('RGBA')
 raw=Image.open(job['savedPath']).convert('RGBA');assert raw.width==raw.height, f'Non-square unreviewed output: frame{n:03} {raw.size}; inspect and reject rather than stretching'
 new=raw.resize((256,256),Image.Resampling.LANCZOS);new.save(OUT/f'canvas-normalized-study-{n:03}.png')
 bare=Image.open(ROOT/'character/bill-walk-west-master-repair-v2'/bare_studies[n]).convert('RGBA')
 a=mask(old);b=mask(new);regions={}
 for name,box in [('helmet window',[103,65,148,115]),('glove window',[95,130,150,164]),('boot window',[70,197,180,232])]:
  aa=bounds(a,box);bb=bounds(b,box);regions[name]={'selected':aa,'edited':bb,'delta':[v-u for u,v in zip(aa,bb)]}
 x=np.array(old);y=np.array(new);protected=[103,65,148,109];xx,yy,x1,y1=protected
 changed=int(np.any(x[yy:y1,xx:x1]!=y[yy:y1,xx:x1],axis=2).sum())
 rec={'frame':n,'revision':int(re.search(r'-v(\d+)\.png$',job['savedPath']).group(1)),'status':job.get('candidateDisposition','unselected_source_candidate'),'rawCanvas':list(raw.size),'uniformWholeCanvasScale':256/raw.width,'translation':[0,0],'silhouetteIoU':float((a&b).sum()/(a|b).sum()),'regions':regions,'helmetRgbaChangedPixels':changed,'helmetPixelComparisonWindow':protected,'helmetIdentityAccepted':False,'normalAdmission':False,'nativeAcceptance':False,'scope':'Window bounds/pixel differences are diagnostics, not joint, face or motion acceptance.'}
 (OUT/f'review-{n:03}.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8');records.append(rec)
 board=Image.new('RGB',(2048,1150),(23,42,51));draw=ImageDraw.Draw(board)
 for i,(title,im) in enumerate([('Original West master',mc),('Selected helmet walk',old),('Helmet material candidate',new),('Corresponding bare material study',bare)]):
  draw.text((i*512+12,10),f'{n:03} '+title,fill='white');z=im.resize((512,512),Image.Resampling.NEAREST);board.paste(z,(i*512,35),z)
 for i,(title,im) in enumerate([('Selected helmet / collar',old),('Edited helmet / collar',new),('Selected shoulder / glove',old),('Edited shoulder / glove',new)]):
  draw.text((i*512+12,560),title,fill='white');box=(99,65,155,122) if i<2 else (95,102,155,170);z=im.crop(box).resize(((box[2]-box[0])*7,(box[3]-box[1])*7),Image.Resampling.NEAREST);board.paste(z,(i*512+30,590),z)
 board.save(OUT/f'master-pose-review-{n:03}.png')
records=list({r['frame']:r for r in records}.values())
report={'attemptedDistinctPhases':len({int(re.search(r'provenance-(\d{3})-',q.name).group(1)) for q in OUT.glob('generation-provenance-*-v*.json')}),'generatedResultCount':len(list(OUT.glob('generation-provenance-*-v*.json'))),'rejectedResultCount':sum('rejected' in json.loads(q.read_text(encoding='utf-8')).get('candidateDisposition','') for q in OUT.glob('generation-provenance-*-v*.json')),'status':('full_helmet_source_bank_continuity_pending_unselected' if len(records)==48 else 'representative_helmet_bank_incomplete_unselected'),'authoredHelmetStudies':len(records),'remainingHelmet':48-len(records),'frames':[r['frame'] for r in records],'selectedGaitFilesUnchanged':98,'normalAdmission':False,'nativeAcceptance':False,'records':records,'scope':'Master/pose inspection of distinct authored phases; contiguous windows are reviewed separately in continuity.html. Not full48/native acceptance.'}
(OUT/'bank-assessment.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill West helmet master pass</title><style>body{background:#172a33;color:#d9e2e7;font:17px system-ui;margin:28px}img{max-width:100%;height:auto}a{color:#80c9d1}</style><h1>Bill West helmet master pass</h1><p>'+str(len(records))+' of 48 helmet frame candidates. Original master controls suit material; canonical helmet controls equipment design. Master/pose boards inspect each authored phase. The linked continuity preview plays only complete contiguous windows. The current in-game walk remains selected.</p><p>Retries are retained and counted as revisions, not extra phases. Helmet fit, face/collar identity, shoulders, gloves and boot continuity remain unaccepted. <a href="../bill-walk-west-master-repair-v2/bank.html">Compare the bare source sequence</a>.</p>'
for r in records:html+=f'<h2>Walking phase {r["frame"]:03}</h2><img src="master-pose-review-{r["frame"]:03}.png" alt="Original master, selected helmet walk, edited candidate, corresponding bare study and closeups">'
(OUT/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='records'}))
