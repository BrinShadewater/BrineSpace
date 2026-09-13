"""Neutral directional head fitting from raw identity art, preserving movement bodies."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/turnaround-01.png';raw=binary(chroma(source))
    registration=json.loads((BASE/'review/registration.json').read_text())
    out=BASE/'review/directional-movement-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,3072),'#293b40');draw=ImageDraw.Draw(sheet);records=[]
    for d,direction in enumerate(['south','west','north']):
        for row,variant in enumerate(['body','equipment']):
            rec=next(x for x in registration['frames'] if x['direction']==direction and x['variant']==('bare' if row==0 else 'helmet'))
            sx,sy,_,_=rec['sourceCrop'];ox,oy=rec['offset'];scale=rec['scale']
            crop=[round(sx+(70-ox)/scale),round(sy+(18-oy)/scale),round(sx+(114-ox)/scale),round(sy+(54-oy)/scale)]
            # One resample from raw source, avoiding repeated reduction of reference PNGs.
            head=binary(raw.crop(crop).resize((37,31),Image.Resampling.BOX),True)
            for action_index,action in enumerate(['idle','walk']):
                key=action+'-'+direction
                for i in range(6):
                    body=Image.open(BASE/'sources'/f'{key}-{variant}-original-{i:03}.png').convert('RGBA')
                    bare=Image.open(BASE/'sources'/f'{key}-body-original-{i:03}.png').convert('RGBA')
                    top=bare.getbbox()[1]
                    pose=body.copy();regions=[(104,top-6,152,top+23),(103 if direction=='west' else 113,top+23,143,top+29)]
                    for region in regions:pose.paste((0,0,0,0),region)
                    pose.alpha_composite(head,(110,top-2))
                    assert pose.crop((0,top+29,256,256)).tobytes()==body.crop((0,top+29,256,256)).tobytes()
                    name=('helmet-' if row else '')+f'{key}-{i:03}.png';pose.save(out/name)
                    sheet.paste(pose,(i*256,(d*4+action_index*2+row)*256),pose)
                    records.append(dict(state=key,variant=variant,slot=i,sourceCrop=crop,position=[110,top-2],protectedBelow=top+29))
                draw.text((4,(d*4+action_index*2+row)*256+4),key+' '+variant,fill='white')
    sheet.save(out/'paired-contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='prepared_identity_source_selection_tracked_in_ledger',canonical='character/dr-veld-v1/concept-01.png',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),headCanvas=[37,31],frames=records,limits=['Neutral head references only; original body/equipment placement and lower motion retained.','Selection and native evidence are tracked in the clip ledger and README; continuous live context remains pending.']),indent=2)+'\n')
    print('Prepared72directional idle/walk identity frames; lower-body pixels preserved.')
if __name__=='__main__':main()
