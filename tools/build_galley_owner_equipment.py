"""Extract registered overhead kitchen/serving silhouettes without altering originals."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];pack=root/'assets/galley-owner-v2'
records=[]
for name,registration in [('kitchen','side-galley-kitchen-south'),('serving','side-galley-serving-south')]:
    rp=root/f'rooms/full-wall-v1/registrations/{registration}.json'
    reg=json.loads(rp.read_text());source=root/reg['source'].removeprefix('res://')
    im=Image.open(source).convert('RGBA');mask=Image.new('L',im.size);draw=ImageDraw.Draw(mask)
    for polygon in reg['pieces']:draw.polygon([tuple(p) for p in polygon],fill=255)
    im.putalpha(mask);crop=im.getbbox();im=im.crop(crop)
    # South source operates upward. Kitchen sits north and must operate downward.
    if name=='kitchen':im=im.transpose(Image.Transpose.ROTATE_180)
    for q,turn in enumerate([im,im.transpose(Image.Transpose.ROTATE_270),im.transpose(Image.Transpose.ROTATE_180),im.transpose(Image.Transpose.ROTATE_90)]):turn.save(pack/f'{name}-q{q}.png')
    records.append({'id':name,'source':str(source.relative_to(root)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'registration':str(rp.relative_to(root)),'crop':crop,'base_turn':180 if name=='kitchen' else 0,'stage':'prepared, pending native review'})
(pack/'equipment-review.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records))
