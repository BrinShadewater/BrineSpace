"""Extract preserved human cargo pickup sources using each actor/view's idle ruler."""
from pathlib import Path
import json,hashlib
import argparse
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import chroma,binary

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/crew-action-detail-v2/sources/veld-pickup-east-candidate-03.png'
OUT=ROOT/'character/crew-action-detail-v2/review/veld-pickup-east-03'

def main(actor='veld',revision=None,direction='east'):
    revision=revision or ('03' if actor=='veld' and direction=='east' else '01')
    source_path=SOURCE.with_name(f'{actor}-pickup-{direction}-candidate-{revision}.png')
    out=OUT.with_name(f'{actor}-pickup-{direction}-{revision}')
    out.mkdir(parents=True,exist_ok=True)
    reference=Image.open(ROOT/f'character/crew-action-detail-v2/sources/{actor}-idle-{direction}-reference-01.png').convert('RGBA')
    bounds=reference.getbbox();standing_height=bounds[3]-bounds[1]
    source=chroma(source_path);tiles=[source.crop((i*source.width//6,0,(i+1)*source.width//6,source.height)) for i in range(6)]
    standing=tiles[-1 if direction in ['south','north'] else 0].getbbox();scale=standing_height/(standing[3]-standing[1])
    sheet=Image.new('RGB',(256*7,280),'#293b40');records=[];frames=[]
    sheet.paste(reference,(36,52),reference)
    draw=ImageDraw.Draw(sheet);draw.text((4,4),'Selected idle reference',fill='white')
    for i,tile in enumerate(tiles):
        bounds=tile.getbbox();a=np.array(tile)
        # Register by the boot's floor contact, excluding the crate ahead.
        sole=bounds[3]
        if direction=='south':
            # Front cargo overlaps the center. Use the exposed outer boot edges
            # in the bottom quarter, not the crate's slightly lower front lip.
            mask=a[:,:,3]>0;left,right=bounds[0],bounds[2];span=right-left
            mask[:round(bounds[1]+(bounds[3]-bounds[1])*.75)]=False
            mask[:,round(left+span*.24):round(right-span*.24)]=False
            yy,xx=np.where(mask)
            if not len(xx):raise ValueError('Front boots are occluded; author explicit anchors')
            sole=int(yy.max())+1
            ys,xs=np.where(mask[max(0,sole-5):sole])
            x0=0
        else:
            x0=round(tile.width*.45) if direction=='west' else 0
            x1=tile.width if direction in ['west','north'] else round(tile.width*.55)
            ys,xs=np.where(a[max(0,sole-5):sole,x0:x1,3]>0)
        if not len(xs):raise ValueError('Missing boot anchor')
        anchor=float(xs.min()+xs.max()+1)/2 if direction in ['south','north'] else float(np.median(xs))+x0
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(dense,(round(128-anchor*scale),round(224-sole*scale)))
        canvas.save(out/f'{i:03}.png');sheet.paste(canvas,((i+1)*256,0),canvas)
        frames.append(canvas)
        draw.text(((i+1)*256+4,4),str(i),fill='white')
        records.append({'slot':i,'sourceBounds':bounds,'bootAnchorX':anchor,'sourceSole':sole,'denseBounds':canvas.getbbox(),
                        'crownToBootHeight':round((sole-bounds[1])*scale)})
    sheet.save(out/'contact.png')
    (out/'extraction.json').write_text(json.dumps({'status':'source_extraction_selection_recorded_separately','actor':actor,'source':str(source_path.relative_to(ROOT)),
        'sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'scale':scale,'pivot':[128,224],
        'standingReferenceHeight':standing_height,'frames':records},indent=2)+'\n')
    print(json.dumps({'frames':6,'scale':scale,'standingHeights':[r['crownToBootHeight'] for r in [records[0],records[-1]]]}))
    return frames

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',choices=['veld','branforth'],default='veld')
    parser.add_argument('--direction',choices=['east','west','south','north'],default='east')
    parser.add_argument('--revision',choices=['01','02','03'])
    args=parser.parse_args()
    main(args.actor,args.revision,args.direction)
