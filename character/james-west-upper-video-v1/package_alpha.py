from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
frozen=json.loads((p/'alpha-inputs.json').read_bytes());assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in frozen.items())
raw=Image.open(p/'alpha-raw.png').convert('RGBA');assert raw.size==(1254,1254)
assert raw.getchannel('A').getextrema()==(0,255)
m=json.loads((r/'character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json').read_bytes());state=m['states'][0]
paths=[r/f[6:] if f.startswith('res://') else r/'character/james-cargo-return-bridges-v1'/f for f in state['frameFiles']]
original=[Image.open(f).convert('RGBA') for f in paths];poses=[original[0]];out=p/'alpha-frames';out.mkdir(exist_ok=True)
for j in range(4):
    crop=raw.crop(((j%2)*627,(j//2)*627,(j%2+1)*627,(j//2+1)*627)).resize((80,80),Image.Resampling.LANCZOS)
    im=original[j+1].copy();im.paste(crop.crop((8,8,66,78)),(104,64))
    assert all(im.getpixel((x,y))==original[j+1].getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
    im.save(out/('%03d.png'%j));poses.append(im)
poses.append(original[-1]);board=Image.new('RGB',(1920,640),'#303b40');draw=ImageDraw.Draw(board)
for j,im in enumerate(poses):
    draw.text((j*320+8,8),str(j),fill='white');board.paste(im,(j*320+32,30),im)
    crop=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(crop,(j*320,290),crop)
board.save(p/'whole-alpha-review.png')
comparison=Image.new('RGB',(1920,550),'#303b40');cd=ImageDraw.Draw(comparison)
for j,(old,new) in enumerate(zip(original,poses)):
    cd.text((j*320+8,8),str(j)+' original above / trial below',fill='white')
    comparison.paste(old,(j*320+32,25),old);comparison.paste(new,(j*320+32,280),new)
comparison.save(p/'alpha-original-comparison.png')
native=Image.new('RGB',(1200,250),'#303b40')
for j,im in enumerate(poses):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'alpha-station-scale.png')
preview=[]
for im in poses:
    bg=Image.new('RGBA',(384,256),'#303b40');bg.alpha_composite(im,(64,0));preview.append(bg.convert('RGB'))
preview[0].save(p/'bare-source-trial.png',save_all=True,append_images=preview[1:],duration=[80]*6,loop=0,disposal=0,blend=0)
replay=Image.open(p/'bare-source-trial.png');assert replay.n_frames==6
for j,f in enumerate(ImageSequence.Iterator(replay)):
    assert f.convert('RGB').tobytes()==preview[j].tobytes();assert f.info['duration']==80
report={'selected':False,'visualReviewPending':True,'exactFirstLast':True,'protectedPixelsEach':61476,'decodedRgbDurationChecks':6,'registration':'Uniform627->80,original96/56 crop origin,no per-pose fit/grade','sourceSha256':hashlib.sha256((p/'alpha-raw.png').read_bytes()).hexdigest(),'scope':'Paired endpoint source trial bare only,not native/helmet/normal motion acceptance. Six80ms viewer source holds mirror originalV9,not new actor clocks.'}
(p/'alpha-review.json').write_text(json.dumps(report,indent=2)+'\n');print('Direct generated alpha preserved;61476 outside pixels exact each;6APNG RGB/80ms holds checked.')
