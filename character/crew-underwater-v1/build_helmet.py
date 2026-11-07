"""Extract authored helmet pixels; fitted character overlays remain separate."""
from pathlib import Path
import hashlib, json, argparse
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--view',choices=['front','east','north','west'],default='front')
view=parser.parse_args().view
source=root/'generated'/f'helmet-{view}-overlay.png'
if view=='north': source=root/'generated/diving-helmet-views.png'
pixels=np.array(Image.open(source).convert('RGBA'))
rgb=pixels[:,:,:3].astype(np.int16)
key=(rgb[:,:,0]>rgb[:,:,1]+35)&(rgb[:,:,2]>rgb[:,:,1]+35)
pixels[key]=0
im=Image.fromarray(pixels)
if view=='west':
    # Match the final binary-alpha contract before measuring faint alpha debris.
    im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
if view=='north':
    # Authored rear view, second column of the four-view source.
    im=im.crop((460,240,800,640))
visor_point=(627,640) if view=='front' else (820,600)
if view=='west': visor_point=(420,600)
if view!='north': assert im.getpixel(visor_point)[3]==0, 'Visor must be open'
box=im.getbbox(); im=im.crop(box)
out=root/'equipment'/view;out.mkdir(parents=True,exist_ok=True)
im.save(out/'source-cutout.png')
small=im.resize((round(im.width*28/im.height),28),Image.Resampling.BOX)
small.putalpha(small.getchannel('A').point(lambda a:255 if a>=128 else 0))
packed_point=(round((visor_point[0]-box[0])*28/im.height),round((visor_point[1]-box[1])*28/im.height))
if view!='north': assert small.getpixel(packed_point)[3]==0, 'Packed visor must remain open'
small.save(out/'overlay.png')
(out/'manifest.json').write_text(json.dumps({'status':'overlay_pilot_not_fitted','direction':'south' if view=='front' else view,'source':f'../../generated/helmet-{view}-overlay.png','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceCrop':box,'size':small.size,'visor':'open alpha; no glass layer yet','characterAnchors':'pending','hairOcclusion':'pending'},indent=2)+'\n')
if view=='north':
    metadata=json.loads((out/'manifest.json').read_text())
    metadata.update(source='../../generated/diving-helmet-views.png',sourceRegion=[460,240,800,640],visor='opaque rear shell; no rear visor')
    (out/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(view+' helmet extracted; '+('opaque rear shell' if view=='north' else 'visor alpha verified')+'; character fitting pending')
