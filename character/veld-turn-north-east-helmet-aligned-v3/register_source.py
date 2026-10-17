from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent;R=P.parents[1]
version=1;raw=P/'raw-skin-hair-v1.png'
a=np.array(Image.open(raw).convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>160)
components=[]
for k in range(1,n+1):
    y,x=np.where(labels==k)
    if len(x)>4000:components.append((len(x),k,int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)))
assert len(components)==1,components
_,k,x0,y0,x1,y1=components[0];pad=4
box=(max(0,x0-pad),max(0,y0-pad),min(a.shape[1],x1+pad),min(a.shape[0],y1+pad))
x0,y0,x1,y1=box;c=a[y0:y1,x0:x1].copy()
c[~ndimage.binary_dilation((labels==k)[y0:y1,x0:x1],iterations=3)]=0
source=Image.fromarray(c)
# Single complete-source ruler interpolates rear36 and profile38 incl short gasket.
scale=37/source.height
shell=source.resize((round(source.width*scale),37),Image.Resampling.LANCZOS)
dest=P/'matched-skin-hair-shell.png';shell.save(dest)
board=Image.new('RGB',(1160,340),'#202a30');d=ImageDraw.Draw(board)
items=[(R/'character/veld-turn-north-east-helmet-aligned-v1/intermediate-v5-shell.png','previous partial-face'),(dest,'skin/hair finish candidate'),(R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png','original profile')]
for i,(path,label) in enumerate(items):
    im=Image.open(path).convert('RGBA');big=im.resize((im.width*7,im.height*7),Image.Resampling.NEAREST)
    board.paste(big,(i*380+35,45),big);d.text((i*380+20,10),label+' '+str(im.size),fill='white')
board.save(P/'master-finish-comparison.png')
report={'version':version,'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceCoreBox':list(components[0][2:]),'extractionBox':list(box),'scale':scale,'wholeGasketHeight':37,'nativeSize':list(shell.size),'alphaExtraction':'largest complete opaque component plus 3px dilation preserves local alpha','postGenerationRGBChanged':False,'sourceOnly':True,'visualVerdict':'pending'}
(P/'source-registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
