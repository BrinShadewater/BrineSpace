from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio
import json
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'inputs.json').read_bytes())
reader=iio.get_reader(str(p/'source.mp4'));frames=[Image.fromarray(x[:,:,:3]).resize((256,256),Image.Resampling.LANCZOS) for x in reader];reader.close()
def endpoint(path):
    im=Image.open(r/path).convert('RGBA');bg=Image.new('RGBA',(256,256),'white');bg.alpha_composite(im);return bg.convert('RGB')
rows=[('entry',endpoint(d['sources'][0]))]+[(str(i),frames[i]) for i in [0,24,48,72,96,120,len(frames)-1]]+[('exit',endpoint(d['sources'][1]))]
for page in [0,1]:
    board=Image.new('RGB',(1600,640),'#303b40');draw=ImageDraw.Draw(board)
    for j,(name,im) in enumerate(rows[page*5:page*5+5]):
        draw.text((j*320+8,8),name,fill='white');board.paste(im,(j*320+32,30))
        crop=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(crop,(j*320,290))
    board.save(p/'raw-review'/('join-%d.png'%page))
print('Exact endpoint and seven raw sample whole/upper comparisons saved at fixed1/3scale.')
