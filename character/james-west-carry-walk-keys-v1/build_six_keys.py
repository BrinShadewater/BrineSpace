from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[p/'walk00-case-v2-fleck.png',p/'walk08-carry.png',r/'character/james-west-carry-depth-v1/walk12-carry.png',p/'walk20-carry.png',p/'walk28-tool-fix.png',p/'walk36-tool-fix.png']
indices=[0,8,12,20,28,36]
whole=Image.new('RGBA',(1536,282),(48,59,63,255));upper=Image.new('RGBA',(2304,410),(48,59,63,255));wd=ImageDraw.Draw(whole);ud=ImageDraw.Draw(upper)
station=Image.new('RGBA',(900,1230),(48,59,63,255));sd=ImageDraw.Draw(station)
files=[]
for i,(source,index) in enumerate(zip(sources,indices)):
    im=Image.open(source).convert('RGBA');whole.alpha_composite(im,(i*256,26));upper.alpha_composite(im.crop((80,88,176,184)).resize((384,384),Image.Resampling.NEAREST),(i*384,26));wd.text((i*256+5,7),f'phase{index}',fill='white');ud.text((i*384+5,7),f'phase{index}',fill='white')
    orig=r/'character/james-west-carry-depth-v1/walk12-original.png' if index==12 else p/f'walk{index:02}-carry-original.png'
    a=Image.open(orig).convert('RGBA');aa=a.copy();bb=im.copy()
    for f in (aa,bb):f.paste((0,0,0,0),(88,104,166,169))
    assert aa.tobytes()==bb.tobytes()
    files.extend([source,orig])
    for j,h in enumerate([148,82,54,27]):
        sz=round(256*h/148);x=[140,410,620,790][j];station.alpha_composite(im.resize((sz,sz),Image.Resampling.LANCZOS),(round(x-128*h/148),round(i*205+195-224*h/148)));sd.text((x-60,i*205+7),f'phase{index} {h}',fill='white')
whole.convert('RGB').save(p/'six-key-full.png');upper.convert('RGB').save(p/'six-key-upper.png');station.convert('RGB').save(p/'six-key-station.png')
(p/'six-key-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'indices':indices,'allOutside60466Exact':True,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Six authored source poses, incomplete loop; no invented/repeated49frame bank or temporal/native acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Six provisional source keys compared, original head/legs outside upper admission exact.')
