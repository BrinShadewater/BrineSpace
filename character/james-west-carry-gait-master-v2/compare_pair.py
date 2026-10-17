from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];names=['contact-near','base','contact-far'];rect=(88,154,176,224)
gearSource=r/'character/james-carry-authored-helmet-v1/frames/004.png';gearBase=Image.open(gearSource).convert('RGBA');base=Image.open(p/'base.png').convert('RGBA');groups=[[],[]];files=[gearSource]
for name in names:
    source=p/(name+'.png');bare=Image.open(source).convert('RGBA');files.append(source);helmet=gearBase.copy();helmet.paste(bare.crop(rect),rect[:2]);helmet.save(p/(name+'-helmet.png'));files.append(p/(name+'-helmet.png'))
    aa=base.copy();bb=bare.copy()
    for im in [aa,bb]:im.paste((0,0,0,0),rect)
    assert aa.tobytes()==bb.tobytes()
    aa=gearBase.copy();bb=helmet.copy()
    for im in [aa,bb]:im.paste((0,0,0,0),rect)
    assert aa.tobytes()==bb.tobytes()
    assert bare.crop(rect).tobytes()==helmet.crop(rect).tobytes()
    groups[0].append(bare);groups[1].append(helmet)
out=Image.new('RGBA',(768,564),(48,59,63,255));d=ImageDraw.Draw(out)
for row,group in enumerate(groups):
    for col,im in enumerate(group):out.alpha_composite(im,(col*256,row*282+26));d.text((col*256+5,row*282+7),('bare ' if not row else 'helmet ')+names[col],fill='white')
out.convert('RGB').save(p/'paired-contact-study.png')
detail=Image.new('RGBA',(1152,410),(48,59,63,255));d=ImageDraw.Draw(detail)
for col,im in enumerate(groups[0]):detail.alpha_composite(im.crop((80,144,176,240)).resize((384,384),Image.Resampling.NEAREST),(col*384,26));d.text((col*384+5,7),names[col],fill='white')
detail.convert('RGB').save(p/'opposed-contact-detail.png')
(p/'pair-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'bareGearLegPixelsExact':True,'outsideLowerBodyExact':True,'protectedOutsidePixelsPerSource':59376,'bodyRuler':148,'bounds':[[im.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox() for im in group] for group in groups],'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Two opposed contacts and static endpoint, paired gear source study; not complete walking loop/native/cadence.'},indent=2)+'\n',encoding='utf-8')
print('Opposed contacts and exact paired legs compared;59376outside pixels preserved.')
