from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
frozen=json.loads((p/'late-inputs.json').read_bytes())
assert all(hashlib.sha256((p/n).read_bytes()).hexdigest()==h for n,h in frozen['preCallSha256'].items())
m=json.loads((r/'character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json').read_bytes());state=m['states'][0]
paths=[r/f[6:] if f.startswith('res://') else r/'character/james-cargo-return-bridges-v1'/f for f in state['frameFiles']]
original=[Image.open(f).convert('RGBA') for f in paths]
raw=Image.open(p/'late-raw.png').convert('RGBA');assert raw.width==raw.height and raw.getchannel('A').getextrema()==(0,255)
crop=raw.resize((80,80),Image.Resampling.LANCZOS)
late=original[4].copy();late.paste(crop.crop((8,8,66,78)),(104,64))
assert all(late.getpixel((x,y))==original[4].getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
late.save(p/'late-whole.png')
poses=[original[0]]+[Image.open(p/'alpha-frames'/('%03d.png'%j)).convert('RGBA') for j in range(3)]+[late,original[-1]]
board=Image.new('RGB',(1920,640),'#303b40');draw=ImageDraw.Draw(board)
for j,im in enumerate(poses):
    draw.text((j*320+8,8),str(j),fill='white');board.paste(im,(j*320+32,30),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(j*320,290),upper)
board.save(p/'late-whole-review.png')
native=Image.new('RGB',(1200,250),'#303b40')
for j,im in enumerate(poses):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'late-station-scale.png')
comparison=Image.new('RGB',(1280,500),'#303b40');draw=ImageDraw.Draw(comparison)
for j,(label,im) in enumerate([('previous row3',poses[3]),('old late row4',Image.open(p/'alpha-frames/003.png').convert('RGBA')),('new late row4',late),('exact outgoing',poses[5])]):
    draw.text((j*320+8,8),label,fill='white');comparison.paste(im,(j*320+32,24),im)
    upper=im.crop((96,56,176,136)).resize((240,240),Image.Resampling.NEAREST);comparison.paste(upper,(j*320+40,270),upper)
comparison.save(p/'late-join-comparison.png')
preview=[]
for im in poses:
    bg=Image.new('RGBA',(384,256),'#303b40');bg.alpha_composite(im,(64,0));preview.append(bg.convert('RGB'))
preview[0].save(p/'bare-late-source-trial.png',save_all=True,append_images=preview[1:],duration=[80]*6,loop=0,disposal=0,blend=0)
replay=Image.open(p/'bare-late-source-trial.png');assert replay.n_frames==6
for j,f in enumerate(ImageSequence.Iterator(replay)):
    assert f.convert('RGB').tobytes()==preview[j].tobytes() and f.info['duration']==80
crowns=[]
for im in poses:
    ys=[y for y in range(56,110) for x in range(110,145) if im.getpixel((x,y))[3]>=180]
    crowns.append(min(ys))
report={'selected':False,'visualReviewPending':True,'rawSize':list(raw.size),'headRegionOpaque180Top':crowns,'protectedPixelsLate':61476,'exactFirstLast':True,'decodedRgbDurationChecks':6,'registration':'Uniform whole generated square to80,original96/56 origin;no fitting/grade','sourceSha256':hashlib.sha256((p/'late-raw.png').read_bytes()).hexdigest(),'scope':'Bare-only source trial,not helmet/native/normal acceptance.'}
(p/'late-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
