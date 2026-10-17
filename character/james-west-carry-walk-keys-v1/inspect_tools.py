from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];files=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'walk00-carry-original.png',p/'walk00-carry.png',p/'walk28-carry.png',p/'walk36-carry.png'];labels=['standing carry','walk0 original','walk0 carry','walk28 carry','walk36 carry'];out=Image.new('RGBA',(2000,420),(48,59,63,255))
for i,(f,label) in enumerate(zip(files,labels)):
    im=Image.open(f).convert('RGBA').crop((94,122,144,170)).resize((400,384),Image.Resampling.NEAREST);out.alpha_composite(im,(i*400,30));d=ImageDraw.Draw(out);d.text((i*400+3,8),label,fill='white')
    for y in [128,136,144,152,160]:d.line((i*400,30+(y-122)*8,(i+1)*400,30+(y-122)*8),fill=(150,150,150,120),width=1);d.text((i*400+4,31+(y-122)*8),str(y),fill='white')
out.convert('RGB').save(p/'belt-device-comparison.png')
print('Aligned case/belt detail with native height guides prepared.')
