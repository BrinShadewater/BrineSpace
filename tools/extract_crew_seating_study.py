"""Extract a preserved two-row seating source at one anatomical scale."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import chroma, binary

ROOT=Path(__file__).resolve().parents[1]

def main(actor='veld',direction='east',revision='01',family='seating',columns='equal',match_sleep_scale=False):
    sources=ROOT/'character/crew-action-detail-v2/sources'
    source=sources/f'{actor}-{family}-{direction}-candidate-{revision}.png'
    reference=Image.open(sources/f'{actor}-{family}-{direction}-identity-01.png').convert('RGBA')
    # Generated transparent sources can contain almost-invisible alpha speckles.
    # Apply the exported visibility threshold before measuring bounds/anchors.
    raw=binary(chroma(source))
    if raw.getchannel('A').getextrema()[0] > 0:
        raise ValueError(f'{source.name}: no transparent pixels after chroma removal; reject baked backgrounds before extraction')
    # Generated rows may sit slightly off the geometric midpoint. Split only
    # through an empty gutter so boots cannot leak into the sleeping row.
    alpha=np.asarray(raw.getchannel('A'))
    empty=np.flatnonzero(~np.any(alpha,axis=1))
    candidates=empty[(empty>=raw.height*.35)&(empty<=raw.height*.65)]
    if not len(candidates):
        raise ValueError(f'{source.name}: no clear central row gutter')
    split=int(candidates[np.argmin(abs(candidates-raw.height//2))])
    rows=[(0,split),(split,raw.height)]
    tiles=[[raw.crop((i*raw.width//6,y0,(i+1)*raw.width//6,y1)) for i in range(6)] for y0,y1 in rows]
    if columns=='gutter':
        tiles=[]
        for y0,y1 in rows:
            occupied=np.any(alpha[y0:y1],axis=0)
            edges=np.flatnonzero(np.diff(np.pad(occupied.astype(int),(1,1))))
            spans=list(zip(edges[::2],edges[1::2]))
            if len(spans)!=6:
                raise ValueError(f'{source.name}: expected six isolated column silhouettes, found {len(spans)}')
            tiles.append([raw.crop((int(x0),y0,int(x1),y1)) for x0,x1 in spans])
    bounds=tiles[0][0].getbbox();ref_bounds=reference.getbbox()
    scale=(ref_bounds[3]-ref_bounds[1])/(bounds[3]-bounds[1])
    out=ROOT/f'character/crew-action-detail-v2/review/{actor}-{family}-{direction}-{revision}'
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(7*256,2*280),'#293b40');draw=ImageDraw.Draw(sheet)
    sheet.paste(reference,(36,52),reference);draw.text((4,4),'Selected standing identity',fill='white')
    frames={};records=[]
    loop_scale=1.0
    if match_sleep_scale:
        if family!='sleeping' or direction not in ['east','west']:
            raise ValueError('Sleep-row scale calibration requires a side-facing sleeping sheet')
        endpoint=tiles[0][-1].getbbox();loop=tiles[1][0].getbbox()
        loop_scale=(endpoint[2]-endpoint[0])/(loop[2]-loop[0])
    for row,state in enumerate(['sit-down','sit-idle'] if family=='seating' else ['lie-down','sleep']):
        pose_scale=scale*(loop_scale if row else 1.0)
        frames[state]=[]
        for i,tile in enumerate(tiles[row]):
            bounds=tile.getbbox();a=np.array(tile)
            yy,xx=np.where(a[max(0,bounds[3]-5):bounds[3],:,3]>0)
            if not len(xx):raise ValueError('Missing sole anchor')
            anchor=float(xx.min()+xx.max()+1)/2
            dense=binary(tile.resize((round(tile.width*pose_scale),round(tile.height*pose_scale)),Image.Resampling.BOX),True)
            frame=Image.new('RGBA',(256,256));frame.alpha_composite(dense,(round(128-anchor*pose_scale),round(224-bounds[3]*pose_scale)))
            frame.save(out/f'{state}-{i:03}.png');frames[state].append(frame)
            sheet.paste(frame,((i+1)*256,row*280),frame)
            draw.text(((i+1)*256+4,row*280+4),f'{state} {i}',fill='white')
            records.append({'state':state,'slot':i,'sourceBounds':bounds,'soleAnchorX':anchor,'denseBounds':frame.getbbox()})
    sheet.save(out/'contact.png')
    (out/'extraction.json').write_text(json.dumps({'status':'candidate_not_selected','source':source.relative_to(ROOT).as_posix(),
        'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'pivot':[128,224],
        'standingReferenceHeight':ref_bounds[3]-ref_bounds[1],'rowSplit':split,'columns':columns,'sleepRowScale':loop_scale,'frames':records,
        'limits':'Uniform scale within each row; optional sleep-row calibration is recorded. Anatomy, furniture contact and joins require visual review.'},indent=2)+'\n')
    print(json.dumps({'actor':actor,'direction':direction,'frames':12,'scale':scale,'output':out.relative_to(ROOT).as_posix()}))
    return frames

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--actor',choices=['veld','branforth'],default='veld')
    p.add_argument('--direction',choices=['east','west','south','north'],default='east');p.add_argument('--revision',default='01')
    p.add_argument('--family',choices=['seating','sleeping'],default='seating')
    p.add_argument('--columns',choices=['equal','gutter'],default='equal')
    p.add_argument('--match-sleep-scale',action='store_true')
    args=p.parse_args();main(args.actor,args.direction,args.revision,args.family,args.columns,args.match_sleep_scale)
