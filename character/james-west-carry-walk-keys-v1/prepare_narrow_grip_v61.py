from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'narrow-grip-phase24-v61';out.mkdir(exist_ok=True)
crop=Image.open(p/'case-grip-material-phase24-v57/native-generated-crop.png').convert('RGBA');boxes=[(90,128,134,155),(107,122,119,128)]
for mode in ['bare','helmet']:
    f=p/'master-material-phase24-v52'/(mode+'-head-protected.png');src=Image.open(f).convert('RGBA');im=src.copy();mask=np.ones((256,256),dtype=bool)
    for box in boxes:
        im.paste(crop.crop((box[0]-80,box[1]-104,box[2]-80,box[3]-104)),box[:2]);mask[box[1]:box[3],box[0]:box[2]]=False
    assert np.array_equal(np.asarray(im)[mask],np.asarray(src)[mask]);assert int(mask.sum())==64276
    im.save(out/(mode+'-candidate.png'))
board=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('material base',p/'master-material-phase24-v52'/(mode+'-head-protected.png')),('broad patch V57',p/'case-grip-material-phase24-v57'/(mode+'-candidate.png')),('narrow patch V61',out/(mode+'-candidate.png'))]):
        board.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+4,row*280+5),mode+' '+label,fill='white')
board.save(out/'admission-review.png')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
fs=[p/'case-grip-material-phase24-v57/native-generated-crop.png']+[p/'master-material-phase24-v52'/(m+'-head-protected.png') for m in ['bare','helmet']]
(out/'inputs.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():sha(f) for f in fs},admissionBoxes=boxes,outsidePixelsExact=64276,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
# Rebuild the same consecutive fixture under a new immutable study identity.
s=(p/'prepare_middle_window_v60.py').read_text().replace("out=p/'middle-window-v60'","out=p/'middle-window-v61'").replace('middle-window-v60','middle-window-v61').replace("p/'case-grip-material-phase24-v57'","p/'narrow-grip-phase24-v61'")
(p/'prepare_middle_window_v61.py').write_text(s,encoding='utf-8')
print('Narrow admission protects64276outside pixels, including sleeve/chest context. New window helper saved.')
