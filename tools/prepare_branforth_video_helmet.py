"""Fit Branforth's authored directional helmet head to a whole-body walk source."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/branforth-motion-polish-v1'

def main(direction='east'):
    if direction not in ('east','west','north','south'):raise ValueError('Unreviewed helmet direction')
    source=BASE/f'sources/{direction}-helmet-head-01.png';raw=binary(chroma(source));box=raw.getbbox();tile=raw.crop(box)
    scale=36/tile.height;bottom=tile.height-1
    _,xs=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0);neck=float(xs.min()+xs.max())/2
    head=binary(tile.resize((round(tile.width*scale),36),Image.Resampling.BOX),True)
    recipe=json.loads((BASE/f'{direction}-cycle-recipe.json').read_text())
    folder=ROOT/recipe['output'];sheet=Image.new('RGB',(1536,512),'#293b40');records=[]
    for i in range(6):
        body=Image.open(folder/f'walk-{direction}-{i:03}.png').convert('RGBA');top=body.getbbox()[1]
        _,xs=np.where(np.asarray(body)[top:top+12,:,3]>0);center=float(xs.min()+xs.max())/2
        anchor=(round(center+(1 if direction=='east' else -1 if direction=='west' else 0)),top+31);pose=body.copy()
        regions=[(round(center-20),top-5,round(center+20),top+26),(round(center-(12 if direction=='east' else 17)),top+26,round(center+(17 if direction=='east' else 12)),top+32)]
        if direction in ('north','south'):regions=[(round(center-20),top-5,round(center+20),top+26),(round(center-15),top+26,round(center+15),top+32)]
        for region in regions:pose.paste((0,0,0,0),region)
        at=(round(anchor[0]-neck*scale),anchor[1]-35);pose.alpha_composite(head,at)
        assert np.array_equal(np.asarray(body)[top+33:],np.asarray(pose)[top+33:]),'Body below collar changed'
        pose.save(folder/f'helmet-walk-{direction}-{i:03}.png');sheet.paste(body,(i*256,0),body);sheet.paste(pose,(i*256,256),pose)
        records.append(dict(slot=i,anchor=anchor,offset=at,regions=regions))
    sheet.save(folder/'paired-contact.png')
    (folder/'helmet-registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceCrop=box,scale=scale,records=records,limits=['Inspect collar and silhouette at native scale before selection.']),indent=2)+'\n')
    print('Prepared six Branforth-specific helmet walk poses; body below collar unchanged.')
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('direction',choices=['east','west','north','south'],nargs='?',default='east');main(parser.parse_args().direction)
