"""Register Veld helmet pickup/don source poses with independent endpoint refs."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'
def main():
    source=BASE/'sources/helmet-don-east-body-02.png';raw=binary(chroma(source))
    assert raw.size==(2172,724)
    occupied=np.asarray(raw)[:,:,3].any(axis=0);edge=np.diff(np.r_[False,occupied,False].astype(int))
    starts,ends=np.where(edge==1)[0],np.where(edge==-1)[0];assert len(starts)==len(ends)==6
    scale=140/453;poses=[];records=[]
    for i,(start,end) in enumerate(zip(starts,ends)):
        left,right=int(start)-2,int(end)+2;tile=raw.crop((left,0,right,724));sole=636
        _,xs=np.where(np.asarray(tile)[sole-10:sole+1,:,3]>0);support=float((xs.min()+xs.max())/2)
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        offset=(round(128-support*scale),round(223-sole*scale));pose=Image.new('RGBA',(256,256));pose.alpha_composite(dense,offset);poses.append(pose)
        records.append(dict(sourceCrop=[left,0,right,724],support=[support,sole],position=offset))
    bare=Image.open(BASE/'review/east-chain-01/idle-east-000.png').convert('RGBA')
    helmet=Image.open(BASE/'review/east-chain-01/helmet-idle-east-000.png').convert('RGBA')
    mapping=[0,1,1,2,2,3,3,4,4,5]
    don=[bare]+[poses[i].copy() for i in mapping]+[helmet]
    out=BASE/'review/helmet-transition-body-01';out.mkdir(exist_ok=True)
    for key,frames in [('equip-helmet-east',don),('remove-helmet-east',list(reversed(don)))]:
        sheet=Image.new('RGB',(1536,512),'#293b40')
        for i,frame in enumerate(frames):frame.save(out/f'{key}-{i:03}.png');sheet.paste(frame,(i%6*256,i//6*256),frame)
        sheet.save(out/(key+'-contact.png'))
    (out/'registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,pivot=[128,224],records=records,interiorSourceSlots=mapping,derived='Removal reverses pickup/don study poses; distinct original timing still required.',limits=['Six authored interiors expanded through explicit held poses; exact corrected bare/equipped idle endpoints.','Review held helmet emptiness, overhead clearance, body proportions and removal credibility before native selection.']),indent=2)+'\n')
    print('Prepared 24 transition frames from six authored key poses and exact idle endpoints; selection is tracked in the ledger.')
if __name__=='__main__':main()
