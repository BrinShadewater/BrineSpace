from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];rect=(88,154,176,224)
sources=[r/'character/james-west-carry-gait-master-v2/near-feet2.png',p/'passing-near-support.png',r/'character/james-west-carry-gait-master-v2/contact-far-feet.png'];labels=['near contact','near support / far swing','far contact']
gearFile=r/'character/james-carry-authored-helmet-v1/frames/004.png';gear=Image.open(gearFile).convert('RGBA');files=sources+[gearFile];images=[]
board=Image.new('RGBA',(768,564),(48,59,63,255));d=ImageDraw.Draw(board)
for i,source in enumerate(sources):
    bare=Image.open(source).convert('RGBA');helmet=gear.copy();helmet.paste(bare.crop(rect),rect[:2]);images.append(bare)
    if i==1:helmet.save(p/'passing-near-support-helmet.png');files.append(p/'passing-near-support-helmet.png')
    for row,im in enumerate([bare,helmet]):board.alpha_composite(im,(i*256,row*282+26));d.text((i*256+4,row*282+7),('bare ' if not row else 'helmet ')+labels[i],fill='white')
board.convert('RGB').save(p/'contact-passing-source-study.png')
detail=Image.new('RGBA',(1152,410),(48,59,63,255));d=ImageDraw.Draw(detail)
for i,im in enumerate(images):detail.alpha_composite(im.crop((80,144,176,240)).resize((384,384),Image.Resampling.NEAREST),(i*384,26));d.text((i*384+5,7),labels[i],fill='white')
detail.convert('RGB').save(p/'contact-passing-detail.png')
raw=Image.open(p/'passing-near-support-native-crop.png').convert('RGBA');rawData=json.loads((p/'raw-contact-review.json').read_bytes());rawRow=next(v for v in rawData['poses'] if v['pose']=='passing-near-support');assert rawRow['rawBottomWorld']==224 and rawRow['rawAlpha128PixelsAtOrBelowWorld224']==0 and rawRow['rawRedGuidePixels']==0
pose=images[1];regions=[(88,197,120,240),(124,197,152,240)];boxes=[pose.getchannel('A').crop(box).point(lambda x:255 if x>=128 else 0).getbbox() for box in regions];assert boxes[0][3]+197<224 and boxes[1][3]+197==224
(p/'source-study-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'supportSwingRegions':regions,'regionBounds':boxes,'rawContact':rawRow,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Three source poses show near contact -> gold-near support/plain-far swing -> far contact. Not complete loop, temporal gait or context acceptance.'},indent=2)+'\n',encoding='utf-8')
print('One raw224 support pose, lifted far foot, paired helmet and adjacent contact sources compared.')
