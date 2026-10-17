from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-north-v1'
F=P/'bare/frames/land-swim-north';F.mkdir(parents=True,exist_ok=True)
frames=[Image.open(OLD/f'bare/frames/land-swim-north/{i:03}.png').convert('RGBA') for i in range(9)]
raw=Image.open(P/'sources/lift-atlas-v2.png').convert('RGBA');assert raw.size==(1536,1024)
pose=raw.crop((0,512,512,1024));a=np.array(pose);labs,count=label(a[:,:,3]>250);sizes=np.bincount(labs.ravel());assert count>0 and sizes[1:].max()>10000
keep=binary_dilation(labs==np.argmax(sizes[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
yy,xx=np.indices(a.shape[:2]);rgb=a[:,:,:3].astype(float)
hair=(a[:,:,3]>180)&(xx>245)&(xx<305)&(yy>65)&(yy<128)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)
y,x=np.where(hair);assert len(y)>100;top=int(y.min());axis=int(np.median(x[y<top+5]))
assert 264<=axis<=284 and 575<=top+512<=605,'Semantic rear crown, not warm cuff hardware'
im=Image.fromarray(a).resize((128,128),Image.Resampling.LANCZOS)
shift=(160-round(axis*.25),169-round(top*.25));out=Image.new('RGBA',(320,352));out.paste(im,shift)
assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(np.array(im)[:,:,3])
old=frames[5];frames[5]=out
for i,im in enumerate(frames):
    im.save(F/f'{i:03}.png')
    if i!=5:assert im.tobytes()==Image.open(OLD/f'bare/frames/land-swim-north/{i:03}.png').convert('RGBA').tobytes()
m=json.loads((OLD/'bare/manifest.json').read_text());m['name']='Bill North axial lift entry candidate';m['states'][0]['provenance']='Eight V1 poses pixel exact. New independently articulated axial lift5 from targeted atlas edit, fixed original atlas density .25 and whole-figure crown registration. Source-only.'
(P/'bare/manifest.json').write_text(json.dumps(m,indent=2)+'\n')
times=m['states'][0]['frameDurationsMs'];frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
    assert ap.n_frames==9
    for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
e=json.loads((OLD/'entry-review.json').read_text());e['registrations'][4].update(source='sources/lift-atlas-v2.png',sourceCell=[0,512,512,1024],headAnchor=[160,169],sourceHairCrown=[axis,top+512],scale=.25,wholeFigureTranslation=shift,alphaBounds=out.getchannel('A').getbbox())
e['repair']={'pose':5,'generation':'exec-923168a1-d880-4777-9f60-5c30e92d20ad','fixedSourceScale':.25,'sourceHairCrown':[axis,top+512],'wholeFigureTranslation':shift,'otherEightBareFramesExact':True,'sourceSHA256':hashlib.sha256((P/'sources/lift-atlas-v2.png').read_bytes()).hexdigest(),'promptSHA256':hashlib.sha256((P/'sources/lift-prompt-v2.txt').read_bytes()).hexdigest()}
e['visualReview']='pending new axial lift and neighbour/master comparison';e['helmetVisualReview']='pending rebuilt fitting'
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
for file in ['build_helmet.py','build_review.py']:
    text=(OLD/file).read_text(encoding='utf-8')
    if file=='build_review.py':
        text=text.replace('Lift pose still has a slight twist to refine.','Axial lift revision; full motion and master acceptance pending.')
        text=text.replace('Lift pose5 has slight lateral twist;', 'Axial lift5 revised;')
        text=text.replace('canvas{background:#182932}', 'canvas{background:#182932;height:min(704px,calc(100vh - 190px));width:auto;max-width:100%}')
    (P/file).write_text(text,encoding='utf-8')
board=Image.new('RGB',(1600,470),'#182932');d=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('preceding push',frames[4]),('old twisted lift',old),('new axial lift',out),('next near-prone',frames[6]),('selected idle/master ruler',frames[0])]):
    board.paste(im,(col*320,25),im);d.text((col*320+6,6),label,fill='white')
board.save(P/'lift-comparison.png')
print(json.dumps({'replacementPose':5,'otherBareFramesExact':8,'sourceCrown':[axis,top+512],'sharedScale':.25,'decodedAPNGExact':9}))
