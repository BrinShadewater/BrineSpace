from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-crossing-v274';d=json.loads((out/'inputs.json').read_bytes())
polys={26:[[119,145],[137,145],[141,163],[122,165],[120,154]],27:[[119,145],[136,145],[139,162],[119,164],[118,154]],28:[[116,146],[131,145],[134,158],[129,163],[115,161]],29:[[116,146],[128,145],[131,158],[125,162],[113,160]],30:[[114,146],[128,145],[132,158],[125,162],[111,159]]}
knees={26:[120,164,136,180],27:[119,163,134,180],28:[115,162,132,179],29:[112,161,129,178],30:[111,160,128,178]}
board=Image.new('RGBA',(1296,768),(47,59,63,255));draw=ImageDraw.Draw(board)
for i,row in enumerate(d['sources']):
 phase=row['phase']
 if phase in polys:row['admissionPolygon']=polys[phase];row['protectedRectangles']=[knees[phase],[96,112,129,147]]
 im=Image.open(r/row['files']['bare']['file']).convert('RGBA');ad=ImageDraw.Draw(im);poly=[tuple(xy) for xy in row['admissionPolygon']];ad.line(poly+[poly[0]],fill=(0,220,220,255))
 for x0,y0,x1,y1 in row['protectedRectangles']:ad.rectangle((x0,y0,x1-1,y1-1),outline=(230,120,70,255))
 board.alpha_composite(im.crop((104,128,176,192)).resize((432,384),Image.Resampling.NEAREST),((i%3)*432,(i//3)*384));draw.text(((i%3)*432+5,(i//3)*384+5),f'phase{phase}',fill='white')
board.save(out/'admission-review.png');(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print('Five crossing-thigh extents configured; source knees and glove zone protected.')
