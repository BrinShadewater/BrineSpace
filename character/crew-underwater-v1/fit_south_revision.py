"""Package the generated overhead helmet and fit south candidate bodies."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
source=ROOT/'generated/helmet-swim-south-candidate-03.png'
raw=Image.open(source).convert('RGBA')
keyed=np.array(raw);rgb=keyed[:,:,:3].astype(np.int16)
keyed[(rgb[:,:,0]>rgb[:,:,1]+35)&(rgb[:,:,2]>rgb[:,:,1]+35)]=0
raw=Image.fromarray(keyed)
crop=raw.getbbox()
overlay=raw.crop(crop).resize((23,28),Image.Resampling.BOX)
data=np.array(overlay);data[data[:,:,3]<128]=0;data[data[:,:,3]>=128,3]=255
overlay=Image.fromarray(data)
assert overlay.getpixel((11,23))[3] == 0, 'Visor center must remain transparent'
equipment=ROOT/'equipment/swim-south';equipment.mkdir(exist_ok=True)
overlay.save(equipment/'overlay.png')
(equipment/'source-contract.json').write_text(json.dumps({'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':crop,'size':[23,28],'status':'integrated_provisional_fitting'},indent=2)+'\n',encoding='utf-8')
sheet=Image.new('RGB',(1248,672),'#1d252a')
for row,actor in enumerate(['bill','veld','branforth']):
    pack=ROOT/'revisions'/f'{actor}-swim-south-v2';out=pack/'helmet';out.mkdir(exist_ok=True)
    manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'));manifest['equipment']='diving-helmet'
    evidence={'overlay':'equipment/swim-south/overlay.png','overlaySha256':hashlib.sha256((equipment/'overlay.png').read_bytes()).hexdigest(),'status':'integrated_provisional_fitting','frames':[]}
    for i,file in enumerate(manifest['states'][0]['frameFiles']):
        body=Image.open(pack/file).convert('RGBA');frame=body.copy();pos=(40,65)
        frame.alpha_composite(overlay,pos);frame.save(out/file)
        evidence['frames'].append({'bodySha256':hashlib.sha256((pack/file).read_bytes()).hexdigest(),'overlayTopLeft':pos})
        large=frame.resize((208,224),Image.Resampling.NEAREST);sheet.paste(large,(i*208,row*224),large)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (out/'registration.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
sheet.save(ROOT/'revisions/helmet-south-contact.png')
print('18 south helmet candidate frames packaged')
