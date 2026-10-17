from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
originals=[Image.open(r/file).convert('RGBA') for file in inputs['sources']]
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.width==raw.height and raw.width%2==0
cell=raw.width//2;region=(104,64,162,134);frames=[originals[0]];out=p/'frames';out.mkdir(exist_ok=True)
checks=[]
for i in range(4):
    source=raw.crop((i%2*cell,i//2*cell,(i%2+1)*cell,(i//2+1)*cell)).resize((80,80),Image.Resampling.LANCZOS)
    layer=Image.new('RGBA',(256,256));layer.alpha_composite(source,(96,56))
    candidate=originals[i+1].copy();candidate.paste(layer.crop(region),(104,64))
    a=np.asarray(originals[i+1]);b=np.asarray(candidate);mask=np.ones((256,256),bool);mask[64:134,104:162]=False
    assert np.array_equal(a[mask],b[mask]);candidate.save(out/f'{i:03d}.png');frames.append(candidate)
    checks.append({'index':i,'protectedOriginalPixels':int(mask.sum())})
frames.append(originals[-1])
def diag(im):
    a=np.asarray(im);yy,xx=np.where(a[:,:,3]>=32);return {'crownRoot':int(224-yy.min()),'lowestAlphaRow':int(yy.max())}
def flat(im):
    bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im);return bg.convert('RGB')
board=Image.new('RGB',(1536,2*560),'#303b40');d=ImageDraw.Draw(board)
for row,poses in enumerate([originals,frames]):
    for i,im in enumerate(poses):
        y=row*560;bg=flat(im);board.paste(bg,(i*256,y+24));d.text((i*256+4,y+4),f'{"normal" if row==0 else "joint atlas"} {i} crown{diag(im)["crownRoot"]}',fill='white')
        board.paste(bg.crop((96,56,160,120)).resize((256,256),Image.Resampling.NEAREST),(i*256,y+290))
board.save(p/'whole-upper-review.png')
report={'selected':False,'normalSelectionChanged':False,'visualReviewPending':True,'rawSize':list(raw.size),'cellUniformScale':80/cell,'cropOrigin':[96,56],'admissionRect':list(region),'checks':checks,'normalDiagnostics':[diag(im) for im in originals],'trialDiagnostics':[diag(im) for im in frames],'inputHashesUnchanged':True,'rawSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'scope':'Joint four upper crops at one cell scale, no grading, translation or per-pose fit. Twelve full poses/twelve enlarged upper views beside exact endpoints; anatomical/camera/temporal acceptance separate from pixel protection.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
