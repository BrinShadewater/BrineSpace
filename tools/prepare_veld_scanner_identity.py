"""Pose-aware scanner heads and independent corrected idle endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/scanner-south-west-heads-01.png';raw=binary(chroma(source))
    neutral=binary(chroma(BASE/'sources/turnaround-01.png'))
    registration=json.loads((BASE/'review/registration.json').read_text())
    out=BASE/'review/directional-scanner-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,1536),'#293b40');draw=ImageDraw.Draw(sheet);records=[]
    for d,direction in enumerate(['south','west','north']):
        for row,variant in enumerate(['body','equipment']):
            prefix='helmet-' if row else '';key='interact-'+direction
            for i in range(6):
                if i in [0,5]:
                    pose=Image.open(BASE/'review/directional-movement-01'/f'{prefix}idle-{direction}-000.png').convert('RGBA')
                    records.append(dict(state=key,variant=variant,slot=i,endpointSource=f'{prefix}idle-{direction}-000.png'))
                else:
                    body=Image.open(BASE/'sources'/f'{key}-{variant}-original-{i:03}.png').convert('RGBA')
                    top=Image.open(BASE/'sources'/f'{key}-body-original-{i:03}.png').getbbox()[1]
                    if direction=='north':
                        rec=next(x for x in registration['frames'] if x['direction']=='north' and x['variant']==('bare' if row==0 else 'helmet'))
                        sx,sy,_,_=rec['sourceCrop'];ox,oy=rec['offset'];scale=rec['scale']
                        box=[round(sx+(70-ox)/scale),round(sy+(18-oy)/scale),round(sx+(114-ox)/scale),round(sy+(54-oy)/scale)]
                        head=binary(neutral.crop(box).resize((37,31),Image.Resampling.BOX),True);position=(110,top-2);slot='neutral-rear'
                    else:
                        slot=[0,1,2,0][i-1]+(3 if direction=='west' else 0)
                        tile=raw.crop((slot*362,row*362,(slot+1)*362,(row+1)*362));bottom=tile.getbbox()[3]-1
                        _,xs=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0);neck=float((xs.min()+xs.max())/2)
                        head=binary(tile.resize((36,36),Image.Resampling.BOX),True)
                        position=(round((125 if direction=='west' else 128)-neck*.1),round(top+31-bottom*.1))
                    pose=body.copy();regions=[(106 if direction=='west' else 110,top-5,153 if direction=='west' else 146,top+28),(113,top+28,144,top+33)]
                    for region in regions:pose.paste((0,0,0,0),region)
                    pose.alpha_composite(head,position)
                    assert pose.crop((0,top+33,256,256)).tobytes()==body.crop((0,top+33,256,256)).tobytes()
                    records.append(dict(state=key,variant=variant,slot=i,headSourceSlot=slot,position=position,protectedBelow=top+33))
                pose.save(out/f'{prefix}{key}-{i:03}.png');sheet.paste(pose,(i*256,(d*2+row)*256),pose)
            draw.text((4,(d*2+row)*256+4),key+' '+variant,fill='white')
    sheet.save(out/'paired-contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='unselected_scanner_identity_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frames=records,limits=['Front/left authored gaze changes; rear neutral head follows existing vertical body motion.','Endpoints deliberately match corrected idle; study needs native and live transition review.']),indent=2)+'\n')
    print('Prepared36paired directional scanner frames with corrected idle endpoints.')
if __name__=='__main__':main()
