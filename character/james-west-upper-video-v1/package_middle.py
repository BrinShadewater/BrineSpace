from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
frozen=json.loads((p/'middle-inputs.json').read_bytes())
assert all(hashlib.sha256((p/n).read_bytes()).hexdigest()==h for n,h in frozen['preCallSha256'].items())
m=json.loads((r/'character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json').read_bytes());state=m['states'][0]
paths=[r/f[6:] if f.startswith('res://') else r/'character/james-cargo-return-bridges-v1'/f for f in state['frameFiles']]
original=[Image.open(f).convert('RGBA') for f in paths];poses=[im.copy() for im in original]
out=p/'middle-frames';out.mkdir(exist_ok=True)
for row,name in [(3,'middle-raw.png'),(4,'late-raw.png')]:
    raw=Image.open(p/name).convert('RGBA');assert raw.width==raw.height and raw.getchannel('A').getextrema()==(0,255)
    crop=raw.resize((80,80),Image.Resampling.LANCZOS)
    poses[row].paste(crop.crop((8,8,66,78)),(104,64))
    assert all(poses[row].getpixel((x,y))==original[row].getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
for j,im in enumerate(poses):im.save(out/('%03d.png'%j))
for j in [0,1,2,5]:assert poses[j].tobytes()==original[j].tobytes()
board=Image.new('RGB',(1920,640),'#303b40');draw=ImageDraw.Draw(board)
for j,im in enumerate(poses):
    draw.text((j*320+8,8),str(j)+(' exact original' if j in [0,1,2,5] else ' new upper'),fill='white')
    board.paste(im,(j*320+32,30),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(j*320,290),upper)
board.save(p/'middle-whole-review.png')
native=Image.new('RGB',(1200,250),'#303b40')
for j,im in enumerate(poses):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'middle-station-scale.png')
comparison=Image.new('RGB',(1920,550),'#303b40');draw=ImageDraw.Draw(comparison)
for j,(old,new) in enumerate(zip(original,poses)):
    draw.text((j*320+8,8),str(j)+' original above / trial below',fill='white')
    comparison.paste(old,(j*320+32,25),old);comparison.paste(new,(j*320+32,280),new)
comparison.save(p/'middle-original-comparison.png')
preview=[]
for im in poses:
    bg=Image.new('RGBA',(384,256),'#303b40');bg.alpha_composite(im,(64,0));preview.append(bg.convert('RGB'))
preview[0].save(p/'bare-middle-source-trial.png',save_all=True,append_images=preview[1:],duration=[80]*6,loop=0,disposal=0,blend=0)
replay=Image.open(p/'bare-middle-source-trial.png');assert replay.n_frames==6
for j,f in enumerate(ImageSequence.Iterator(replay)):
    assert f.convert('RGB').tobytes()==preview[j].tobytes() and f.info['duration']==80
crowns=[min(y for y in range(56,110) for x in range(110,145) if im.getpixel((x,y))[3]>=180) for im in poses]
report={'selected':False,'visualReviewPending':True,'exactOriginalRows':[0,1,2,5],'editedRows':[3,4],'headRegionOpaque180Top':crowns,'protectedPixelsEachEdited':61476,'decodedRgbDurationChecks':6,'registration':'Uniform whole generated square to80,original96/56 origin,no fit/grade','prePackageSources':{str(f.relative_to(r)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},'generatedSources':{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in ['middle-raw.png','late-raw.png']},'scope':'Bare-only fixed-clock source trial;no helmet/native/normal acceptance.'}
(p/'middle-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['exactOriginalRows','editedRows','headRegionOpaque180Top','protectedPixelsEachEdited','decodedRgbDurationChecks']}))
