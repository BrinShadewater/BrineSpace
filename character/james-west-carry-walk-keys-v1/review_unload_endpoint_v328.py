from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-coherent-video-v328'
raw=Image.open(o/'endpoint-raw.png').convert('RGBA');frame=raw.resize((256,256),Image.Resampling.NEAREST);frame.save(o/'endpoint-256.png')
first=Image.open(r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png').convert('RGBA')
old=Image.open(r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/005.png').convert('RGBA')
ims=[first,frame,old];bounds=[im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for im in ims]
board=Image.new('RGB',(1152,430),(48,59,64));d=ImageDraw.Draw(board)
for j,(im,label,b) in enumerate(zip(ims,['Turn endpoint','Trial unload endpoint','Current unload endpoint'],bounds)):
    x=j*384;board.paste(im,(x+64,20),im);d.text((x+5,3),f'{label} {b}',fill='white')
    pos=x+10
    for h in [82,54,27]:
        n=round(256*h/148);small=im.resize((n,n),Image.Resampling.LANCZOS);board.paste(small,(pos,420-n),small);pos+=n+6
board.save(o/'endpoint-review.png')
report=dict(referenceBounds=bounds[0],candidateBounds=bounds[1],oldFinalBounds=bounds[2],mode='built-in imagegen',
    prompt='endpoint-submitted-prompt.txt',generationFile='exec-389922d5-c924-4c65-bd59-c8da08bcad80.png',
    normalChanged=False,selected=False,nativeRun=False,geometryEligibleForTemporalStudy=abs(bounds[0][1]-bounds[1][1])<=1 and abs(bounds[0][3]-bounds[1][3])<=1,
    caveats=['candidate case is broader and visible outside the boots; original-master/full prop acceptance remains open','cloth finish and equipment detail still require master comparison','source pixels redrawn; registration measurements are not identity proof'])
(o/'endpoint-review.json').write_text(json.dumps(report,indent=2)+'\n')
v=p/'north-unload-coherent-motion-v329';v.mkdir(exist_ok=True)
for im,name in zip([first,frame],['first.png','last.png']):
    bg=Image.new('RGB',(256,256),(48,59,64));bg.paste(im,(0,0),im);bg.resize((768,768),Image.Resampling.NEAREST).save(v/name)
prompt=(o/'prompt.txt').read_text();(v/'prompt.txt').write_text(prompt)
(v/'inputs.json').write_text(json.dumps(dict(firstSource='character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png',lastSource=str((o/'endpoint-256.png').relative_to(r)),sourceHashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in [first,frame]],authoringHashes=[hashlib.sha256((v/n).read_bytes()).hexdigest() for n in ['first.png','last.png']],normalChanged=False,endpointPropAndMasterAcceptance=False),indent=2)+'\n')
print(json.dumps(report))
