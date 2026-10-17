"""Whole authored draw poses; reverse poses are explicitly declared return derivation."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
import imageio.v2 as iio

ROOT=Path(__file__).resolve().parent
atlas=Image.open(ROOT/'source-atlas.png').convert('RGBA');parts=[]
assert atlas.size==(1536,1024)
for i in range(8):
    x=(i%4)*384;y=(i//4)*512;region=atlas.crop((x,y,x+384,y+512))
    alpha=np.asarray(region.getchannel('A'));bbox=Image.fromarray((alpha>32).astype('uint8')*255).getbbox()
    assert bbox and bbox[0]>3 and bbox[2]<381 and bbox[1]>3 and bbox[3]<509
    box=(bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3);crop=region.crop(box)
    opaque=np.asarray(crop.getchannel('A'))>180;yy,xx=np.where(opaque);floor=int(yy.max());top=int(yy.min())
    support=opaque&(np.indices(opaque.shape)[0]>=floor-6);sy,sx=np.where(support)
    parts.append({'crop':crop,'source_bounds':[x+box[0],y+box[1],x+box[2],y+box[3]],
        'floor':floor,'top':top,'anchor':float((sx.min()+sx.max())/2)})
scale=147/(parts[0]['floor']-parts[0]['top']+1)
(ROOT/'frames').mkdir(exist_ok=True);poses=[];records=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for i,part in enumerate(parts):
    crop=part['crop'];dense=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    pos=(92-round(part['anchor']*scale),172-round(part['floor']*scale))
    out=Image.new('RGBA',(184,184));box=dense.getbbox();assert box and box[0]+pos[0]>0 and box[1]+pos[1]>0 and box[2]+pos[0]<184 and box[3]+pos[1]<184
    out.alpha_composite(dense,pos);path=ROOT/'frames'/f'{i:02}.png';out.save(path);poses.append(out)
    yy,xx=np.where(np.asarray(out.getchannel('A'))>180)
    records.append({'key':i,'source_bounds':part['source_bounds'],'sole_support_anchor':[part['anchor'],part['floor']],
        'registration':pos,'opaque_height':int(yy.max()-yy.min()+1),'alpha_bounds':out.getbbox(),'sha256':sha(path)})
canonical_path=ROOT.parent/'kris-krug-masters-v1/rotations/east.png'
canonical=Image.open(canonical_path).convert('RGBA')
board=Image.new('RGB',(1472,484),'#30373c');draw=ImageDraw.Draw(board)
for i,pose in enumerate(poses):
    board.paste(pose,(i*184,25),pose);draw.text((i*184+8,5),'Draw key '+str(i),fill='white')
    crop=pose.resize((368,368),Image.Resampling.NEAREST).crop((92,0,276,232));board.paste(crop,(i*184,235),crop)
board.save(ROOT/'source-review.png')
# Complete authored keys: canonical entry, draw1-6, tap7/6/7, reverse6-1, canonical exit.
keys=[0,1,2,3,4,5,6,7,6,7,6,5,4,3,2,1,0]
durations=[350,100,100,130,130,150,180,260,150,260,160,150,130,130,100,100,350]
sequence=[poses[k] for k in keys]
with iio.get_writer(ROOT/'action-preview.mp4',fps=60,codec='libx264',macro_block_size=2,quality=8) as writer:
    for pose,ms in zip(sequence,durations):
        frame=Image.new('RGB',(840,230),'#30373c');d=ImageDraw.Draw(frame)
        frame.paste(canonical,(5,30),canonical);d.text((8,8),'Standing reference',fill='white')
        for height,x in [(147,200),(82,420),(54,555),(27,650)]:
            side=round(184*height/147);small=pose.resize((side,side),Image.Resampling.BILINEAR);frame.paste(small,(x,30),small);d.text((x,8),str(height)+'px',fill='white')
        for _ in range(round(ms*60/1000)):writer.append_data(np.asarray(frame))
manifest={'name':'Kris Krüg / east tablet source candidate','canvas':[184,184],'pivot':[92,172],
 'standing_ruler':147,'common_source_scale':scale,'unique_authored_poses':8,'poses':records,
 'sequence':keys,'durations_ms':durations,'return_method':'Explicit reversed whole-source draw; no new return poses claimed',
 'preview_duration_ms':round(sum(round(ms*60/1000) for ms in durations)*1000/60,3),
 'endpoint_method':'Whole source key0 is staged family idle and identical action first/last; earlier standing remains identity/scale reference, no normal selection replaced.',
 'status':'Staged coarse source animation; requires anatomical/holster/join/motion review before runtime selection',
 'source_sha256':sha(ROOT/'source-atlas.png'),'canonical_sha256':sha(canonical_path),
 'generator':'built-in image_gen','generated_source':'C:/Users/Alex/.codex/generated_images/01a10108-0cea-7ee1-8d89-586acd3a735c/exec-8c7e8b95-eea3-4997-a2dd-3d0b0722fa1d.png',
 'prompt':'prompt.txt','references':[{'path':str(p),'sha256':sha(p)} for p in [ROOT.parent/'kris-krug-masters-v1/identity-east-source.png',ROOT.parent/'kris-krug-tablet-east-v1/key-poses/03.png']],
 'processing':'Whole figure alpha>32+3px crops; 1 first-standing scale; sole-support translation; raw interior RGBA retained, no RGB grade/limb patches/interpolation.'}
(ROOT/'source-contract.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
engine={'name':'Kris Krüg / staged east tablet source family','frameWidth':184,'frameHeight':184,'pivot':[92,172],
 'standingHeight':147,'precomposed':True,'states':[
 {'id':'idle-east','frameCount':1,'frameFiles':['res://character/kris-krug-tablet-draw-east-v1/frames/00.png'],'frameDurationsMs':[1000],'loop':True},
 {'id':'interact-east','frameCount':len(keys),'frameFiles':['res://character/kris-krug-tablet-draw-east-v1/frames/'+f'{k:02}.png' for k in keys],
  'frameDurationsMs':durations,'loop':False,'actionMeaning':'alignment tablet draw/inspect/derived reverse holster'}]}
(ROOT/'manifest.json').write_text(json.dumps(engine,indent=2),encoding='utf-8')
print(json.dumps({'authored_poses':8,'timeline_slots':len(sequence),'requested_duration_ms':sum(durations),'heights':[r['opaque_height'] for r in records],'canvas_clipping':0,'return':'derived reverse, not new art'}))
