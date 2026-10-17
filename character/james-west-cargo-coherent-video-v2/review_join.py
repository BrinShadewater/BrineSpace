from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio
import json
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'inputs.json').read_bytes())
reader=iio.get_reader(str(p/'source.mp4'));frames=[Image.fromarray(x[:,:,:3]).resize((256,256),Image.Resampling.LANCZOS) for x in reader];reader.close()
def endpoint(path):
    im=Image.open(r/path).convert('RGBA');bg=Image.new('RGBA',(256,256),'white');bg.alpha_composite(im);return bg.convert('RGB')
rows=[('entry',endpoint(d['entry']))]+[(str(i),frames[i]) for i in [24,28,32,36,40,44,48]]+[('exit',endpoint(d['exit'])),('last140',frames[-1])]
for page in [0,1]:
    board=Image.new('RGB',(1600,640),'#303b40');draw=ImageDraw.Draw(board)
    for j,(name,im) in enumerate(rows[page*5:page*5+5]):
        draw.text((j*320+8,8),name,fill='white');board.paste(im,(j*320+32,30))
        crop=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(crop,(j*320,290))
    board.save(p/'raw-review'/('join-%d.png'%page))
print('Actual endpoints and eight early/terminal raw samples compared at uniform1/3 canvas scale;no extraction.')
