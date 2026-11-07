"""Fit corrected pose-specific helmet heads to the replacement scanner bodies."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/scanner-south-west-heads-01.png';raw=binary(chroma(source))
    out=BASE/'review/south-scanner-body-02';records=[]
    idle=Image.open(BASE/'review/directional-movement-01/helmet-idle-south-000.png').convert('RGBA')
    frames=[idle];scale=.105
    for i,slot in enumerate([0,0,2,0],1):
        body=Image.open(out/f'interact-south-{i:03}.png').convert('RGBA')
        tile=raw.crop((slot*362,362,(slot+1)*362,724));bottom=tile.getbbox()[3]-1
        _,xs=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0);neck=float((xs.min()+xs.max())/2)
        head=binary(tile.resize((38,38),Image.Resampling.BOX),True)
        offset=(round(128-neck*scale),round(109-bottom*scale))
        pose=body.copy();pose.paste((0,0,0,0),(110,76,146,107));pose.paste((0,0,0,0),(116,107,141,110));pose.alpha_composite(head,offset)
        assert pose.crop((0,110,256,256)).tobytes()==body.crop((0,110,256,256)).tobytes(),i
        frames.append(pose);records.append(dict(slot=i,headSourceSlot=slot,offset=offset))
    frames.append(idle.copy());sheet=Image.new('RGB',(1536,512),'#293b40')
    for i,frame in enumerate(frames):
        frame.save(out/f'helmet-interact-south-{i:03}.png');sheet.paste(frame,(i*256,256),frame)
        body=Image.open(out/f'interact-south-{i:03}.png');sheet.paste(body,(i*256,0),body)
    sheet.save(out/'paired-contact.png')
    (out/'equipment-registration.json').write_text(json.dumps(dict(status='prepared_source_selection_recorded_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,records=records,protectedBelow=110,limits=['Exact corrected equipped idle endpoints; original body/hand/scanner pixels below collar retained.','Paired native evidence is recorded in README and ledger; continuous live context remains pending.']),indent=2)+'\n')
    print('Prepared six fitted helmet frames with original scanner/hand pixels preserved.')
if __name__=='__main__':main()
