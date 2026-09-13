"""Register fitted generated equipment using bare-source geometry, never helmet height."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import chroma,binary
from extract_crew_seating_study import main as extract

ROOT=Path(__file__).resolve().parents[1]

def main(actor='veld'):
    bare_frames=extract(actor,'south','01','sleeping','gutter')
    folder=ROOT/f'character/crew-action-detail-v2/review/{actor}-sleeping-south-01'
    recipe=json.loads((folder/'extraction.json').read_text())
    sources=ROOT/'character/crew-action-detail-v2/sources'
    source=sources/f'{actor}-sleeping-south-equipped-01.png'
    bare=binary(chroma(sources/f'{actor}-sleeping-south-candidate-01.png'))
    gear=binary(chroma(source))
    if bare.size!=gear.size:raise ValueError('Equipped source changed sheet dimensions; register explicitly before extraction')
    split=recipe['rowSplit'];scale=recipe['scale'];frames={}
    out=folder.parent/f'{actor}-sleeping-south-equipped-01';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(6*256,4*256),'#293b40');draw=ImageDraw.Draw(sheet)
    for row,(y0,y1) in enumerate([(0,split),(split,bare.height)]):
        occupied=np.any(np.asarray(bare)[y0:y1,:,3],axis=0)
        edges=np.flatnonzero(np.diff(np.pad(occupied.astype(int),(1,1))))
        spans=list(zip(edges[::2],edges[1::2]))
        if len(spans)!=6:raise ValueError('Expected six bare silhouettes')
        state=['lie-down','sleep'][row];frames[state]=[]
        for i,(x0,x1) in enumerate(spans):
            tile=gear.crop((int(x0),y0,int(x1),y1))
            record=recipe['frames'][row*6+i]
            dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
            frame=Image.new('RGBA',(256,256));frame.alpha_composite(dense,(round(128-record['soleAnchorX']*scale),round(224-record['sourceBounds'][3]*scale)))
            frame.save(out/f'{state}-{i:03}.png');frames[state].append(frame)
            for offset,pose in [(0,bare_frames[state][i]),(256,frame)]:sheet.paste(pose,(i*256,row*512+offset),pose)
            draw.text((i*256+4,row*512+4),f'{state} {i}',fill='white')
    sheet.save(out/'contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='study_not_selected',source=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bareRecipe=str((folder/'extraction.json').relative_to(ROOT)),scale=scale),indent=2)+'\n')
    print(out.relative_to(ROOT));return frames

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--actor',default='veld',choices=['veld','branforth'])
    main(parser.parse_args().actor)
