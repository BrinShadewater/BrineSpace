"""Inspect a preserved motion video before choosing or registering a sprite cycle."""
from pathlib import Path
import argparse,hashlib,json
import imageio.v2 as imageio
import numpy as np
from PIL import Image,ImageDraw

def review(source,output,start=None,stop=None,step=1):
    source=Path(source).resolve();output=Path(output).resolve()
    if output.exists():raise ValueError('Use a fresh review folder; preserve earlier evidence')
    reader=imageio.get_reader(str(source),format='ffmpeg')
    meta=reader.get_meta_data();fps=float(meta['fps'])
    if not 0<fps<=120:raise ValueError('Unexpected video frame rate')
    duration=float(meta.get('duration',0))
    if not 0<duration<=15:raise ValueError('Review expects a short motion study')
    count=reader.count_frames()
    if count>600:raise ValueError('Unexpected motion study length')
    if step<1:raise ValueError('Sample step must be positive')
    if start is None and stop is None:
        selected=set(np.linspace(0,count-1,12,dtype=int).tolist())
    else:
        start=0 if start is None else start;stop=count if stop is None else stop
        if not 0<=start<stop<=count:raise ValueError('Sample interval must stay inside the decoded video')
        selected=set(range(start,stop,step))
    output.mkdir(parents=True)
    contact=Image.new('RGB',(1200,300*((len(selected)+5)//6)),'#293b40');draw=ImageDraw.Draw(contact)
    records=[];tile=0
    for index,data in enumerate(reader):
        rgb=np.asarray(data)[:,:,:3];r,g,b=rgb.astype(int).transpose(2,0,1)
        keep=~((r>g+35)&(b>g+35))
        rgba=np.dstack([rgb,keep.astype(np.uint8)*255]);rgba[~keep]=0
        image=Image.fromarray(rgba,'RGBA');bounds=image.getbbox()
        records.append({'frame':index,'timeSeconds':index/fps,'bounds':bounds,'foregroundPixels':int(keep.sum())})
        if index in selected:
            # Raw and keyed evidence share exact source geometry; no per-frame alignment.
            Image.fromarray(rgb).save(output/f'raw-{index:03}.png')
            image.save(output/f'keyed-{index:03}.png')
            thumb=image.copy();thumb.thumbnail((200,270),Image.Resampling.LANCZOS)
            x=(tile%6)*200+(200-thumb.width)//2;y=(tile//6)*300
            contact.paste(thumb,(x,y),thumb)
            draw.text(((tile%6)*200+5,y+276),f'{index}: {index/fps:.3f}s',fill='white');tile+=1
    reader.close();contact.save(output/'temporal-contact.png')
    report={'status':'unselected_motion_source_review','source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fps':fps,'frameCount':len(records),'dimensions':list(meta['size']),'samples':sorted(selected),'frames':records,'limits':['Key removes magenta only; inspect compression fringe and enclosed detail.','Bounds variation combines articulation and possible camera/scale drift; not an automatic motion-quality metric.','A cycle, landmarks, timing and native moving comparison must be selected separately.']}
    (output/'review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','fps','frameCount','dimensions','samples']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source');parser.add_argument('output')
    parser.add_argument('--start',type=int);parser.add_argument('--stop',type=int,help='Exclusive source-frame index');parser.add_argument('--step',type=int,default=1)
    args=parser.parse_args();review(args.source,args.output,args.start,args.stop,args.step)
