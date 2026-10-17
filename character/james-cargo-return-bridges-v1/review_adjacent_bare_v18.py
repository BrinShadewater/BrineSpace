from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];m=json.loads((p/'bare-joined-manifest-v9.json').read_bytes())
files=[r/ref[6:] if ref.startswith('res://') else p/ref for ref in m['states'][0]['frameFiles']]
old=[Image.open(f).convert('RGBA') for f in files]
trial=list(old);trial[2]=Image.open(p/'upper-v17-bare.png').convert('RGBA');trial[3]=Image.open(p/'upper-v18-bare.png').convert('RGBA')
board=Image.new('RGB',(1536,1040),'#303b40');draw=ImageDraw.Draw(board)
def stats(images):
    result=[];crowns=[]
    for im in images:
        box=im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox();crowns.append(224-box[1])
    for a,b in zip(images,images[1:]):
        aa=list(a.crop((0,0,256,110)).get_flattened_data());bb=list(b.crop((0,0,256,110)).get_flattened_data())
        result.append(sum(sum(abs(x[c]*x[3]-y[c]*y[3])/255 for c in range(3))+abs(x[3]-y[3]) for x,y in zip(aa,bb)))
    return {'crowns':crowns,'upperRegionPremultipliedL1':result,'largestUpperStep':max(result),'maxCrownStep':max(abs(a-b) for a,b in zip(crowns,crowns[1:]))}
for row,images in enumerate([old,trial]):
    measurements=stats(images)
    for i,im in enumerate(images):
        x=i*256;y=row*520
        draw.text((x+4,y+5),('normal' if row==0 else 'trial')+' '+str(i)+' crown'+str(measurements['crowns'][i]),fill='white')
        board.paste(im,(x,y+25),im)
        bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im)
        board.paste(bg.crop((102,64,164,132)).convert('RGB').resize((186,204),Image.Resampling.NEAREST),(x+35,y+292))
board.save(p/'adjacent-bare-v18-review.png')
hashes={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files+[p/'upper-v17-bare.png',p/'upper-v18-bare.png']}
report={'visualReviewPending':True,'selected':False,'normal':stats(old),'trial':stats(trial),'inputSha256':hashes,'scope':'Two adjacent bare source edits; six normal/six trial registered poses and crops, not paired helmet/native actor/full master acceptance.'}
(p/'adjacent-bare-v18-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['normal','trial']}))
