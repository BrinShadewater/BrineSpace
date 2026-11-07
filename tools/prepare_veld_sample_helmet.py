"""Fit sample-inspection heads without changing the vial/hand region."""
from pathlib import Path
import json,hashlib
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'
def main():
    source=BASE/'sources/veld-east-sample-helmet-heads-01.png'
    raw=binary(chroma(source));assert raw.size==(2172,724)
    out=BASE/'review/veld-east-sample-01'
    frames=[Image.open(BASE/'sources/veld-east-sample-equipped-original-000.png').convert('RGBA')]
    for i in range(4):
        body=Image.open(out/f'repair-east-{i+1:03}.png').convert('RGBA')
        head=raw.crop((i*543+126,168,i*543+440,478))
        head=binary(head.resize((34,34),Image.Resampling.BOX),True)
        fitted=body.copy();fitted.paste((0,0,0,0),(110,121,144,155));fitted.alpha_composite(head,(110,121))
        assert fitted.crop((144,0,256,256)).tobytes()==body.crop((144,0,256,256)).tobytes()
        assert fitted.crop((0,155,256,256)).tobytes()==body.crop((0,155,256,256)).tobytes()
        frames.append(fitted)
    frames.append(Image.open(BASE/'sources/veld-east-sample-equipped-original-005.png').convert('RGBA'))
    sheet=Image.new('RGB',(1536,256),'#293b40')
    for i,frame in enumerate(frames):frame.save(out/f'helmet-repair-east-{i:03}.png');sheet.paste(frame,(i*256,0),frame)
    sheet.save(out/'helmet-contact.png')
    (out/'helmet-registration.json').write_text(json.dumps(dict(status='unselected_head_fit_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),headSize=[34,34],position=[110,121],protectedRegions=['x>=144','y>=155'],limits='Head seam and hand/visor clearance require native review.'),indent=2)+'\n')
    print('Prepared fitted sample heads; hand region and lower body unchanged.')
if __name__=='__main__':main()
