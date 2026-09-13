"""Extract a review-only identity reference; never replace runtime animation art."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/turnaround-01.png'
    raw=binary(chroma(source));assert raw.size==(1448,1086)
    out=BASE/'review';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(736,416),'#293b40');labels=ImageDraw.Draw(sheet)
    heads=Image.new('RGB',(512,256),'#293b40')
    records=[];scale=148/490
    for row,variant in enumerate(['bare','helmet']):
        for column,(direction,x) in enumerate(zip(['south','east','north','west'],[156,438,720,1002])):
            tile=raw.crop((x,row*543,x+282,(row+1)*543));box=tile.getbbox();sole=box[3]-1
            _,xs=np.where(np.asarray(tile)[sole-20:sole+1,:,3]>0)
            support=float((xs.min()+xs.max())/2)
            reduced=binary(tile.resize((round(282*scale),round(543*scale)),Image.Resampling.BOX),True)
            frame=Image.new('RGBA',(184,184));offset=(round(92-support*scale),round(171-sole*scale));frame.alpha_composite(reduced,offset)
            frame.save(out/f'{variant}-{direction}.png')
            sheet.paste(frame,(column*184,row*208+24),frame);labels.text((column*184+4,row*208+4),variant+' '+direction,fill='white')
            head=frame.crop((64,16,128,80)).resize((128,128),Image.Resampling.NEAREST);heads.paste(head,(column*128,row*128),head)
            records.append(dict(variant=variant,direction=direction,sourceCrop=[x,row*543,x+282,(row+1)*543],scale=scale,offset=offset,pivot=[92,172]))
    sheet.save(out/'same-scale.png');heads.save(out/'face-comparison.png')
    report=dict(status='identity_reference_only_not_runtime_selected',canonical='character/dr-veld-v1/concept-01.png',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frames=records,limits=['Review face, silver streak and absence of glasses against canonical concept.','Generated body equipment differs between rows, including rear vial side; do not use turnaround bodies as paired animation replacements.','No motion, transition or live gameplay acceptance.'])
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Extracted 8 identity views at a common ruler; runtime selection unchanged.')
if __name__=='__main__':main()
