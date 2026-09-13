"""Extract Marsh's independent welding views at canonical body scale."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma

ROOT=Path(__file__).resolve().parents[1]
VIEWS={'sides':('east','west'),'axial':('north','south')}
REVISIONS={'sides':'02','axial':'01'}
SELECTED={state+'-'+direction for group in REVISIONS for direction in VIEWS[group]
          for state in ['weld','torch-draw','torch-stow']}

def main(revision=None,group='sides'):
    revision=revision or REVISIONS.get(group,'01')
    root=ROOT/'character/crew-action-detail-v2'
    source=root/f'sources/marsh-welding-{group}-candidate-{revision}.png'
    raw=binary(chroma(source))
    alpha=np.asarray(raw.getchannel('A'))
    if alpha.min()>0:raise ValueError('Welding source has no transparent background')
    empty=np.flatnonzero(~np.any(alpha,axis=1))
    candidates=empty[(empty>=raw.height*.35)&(empty<=raw.height*.65)]
    if not len(candidates):raise ValueError('Welding rows have no clear central gutter')
    split=int(candidates[np.argmin(abs(candidates-raw.height/2))])
    out=root/f'review/marsh-welding-{group}-{revision}'
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(7*184,2*208),'#293b40');draw=ImageDraw.Draw(sheet)
    result={};records=[]
    for row,(direction,y0,y1) in enumerate([(VIEWS[group][0],0,split),(VIEWS[group][1],split,raw.height)]):
        occupied=np.any(alpha[y0:y1],axis=0)
        edges=np.flatnonzero(np.diff(np.pad(occupied.astype(int),(1,1))))
        spans=list(zip(edges[::2],edges[1::2]))
        if len(spans)!=6:raise ValueError(f'{direction}: expected 6 isolated poses, got {len(spans)}')
        identity=Image.open(root/f'sources/marsh-welding-{direction}-identity-01.png').convert('RGBA')
        tiles=[raw.crop((int(x0),y0,int(x1),y1)) for x0,x1 in spans]
        bounds=tiles[0].getbbox();ref=identity.getbbox()
        scale=(ref[3]-ref[1])/(bounds[3]-bounds[1])
        poses=[];sheet.paste(identity,(0,row*208+24),identity)
        for index,tile in enumerate(tiles):
            bounds=tile.getbbox();a=np.asarray(tile.getchannel('A'))
            _,xx=np.where(a[max(0,bounds[3]-5):bounds[3]]>0)
            anchor=float(xx.min()+xx.max()+1)/2
            dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
            pose=Image.new('RGBA',(184,184))
            pose.alpha_composite(dense,(round(92-anchor*scale),round(172-bounds[3]*scale)))
            b=pose.getbbox()
            if b is None or b[0]==0 or b[1]==0 or b[2]==184 or b[3]==184:
                raise ValueError(f'{direction} {index}: clipped pose requires larger registered profile')
            pose.save(out/f'{direction}-source-{index:03}.png')
            # Preserve exact existing idle joins; review source interiors separately.
            if index in [0,5]:pose=identity.copy()
            pose.save(out/f'{direction}-{index:03}.png');poses.append(pose)
            sheet.paste(pose,((index+1)*184,row*208+24),pose)
            draw.text(((index+1)*184+4,row*208+4),f'{direction} {index}',fill='white')
            records.append(dict(direction=direction,index=index,sourceBounds=bounds,
                                sourceSpan=[int(v) for v in spans[index]],scale=scale,soleAnchorX=anchor,
                                canonicalIdleJoin=index in [0,5]))
        result['weld-'+direction]=poses
    sheet.save(out/'contact.png')
    (out/'extraction.json').write_text(json.dumps(dict(status='selection_recorded_separately',
        source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        rowSplit=split,pivot=[92,172],frames=records,
        limitations='Source geometry and exact idle joins do not establish continuous motion quality.'),indent=2)+'\n')
    print(out.relative_to(ROOT));return result

def build_selected():
    result={}
    mapping={'torch-draw':[0,0,1,1,2,2],
             'weld':[2,2,3,3,4,2],
             'torch-stow':[2,2,1,1,0,0]}
    for group,revision in REVISIONS.items():
        source=main(revision,group)
        out=ROOT/f'character/crew-action-detail-v2/review/marsh-welding-{group}-{revision}'
        sheet=Image.new('RGB',(6*184,6*208),'#293b40');draw=ImageDraw.Draw(sheet)
        for row,direction in enumerate(VIEWS[group]):
            poses=source['weld-'+direction]
            for action_index,(state,indices) in enumerate(mapping.items()):
                frames=[poses[index].copy() for index in indices]
                result[state+'-'+direction]=frames
                for index,frame in enumerate(frames):
                    frame.save(out/f'{direction}-{state}-{index:03}.png')
                    y=(row*3+action_index)*208
                    sheet.paste(frame,(index*184,y+24),frame)
                    draw.text((index*184+4,y+4),f'{direction} {state} {index}',fill='white')
        sheet.save(out/'tool-sequence-contact.png')
        (out/'tool-sequence.json').write_text(json.dumps(dict(sourceRevision=revision,
            viewGroup=group,poseIndices=mapping,durationsMs=[150]*6,
            joins='Canonical idle to ready; active loop stays equipped; exact reverse stow.'),indent=2)+'\n')
    from marsh_low_welding import SELECTED as LOW_SELECTED,main as low_build
    if LOW_SELECTED:result.update(low_build())
    return result

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group',choices=list(VIEWS),default='sides')
    parser.add_argument('--revision')
    args=parser.parse_args();main(args.revision,args.group)
