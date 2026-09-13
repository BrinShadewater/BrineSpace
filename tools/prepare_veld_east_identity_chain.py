"""Review a connected identity correction with a shared head ruler and exact joins."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'
SAMPLE=ROOT/'character/crew-action-detail-v2/review/veld-east-sample-01'
SCALE=.1

def head_layer(raw,row,slot,anchor):
    tile=raw.crop((slot*362,row*362,(slot+1)*362,(row+1)*362))
    bottom=tile.getbbox()[3]-1
    _,xs=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0)
    neck=float((xs.min()+xs.max())/2)
    dense=binary(tile.resize((36,36),Image.Resampling.BOX),True)
    layer=Image.new('RGBA',(256,256))
    layer.alpha_composite(dense,(round(anchor[0]-neck*SCALE),round(anchor[1]-bottom*SCALE)))
    return layer

def main():
    source=BASE/'sources/east-sample-heads-01.png';raw=binary(chroma(source))
    out=BASE/'review/east-chain-01';out.mkdir(exist_ok=True)
    records=[];all_frames={}
    for row,variant in enumerate(['body','equipment']):
        prefix='helmet-' if row else ''
        for key in ['idle-east','kneel-east','repair-east','interact-east','walk-east']:
            frames=[]
            for i in range(6):
                if key=='repair-east':
                    body=Image.open(SAMPLE/f'{prefix}{key}-{i:03}.png').convert('RGBA')
                    top=123;slot=0 if i==5 else i;anchor=(132,153)
                    regions=[(108,120,151,148),(115,148,144,155)]
                else:
                    body=Image.open(BASE/'sources'/f'{key}-{variant}-original-{i:03}.png').convert('RGBA')
                    bare=Image.open(BASE/'sources'/f'{key}-body-original-{i:03}.png')
                    top=bare.getbbox()[1]
                    slot=0 if key in ['idle-east','walk-east'] else ([0,2,2,3,0,0][i] if key=='interact-east' else [0,0,2,2,2,0][i])
                    anchor=(132,top+30)
                    regions=[(105,top-5,150,top+23),(116,top+23,146,top+32)]
                layer=head_layer(raw,row,slot,anchor);pose=body.copy()
                for region in regions:pose.paste((0,0,0,0),region)
                pose.alpha_composite(layer)
                # Diagnose preservation against an explicit bounded head edit.
                mask=Image.new('1',(256,256));draw=ImageDraw.Draw(mask)
                for x1,y1,x2,y2 in regions:draw.rectangle((x1,y1,x2-1,y2-1),fill=1)
                mask_arr=np.array(mask);mask_arr|=np.array(layer)[:,:,3]>0
                assert np.array_equal(np.array(pose)[~mask_arr],np.array(body)[~mask_arr])
                frames.append(pose);records.append(dict(variant=variant,state=key,slot=i,headSourceSlot=slot,anchor=anchor,regions=regions))
            all_frames[variant,key]=frames
        # Transition endpoints must share the corrected source, not approximate it.
        all_frames[variant,'kneel-east'][0]=all_frames[variant,'idle-east'][0].copy()
        all_frames[variant,'kneel-east'][5]=all_frames[variant,'repair-east'][0].copy()
        all_frames[variant,'stand-east']=list(reversed(all_frames[variant,'kneel-east']))
        all_frames[variant,'interact-east'][0]=all_frames[variant,'idle-east'][0].copy()
        all_frames[variant,'interact-east'][5]=all_frames[variant,'idle-east'][0].copy()
    sheet=Image.new('RGB',(1536,3072),'#293b40');draw=ImageDraw.Draw(sheet)
    for k,key in enumerate(['idle-east','kneel-east','repair-east','stand-east','interact-east','walk-east']):
        for row,variant in enumerate(['body','equipment']):
            for i,frame in enumerate(all_frames[variant,key]):
                prefix='helmet-' if row else '';frame.save(out/f'{prefix}{key}-{i:03}.png')
                sheet.paste(frame,(i*256,(k*2+row)*256),frame)
            draw.text((4,(k*2+row)*256+4),key+' '+variant,fill='white')
    sheet.save(out/'paired-contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='prepared_identity_source_selection_tracked_in_ledger',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),headScale=SCALE,records=records,joins=['idle0=kneel0=stand5','kneel5=repair0=stand0','interact0=interact5=idle0'],limits=['See README and per-clip ledger for current selection and verification evidence.','Continuous live workplace review and other Veld identity families remain pending.']),indent=2)+'\n')
    print('Prepared 72 paired frames with one head ruler and exact action transition endpoints.')
if __name__=='__main__':main()
