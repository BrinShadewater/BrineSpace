"""Fit the existing canonical helmet sources to the painted candidate only."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/'tools'))
from build_veld_painted import extract,head_axis
from rebuild_bill_art import binary,chroma

def main():
    body=ROOT/'veld-painted-v2';out=ROOT/'veld-painted-v2-helmet';out.mkdir(exist_ok=True)
    pack=json.loads((body/'manifest.json').read_text());records=[];sources={}
    calibration=json.loads((body/'provenance.json').read_text())['calibration']
    actions={d:extract('veld-'+d+'-actions-v1',4,3) for d in ['east','west','south','north']}
    names={'east':'east-sample-heads-01.png','west':'scanner-south-west-heads-01.png','south':'scanner-south-west-heads-01.png','north':'scanner-north-helmet-heads-01.png'}
    for direction,name in names.items():
        path=ROOT.parent/'veld-identity-correction-v1/sources'/name
        sources[direction]=binary(chroma(path))
    for state in pack['states']:
        direction=state['id'].split('-')[-1]
        for relative in state['frameFiles']:
            im=Image.open(body/relative).convert('RGBA');a=np.array(im);top=im.getbbox()[1]
            c=calibration[direction];kind=state['id'].split('-')[0]
            if kind=='walk':expected=128
            elif kind=='repair' or (kind=='kneel' and relative.endswith('004.png')) or (kind=='stand' and relative.endswith('000.png')):
                # Original work head centre is retained by the body builder.
                tile=actions[direction][7][0]
                expected=head_axis(tile)*c['actionScale']+c['action'][7]['offset'][0]
            else:
                slot=int(Path(relative).stem)
                source_index={'idle':[0,1,0],'kneel':[0,2,3,4,7],'stand':[7,4,3,2,0]}[kind][slot]
                tile=actions[direction][source_index][0]
                expected=head_axis(tile)*c['actionScale']+c['action'][source_index]['offset'][0]
            band=(round(expected)-9,round(expected)+10)
            ys,xs=np.where(a[:,band[0]:band[1],3]>0);top=int(ys.min())
            _,xs=np.where(a[top:top+10,max(0,round(expected)-17):round(expected)+18,3]>0)
            center=float(xs.min()+xs.max())/2+max(0,round(expected)-17)
            anchor=(round(center+({'east':3,'west':-3}.get(direction,0))),top+27)
            raw=sources[direction]
            if direction=='north':tile=raw.crop((0,0,raw.width//2,raw.height))
            else:
                slot=3 if direction=='west' else 0
                tile=raw.crop((slot*362,362,(slot+1)*362,724))
            tile=tile.crop(tile.getbbox());bottom=tile.height-1
            _,neck_x=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0)
            neck=float(neck_x.min()+neck_x.max())/2;scale=34/tile.height
            head=binary(tile.resize((round(tile.width*scale),34),Image.Resampling.LANCZOS),True)
            layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,(round(anchor[0]-neck*scale),anchor[1]-33))
            regions=[(round(center-18),top-5,round(center+19),top+22),(round(center-10),top+22,round(center+14),top+28)]
            pose=im.copy()
            for box in regions:pose.paste((0,0,0,0),box)
            pose.alpha_composite(layer)
            assert np.array_equal(a[top+29:],np.array(pose)[top+29:]),relative
            dest=out/relative;dest.parent.mkdir(parents=True,exist_ok=True);pose.save(dest)
            records.append(dict(frame=relative,anchor=anchor,regions=regions,source=names[direction]))
    pack.update(name='Veld painted core candidate fitted helmet',precomposed=True)
    (out/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
    (out/'registration.json').write_text(json.dumps(dict(records=records,sourceHashes={n:hashlib.sha256((ROOT.parent/'veld-identity-correction-v1/sources'/n).read_bytes()).hexdigest() for n in set(names.values())}),indent=2)+'\n')
    board=Image.new('RGBA',(1280,1024),'#242b2e');draw=ImageDraw.Draw(board)
    for row,d in enumerate(names):
        for col,kind in enumerate(['idle','walk','kneel','repair','stand']):
            state=next(s for s in pack['states'] if s['id']==kind+'-'+d)
            im=Image.open(out/state['frameFiles'][min(2,len(state['frameFiles'])-1)])
            board.alpha_composite(im,(col*256,row*256));draw.text((col*256+4,row*256+4),state['id'],fill='white')
    board.save(out/'contact.png');print(json.dumps(dict(equippedFrames=len(records),bodyPreservationChecks=len(records))))
if __name__=='__main__':main()
