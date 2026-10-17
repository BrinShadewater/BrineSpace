from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[p/'walk00-tool-fix.png',r/'character/james-west-carry-depth-v1/walk12-carry.png',p/'walk28-tool-fix.png',p/'walk36-tool-fix.png'];labels=['phase0','phase12','phase28','phase36'];body=[];files=[]
board=Image.new('RGBA',(1280,282),(48,59,63,255));upper=Image.new('RGBA',(1920,410),(48,59,63,255));d=ImageDraw.Draw(board);u=ImageDraw.Draw(upper);master=r/'character/james-carry-headcaps-v1/frames/004.png'
for i,(source,label) in enumerate(zip([master]+sources,['standing carry']+labels)):
    im=Image.open(source).convert('RGBA');files.append(source);board.alpha_composite(im,(i*256,26));d.text((i*256+5,7),label,fill='white');upper.alpha_composite(im.crop((80,88,176,184)).resize((384,384),Image.Resampling.NEAREST),(i*384,26));u.text((i*384+5,7),label,fill='white')
    if i:body.append(im)
board.convert('RGB').save(p/'four-key-source-comparison.png');upper.convert('RGB').save(p/'four-key-upper-comparison.png')
station=Image.new('RGBA',(900,820),(48,59,63,255));d=ImageDraw.Draw(station)
for row,(im,label) in enumerate(zip(body,labels)):
    for j,h in enumerate([148,82,54,27]):
        size=round(256*h/148);x=[140,410,620,790][j];station.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(round(x-128*h/148),round(row*205+195-224*h/148)));d.text((x-60,row*205+7),label+' '+str(h),fill='white')
station.convert('RGB').save(p/'four-key-station-comparison.png')
inputs=[]
for index,source in zip([0,12,28,36],sources):
    orig=r/'character/james-west-carry-depth-v1/walk12-original.png' if index==12 else p/f'walk{index:02}-carry-original.png';files.append(orig);a=Image.open(orig).convert('RGBA');b=Image.open(source).convert('RGBA');aa=a.copy();bb=b.copy()
    for im in [aa,bb]:im.paste((0,0,0,0),(88,104,166,169))
    assert aa.tobytes()==bb.tobytes();assert a.crop((0,169,256,256)).tobytes()==b.crop((0,169,256,256)).tobytes();assert a.crop((0,0,256,104)).tobytes()==b.crop((0,0,256,104)).tobytes();inputs.append({'index':index,'source':source.relative_to(r).as_posix(),'outside60466Exact':True,'donorBounds':a.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'carryBounds':b.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox()})
(p/'study-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'poses':inputs,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Four authored source keys plus master comparison, no interpolated/repeated fake49frame bank. Complete carrying gait/cadence/native and owner acceptance pending.'},indent=2)+'\n',encoding='utf-8')
print('Four source key poses: original head/legs retained; complete cycle and source joins still pending.')
