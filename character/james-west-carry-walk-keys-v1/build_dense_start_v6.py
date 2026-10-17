from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];indices=list(range(13))
sources=[p/('walk12-case-master-v5-seam.png' if i==12 else f'walk{i:02d}-case-master-v5.png' if i in (0,8) else f'walk{i:02d}-dense-carry-v6.png') for i in indices]
files=[];checks=[]
for i,f in zip(indices,sources):
    donor=p/f'walk{i:02d}-dense-carry-v6-original.png' if i not in (0,8,12) else r/'character/james-west-carry-depth-v1/walk12-original.png' if i==12 else p/f'walk{i:02d}-carry-original.png'
    a=Image.open(donor).convert('RGBA');b=Image.open(f).convert('RGBA');aa=a.copy();bb=b.copy()
    for im in (aa,bb):im.paste((0,0,0,0),(88,104,166,169))
    assert aa.tobytes()==bb.tobytes();files.extend([donor,f]);checks.append({'phase':i,'outside60466Exact':True})
for start in (0,7):
    subset=list(zip(indices,sources))[start:start+7]
    full=Image.new('RGBA',(len(subset)*256,282),(48,59,63,255));upper=Image.new('RGBA',(len(subset)*192,218),(48,59,63,255));fd=ImageDraw.Draw(full);ud=ImageDraw.Draw(upper)
    for col,(i,f) in enumerate(subset):
        im=Image.open(f).convert('RGBA');full.alpha_composite(im,(col*256,26));upper.alpha_composite(im.crop((80,88,176,184)).resize((192,192),Image.Resampling.NEAREST),(col*192,26));fd.text((col*256+5,7),f'phase{i}',fill='white');ud.text((col*192+5,7),f'phase{i}',fill='white')
    full.convert('RGB').save(p/f'dense-start-v6-full-{start}.png');upper.convert('RGB').save(p/f'dense-start-v6-upper-{start}.png')
for start in (0,4,8,12):
    subset=list(zip(indices,sources))[start:start+4];board=Image.new('RGBA',(900,len(subset)*205),(48,59,63,255));d=ImageDraw.Draw(board)
    for row,(i,f) in enumerate(subset):
        im=Image.open(f).convert('RGBA')
        for j,h in enumerate((148,82,54,27)):
            size=round(256*h/148);x=(140,410,620,790)[j];board.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(round(x-128*h/148),round(row*205+195-224*h/148)));d.text((x-60,row*205+7),f'phase{i} {h}',fill='white')
    board.convert('RGB').save(p/f'dense-start-v6-station-{start}.png')
plan=json.loads((p/'dense-walk-v6-plan.json').read_bytes());durations=plan['state']['frameDurationsMs'];assert len(durations)==49
(p/'dense-start-v6-review.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'checks':checks,'phases':indices,'fullWalkDurationsMs':durations,'fullWalkDurationMs':sum(durations),'sliceDurationsMs':durations[:13],'sliceDurationMs':sum(durations[:13]),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'13consecutive chronological original-body carrying sources. Finite initial slice only;31interiors still missing. No complete loop/helmet/native/context acceptance.'},indent=2)+'\n',encoding='utf-8')
print(f'13consecutive sources compared; actual selected variable full-clock{sum(durations)}ms, slice{sum(durations[:13])}ms.')
