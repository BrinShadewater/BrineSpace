"""Measure selected south hot-tip pixels against a captured work anchor."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'output/crew-replacement-2026-09-12/marsh'

def hot_tip_pixels(a, minimum_y):
    """Select the lowest connected hot-color patch, excluding the copper grip."""
    mask=(a[:,:,0]>200)&(a[:,:,1]>75)&(a[:,:,2]<110)&(a[:,:,3]>0)
    mask[:max(0,int(minimum_y)+1)]=False
    remaining=set(zip(*np.where(mask)))
    components=[]
    while remaining:
        seed=remaining.pop();component=[seed];pending=[seed]
        while pending:
            y,x=pending.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    neighbor=(y+dy,x+dx)
                    if neighbor in remaining:
                        remaining.remove(neighbor);pending.append(neighbor);component.append(neighbor)
        components.append(component)
    if not components:raise ValueError('Missing hot-tip candidates')
    chosen=max(components,key=lambda c:(max(y for y,x in c),len(c)))
    y,x=np.array(chosen).T
    return y,x

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--anchor',type=Path,default=QA/'construction-motion/side-2-anchor.json')
    parser.add_argument('--output',type=Path,default=QA/'south-reach-audit.json')
    parser.add_argument('--door',type=Path,default=QA/'door-work-targets.json')
    args=parser.parse_args()
    anchor=json.loads(args.anchor.read_text())
    door=json.loads(args.door.read_text()) if args.door.exists() else None
    leaf_y=min(p['rect'][1] for p in door['pieces'] if p['leaf']) if door else None
    track_y=min(p['rect'][1] for p in door['pieces'] if p['floor']) if door else None
    root=ROOT/'character/marsh-v2';catalog=json.loads((root/'catalog.json').read_text())
    rows=[]
    for relative in catalog['body']:
        manifest=root/relative;pack=json.loads(manifest.read_text())
        for state in pack['states']:
            if state['id']!='weld-south':continue
            pivot=pack['pivot'];scale=65.28/pack['standingHeight']
            for index,relative_frame in enumerate(state['frameFiles']):
                path=(manifest.parent/relative_frame).resolve()
                a=np.asarray(Image.open(path).convert('RGBA'))
                y,x=hot_tip_pixels(a,pivot[1]-22)
                if not len(x):raise ValueError(f'Missing hot-tip candidates in {path}')
                offset=[(float(x.mean())-pivot[0])*scale,(float(y.mean())-pivot[1])*scale]
                # main.get_marsh_position subtracts .038 cells; renderer adds it back.
                tip_y=anchor['foot_local'][1]+offset[1]
                rows.append(dict(frame=index,hotPixelCount=len(x),tipPixel=[float(x.mean()),float(y.mean())],
                                 tipWorldOffset=offset,tipLocalY=tip_y,gapToDoorEdge=192-tip_y,
                                 gapToLeafNearEdge=leaf_y-tip_y if leaf_y is not None else None,
                                 gapToTrackNearEdge=track_y-tip_y if track_y is not None else None))
    if len(rows)!=6:raise ValueError('Expected one selected six-frame south welding clip')
    report=dict(anchor=anchor,rendererFootOffset=0.0,positionAdapterOffset=-384*.038,drawOffset=384*.038,doorEdgeLocalY=192,door=door,frames=rows,
                method='Lowest 8-connected hot-color component below pivot-22; excludes copper grip. Inspect selected pixels visually.',
                limits='Door edge plane is a geometric reference, not proof of contact with painted seal detail.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    ranges={key:[min(r[key] for r in rows),max(r[key] for r in rows)] for key in ['gapToDoorEdge','gapToLeafNearEdge','gapToTrackNearEdge'] if rows[0][key] is not None}
    print(json.dumps({'frames':len(rows),'gapRanges':ranges,'output':str(args.output)}))

if __name__=='__main__':main()
