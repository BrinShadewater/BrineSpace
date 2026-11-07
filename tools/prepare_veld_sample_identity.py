"""Fit canonical-identity action heads for paired review; no runtime selection."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'
BODY=ROOT/'character/crew-action-detail-v2/review/veld-east-sample-01'

def main():
    source=BASE/'sources/east-sample-heads-01.png'
    raw=binary(chroma(source));assert raw.size==(2172,724)
    out=BASE/'review/east-sample-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,512),'#293b40');records=[]
    scale=34/263
    for row,variant in enumerate(['bare','helmet']):
        for i in range(6):
            source_slot=0 if i==5 else i
            tile=raw.crop((source_slot*362,row*362,(source_slot+1)*362,(row+1)*362))
            box=tile.getbbox();bottom=box[3]-1
            _,xs=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0)
            neck=float((xs.min()+xs.max())/2)
            head=binary(tile.resize((round(362*scale),round(362*scale)),Image.Resampling.BOX),True)
            offset=(round(132-neck*scale),round(153-bottom*scale))
            layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,offset)
            bounds=layer.getbbox()
            prefix='helmet-' if row else ''
            body=Image.open(BODY/f'{prefix}repair-east-{i:03}.png').convert('RGBA')
            pose=body.copy()
            pose.paste((0,0,0,0),(108,120,151,148))
            pose.paste((0,0,0,0),(115,148,144,155))
            pose.alpha_composite(layer)
            assert pose.crop((151,0,256,256)).tobytes()==body.crop((151,0,256,256)).tobytes(),(variant,i,'vial/hand changed')
            assert pose.crop((0,155,256,256)).tobytes()==body.crop((0,155,256,256)).tobytes()
            name=('helmet-' if row else '')+f'repair-east-{i:03}.png'
            pose.save(out/name);sheet.paste(pose,(i*256,row*256),pose)
            records.append(dict(variant=variant,slot=i,sourceSlot=source_slot,neck=[neck,bottom],offset=offset,bounds=bounds))
    sheet.save(out/'paired-contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='unselected_identity_correction_study',canonical='character/dr-veld-v1/concept-01.png',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,frames=records,limits=['Head/collar seams and identity require paired visual review.','Changing endpoint heads requires matching kneel/stand joins before runtime selection.','Original timing retained; no live or temporal acceptance yet.']),indent=2)+'\n')
    print('Prepared 12 corrected identity frames; vial/hand and lower body unchanged.')
if __name__=='__main__':main()
