"""Fit authored helmet head crops while preserving scanner body pixels."""
from pathlib import Path
import json, hashlib
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main():
    source=BASE/'sources/branforth-south-helmet-heads-01.png'
    raw=binary(chroma(source));assert raw.size==(2169,725)
    out=BASE/'review/branforth-role-interact-south-strip-01'
    frames=[Image.open(BASE/'sources/branforth-south-meter-equipment-opening-01.png').convert('RGBA')]
    for i in range(4):
        body=Image.open(out/f'interact-south-{i+1:03}.png').convert('RGBA')
        # Crop only the authored shell/face/collar, excluding generated shoulders.
        head=raw.crop((i*raw.width//4+117,181,i*raw.width//4+424,521))
        head=binary(head.resize((38,40),Image.Resampling.BOX),True)
        fitted=body.copy()
        fitted.paste((0,0,0,0),(72,21,112,60))
        fitted.alpha_composite(head,(73,20))
        assert fitted.crop((0,60,184,184)).tobytes()==body.crop((0,60,184,184)).tobytes()
        frames.append(fitted)
    frames.append(Image.open(BASE/'sources/branforth-south-meter-equipment-closing-01.png').convert('RGBA'))
    contact=Image.new('RGB',(1104,184),'#293b40')
    for i,frame in enumerate(frames):
        frame.save(out/f'helmet-interact-south-{i:03}.png');contact.paste(frame,(i*184,0),frame)
    contact.save(out/'helmet-contact.png')
    report=dict(status='unselected_head_fit_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),headSize=[38,40],position=[73,20],bodyPixelsPreservedBelowY=60,limits='Head seam and paired native visual review pending; generated shoulders excluded.')
    (out/'helmet-registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
