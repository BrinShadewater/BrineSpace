"""Compare whole source revisions and fixed detail windows with master/water."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={}
master=OUT.parent/'bill-west-master-head-audit-v1/master-sole-registered.png'
water=OUT.parent/'bill-west-water-joint-continuity-v1'
rows=[
 [('026 proportion v1',OUT/'bare-walk-026-proportion-v1-candidate.png'),('026 face v2',OUT/'bare-walk-026-face-v2-candidate.png'),('026 detail v3',OUT/'bare-walk-026-candidate.png'),('Original master',master)],
 [('030 proportion v1',OUT/'bare-walk-030-proportion-v1-candidate.png'),('030 detail v2',OUT/'bare-walk-030-candidate.png'),('Original master',master),('Water ready / prior source',water/'bare-ready-candidate.png')],
 [('033 proportion v1',OUT/'bare-walk-033-proportion-v1-candidate.png'),('033 detail v2',OUT/'bare-walk-033-candidate.png'),('Original master',master),('Water rise / prior source',water/'bare-rise-candidate.png')],
 [('019 face v2',OUT/'bare-walk-019-face-v2-candidate.png'),('019 detail v3',OUT/'bare-walk-019-candidate.png'),('Original master',master),('Water ready / prior source',water/'bare-ready-candidate.png')],
 [('039 face v2',OUT/'bare-walk-039-face-v2-candidate.png'),('039 detail v3',OUT/'bare-walk-039-candidate.png'),('Original master',master),('Water rise / prior source',water/'bare-rise-candidate.png')]]
board=Image.new('RGBA',(1520,530*len(rows)),(31,35,40,255));d=ImageDraw.Draw(board)
for row,sources in enumerate(rows):
 for col,(label,path) in enumerate(sources):
  inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
  if im.size==(256,256):
   common=Image.new('RGBA',(352,320));common.alpha_composite(im,(32,0));im=common
  assert im.size==(352,320),path
  x=col*380;y=row*530;d.text((x+8,y+8),label,fill='white');board.alpha_composite(im,(x+8,y+30))
  board.alpha_composite(im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+75,y+370))
for key,revision in [('026',2),('026',3),('030',2),('033',2),('019',3),('039',3)]:
 path=OUT/f'generation-provenance-bare-walk-{key}-v{revision}.json';inputs[str(path)]=sha(path)
board.save(OUT/'cropped-master-detail-review.png')
neighbors=Image.new('RGBA',(2660,1590),(31,35,40,255));nd=ImageDraw.Draw(neighbors)
sources=[[(f'{n:03} current detail',OUT/f'bare-walk-{n:03}-candidate.png') for n in group] for group in [(16,17,18,19,20,21,22),(36,37,38,39,40,41,42)]]
sources.append([('Original master',master),('Water ready / prior source',water/'bare-ready-candidate.png'),('Water rise / prior source',water/'bare-rise-candidate.png')])
for row,group in enumerate(sources):
 for col,(label,path) in enumerate(group):
  inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
  if im.size==(256,256):
   common=Image.new('RGBA',(352,320));common.alpha_composite(im,(32,0));im=common
  assert im.size==(352,320)
  x=col*380;y=row*530;nd.text((x+8,y+8),label,fill='white');neighbors.alpha_composite(im,(x+8,y+30))
  neighbors.alpha_composite(im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+75,y+370))
for key,revision in [('016',2),('017',2),('018',2),('020',2),('021',2),('022',2),('036',2),('037',4),('038',2),('040',2),('041',2),('042',2)]:
 path=OUT/f'generation-provenance-bare-walk-{key}-v{revision}.json';inputs[str(path)]=sha(path)
neighbors.save(OUT/'neighbor-detail-family-review.png')
middle=Image.new('RGBA',(1900,1590),(31,35,40,255));md=ImageDraw.Draw(middle)
groups=[[(f'{n:03} current source',OUT/f'bare-walk-{n:03}-candidate.png') for n in group] for group in [(22,23,24,25,26),(31,32,33,34,35)]]
groups.append([('Original master',master),('Water ready / prior source',water/'bare-ready-candidate.png'),('Water rise / prior source',water/'bare-rise-candidate.png')])
for row,group in enumerate(groups):
 for col,(label,path) in enumerate(group):
  inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
  if im.size==(256,256):
   common=Image.new('RGBA',(352,320));common.alpha_composite(im,(32,0));im=common
  assert im.size==(352,320)
  x=col*380;y=row*530;md.text((x+8,y+8),label,fill='white');middle.alpha_composite(im,(x+8,y+30))
  middle.alpha_composite(im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+75,y+370))
for key,revision in [('023',2),('024',2),('032',3),('035',3)]:
 path=OUT/f'generation-provenance-bare-walk-{key}-v{revision}.json';inputs[str(path)]=sha(path)
for key,revision in [('023',3),('025',3),('031',3),('047',2)]:
 path=OUT/f'generation-provenance-bare-walk-{key}-v{revision}.json';inputs[str(path)]=sha(path)
middle.save(OUT/'middle-detail-family-review.png')
seam=Image.new('RGBA',(1900,1590),(31,35,40,255));sd=ImageDraw.Draw(seam)
preferred={p['key']:p for p in json.loads((OUT/'review.json').read_text())['poses']}
seamGroups=[]
for label in ['Before preferred edit','Current source']:
 seamGroups.append([(f'{n:03} | {label}',Path(preferred[f'bare-walk-{n:03}']['sourcePath']) if label=='Before preferred edit' else OUT/f'bare-walk-{n:03}-candidate.png') for n in [45,46,47,0,1]])
seamGroups.append([('Original master',master),('Water ready / prior source',water/'bare-ready-candidate.png'),('Water rise / prior source',water/'bare-rise-candidate.png')])
for row,group in enumerate(seamGroups):
 for col,(label,path) in enumerate(group):
  inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
  if im.size==(256,256):
   common=Image.new('RGBA',(352,320));common.alpha_composite(im,(32,0));im=common
  assert im.size==(352,320)
  x=col*380;y=row*530;sd.text((x+8,y+8),label,fill='white');seam.alpha_composite(im,(x+8,y+30))
  seam.alpha_composite(im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+75,y+370))
for key in ['000','001','045','046']:
 path=OUT/f'generation-provenance-bare-walk-{key}-v2.json';inputs[str(path)]=sha(path)
faceSupport=OUT/'sources/original-master-face-detail-reference.png';inputs[str(faceSupport)]=sha(faceSupport)
seam.save(OUT/'seam-face-detail-review.png')
trials=Image.new('RGBA',(1520,1120),(31,35,40,255));td=ImageDraw.Draw(trials)
for row,key in enumerate(['000','046']):
 rejectedReceipt=OUT/f'generation-provenance-bare-walk-{key}-v2.json';rejected=json.loads(rejectedReceipt.read_text())
 inputs[str(rejectedReceipt)]=sha(rejectedReceipt)
 trialPaths=[('Before face trial',Path(rejected['sourcePath'])),('Rejected face-reference / full canvas',Path(rejected['savedPath'])),('Preferred study',OUT/f'bare-walk-{key}-candidate.png'),('Original master',master)]
 for col,(label,path) in enumerate(trialPaths):
  inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
  if col==1:im=im.resize((352,352),Image.Resampling.LANCZOS)
  elif im.size==(256,256):
   common=Image.new('RGBA',(352,352));common.alpha_composite(im,(32,0));im=common
  elif im.size==(352,320):
   common=Image.new('RGBA',(352,352));common.alpha_composite(im);im=common
  assert im.size==(352,352)
  x=col*380;y=row*560;td.text((x+8,y+8),f'{key} | {label}',fill='white');trials.alpha_composite(im,(x+8,y+30))
  trials.alpha_composite(im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+75,y+400))
retryReceipt=OUT/'generation-provenance-bare-walk-046-v3.json';inputs[str(retryReceipt)]=sha(retryReceipt)
commonReceipt=OUT/'generation-provenance-bare-walk-046-v4.json';inputs[str(commonReceipt)]=sha(commonReceipt)
commonSupport=OUT/'sources/original-master-face-common-canvas-reference.png';inputs[str(commonSupport)]=sha(commonSupport)
trials.save(OUT/'face-reference-trials-review.png')
for name in ['generation-provenance-bare-walk-046-v5.json','sources/bare-walk-046-prompt-v5.txt','sources/bare-walk-046-edit-v5.png','bare-walk-046-rejected-v5-candidate.png','bare-walk-046-rejected-v5-review.png']:
 path=OUT/name;inputs[str(path)]=sha(path)
(OUT/'cropped-master-detail-review.json').write_text(json.dumps({'inputs':inputs,'normalAdmission':False,'fullVisualAcceptance':False},indent=2)+'\n',encoding='utf-8')
review=OUT/'review.json';phases={}
standardHash=sha(OUT/'sources/bare-walk-041-prompt-v2.txt')
restrainedHash=sha(OUT/'sources/bare-walk-023-prompt-v3.txt')
faceHash=sha(OUT/'sources/bare-walk-000-prompt-v2.txt')
singleFaceHash=sha(OUT/'sources/bare-walk-046-prompt-v3.txt')
commonFaceHash=sha(OUT/'sources/bare-walk-046-prompt-v4.txt')
for pose in json.loads(review.read_text())['poses']:
 if not pose['key'].startswith('bare-walk-'):continue
 receipt=OUT/f"generation-provenance-{pose['key']}-v{pose['revision']}.json"
 authored=json.loads(receipt.read_text())
 phases[pose['key']]={'revision':pose['revision'],'receiptPath':str(receipt),'receiptSha256':sha(receipt),'croppedMasterDetailPrompt':authored['promptSha256']==standardHash,'restrainedSleeveCollarPrompt':authored['promptSha256']==restrainedHash,'faceInteriorDefinitionPrompt':authored['promptSha256']==faceHash,'provisional':True}
 phases[pose['key']]['singleTargetFaceDefinitionPrompt']=authored['promptSha256']==singleFaceHash
 phases[pose['key']]['commonCanvasFaceDefinitionPrompt']=authored['promptSha256']==commonFaceHash
coverage={'reviewSha256':sha(review),'phases':phases,'croppedMasterDetailCount':sum(p['croppedMasterDetailPrompt'] for p in phases.values()),'restrainedSleeveCollarCount':sum(p['restrainedSleeveCollarPrompt'] for p in phases.values()),'coverageMeaning':'authoring method only, not visual acceptance','normalAdmission':False,'fullVisualAcceptance':False}
coverage['faceInteriorDefinitionCount']=sum(p['faceInteriorDefinitionPrompt'] for p in phases.values())
coverage['singleTargetFaceDefinitionCount']=sum(p['singleTargetFaceDefinitionPrompt'] for p in phases.values())
coverage['commonCanvasFaceDefinitionCount']=sum(p['commonCanvasFaceDefinitionPrompt'] for p in phases.values())
(OUT/'detail-pass-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n',encoding='utf-8')
print(f'{len(inputs)} frozen material comparison inputs')
