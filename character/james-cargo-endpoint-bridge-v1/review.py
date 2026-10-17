from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preGenerationSha256'].items())
raw=Image.open(p/'raw.png').convert('RGBA');w,h=raw.size
cells=[]
for row in range(2):
    for col in range(2):
        cells.append(raw.crop((round(col*w/2),round(row*h/2),round((col+1)*w/2),round((row+1)*h/2))))
def bounds(im):
    yy,xx=np.where(np.asarray(im)[:,:,3]>=32)
    return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
b=bounds(cells[0]);scale=148/(b[3]-b[1])
a=np.asarray(cells[0])[:,:,3]>=32;yy,xx=np.where(a & (np.indices(a.shape)[0]>=b[3]-20))
anchor=[int(xx.max()+1),b[3]]
offset=[round(128-anchor[0]*scale),round(224-anchor[1]*scale)]
out=p/'fixed-first-ruler';out.mkdir(exist_ok=True)
poses=[];diagnostics=[]
for i,cell in enumerate(cells):
    small=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(256,256));im.alpha_composite(small,tuple(offset));im.save(out/f'{i:03d}.png');poses.append(im)
    diagnostics.append({'index':i,'rawBounds':bounds(cell),'packagedBounds':bounds(im)})
entry=Image.open(r/inputs['roles']['entry']).convert('RGBA');ending=Image.open(r/inputs['roles']['exit']).convert('RGBA')
board=Image.new('RGB',(1536,550),'#303b40');d=ImageDraw.Draw(board)
for i,(label,im) in enumerate([('exact entry',entry)]+[(f'intermediate{k+1}',im) for k,im in enumerate(poses)]+[('exact exit',ending)]):
    bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im)
    board.paste(bg.convert('RGB'),(i*256,24));d.text((i*256+4,4),label,fill='white')
    board.paste(bg.convert('RGB').crop((84,64,148,128)).resize((256,256),Image.Resampling.NEAREST),(i*256,290))
board.save(p/'whole-head-review.png')
report={'selected':False,'visualReviewPending':True,'rawSize':[w,h],
 'preCallInputHashesUnchanged':True,'rawSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),
 'recipe':{'scaleFromFirstAlpha32HeightOnly':scale,'firstFootRightBottomDiagnosticAnchor':anchor,'oneCommonOffset':offset,'canvas':[256,256],'pivot':[128,224],'standingReferenceHeight':148,'perPoseFitting':False,'gradeApplied':False},
 'diagnostics':diagnostics,'scope':'Unselected source review. First alpha-height ruler and bottom/right foot proxy are diagnostics, not anatomical/contact acceptance. No native actor, helmet, timing or normal admission.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
