from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-return-v272';d=json.loads((out/'inputs.json').read_bytes())
polys={21:[[122,145],[141,144],[148,161],[128,165],[123,156]],22:[[122,145],[141,144],[148,161],[128,165],[123,156]],23:[[123,145],[141,144],[146,162],[128,165],[123,156]],24:[[121,146],[138,144],[144,162],[128,165],[123,156]],25:[[122,145],[138,145],[142,163],[126,165],[122,156]]}
knees={21:[128,164,145,180],22:[128,164,145,180],23:[128,164,145,180],24:[126,164,140,180],25:[125,164,138,180]}
board=Image.new('RGBA',(1296,768),(47,59,63,255));draw=ImageDraw.Draw(board)
for i,row in enumerate(d['sources']):
 phase=row['phase']
 if phase in polys:row['admissionPolygon']=polys[phase];row['protectedRectangles']=[knees[phase],[96,112,134,147]]
 im=Image.open(r/row['files']['bare']['file']).convert('RGBA');ad=ImageDraw.Draw(im);poly=[tuple(xy) for xy in row['admissionPolygon']];ad.line(poly+[poly[0]],fill=(0,220,220,255))
 for x0,y0,x1,y1 in row['protectedRectangles']:ad.rectangle((x0,y0,x1-1,y1-1),outline=(230,120,70,255))
 board.alpha_composite(im.crop((104,128,176,192)).resize((432,384),Image.Resampling.NEAREST),((i%3)*432,(i//3)*384));draw.text(((i%3)*432+5,(i//3)*384+5),f'phase{phase}',fill='white')
board.save(out/'admission-review.png');(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print('Configured pose-specific upright thigh polygons with original knees and glove zone protected.')
