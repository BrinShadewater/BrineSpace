"""Fit authored helmet heads through Veld south kneel/sample/stand."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/south-sample-chain-helmet-heads-01.png'
    raw=binary(chroma(source));assert raw.size==(2172,724)
    out=BASE/'review/south-kneel-body-01';scale=.09;records=[];clips={}
    for action,slots in [('kneel',[0,1,2,1,1,3]),('repair',[3,3,1,2,3,3])]:
        frames=[]
        for i,slot in enumerate(slots):
            body=Image.open(out/f'{action}-south-{i:03}.png').convert('RGBA')
            top=body.getbbox()[1]
            region=np.asarray(body)[top:top+20,:,3];_,xs=np.where(region>0)
            center=float((xs.min()+xs.max())/2)
            tile=raw.crop((slot*543,0,(slot+1)*543,724))
            head=binary(tile.resize((round(543*scale),round(724*scale)),Image.Resampling.BOX),True)
            box=head.getbbox();offset=(round(center-(box[0]+box[2]-1)/2),top+29-(box[3]-1))
            pose=body.copy();pose.paste((0,0,0,0),(round(center)-19,top-4,round(center)+20,top+29));pose.alpha_composite(head,offset)
            raised=(action=='kneel' and i==5) or (action=='repair' and i in [0,1,2,4,5])
            if raised:
                # Vial and glove pass in front of the collar, not behind it.
                front=(110,top+23,122,top+37);pose.paste(body.crop(front),front)
            assert pose.crop((0,top+30,256,256)).tobytes()==body.crop((0,top+30,256,256)).tobytes()
            frames.append(pose);records.append(dict(action=action,slot=i,headSlot=slot,position=offset,protectedBelow=top+30))
        clips[action]=frames
    idle=Image.open(BASE/'review/directional-movement-01/helmet-idle-south-000.png').convert('RGBA')
    clips['kneel'][0]=idle
    clips['repair'][0]=clips['kneel'][5].copy();clips['repair'][5]=clips['kneel'][5].copy()
    clips['stand']=list(reversed(clips['kneel']))
    sheet=Image.new('RGB',(1536,1536),'#293b40')
    for row,action in enumerate(['kneel','repair','stand']):
        for i,frame in enumerate(clips[action]):
            frame.save(out/f'helmet-{action}-south-{i:03}.png')
            body=Image.open(out/f'{action}-south-{i:03}.png')
            sheet.paste(body,(i*256,row*512),body);sheet.paste(frame,(i*256,row*512+256),frame)
    sheet.save(out/'paired-chain-contact.png')
    (out/'equipment-registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,records=records,limits=['Close-up collar/vial occlusion and native chain review required before selection.']),indent=2)+'\n')
    print('Prepared 18 fitted helmet poses with exact connected endpoints.')
if __name__=='__main__':main()
