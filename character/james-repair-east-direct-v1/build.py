"""Stage a full James action study with fixed reference registration."""
from pathlib import Path
import hashlib,json
import numpy as np
import imageio.v2 as iio
from scipy import ndimage
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent

def foreground(a):
    f=a.astype(float)
    key=(f[:,:,1]>f[:,:,0]*1.3)&(f[:,:,1]>f[:,:,2]*1.3)&(f[:,:,1]>90)
    labels,_=ndimage.label(~key);counts=np.bincount(labels.ravel());counts[0]=0
    return labels==counts.argmax()

def main():
    reference=np.asarray(Image.open(HERE/'master-input.png').convert('RGB'))
    reader=iio.get_reader(HERE/'source.mp4');meta=reader.get_meta_data();fps=meta['fps']
    # Invert the saved 4x enlargement. Scale is fixed for the entire source.
    sx=reference.shape[1]/meta['size'][0]/4;sy=reference.shape[0]/meta['size'][1]/4
    size=(round(meta['size'][0]*sx),round(meta['size'][1]*sy));offset=(-4,-4)
    frames=[];records=[];dest=HERE/'frames';dest.mkdir(exist_ok=True)
    for index,a in enumerate(reader):
        keep=foreground(a);rgba=np.dstack((a,keep.astype(np.uint8)*255));rgba[~keep]=0
        raw=Image.fromarray(rgba);small=raw.resize(size,Image.Resampling.LANCZOS)
        out=Image.new('RGBA',(184,184));out.alpha_composite(small,offset)
        box=small.getbbox();clipped=box is None or box[0]-4<0 or box[1]-4<0 or box[2]-4>184 or box[3]-4>184
        out.save(dest/f'{index:03}.png');frames.append(out);records.append(dict(sourceFrame=index,bounds=out.getbbox(),clipped=clipped))
    reader.close();previews=[]
    for im in frames:
        board=Image.new('RGB',(660,240),'#303b40');d=ImageDraw.Draw(board)
        for h,x in [(148,0),(82,210),(54,350),(27,450)]:
            side=round(184*h/148);s=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(s,(x,35+172-side*172//184),s);d.text((x,8),str(h)+'px reference',fill='white')
        previews.append(board)
    previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=round(1000/fps),loop=0)
    sheet=Image.new('RGB',(1104,660),'#303b40');d=ImageDraw.Draw(sheet)
    for j,index in enumerate(np.linspace(0,len(frames)-1,18).astype(int)):
        at=(j%6*184,j//6*220+20);sheet.paste(frames[index],at,frames[index]);d.text((at[0]+5,at[1]-16),str(index),fill='white')
    sheet.save(HERE/'contact.png')
    report=dict(frames=len(frames),fps=fps,sourceSha256=hashlib.sha256((HERE/'source.mp4').read_bytes()).hexdigest(),fixedScale=[sx,sy],offset=offset,pivot=[92,172],additionalGrade=False,loopSelected=False,clippedFrames=sum(r['clipped'] for r in records),records=records)
    (HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1104px;margin:auto}img,video{max-width:100%}</style><h1>James east repair source study</h1><p>Full generated clip from installed idle. Fixed registration; no extra palette treatment. Staged source only; action segmentation, helmet fitting and native validation remain pending.</p><img src="review.gif"><video src="source.mp4" controls loop></video><img src="contact.png">')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}))
if __name__=='__main__':main()
