"""Full authored family packaging; all pose registration remains source-derived."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
pilot=json.loads((P/'generation-provenance-v1.json').read_text())
inputs={};records=[];frames=[];old=[]
def frozen(path,digest=None):
 path=Path(path);actual=sha(path)
 if digest:assert actual==digest,path
 inputs[str(path)]=actual
def common(im):
 canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(im,(68,52));return canvas
def bounds(a):
 y,x=np.where(a);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
for n in range(6):
 receipt=P/('generation-provenance-v1.json' if n==3 else f'generation-provenance-{n:03}-v1.json')
 q=json.loads(receipt.read_text());frozen(receipt)
 for path,h in q['frozenInputs'].items():frozen(path,h)
 frozen(q['source'],q['sourceSha256']);frozen(q['promptFile'],q['promptSha256']);assert q['promptSha256']==q['submittedPromptSha256']
 for r in q['references']:frozen(r['path'],r['sha256'])
 frozen(q['savedPath'],q['sha256']);frozen(q['originalPath'],q['sha256'])
 before=Image.open(q['source']).convert('RGBA');old.append(common(before))
 assert old[-1].resize((1408,1408),Image.Resampling.NEAREST).tobytes()==Image.open(q['references'][0]['path']).convert('RGBA').tobytes()
 if q.get('derivedEndpoint'):
  frozen(q['derivedReceipt'],q['derivedReceiptSha256'])
  origin=json.loads(Path(q['derivedReceipt']).read_text());assert origin['generationId']==q['generationId'] and origin['sha256']==q['sha256']
  assert Image.open(origin['source']).convert('RGBA').tobytes()==before.tobytes()
 raw=Image.open(q['savedPath']).convert('RGBA');assert raw.width==raw.height
 candidate=raw.resize((352,352),Image.Resampling.LANCZOS);frames.append(candidate)
 mask=np.asarray(candidate)[:,:,3]>127;baseline=np.asarray(old[-1])[:,:,3]>127
 keep=np.zeros(mask.shape,bool);x,y,r,b=q['returnCrop'];keep[y:b,x:r]=True
 records.append({'index':n,'beforeBounds':bounds(baseline),'candidateBounds':bounds(mask),'bodyBelow115IoU':float((baseline[115:]&mask[115:]).sum()/(baseline[115:]|mask[115:]).sum()),'opaquePixelsOutsideOriginalCanvas':int((mask&~keep).sum()),'generationId':q['generationId'],'derivedEndpoint':q.get('derivedEndpoint',False)})
 folder=P/'frames/interact-east';folder.mkdir(parents=True,exist_ok=True);candidate.crop(q['returnCrop']).save(folder/f'{n:03}.png')
 assert not records[-1]['opaquePixelsOutsideOriginalCanvas']
assert frames[0].tobytes()==frames[5].tobytes()
manifestPath=ROOT/'character/bill-bare-east-selected-v1/manifest.json';frozen(manifestPath)
manifest=json.loads(manifestPath.read_text());state=copy.deepcopy(next(s for s in manifest['states'] if s['id']=='interact-east'))
times=state['frameDurationsMs'];state['frameFiles']=[f'res://character/bill-east-interact-master-consistency-v1/frames/interact-east/{n:03}.png' for n in range(6)]
staged={k:v for k,v in manifest.items() if k!='states'};staged.update(name='Bill East interaction original-master consistency study',status='provisional_unselected',states=[state]);(P/'manifest.json').write_text(json.dumps(staged,indent=2)+'\n')
decoded=0
for name,mult in [('interaction-normal.png',1),('interaction-slow.png',4)]:
 path=P/name;frames[0].save(path,save_all=True,append_images=frames[1:],duration=[t*mult for t in times],loop=1,disposal=0,blend=0)
 with Image.open(path) as media:
  assert media.n_frames==6
  for n,frame in enumerate(frames):media.seek(n);assert media.convert('RGBA').tobytes()==frame.tobytes();decoded+=1
  assert sum(media.seek(n) or media.info['duration'] for n in range(6))==sum(times)*mult
master=Image.open(pilot['references'][1]['path']).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
context=[('Original East master',master)]
auditPath=ROOT/'character/bill-full-family-consistency-2026-10-03-v1/source-audit.json';frozen(auditPath);audit=json.loads(auditPath.read_text())
for action in ['idle','walk','run','carry','weld']:
 s=audit['selected']['bare'][action+'-east'];n=0 if action=='idle' else len(s['files'])//2;path=ROOT/s['files'][n];frozen(path)
 im=Image.open(path).convert('RGBA');factor=148/s['standingHeight'];im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(im,(round(160-s['pivot'][0]*factor),round(224-s['pivot'][1]*factor)));context.append(('Selected '+action,canvas))
board=Image.new('RGBA',(2280,1560),(31,35,40,255));d=ImageDraw.Draw(board)
for row,group in enumerate([[(f'{n:03} Selected',im) for n,im in enumerate(old)],[(f'{n:03} New study',im) for n,im in enumerate(frames)],context]):
 for n,(label,im) in enumerate(group):
  x=n*380;y=row*520;d.text((x+8,y+8),label,fill='white');board.alpha_composite(im,(x+8,y+30));d.line((x+95,y+254,x+275,y+254),fill=(70,185,195));board.alpha_composite(im.crop((130,60,210,135)).resize((160,150),Image.Resampling.NEAREST),(x+95,y+365))
board.save(P/'family-master-context-review.png')
report={'records':records,'frozenInputs':inputs,'distinctGenerationUnits':len({r['generationId'] for r in records}),'decodedApngFramesExact':decoded,'timelineMs':sum(times),'endpointPixelsEqual':True,'visualReview':'pending full family and context board','normalAdmission':False,'nativeRun':False,'fullVisualAcceptance':False,'scope':'Five independently authored full figures and one exact derived endpoint. Uniform whole-canvas resampling only; original timeline/pivot/H148 preserved. No anatomy fit or source recoloring. Provisional staged manifest; selected library unchanged.'}
(P/'family-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'records':records,'distinctGenerationUnits':report['distinctGenerationUnits'],'decodedApngFramesExact':decoded,'timelineMs':sum(times)}))
