"""Register authored vial/case handling at the original south kneeling ruler."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main():
    source=BASE/'sources/veld-south-sample-strip-01.png'
    raw=binary(chroma(source));assert raw.size==(2172,724)
    scale=132/491
    frames=[Image.open(BASE/'sources/veld-south-sample-body-original-000.png').convert('RGBA')]
    anchors=[]
    # Rightmost planted boot defines contact, independent of moving arms/head.
    for i in range(4):
        tile=raw.crop((i*543,0,(i+1)*543,724));sole=624
        _,xs=np.where(np.asarray(tile)[sole-15:sole+1,:,3]>0)
        support=float((xs.min()+xs.max())/2);anchors.append([support,sole])
        dense=binary(tile.resize((round(543*scale),round(724*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(256,256))
        pose.alpha_composite(dense,(round(147-support*scale),round(223-sole*scale)))
        frames.append(pose)
    frames.append(Image.open(BASE/'sources/veld-south-sample-body-original-005.png').convert('RGBA'))
    out=BASE/'review/veld-south-sample-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,256),'#293b40')
    for i,frame in enumerate(frames):
        frame.save(out/f'repair-south-{i:03}.png');sheet.paste(frame,(i*256,0),frame)
    sheet.save(out/'contact.png')
    report=dict(status='unselected_body_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,pivot=[128,224],supports=anchors,limits='Original endpoints retained; fitted helmets and native temporal/live-context review pending.')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
