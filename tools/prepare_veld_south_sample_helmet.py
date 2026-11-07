"""Fit independent sample-action heads while preserving hands and case pixels."""
from pathlib import Path
import json,hashlib
from PIL import Image
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main():
    source=BASE/'sources/veld-south-sample-helmet-heads-01.png'
    raw=binary(Image.open(source).convert('RGBA'));assert raw.size==(2172,724)
    out=BASE/'review/veld-south-sample-01'
    frames=[Image.open(BASE/'sources/veld-south-sample-equipment-original-000.png').convert('RGBA')]
    for i in range(4):
        body=Image.open(out/f'repair-south-{i+1:03}.png').convert('RGBA')
        head=raw.crop((i*543+109,154,i*543+448,539))
        head=binary(head.resize((34,39),Image.Resampling.BOX),True)
        fitted=body.copy();fitted.paste((0,0,0,0),(110,90,145,130));fitted.alpha_composite(head,(110,90))
        assert fitted.crop((0,130,256,256)).tobytes()==body.crop((0,130,256,256)).tobytes()
        assert fitted.crop((0,0,110,256)).tobytes()==body.crop((0,0,110,256)).tobytes()
        frames.append(fitted)
    frames.append(Image.open(BASE/'sources/veld-south-sample-equipment-original-005.png').convert('RGBA'))
    sheet=Image.new('RGB',(1536,256),'#293b40')
    for i,frame in enumerate(frames):frame.save(out/f'helmet-repair-south-{i:03}.png');sheet.paste(frame,(i*256,0),frame)
    sheet.save(out/'helmet-contact.png')
    (out/'helmet-registration.json').write_text(json.dumps(dict(status='unselected_fitted_head_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),size=[34,39],position=[110,90],protectedRegions=['y>=130','x<110'],limits='Native timing, clearance and continuous workplace review pending.'),indent=2)+'\n')
    print('Prepared six fitted south sample frames; hands/case/lower body preserved.')
if __name__=='__main__':main()
