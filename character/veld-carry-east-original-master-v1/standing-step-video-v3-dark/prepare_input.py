from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[2]; S=P.parent/'standing-step-video-v2-native'
assert not (P/'generation.json').exists()
source=R/'character/veld-east-held-original-master-v1/frames/bare/000.png'
im=Image.open(source).convert('RGBA'); plate=Image.new('RGBA',(768,960));plate.alpha_composite(im.resize((768,768),Image.Resampling.NEAREST),(0,96))
background=(12,18,24); opaque=Image.new('RGBA',plate.size,background+(255,));opaque.alpha_composite(plate);opaque.convert('RGB').save(P/'master-input.png');plate.save(P/'whole-source-reference.png')
registered=plate.resize((256,320),Image.Resampling.NEAREST).crop((0,32,256,288));assert registered.tobytes()==im.tobytes();registered.save(P/'registered-reference.png')
prior=Image.open(S/'master-input.png').convert('RGB'); current=opaque.convert('RGB')
board=Image.new('RGB',(1536,960),(32,43,49));board.paste(prior,(0,0));board.paste(current,(768,0));board.save(P/'background-conditioning-review.png')
old=(S/'prompt.txt').read_text(encoding='utf-8').strip(); prompt=old.replace('Plain uniform white background.','Plain perfectly uniform dark blue-black background, RGB12,18,24.').replace('Keep the same white background','Keep the same dark blue-black background')
assert len(prompt)<=2000
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
record={'source':source.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'inputSha256':hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest(),'backgroundRGB':background,'plateSize':[768,960],'nativeScale':3,'plateOffset':[0,96],'sourceScale':1/3,'fixedOffset':[0,-32],'nativeSize':[256,320],'exactInverseRGBA':True,'endpointIdentical':True,'estimatedUSD':.28,'billingVerified':False,'conditioningChange':'Only flat background changed from white to dark RGB12,18,24. Same native original whole source,3xnearest,plate and exact motion prompt apart from background terms. No identity/density/anatomy/region RGB repair.','scope':'Single explicit background-conditioning trial. Original full142 white source retained. Full returned clip and master/edge/leg contact must be reviewed before any admission; no automatic paid retry.'}
(P/'input-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exactInverseRGBA':True,'backgroundRGB':background,'promptCharacters':len(prompt),'inputSHA256':record['inputSha256']}))
