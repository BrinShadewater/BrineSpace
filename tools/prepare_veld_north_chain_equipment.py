"""Fit authored helmet heads through Veld north kneel/sample/stand."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/scanner-north-helmet-heads-01.png'
    raw=binary(chroma(source));assert raw.size==(2043,770)
    out=BASE/'review/north-kneel-body-01';scale=.09;records=[];clips={}
    for action,slots in [('kneel',[0,0,0,0,0,0]),('repair',[0,0,1,1,0,0])]:
        frames=[]
        for i,slot in enumerate(slots):
            body=Image.open(out/f'{action}-north-{i:03}.png').convert('RGBA')
            top=body.getbbox()[1]
            region=np.asarray(body)[top:top+14,105:140,3];_,xs=np.where(region>0);xs=xs+105
            center=float((xs.min()+xs.max())/2)
            tile=raw.crop((slot*raw.width//2,0,(slot+1)*raw.width//2,raw.height))
            head=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
            box=head.getbbox();offset=(round(center-(box[0]+box[2]-1)/2),top+26-(box[3]-1))
            pose=body.copy()
            pose.paste((0,0,0,0),(round(center)-15,top-4,round(center)+16,top+21))
            pose.alpha_composite(head,offset)
            assert pose.crop((0,top+27,256,256)).tobytes()==body.crop((0,top+27,256,256)).tobytes()
            assert pose.crop((144,0,256,256)).tobytes()==body.crop((144,0,256,256)).tobytes()
            frames.append(pose);records.append(dict(action=action,slot=i,headSlot=slot,position=offset,protectedBelow=top+27))
        clips[action]=frames
    idle=Image.open(BASE/'review/directional-movement-01/helmet-idle-north-000.png').convert('RGBA')
    clips['kneel'][0]=idle
    clips['repair'][0]=clips['kneel'][5].copy();clips['repair'][5]=clips['kneel'][5].copy()
    clips['stand']=list(reversed(clips['kneel']))
    sheet=Image.new('RGB',(1536,1536),'#293b40')
    for row,action in enumerate(['kneel','repair','stand']):
        for i,frame in enumerate(clips[action]):
            frame.save(out/f'helmet-{action}-north-{i:03}.png')
            body=Image.open(out/f'{action}-north-{i:03}.png')
            sheet.paste(body,(i*256,row*512),body);sheet.paste(frame,(i*256,row*512+256),frame)
    sheet.save(out/'paired-chain-contact.png')
    (out/'equipment-registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,records=records,limits=['Close-up collar/vial occlusion and native chain review required before selection.']),indent=2)+'\n')
    print('Prepared 18 fitted helmet poses with exact connected endpoints.')
if __name__=='__main__':main()
