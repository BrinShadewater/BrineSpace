from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
import sys
P=Path(__file__).resolve().parent;R=P.parents[1];installed='--installed' in sys.argv;report=json.loads((P/('installed-route-evidence.json' if installed else 'route-evidence.json')).read_text());rows=[s for s in report['results'] if s.get('arrived')]
board=Image.new('RGB',(1440,2080),'#303b40');draw=ImageDraw.Draw(board)
for row,s in enumerate(rows):
 files=s['captures'];indices=np.linspace(0,len(files)-1,6).round().astype(int)
 for col,index in enumerate(indices):
  file=R/files[index].removeprefix('res://');im=Image.open(file).convert('RGB');x=im.width//2;y=im.height//2;crop=im.crop((x-115,y-95,x+115,y+145));board.paste(crop,(col*240,row*260+20));draw.text((col*240+4,row*260+4),s['mode']+' '+s['initialFacing']+' '+file.stem.rsplit('-',1)[-1],fill='white')
board.save(P/('native-installed-route-contact.png' if installed else 'native-route-contact.png'))
print(len(rows),'real rendered routes /48 selected contact samples')
