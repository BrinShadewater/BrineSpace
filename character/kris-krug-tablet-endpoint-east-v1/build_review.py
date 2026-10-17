from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,hashlib
import imageio.v2 as iio
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
reader=iio.get_reader(ROOT/'source.mp4');meta=reader.get_meta_data();w,h=meta['size'];fps=meta['fps']
assert w==h, 'Source changed aspect ratio; fixed endpoint registration invalid'
(ROOT/'frames').mkdir(exist_ok=True)
poses=[];records=[]
def key(rgb):
    a=np.asarray(rgb).astype(float);magenta=(a[:,:,0]>a[:,:,1]+35)&(a[:,:,2]>a[:,:,1]+35)
    labels,_=ndimage.label(~magenta);sizes=np.bincount(labels.ravel());sizes[0]=0
    return labels==sizes.argmax()
for n,rgb in enumerate(reader):
    mask=key(rgb);rgba=np.dstack([rgb,mask.astype('uint8')*255]);rgba[~mask]=0
    pose=Image.fromarray(rgba).resize((184,184),Image.Resampling.LANCZOS)
    pose.save(ROOT/'frames'/f'{n:03}.png');poses.append(pose)
    a=np.asarray(pose);ys,xs=np.where(a[:,:,3]>180);yy=np.indices(a.shape[:2])[0]
    body=(a[:,:,3]>180)&(yy>ys.min()+(ys.max()-ys.min())*.35)&(yy<ys.min()+(ys.max()-ys.min())*.8)
    median=np.median(a[:,:,:3][body],axis=0).tolist()
    sole=(a[:,:,3]>180)&(yy>ys.max()-5);sy,sx=np.where(sole)
    records.append({'frame':n,'time_ms':round(n*1000/fps,3),'opaque_bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
        'sole_x_center':float((sx.min()+sx.max())/2),'sole_floor':int(ys.max()),'median_body_rgb':median,
        'edge_clipped':bool(xs.min()==0 or xs.max()==183 or ys.min()==0 or ys.max()==183)})
reader.close()
canonical=Image.open(ROOT.parent/'kris-krug-masters-v1/rotations/east.png').convert('RGBA')
target=Image.open(ROOT.parent/'kris-krug-tablet-east-v1/key-poses/03.png').convert('RGBA')
board=Image.new('RGB',(1104,924),'#30373c');draw=ImageDraw.Draw(board)
for j,n in enumerate(np.linspace(0,len(poses)-1,24).astype(int)):
    board.paste(poses[n],(j%6*184,j//6*220+25),poses[n]);draw.text((j%6*184+6,j//6*220+7),str(n)+' / '+f'{n/fps:.2f}s',fill='white')
draw.text((10,898),'FULL CLIP / fixed endpoint canvas / no grade or selected loop',fill='white');board.save(ROOT/'contact.png')
joins=Image.new('RGB',(736,220),'#30373c');jd=ImageDraw.Draw(joins)
for x,label,pose in [(0,'Original standing',canonical),(184,'Decoded first',poses[0]),(368,'Decoded last',poses[-1]),(552,'Requested held',target)]:
    joins.paste(pose,(x,26),pose);jd.text((x+8,7),label,fill='white')
joins.save(ROOT/'endpoint-comparison.png')
with iio.get_writer(ROOT/'scale-preview.mp4',fps=fps,codec='libx264',macro_block_size=2,quality=8) as writer:
    for pose in poses:
        frame=Image.new('RGB',(840,230),'#30373c');d=ImageDraw.Draw(frame)
        frame.paste(canonical,(5,30),canonical);d.text((8,8),'Standing reference',fill='white')
        for height,x in [(147,200),(82,420),(54,555),(27,650)]:
            side=round(184*height/147);small=pose.resize((side,side),Image.Resampling.BILINEAR);frame.paste(small,(x,30),small);d.text((x,8),str(height)+'px moving',fill='white')
        writer.append_data(np.asarray(frame))
report={'source_sha256':hashlib.sha256((ROOT/'source.mp4').read_bytes()).hexdigest(),'source_size':[w,h],
 'fps':fps,'frame_count':len(poses),'duration_ms':round(len(poses)*1000/fps),'canvas':[184,184],'pivot':[92,172],
 'registration':'Whole square source at fixed184/source-size; no per-frame scale, translation or grade',
 'clipped_frames':[r['frame'] for r in records if r['edge_clipped']],
 'sole_floor_range':[min(r['sole_floor'] for r in records),max(r['sole_floor'] for r in records)],
 'sole_x_range':[min(r['sole_x_center'] for r in records),max(r['sole_x_center'] for r in records)],
 'frames':records,'loop_selected':False,'reverse_return':'not authored/selected: inspect forward first',
 'endpoint_note':'Provided first/last hashes are conditioning; decoded endpoint images are separate visual evidence, not byte-exact sprites.'}
(ROOT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['frame_count','fps','duration_ms','clipped_frames','sole_floor_range','sole_x_range']}))
