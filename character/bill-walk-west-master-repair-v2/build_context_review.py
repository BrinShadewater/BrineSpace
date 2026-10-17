import sys
FRAME=sys.argv[1]
assert FRAME.isdigit() and len(FRAME)==3 and 0<=int(FRAME)<48
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
old=Image.open(ROOT/('character/bill-walk-west-material-v1/frames/bare/walk-west/'+FRAME+'.png')).convert('RGBA')
raw=Image.open(OUT/('sources/walk-'+FRAME+'-material-edit-v2.png')).convert('RGBA')
assert raw.width==raw.height
# Compare complete canvases; no bbox fit, part repositioning, or posed-height normalization.
new=raw.resize(old.size,Image.Resampling.LANCZOS)
new.save(OUT/('canvas-normalized-study-'+FRAME+'.png'))
a=np.array(old);b=np.array(new)
def main_mask(arr):
 lab,n=label(arr[:,:,3]>=180);counts=np.bincount(lab.ravel());return lab==int(counts[1:].argmax()+1)
x=main_mask(a);y=main_mask(b)
def bounds(m):
 ys,xs=np.where(m);return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
def region(m,box):
 xx,yy,x1,y1=box;z=np.zeros_like(m);z[yy:y1,xx:x1]=m[yy:y1,xx:x1];return z
regions={'head window':[105,65,145,108],'glove window':[95,130,150,164],'boot window':[70,197,180,232]}
rows={name:{'selectedBounds':bounds(region(x,box)),'editedBounds':bounds(region(y,box))} for name,box in regions.items()}
freeze=json.loads((OUT/'selected-gait-freeze.json').read_text(encoding='utf-8'));assert len(freeze)==98
for path,sha in freeze.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
job=json.loads((OUT/('generation-provenance-'+FRAME+'-v2.json')).read_text(encoding='utf-8'))
assert hashlib.sha256((OUT/('sources/walk-'+FRAME+'-material-edit-v2.png')).read_bytes()).hexdigest()==job['sha256']
assert hashlib.sha256(Path(job['originalPath']).read_bytes()).hexdigest()==job['sha256']
assert hashlib.sha256(Path(job['promptFile']).read_bytes()).hexdigest()==job['promptSha256']==job['submittedPromptSha256']
for ref in job['references']:assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()==ref['sha256']
report={'status':'unselected_material_edit_study','rawCanvas':list(raw.size),'targetCanvas':[1024,1024],'comparisonCanvas':[256,256],'uniformCanvasScale':256/raw.width,'translation':[0,0],'canvasRequestRetained':raw.size==(1024,1024),'silhouetteIoU':float((x&y).sum()/(x|y).sum()),'selectedBounds':bounds(x),'editedBounds':bounds(y),'regionDiagnostics':rows,'selectedGaitFilesUnchanged':98,'runtimeAdmission':False,'nativeAcceptance':False,'scope':'Whole-canvas comparison only; bounds are diagnostic, not proof of internal joint/face registration. No animation clip or normal selection changed.'}
(OUT/('review-'+FRAME+'.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
master=Image.open(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png').convert('RGBA')
master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS)
mc=Image.new('RGBA',(256,256));mc.alpha_composite(master,(128-master.width//2,224-master.height))
delta=np.zeros((256,256,4),np.uint8);delta[x&y]=[110,150,155,255];delta[x&~y]=[255,100,80,255];delta[y&~x]=[80,200,255,255]
board=Image.new('RGB',(1536,1100),(23,42,51));d=ImageDraw.Draw(board)
for i,(title,im) in enumerate([('Original West master',mc),('Selected walking '+FRAME,old),('Material edit: same canvas',new)]):
 d.text((i*512+12,10),title,fill='white');z=im.resize((512,512),Image.Resampling.NEAREST);board.paste(z,(i*512,35),z)
for i,(title,im,box) in enumerate([('Outline: red old / cyan edit',Image.fromarray(delta),(68,70,180,232)),('Selected head / shoulder',old,(95,72,153,158)),('Edited head / shoulder',new,(95,72,153,158))]):
 d.text((i*512+12,560),title,fill='white');z=im.crop(box);z=z.resize((z.width*5,z.height*5),Image.Resampling.NEAREST) if i else z.resize((336,486),Image.Resampling.NEAREST);board.paste(z,(i*512+30,585),z)
board.save(OUT/('master-pose-review-'+FRAME+'.png'))
print(json.dumps(report))
