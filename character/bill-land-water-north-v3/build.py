from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-north-v2'
F=P/'bare/frames/land-swim-north';F.mkdir(parents=True,exist_ok=True)
frames=[Image.open(OLD/f'bare/frames/land-swim-north/{i:03}.png').convert('RGBA') for i in range(9)]
raw=Image.open(P/'sources/reach-atlas-v3.png').convert('RGBA');assert raw.size==(1536,1024)
pose=raw.crop((1024,0,1536,512));a=np.array(pose);labs,count=label(a[:,:,3]>250);sizes=np.bincount(labs.ravel());assert count>0 and sizes[1:].max()>10000
keep=binary_dilation(labs==np.argmax(sizes[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
yy,xx=np.indices(a.shape[:2]);rgb=a[:,:,:3].astype(float)
hair=(a[:,:,3]>180)&(xx>204)&(xx<246)&(yy>65)&(yy<128)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)
y,x=np.where(hair);assert len(y)>100;top=int(y.min());axis=int(np.median(x[y<top+5]))
assert 214<=axis<=234 and 70<=top<=100,'Semantic rear crown, not warm cuff hardware'
im=Image.fromarray(a).resize((128,128),Image.Resampling.LANCZOS)
shift=(160-round(axis*.25),145-round(top*.25));out=Image.new('RGBA',(320,352));out.paste(im,shift)
assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(np.array(im)[:,:,3])
old=frames[4]
# Preserve original torso below articulated arms, belt/hips/legs/boots exactly.
pixels=np.array(out);previous=np.array(old);pixels[180:]=previous[180:];out=Image.fromarray(pixels)
assert np.array_equal(np.array(out)[180:],previous[180:])
frames[4]=out
for i,im in enumerate(frames):
    im.save(F/f'{i:03}.png')
    if i!=4:assert im.tobytes()==Image.open(OLD/f'bare/frames/land-swim-north/{i:03}.png').convert('RGBA').tobytes()
m=json.loads((OLD/'bare/manifest.json').read_text());m['name']='Bill North intermediate reach entry candidate';m['states'][0]['provenance']='Eight V1 poses pixel exact. New independently articulated intermediate reach5 from targeted atlas edit, fixed original atlas density .25 and whole-figure crown registration. Source-only.'
(P/'bare/manifest.json').write_text(json.dumps(m,indent=2)+'\n')
times=m['states'][0]['frameDurationsMs'];frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
    assert ap.n_frames==9
    for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
e=json.loads((OLD/'entry-review.json').read_text());e['registrations'][3].update(source='sources/reach-atlas-v3.png',sourceCell=[1024,0,1536,512],headAnchor=[160,145],sourceHairCrown=[axis+1024,top],scale=.25,wholeFigureTranslation=shift,alphaBounds=out.getchannel('A').getbbox())
e['repair']={'pose':4,'generation':'exec-19342959-9ddd-4f29-9e5c-d05e0d355ed0','fixedSourceScale':.25,'sourceHairCrown':[axis+1024,top],'wholeFigureTranslation':shift,'otherEightBareFramesExact':True,'sourceSHA256':hashlib.sha256((P/'sources/reach-atlas-v3.png').read_bytes()).hexdigest(),'promptSHA256':hashlib.sha256((P/'sources/reach-prompt-v3.txt').read_bytes()).hexdigest()}
e['visualReview']='pending new intermediate reach and neighbour/master comparison';e['helmetVisualReview']='pending rebuilt fitting'
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
for file in ['build_helmet.py','build_review.py']:
    text=(OLD/file).read_text(encoding='utf-8')
    if file=='build_review.py':text=text.replace('Axial lift revision;', 'Bent-elbow reach revision;')
    if file=='build_review.py':
        text=text.replace('Lift pose still has a slight twist to refine.','Intermediate reach revision; full motion and master acceptance pending.')
        text=text.replace('Lift pose5 has slight lateral twist;', 'Intermediate reach5 revised;')
        text=text.replace('canvas{background:#182932}', 'canvas{background:#182932;height:min(704px,calc(100vh - 190px));width:auto;max-width:100%}')
    (P/file).write_text(text,encoding='utf-8')
board=Image.new('RGB',(1600,470),'#182932');d=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('preceding deep crouch',frames[3]),('old full reach',old),('new bent-elbow reach',out),('next corrected lift',frames[5]),('selected idle/master ruler',frames[0])]):
    board.paste(im,(col*320,25),im);d.text((col*320+6,6),label,fill='white')
board.save(P/'reach-comparison.png')
print(json.dumps({'replacementPose':4,'otherBareFramesExact':8,'sourceCrown':[axis+1024,top],'sharedScale':.25,'decodedAPNGExact':9}))
