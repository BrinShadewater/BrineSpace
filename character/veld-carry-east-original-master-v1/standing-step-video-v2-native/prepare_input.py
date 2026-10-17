from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
assert not (P/'generation.json').exists()
src=R/'character/veld-east-held-original-master-v1/frames/bare/000.png'
im=Image.open(src).convert('RGBA')
large=im.resize((768,768),Image.Resampling.NEAREST)
plate=Image.new('RGBA',(768,960));plate.alpha_composite(large,(0,96))
white=Image.new('RGBA',plate.size,'white');white.alpha_composite(plate)
white.convert('RGB').save(P/'master-input.png');plate.save(P/'whole-source-reference.png')
# Exact inverse reference confirms conditioning starts at the actual master.
registered=plate.resize((256,320),Image.Resampling.NEAREST).crop((0,32,256,288))
assert registered.tobytes()==im.tobytes()
registered.save(P/'registered-reference.png')
board=Image.new('RGB',(640,310),(32,43,49));d=ImageDraw.Draw(board)
for i,(image,label) in enumerate([(registered,'Exact inverse input'),(im,'Original native held master')]):
 board.paste(image,(i*320+32,30),image);d.text((i*320+20,10),label,fill='white')
board.save(P/'input-master-review.png')
record={'source':src.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'plateSize':[768,960],'nativeScale':3,'plateOffset':[0,96],'fixedOffset':[0,-32],'sourceScale':1/3,'nativeSize':[256,320],'exactInverseRGBA':True,'inputSha256':hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest(),'endpointIdentical':True,'estimatedUSD':.28,'billingVerified':False,'conditioningChange':'Actual original native pixel-dense sprite whole3x nearest instead of original high-resolution raw source. White plate unchanged in material purpose; no newly drawn body.','scope':'One changed-conditioning dense two-step trial, fixed camera/ruler, no per-frame position/density correction or paid retries. Full clip must preserve identity/contact before adoption.'}
(P/'input-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
