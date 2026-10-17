from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
import numpy as np,json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for kind in ['action','quarter','rest','rear']:
 source=H/('generated-'+kind+'-heads.png');im=Image.open(source).convert('RGBA');prior=json.loads((R/'character/krusher-head-fit-v7'/(kind+'-extraction.json')).read_text());names=[q['name'] for q in prior['records']];parts=[]
 for i,name in enumerate(names):
  row,col=divmod(i,3);cell=(col*im.width//3,row*im.height//2,(col+1)*im.width//3,(row+1)*im.height//2);a=np.array(im.crop(cell));core=a[:,:,3]>240;lab,_=ndimage.label(core,np.ones((3,3)));counts=np.bincount(lab.ravel());counts[0]=0;main=lab==counts.argmax();admit=ndimage.binary_dilation(main,iterations=2)&(a[:,:,3]>8);a[~admit]=0;p=Image.fromarray(a);box=p.getbbox();parts.append((name,p.crop(box),cell,box))
 scale=(27 if kind=='rear' else 29)/parts[0][1].height;records=[];board=Image.new('RGBA',(1200,540),'#252d31');draw=ImageDraw.Draw(board)
 for i,(name,p,cell,box) in enumerate(parts):
  size=tuple(round(n*scale) for n in p.size);native=p.resize(size,Image.Resampling.LANCZOS);out=H/'sources'/(name.replace('clean-bare-','style-')+'-native.png');native.save(out);x=i%3*400+85;y=i//3*270+40;board.alpha_composite(native.resize((native.width*6,native.height*6),Image.Resampling.NEAREST),(x,y));draw.text((i%3*400+10,y-30),name,font=font,fill='white')
  records.append({'name':name,'cell':cell,'sourceBox':box,'sourceSize':p.size,'uniformScale':scale,'nativeSize':size,'resample':'Lanczos with preserved authored alpha','output':out.relative_to(H).as_posix(),'outputHash':hashlib.sha256(out.read_bytes()).hexdigest()})
 board.save(H/(kind+'-heads-review.png'));(H/(kind+'-extraction.json')).write_text(json.dumps({'source':source.name,'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceMatte':'primary opaque component plus two source-pixel antialiased edge; no binary native alpha','records':records},indent=2)+'\n');print(json.dumps({'family':kind,'uniformScale':scale,'sizes':[q['nativeSize'] for q in records]}))
