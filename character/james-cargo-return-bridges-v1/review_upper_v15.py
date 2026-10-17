from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
files=['frames-v9/bare/001.png','frames-v9/bare/002.png','upper-v15-bare.png','frames-v9/bare/003.png']
labels=['previous','selected target','V15 upper-body trial','next']
board=Image.new('RGB',(4*512,790),'#303b40');draw=ImageDraw.Draw(board)
images=[];metrics=[];hashes={}
for i,(f,label) in enumerate(zip(files,labels)):
    path=p/f;im=Image.open(path).convert('RGBA');images.append(im)
    hashes[str(path.relative_to(r))]=hashlib.sha256(path.read_bytes()).hexdigest()
    box=im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox()
    metrics.append({'label':label,'alpha32Bounds':box,'crownAbovePivot':224-box[1]})
    bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im)
    draw.text((i*512+8,8),label+' crown '+str(224-box[1]),fill='white')
    board.paste(bg.convert('RGB').resize((512,512),Image.Resampling.NEAREST),(i*512,28))
    board.paste(bg.crop((102,64,164,132)).convert('RGB').resize((186,204),Image.Resampling.NEAREST),(i*512+150,565))
board.save(p/'upper-v15-review.png')
original=images[1];candidate=images[2];checks=0
for y in range(256):
    for x in range(256):
        if not (104<=x<162 and 64<=y<134):
            assert original.getpixel((x,y))==candidate.getpixel((x,y));checks+=1
assert checks==61476
hashes['character/james-cargo-return-bridges-v1/upper-crop-v15/raw.png']=hashlib.sha256((p/'upper-crop-v15/raw.png').read_bytes()).hexdigest()
report={'selected':False,'visualReviewPending':True,'metrics':metrics,'protectedOriginalPixels':checks,'inputSha256':hashes,'scope':'Four registered full-body sources plus enlarged upper-body crops; no native actor motion/full master or paired helmet acceptance.'}
(p/'upper-v15-source-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(metrics))
