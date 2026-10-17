"""Package one authored component at a single original-master physical scale."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
raw=P/'sources/master-head-isolated-v1.png'
reference=P.parent/'bill-land-water-west-v9/sources/master-head-reference.png'
inputs=[raw,reference,P/'sources/master-head-isolation-prompt-v1.txt',Path(__file__)]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={str(f):sha(f) for f in inputs}
im=Image.open(raw).convert('RGBA');a=np.array(im)
labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel())
part=labs==np.argmax(counts[1:])+1
ys,xs=np.where(part)
assert xs.min()>0 and ys.min()>0 and xs.max()<im.width-1 and ys.max()<im.height-1
keep=binary_dilation(part,iterations=3)&(a[:,:,3]>0);a[~keep]=0
isolated=Image.fromarray(a);bounds=isolated.getbbox();crop=isolated.crop(bounds)
# Fixed donor calibration from reviewed hair crown to beard tip, not per-pose fitting.
sourceCrownY=66;sourceBeardTipY=1105
originalBrownHeadRuler=141;originalDensity=148/956
factor=originalBrownHeadRuler*originalDensity/(sourceBeardTipY-sourceCrownY)
native=crop.resize((round(crop.width*factor),round(crop.height*factor)),Image.Resampling.LANCZOS)
native.save(P/'sources/canonical-bare-head-v1.png')
ref=Image.open(reference).convert('RGBA');ref=ref.resize((round(ref.width*originalDensity),round(ref.height*originalDensity)),Image.Resampling.LANCZOS)
board=Image.new('RGB',(720,350),'#182932');d=ImageDraw.Draw(board)
for i,(title,head) in enumerate([('Original exact crop / collar included',ref),('Authored isolated component / no body fit',native)]):
    preview=head.resize((head.width*8,head.height*8),Image.Resampling.NEAREST)
    board.paste(preview,(i*360+30,35),preview);d.text((i*360+5,8),title+' / same8x',fill='white')
board.save(P/'head-component-review.png')
assert before=={str(f):sha(f) for f in inputs}
report=dict(generation='exec-f980f138-ec14-43f6-bcd2-2f17f2d8579e',mode='built-in imagegen edit',rawSize=im.size,componentBounds=bounds,opaqueSourceTouchesEdge=False,sourceCrownY=sourceCrownY,sourceBeardTipY=sourceBeardTipY,originalHeadRuler=originalBrownHeadRuler,originalDensity=originalDensity,componentScale=factor,nativeSize=native.size,rotationDegrees=0,inputSHA256=before,frozenInputsStable=4,normalSelected=False,bodyFit=False,scope='One authored master-derived head component at one fixed physical scale. Not exact original pixels or fitted swim body acceptance.')
(P/'head-component-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(nativeSize=native.size,scale=factor,frozenInputs=4,bodyFit=False)))
