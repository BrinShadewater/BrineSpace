from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
indices=[0,8,12,20,28,36];carrying=[p/'walk00-case-v2-fleck.png',p/'walk08-carry.png',p/'walk12-case-v2.png',p/'walk20-carry.png',p/'walk28-case-v2.png',p/'walk36-case-v2.png']
crop=(118,124,158,164);files=[]
for start in (0,3):
    board=Image.new('RGBA',(960,690),(48,59,63,255));d=ImageDraw.Draw(board)
    for column,(index,carry) in enumerate(list(zip(indices,carrying))[start:start+3]):
        orig=r/'character/james-west-carry-depth-v1/walk12-original.png' if index==12 else p/f'walk{index:02d}-carry-original.png'
        for row,(file,label) in enumerate([(orig,'actual walk'),(carry,'carrying')]):
            files.append(file);im=Image.open(file).convert('RGBA').crop(crop).resize((320,320),Image.Resampling.NEAREST);board.alpha_composite(im,(column*320,row*345+25));d.text((column*320+5,row*345+6),f'{label}{index}: belt/wrist',fill='white')
    board.convert('RGB').save(p/f'original-tool-comparison-{start}.png')
(p/'original-tool-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':list(crop),'visualReviewPending':True,'scope':'Aligned donor/carry belt crop, no mask or art changes. Compare actual equipment identity/occlusion.'},indent=2)+'\n',encoding='utf-8')
print('Six actual donor/carry tool comparisons prepared.')
