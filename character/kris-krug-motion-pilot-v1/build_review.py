"""Fixed-registration full-clip extraction, adapted from build_idle_led_candidate.py.
No frame normalization, invented inbetweens, looping selection or RGB grading.
"""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse,hashlib,json
import imageio.v2 as iio
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('state',choices=['idle-east','walk-east','tablet-east']);parser.add_argument('--version',type=int,choices=[1,2],default=1);args=parser.parse_args()
if args.version==2: ROOT=ROOT.parent/'kris-krug-motion-pilot-v2'
dest=ROOT/args.state
source=dest/'source.mp4'
reader=iio.get_reader(source,format='ffmpeg');meta=reader.get_meta_data();fps=meta['fps'];width,height=meta['size']
contract=json.loads((ROOT/'input-contract.json').read_text())
master=json.loads((ROOT.parent/'kris-krug-masters-v1/manifest.json').read_text())
assert abs(width/height-896/1024)<.02, 'Video aspect ratio changed: registration needs review'
scale=master['common_source_scale']*1024/height
def mask(rgb):
    a=np.asarray(rgb).astype(float)
    if contract.get('chroma','green')=='magenta':
        keyed=(a[:,:,0]>a[:,:,1]+35)&(a[:,:,2]>a[:,:,1]+35)
    else:
        keyed=(a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90)
    labels,_=ndimage.label(~keyed);counts=np.bincount(labels.ravel());counts[0]=0
    return labels==counts.argmax()
input_rgb=np.array(Image.open(dest/'master-input.png').convert('RGB'))
yy,xx=np.where(mask(input_rgb));input_ground=int(yy.max())
offset=(92-round(448*master['common_source_scale']),172-round(input_ground*master['common_source_scale']))
frames=[];records=[]
(dest/'frames').mkdir(exist_ok=True)
for n,rgb in enumerate(reader):
    alpha=mask(rgb);rgba=np.dstack([rgb,alpha.astype('uint8')*255]);rgba[~alpha]=0
    im=Image.fromarray(rgba).resize((round(width*scale),round(height*scale)),Image.Resampling.LANCZOS)
    bounds=im.getbbox()
    assert bounds
    clipped=not (bounds[0]+offset[0]>=0 and bounds[1]+offset[1]>=0 and bounds[2]+offset[0]<=184 and bounds[3]+offset[1]<=184)
    canvas=Image.new('RGBA',(184,184));canvas.alpha_composite(im,offset)
    canvas.save(dest/'frames'/f'{n:03}.png');frames.append(canvas)
    opaque=np.array(canvas.getchannel('A'))>180;ys,xs=np.where(opaque)
    records.append({'source_frame':n,'time_ms':round(n*1000/fps,3),'alpha_bounds':canvas.getbbox(),
                    'opaque_bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'clipped':clipped})
reader.close()
assert frames
indices=np.linspace(0,len(frames)-1,18).astype(int)
board=Image.new('RGB',(1104,660),'#30373c');draw=ImageDraw.Draw(board)
for j,n in enumerate(indices):
    board.paste(frames[n],(j%6*184,j//6*220+24),frames[n]);draw.text((j%6*184+8,j//6*220+6),f'{n} / {n/fps:.2f}s',fill='white')
board.save(dest/'contact.png')
pre=[]
for frame in frames:
    bg=Image.new('RGB',(650,230),'#30373c');draw=ImageDraw.Draw(bg)
    for h,x in [(148,10),(82,220),(54,380),(27,510)]:
        side=round(184*h/148);small=frame.resize((side,side),Image.Resampling.BILINEAR)
        bg.paste(small,(x,30),small);draw.text((x,8),str(h)+'px',fill='white')
    pre.append(bg)
with iio.get_writer(dest/'scale-preview.mp4',fps=fps,codec='libx264',macro_block_size=2,quality=8) as writer:
    for frame in pre:writer.append_data(np.array(frame))
report={'state':args.state,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'source_size':[width,height],'fps':fps,'frame_count':len(frames),'duration_ms':round(len(frames)*1000/fps),
        'fixed_scale':scale,'fixed_offset':offset,'front_derived_scale':master['common_source_scale'],
        'input_ground':input_ground,'additional_grade':False,'loop_selected':False,
        'clipped_frames':[r['source_frame'] for r in records if r['clipped']],
        'records':records,'method':'Full video, fixed reference-derived scale/offset, largest non-green component; adapted existing extraction helper.'}
(dest/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['state','frame_count','fps','duration_ms','clipped_frames','loop_selected']}))
