"""Register sample handling using the original kneeling ruler, not standing height."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'
def main():
    source=BASE/'sources/veld-east-sample-strip-01.png'
    raw=binary(chroma(source));assert raw.size==(2060,763)
    reference=Image.open(BASE/'sources/veld-east-sample-original-000.png').convert('RGBA')
    scale=99/434
    frames=[reference];anchors=[]
    for i in range(4):
        tile=raw.crop((i*515,0,(i+1)*515,763));sole=tile.getbbox()[3]-1
        _,xs=np.where(np.asarray(tile)[sole-30:sole+1,:,3]>0)
        x=float((xs.min()+xs.max())/2);anchors.append([x,sole])
        dense=binary(tile.resize((round(515*scale),round(763*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(256,256));pose.alpha_composite(dense,(round(133-x*scale),round(223-sole*scale)));frames.append(pose)
    frames.append(Image.open(BASE/'sources/veld-east-sample-original-005.png').convert('RGBA'))
    out=BASE/'review/veld-east-sample-01';out.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1536,256),'#293b40')
    for i,frame in enumerate(frames):frame.save(out/f'repair-east-{i:03}.png');sheet.paste(frame,(i*256,0),frame)
    sheet.save(out/'contact.png')
    report=dict(status='unselected_kneeling_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,pivot=[128,224],supports=anchors,limits='Original kneeling height99 used as common ruler; anatomy, sample detail, support and equipped/native review pending.')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
