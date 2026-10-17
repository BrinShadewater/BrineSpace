from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'sleeve-phase24-v63';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((48,48),Image.Resampling.LANCZOS);crop.save(out/'native-generated-crop.png');boxes=[(128,112,146,128),(126,128,142,138)]
results={}
for mode in ['bare','helmet']:
    src=Image.open(p/'narrow-grip-phase24-v62'/(mode+'-candidate.png')).convert('RGBA');im=src.copy();mask=np.ones((256,256),dtype=bool)
    for box in boxes:
        im.paste(crop.crop((box[0]-110,box[1]-96,box[2]-110,box[3]-96)),box[:2]);mask[box[1]:box[3],box[0]:box[2]]=False
    assert int(mask.sum())==65088 and np.array_equal(np.asarray(im)[mask],np.asarray(src)[mask])
    assert np.array_equal(np.asarray(im)[:104],np.asarray(src)[:104]) and np.array_equal(np.asarray(im)[138:],np.asarray(src)[138:])
    im.save(out/(mode+'-candidate.png'));results[mode]=im
assert np.array_equal(np.asarray(results['bare'])[110:],np.asarray(results['helmet'])[110:])
board=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
    fs=[p/'master-material-phase23-v58'/(mode+'-head-protected.png'),out/(mode+'-candidate.png'),p/'master-material-phase25-v59'/(mode+'-head-protected.png')]
    for col,f in enumerate(fs):
        board.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+4,row*280+5),mode+' pose'+str(23+col),fill='white')
board.save(out/'consecutive-sleeve-review.png')
contact=Image.new('RGBA',(576,164),(47,58,63,255));cd=ImageDraw.Draw(contact)
for col,(label,im) in enumerate([('before',Image.open(p/'narrow-grip-phase24-v62/bare-candidate.png').convert('RGBA')),('sleeve repair',results['bare']),('previous pose',Image.open(p/'master-material-phase23-v58/bare-head-protected.png').convert('RGBA')),('next pose',Image.open(p/'master-material-phase25-v59/bare-head-protected.png').convert('RGBA'))]):
    contact.alpha_composite(im.crop((110,96,158,144)).resize((144,144),Image.Resampling.NEAREST),(col*144,20));cd.text((col*144+3,3),label,fill='white')
contact.save(out/'sleeve-contact-review.png')
(out/'review.json').write_text(json.dumps(dict(rawSize=list(raw.size),admissionBoxes=boxes,outsidePixelsExact=65088,topHeadAndBelow138Exact=True,pairedBodyBelow110Exact=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,visualReviewPending=True),indent=2)+'\n')
s=(p/'prepare_middle_window_v62.py').read_text().replace('middle-window-v62','middle-window-v63').replace("p/'narrow-grip-phase24-v62'","p/'sleeve-phase24-v63'")
(p/'prepare_middle_window_v63.py').write_text(s,encoding='utf-8')
print('448sleeve-region pixels admitted;65088outside pixels protected. Window helper saved.')
