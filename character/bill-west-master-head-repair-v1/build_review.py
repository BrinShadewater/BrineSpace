from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def common(im,xy=(0,0)):
 c=Image.new('RGBA',(352,320));c.alpha_composite(im,xy);return c
def bounds(a):
 yy,xx=np.where(a);return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] if len(xx) else None
records=[]
for key in sorted({p.name.rsplit('-v',1)[0].removeprefix('generation-provenance-') for p in OUT.glob('generation-provenance-*.json')}):
 available=[]
 for receipt in OUT.glob(f'generation-provenance-{key}-v*.json'):
  q=json.loads(receipt.read_text(encoding='utf-8'))
  assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
  assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
  for r in q['references']:assert sha(Path(r['path']))==r['sha256']
  if not q.get('rejected'):available.append(q)
 if not available:continue
 j=max(available,key=lambda q:q['revision'])
 assert sha(Path(j['promptFile']))==j['promptSha256']==j['submittedPromptSha256']
 assert sha(Path(j['sourcePath']))==j['sourceSha256']
 assert sha(Path(j['savedPath']))==j['sha256']==sha(Path(j['originalPath']))
 for ref in j['references']:assert sha(Path(ref['path']))==ref['sha256']
 raw=Image.open(j['savedPath']).convert('RGBA');assert raw.width==raw.height
 normalizationSide=j.get('rawNormalizedSide',352)
 square=raw.resize((normalizationSide,normalizationSide),Image.Resampling.LANCZOS)
 if j.get('rawCellCrop'):square=square.crop(tuple(j['rawCellCrop']))
 candidate=square.crop(tuple(j['returnCrop']))
 assert list(candidate.size)==j['originalCanvas'];candidate.save(OUT/f'{key}-candidate.png')
 old=Image.open(j['sourcePath']).convert('RGBA');new=candidate
 if key.startswith('bare'):old=common(old,(32,0));new=common(new,(32,0))
 base=json.loads((OUT/f'generation-job-{key}-v1.json').read_text(encoding='utf-8'))
 comparison=base.get('comparisonReference') or base['references'][1]
 assert sha(Path(comparison['path']))==comparison['sha256']
 ref=Image.open(comparison['path']).convert('RGBA').resize((352,352),Image.Resampling.NEAREST).crop((0,0,352,320))
 aa=np.asarray(old)[:,:,3]>127;bb=np.asarray(new)[:,:,3]>127
 full=np.asarray(square)[:,:,3]>127;x,y,r,b=j['returnCrop'];kept=np.zeros(full.shape,dtype=bool);kept[y:b,x:r]=True
 rec={'key':key,'revision':j['revision'],'sourcePath':j['sourcePath'],'sourceSha256':j['sourceSha256'],'rawSize':list(raw.size),'uniformRawScale':normalizationSide/raw.width,'rawNormalizedSide':normalizationSide,'rawCellCrop':j.get('rawCellCrop'),'sharedGenerationId':j['generationId'] if j.get('derivedSheetPose') else None,'returnCrop':j['returnCrop'],'opaquePixelsOutsideOriginalCanvas':int((full&~kept).sum()),'commonOldBounds':bounds(aa),'commonNewBounds':bounds(bb),'bodyBelow115IoU':float((aa[115:]&bb[115:]).sum()/(aa[115:]|bb[115:]).sum()),'windows':{},'normalAdmission':False,'nativeAcceptance':False,'visualAcceptance':False}
 for name,box in [('headCollar',(125,55,195,125)),('handsShoulders',(110,105,195,175)),('boots',(100,185,220,240))]:
  x,y,r,b=box;rec['windows'][name]={'box':list(box),'oldBounds':bounds(aa[y:b,x:r]),'newBounds':bounds(bb[y:b,x:r])}
 board=Image.new('RGB',(1150,740),(31,35,40));d=ImageDraw.Draw(board)
 for n,(label,im) in enumerate([('Before',old),('Candidate',new),('Master / established equipment',ref)]):
  x=n*380;d.text((x+10,10),key+' | '+label,fill='white');board.paste(im,(x+10,35),im)
  d.line((x+110,259,x+260,259),fill=(70,185,195))
  crop=im.crop((125,55,195,125)).resize((280,280),Image.Resampling.NEAREST);board.paste(crop,(x+40,405),crop)
  d.text((x+10,375),'Fixed source head/collar window x4',fill='white')
 d.text((10,710),'Whole-source physical ruler148; cyan pivot224. Only documented canvas enlargement/padding reversed; no head/body fitting.',fill='white')
 board.save(OUT/f'{key}-review.png');records.append(rec)
(OUT/'review.json').write_text(json.dumps({'poses':records,'normalAdmission':False,'nativeAcceptance':False,'fullVisualAcceptance':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps(records))
