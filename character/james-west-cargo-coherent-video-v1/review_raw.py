from pathlib import Path
import json,hashlib
import imageio.v2 as iio
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
reader=iio.get_reader(str(p/'source.mp4'));meta=reader.get_meta_data();frames=[np.asarray(f)[:,:,:3] for f in reader];reader.close()
out=p/'raw-review';out.mkdir(exist_ok=True)
reference=Image.open(p/'master-input.png').convert('RGB').resize((frames[0].shape[1],frames[0].shape[0]),Image.Resampling.NEAREST)
def bounds(a):
    mask=np.min(a,axis=2)<235;labels,_=ndimage.label(mask);counts=np.bincount(labels.ravel());counts[0]=0
    yy,xx=np.where(labels==counts.argmax());return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
stats=[];pages=[]
for start in range(0,len(frames),24):
    selected=frames[start:start+24];board=Image.new('RGB',(1440,4*274+274),'#303b40');draw=ImageDraw.Draw(board)
    thumb=reference.copy();thumb.thumbnail((240,240),Image.Resampling.LANCZOS);board.paste(thumb,(0,24));draw.text((4,4),'provider input / same framing',fill='white')
    for slot,a in enumerate(selected):
        i=start+slot;x=slot%6*240;y=274+slot//6*274
        box=bounds(a);stats.append({'index':i,'time':i/meta['fps'],'whiteDifferenceBounds':box,'diagnosticHeight':box[3]-box[1]})
        im=Image.fromarray(a);im.thumbnail((240,240),Image.Resampling.LANCZOS)
        board.paste(im,(x,y+24));draw.text((x+4,y+4),f'{i:03d} {i/meta["fps"]:.3f}s H{box[3]-box[1]}',fill='white')
    name=f'raw-{start:03d}.png';board.save(out/name);pages.append(name)
for index in [0,len(frames)//2,len(frames)-1]:Image.fromarray(frames[index]).save(out/f'full-{index:03d}.png')
report={'sourceSha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),'fps':meta['fps'],'size':list(meta['size']),'decodedFrames':len(frames),'referenceBounds':bounds(np.asarray(reference)),'frames':stats,'pages':pages,'visualReviewPending':True,'scope':'All raw decoded frames at one common whole-frame display scale beside provider input. White-difference largest-component bounds are diagnostics, not anatomical scale or contact. No extraction, grade, selection, native gameplay or continuous watched cadence acceptance.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['fps','size','decodedFrames','referenceBounds','pages']}))
