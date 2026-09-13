"""Register authored meter edits while retaining original endpoint bodies."""
from pathlib import Path
import json,hashlib
from PIL import Image
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'
def main():
    source=BASE/'sources/branforth-west-meter-endpoints-01.png'
    raw=binary(chroma(source));assert raw.size==(1448,1086)
    out=BASE/'review/branforth-west-meter-endpoints-01'
    region=(48,61,70,88)
    sheet=Image.new('RGB',(736,184),'#293b40')
    for i,name in enumerate(['opening','closing']):
        tile=raw.crop((i*724,0,(i+1)*724,1086))
        tile=binary(tile.resize((64,96),Image.Resampling.BOX),True)
        registered=Image.new('RGBA',(184,184));registered.alpha_composite(tile,(32,40))
        for group in ['body','equipment']:
            original=Image.open(BASE/f'sources/branforth-west-meter-{group}-{name}-01.png').convert('RGBA')
            edited=original.copy();edited.paste(registered.crop(region),region[:2])
            outside=edited.copy();outside.paste(original.crop(region),region[:2]);assert outside.tobytes()==original.tobytes()
            edited.save(out/f'{group}-{name}.png')
            if group=='body':sheet.paste(original,(i*368,0),original);sheet.paste(edited,(i*368+184,0),edited)
    sheet.save(out/'comparison.png')
    (out/'registration.json').write_text(json.dumps(dict(status='unselected_endpoint_prop_edit',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),region=region,outsideRegion='exact original pixels',limits='Prop alignment and endpoint transitions need review before selection.'),indent=2)+'\n')
    print('Registered both endpoint edits, bare/equipped; outside-region pixels unchanged.')
if __name__=='__main__':main()
