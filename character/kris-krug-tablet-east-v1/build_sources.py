"""Whole canonical-led key-source crops, honest finite source preview; no interpolation."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
import imageio.v2 as iio

ROOT=Path(__file__).resolve().parent
im=Image.open(ROOT/'source-strip.png').convert('RGBA')
cuts=[0,309,615,977,1310,1633,1940]
parts=[]
for left,right in zip(cuts,cuts[1:]):
    region=im.crop((left,0,right,im.height));a=np.asarray(region.getchannel('A'))
    substantial=Image.fromarray((a>32).astype('uint8')*255);box=substantial.getbbox()
    assert box and box[0]>3 and box[2]<region.width-3
    box=(box[0]-3,max(0,box[1]-3),box[2]+3,min(region.height,box[3]+3))
    crop=region.crop(box);opaque=np.asarray(crop.getchannel('A'))>180;yy,xx=np.where(opaque)
    floor=int(yy.max());support=opaque & (np.indices(opaque.shape)[0]>=floor-8);sy,sx=np.where(support)
    anchor=(int(sx.min())+int(sx.max()))/2
    parts.append({'image':crop,'bounds':[left+box[0],box[1],left+box[2],box[3]],'floor':floor,'top':int(yy.min()),'anchor':anchor})
scale=147/(parts[0]['floor']-parts[0]['top']+1)
(ROOT/'key-poses').mkdir(exist_ok=True)
poses=[];records=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for i,part in enumerate(parts):
    crop=part['image'];dense=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    offset=(92-round(part['anchor']*scale),172-round(part['floor']*scale))
    bbox=dense.getbbox();assert bbox and bbox[0]+offset[0]>0 and bbox[2]+offset[0]<184 and bbox[1]+offset[1]>0 and bbox[3]+offset[1]<184
    canvas=Image.new('RGBA',(184,184));canvas.alpha_composite(dense,offset);canvas.save(ROOT/'key-poses'/f'{i:02}.png');poses.append(canvas)
    records.append({'index':i,'source_bounds':part['bounds'],'sole_anchor_source':[part['anchor'],part['floor']],
                   'registration':offset,'alpha_bounds':canvas.getbbox(),'sha256':sha(ROOT/'key-poses'/f'{i:02}.png')})
canonical_path=ROOT.parent/'kris-krug-masters-v1/rotations/east.png'
canonical=Image.open(canonical_path).convert('RGBA')
board=Image.new('RGB',(1288,450),'#30373c');draw=ImageDraw.Draw(board)
allposes=[canonical]+poses
for i,pose in enumerate(allposes):
    board.paste(pose,(i*184,26),pose);draw.text((i*184+8,6),'Canonical' if i==0 else 'Key '+str(i-1),fill='white')
    crop=pose.resize((368,368),Image.Resampling.NEAREST).crop((92,0,276,220))
    board.paste(crop,(i*184,225),crop)
board.save(ROOT/'source-review.png')
# Chronology is a KEY-POSE demonstration. Generated pose6 skipped an authored low return.
# Reuse the raised key before reaching for holster, then exact whole canonical endpoint.
sequence=[canonical,poses[1],poses[2],poses[3],poses[4],poses[2],poses[5],canonical]
durations=[350,180,250,400,550,220,180,350]
with iio.get_writer(ROOT/'key-sequence-preview.mp4',fps=24,codec='libx264',macro_block_size=2,quality=8) as writer:
    for pose,duration in zip(sequence,durations):
        frame=Image.new('RGB',(650,230),'#30373c');d=ImageDraw.Draw(frame)
        for h,x in [(147,10),(82,220),(54,380),(27,510)]:
            side=round(184*h/147);small=pose.resize((side,side),Image.Resampling.BILINEAR);frame.paste(small,(x,30),small);d.text((x,8),str(h)+'px',fill='white')
        for _ in range(round(duration*24/1000)):writer.append_data(np.asarray(frame))
manifest={'name':'Kris Krüg — east alignment tablet key-source study','canvas':[184,184],'pivot':[92,172],
 'common_standing_scale':scale,'standing_ruler':147,'keys':records,'key_sequence':["canonical",1,2,3,4,2,5,"canonical"],
 'requested_holds_ms':durations,'timing_note':'Preview quantized to24fps; original requested key holds retained, not engine metadata.',
 'status':'Static key-source study only. Descent/return inbetweens missing; not finished animation.',
 'canonical_endpoint_sha256':sha(canonical_path),'source_sha256':sha(ROOT/'source-strip.png'),
 'tool':'built-in image_gen','generated_source':'C:/Users/Alex/.codex/generated_images/01a10108-0cea-7ee1-8d89-586acd3a735c/exec-e1bfe1d1-a11a-4665-a54b-7a7cb40ce51b.png',
 'reference':'res://character/kris-krug-masters-v1/identity-east-source.png','prompt':'prompt.txt',
 'reference_sha256':sha(ROOT.parent/'kris-krug-masters-v1/identity-east-source.png'),
 'processing':'Complete figure crops alpha>32+3px; one first-standing scale; measured sole-support registration. No RGB grade, limbs/body region edits, interpolation or per-pose stature normalization.'}
(ROOT/'source-contract.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('6 transparent keys packaged; intact canonical first/last in finite KEY-POSE preview; no finished animation claim.')
