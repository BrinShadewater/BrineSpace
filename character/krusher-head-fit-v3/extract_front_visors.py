from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path('character/krusher-head-fit-v3');raw=Image.open(P/'generated-front-heads.png').convert('RGBA');regions={
'visor-south':{'box':[237,701,501,990],'polygon':[[345,704],[408,708],[464,742],[484,792],[487,835],[478,902],[453,951],[420,978],[345,982],[296,964],[263,927],[245,870],[246,811],[260,771],[298,730]]},
'visor-south-bowed':{'box':[830,735,1100,1017],'polygon':[[918,742],[991,740],[1069,773],[1093,826],[1093,893],[1077,970],[1054,1000],[983,1011],[918,999],[879,976],[850,926],[832,870],[833,834],[855,790]]}}
for key,q in regions.items():
 mask=Image.new('L',raw.size);ImageDraw.Draw(mask).polygon([tuple(p) for p in q['polygon']],fill=255);im=raw.copy();im.putalpha(mask);im=im.crop(tuple(q['box'])).resize((23,25),Image.Resampling.NEAREST);out=P/'sources'/f'{key}-native.png';im.save(out);q.update(output=out.relative_to(P).as_posix(),source='generated-front-heads.png',outputSHA256=hashlib.sha256(out.read_bytes()).hexdigest(),sourceSHA256=hashlib.sha256((P/'generated-front-heads.png').read_bytes()).hexdigest(),size=[23,25])
(P/'front-visor-extraction.json').write_text(json.dumps({'regions':regions,'method':'Recorded full bare identity and visor interior extraction, without generated shell/body reuse.'},indent=2)+'\n')
