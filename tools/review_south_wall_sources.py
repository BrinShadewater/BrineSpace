"""Assemble source review board without changing source pixels."""
from pathlib import Path
import sys,json,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
version=sys.argv[1] if len(sys.argv)>1 else 'v1'
folder=ROOT/(sys.argv[2] if len(sys.argv)>2 else 'assets/south-wall-facing-'+version)
if (folder/'generation.json').exists():
    for row in json.loads((folder/'generation.json').read_text()):
        shutil.copy2(row.get('source',row.get('raw')),folder/(row['id']+'.png'))
        (folder/(row['id']+'.prompt.txt')).write_text(row['prompt'])
files=sorted(folder.glob('*.png'))
sheet=Image.new('RGB',(1800,((len(files)+2)//3)*330),'#304449')
draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB');im.thumbnail((590,290))
    x=i%3*600;y=i//3*330
    sheet.paste(im,(x+(600-im.width)//2,y+(290-im.height)//2))
    draw.text((x+8,y+295),p.stem,font=font,fill='white')
sheet.save(ROOT/('output/studio-owner-notes-2026-09-08/south-source-review-'+version+'.jpg'),quality=94)
