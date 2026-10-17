import hashlib,json
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((HERE/'registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'));checks=0
def check(v,message):
 global checks
 assert v,message
 checks+=1
check((p['frameWidth'],p['frameHeight'],p['pivot'],p['standingHeight'])==(208,184,[122,88],148),'water registration')
s=p['states'][0];check(s['loop'] and sum(s['frameDurationsMs'])==960,'retained loop clock');check(s['waterPoses']==[True]*6 and s['waterKinds']==['swim']*6,'water metadata');check(len(s['frameFiles'])==6,'six poses')
check(all(v['scale']==.27 for v in r['frames']),'frozen anatomical scale');check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'source hash')
for file in s['frameFiles']:
 im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox();check(im.size==(208,184),'dimensions');check(box[0]>0 and box[1]>0 and box[2]<208 and box[3]<184,'clearance');check(im.getpixel((0,0))[3]==0,'transparent corner');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'packaging, provenance, metadata and clipping; visual quality/owner/runtime acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' packaging checks PASS; staged candidate')
