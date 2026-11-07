"""Package Veld's straight-facing south tread with the established anchor."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
source=ROOT/'generated/veld-tread-south-candidate-02.png'
raw=Image.open(source).convert('RGBA');pixels=np.array(raw);rgb=pixels[:,:,:3].astype(np.int16)
pixels[(rgb[:,:,0]>rgb[:,:,1]+35)&(rgb[:,:,2]>rgb[:,:,1]+35)]=0
clean=Image.fromarray(pixels);occupied=(pixels[:,:,3]>0).sum(axis=0)>3
edges=np.diff(np.r_[False,occupied,False].astype(int))
groups=[(int(a),int(b)) for a,b in zip(np.where(edges==1)[0],np.where(edges==-1)[0]) if b-a>25]
assert len(groups)==6
anchors=[(177,381),(442,381),(707,381),(966,381),(1228,381),(1490,381)]
factor=raw.width/1672;scale=(14/80)/factor
pack=ROOT/'revisions/veld-tread-south-v2';pack.mkdir(exist_ok=True);helmet_dir=pack/'helmet';helmet_dir.mkdir(exist_ok=True)
overlay_path=ROOT/'equipment/front/overlay.png';overlay=Image.open(overlay_path).convert('RGBA')
sheet=Image.new('RGB',(1104,368),'#1d252a');registration=[]
for i,((left,right),(sx,sy)) in enumerate(zip(groups,anchors)):
    local=clean.crop((left,0,right,raw.height));box=local.getbbox();crop=(left+box[0],box[1],left+box[2],box[3])
    body=clean.crop(crop);body=body.resize((round(body.width*scale),round(body.height*scale)),Image.Resampling.BOX)
    arr=np.array(body);arr[arr[:,:,3]<128]=0;arr[arr[:,:,3]>=128,3]=255;body=Image.fromarray(arr)
    pos=(round(46-(sx*factor-crop[0])*scale),round(35-(sy*factor-crop[1])*scale))
    assert pos[0]>0 and pos[1]>0 and pos[0]+body.width<92 and pos[1]+body.height<92
    frame=Image.new('RGBA',(92,92));frame.alpha_composite(body,pos);name=f'frame_{i:03}.png';frame.save(pack/name)
    fitted=frame.copy();fitted.alpha_composite(overlay,(34,13));fitted.save(helmet_dir/name)
    registration.append({'crop':crop,'shoulder':[sx*factor,sy*factor],'paste':pos,'bodySha256':hashlib.sha256((pack/name).read_bytes()).hexdigest(),'overlayTopLeft':[34,13]})
    for row,image in enumerate([frame,fitted]):
        large=image.resize((184,184),Image.Resampling.NEAREST);sheet.paste(large,(i*184,row*184),large)
manifest={'status':'integrated_provisional_facing_revision','frameWidth':92,'frameHeight':92,'pivot':[46,35],'states':[{'id':'tread-south','frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[160]*6,'loop':True}]}
(pack/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');manifest['equipment']='diving-helmet'
(helmet_dir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(pack/'registration.json').write_text(json.dumps({'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'overlay':overlay_path.relative_to(ROOT).as_posix(),'overlaySha256':hashlib.sha256(overlay_path.read_bytes()).hexdigest(),'frames':registration},indent=2)+'\n',encoding='utf-8')
sheet.save(pack/'contact.png')
print('Six tread bodies and six helmet candidates packaged')
