from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
indices=[0,8,12,20,28,36,44,48]
sources=[p/'walk00-meter-occlusion-v2.png',p/'walk08-carry.png',p/'walk12-case-v2.png',p/'walk20-carry.png',p/'walk28-case-v2.png',p/'walk36-case-v2.png',p/'walk44-carry.png',p/'walk48-carry.png']
whole=Image.new('RGBA',(1024,564),(48,59,63,255));upper=Image.new('RGBA',(1536,820),(48,59,63,255));wd=ImageDraw.Draw(whole);ud=ImageDraw.Draw(upper);files=[];poses=[]
for i,(index,source) in enumerate(zip(indices,sources)):
    im=Image.open(source).convert('RGBA');row,col=divmod(i,4);whole.alpha_composite(im,(col*256,row*282+26));upper.alpha_composite(im.crop((80,88,176,184)).resize((384,384),Image.Resampling.NEAREST),(col*384,row*410+26));wd.text((col*256+5,row*282+7),f'phase{index}',fill='white');ud.text((col*384+5,row*410+7),f'phase{index}',fill='white')
    orig=r/'character/james-west-carry-depth-v1/walk12-original.png' if index==12 else p/f'walk{index:02}-carry-original.png';a=Image.open(orig).convert('RGBA');aa=a.copy();bb=im.copy()
    for x in (aa,bb):x.paste((0,0,0,0),(88,104,166,169))
    assert aa.tobytes()==bb.tobytes();files.extend([source,orig]);poses.append({'index':index,'source':source.relative_to(r).as_posix(),'outside60466Exact':True,'donorBounds':a.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'carryBounds':im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()})
for start in (0,4):
    station=Image.new('RGBA',(900,820),(48,59,63,255));d=ImageDraw.Draw(station)
    for row,(index,source) in enumerate(list(zip(indices,sources))[start:start+4]):
        im=Image.open(source).convert('RGBA')
        for j,h in enumerate([148,82,54,27]):
            size=round(256*h/148);x=[140,410,620,790][j];station.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(round(x-128*h/148),round(row*205+195-224*h/148)));d.text((x-60,row*205+7),f'phase{index} {h}',fill='white')
    station.convert('RGB').save(p/f'eight-key-station-{start}.png')
whole.convert('RGB').save(p/'eight-key-full.png');upper.convert('RGB').save(p/'eight-key-upper.png')
(p/'eight-key-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'poses':poses,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Eight distinct provisional key sources, including actual48body; no complete49frame bank/continuous cadence/native or owner acceptance. Earlier8..36meters still uncorrected.'},indent=2)+'\n',encoding='utf-8')
print('Eight-key comparison prepared; original donor head/legs outside60466upper region exact.')
