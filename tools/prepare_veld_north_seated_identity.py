"""Prepare canonical Veld north seating poses; selection remains ledger-owned."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/seated-north-body-01.png'
    raw=binary(chroma(source));alpha=np.asarray(raw)[:,:,3]
    assert alpha.min()==0,'Source must have real transparent background after chroma'
    edges=np.diff(np.r_[False,alpha.any(axis=0),False].astype(int))
    starts,ends=np.where(edges==1)[0],np.where(edges==-1)[0]
    assert len(starts)==len(ends)==6,'Require six separated figure columns'
    tiles=[raw.crop((int(a)-2,0,int(b)+2,raw.height)) for a,b in zip(starts,ends)]
    runtime=ROOT/'character/dr-veld-v2'
    catalog=json.loads((runtime/'catalog.json').read_text())
    matches=[]
    for relative in catalog['body']:
        manifest_path=runtime/relative;manifest=json.loads(manifest_path.read_text())
        for state in manifest['states']:
            if state['id']=='idle-north':matches.append((manifest_path,manifest,state))
    assert len(matches)==1
    manifest_path,manifest,state=matches[0]
    frame=Image.open(manifest_path.parent/state['frameFiles'][0]).convert('RGBA')
    reference=Image.new('RGBA',(256,256))
    reference.alpha_composite(frame,(round(128-manifest['pivot'][0]),round(224-manifest['pivot'][1])))
    box=reference.getbbox();standing=tiles[0].getbbox();scale=(box[3]-box[1])/(standing[3]-standing[1])
    poses=[];records=[]
    for tile in tiles:
        bounds=tile.getbbox();sole=bounds[3]-1
        _,xs=np.where(np.asarray(tile)[sole-10:sole+1,:,3]>0)
        support=float(xs.min()+xs.max())/2
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        at=(round(128-support*scale),round(223-sole*scale))
        pose=Image.new('RGBA',(256,256));pose.alpha_composite(dense,at);poses.append(pose)
        records.append(dict(sourceBounds=bounds,support=[support,sole],position=at,denseBounds=pose.getbbox()))
    down=[reference]+poses[1:5]+[poses[5]]
    idle=[poses[5],poses[5],poses[4],poses[4],poses[5],poses[5]]
    rows={'sit-down-north':down,'sit-idle-north':idle,'sit-rise-north':list(reversed(down))}
    out=BASE/'review/seated-north-body-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,768),'#293b40')
    for row,(key,frames) in enumerate(rows.items()):
        for i,pose in enumerate(frames):pose.save(out/f'{key}-{i:03}.png');sheet.paste(pose,(i*256,row*256),pose)
    sheet.save(out/'body-contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,pivot=[128,224],records=records,limits=['Seated idle uses two authored settling poses with explicit holds.','Bare study only; fitted equipment, furniture contact and native joins remain unreviewed.']),indent=2)+'\n')
    print('Prepared 18 unselected north seating frames, one anatomical ruler and corrected standing endpoints.')
if __name__=='__main__':main()
