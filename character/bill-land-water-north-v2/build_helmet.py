from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parent
head=Image.open(R/'bill-swim-helmet-north-coherent-v1/sources/canonical-head.png').convert('RGBA');assert head.size==(40,34)
records=json.loads((P/'entry-review.json').read_text())['registrations']
F=P/'helmet/frames/land-swim-north';F.mkdir(parents=True,exist_ok=True)
frames=[];fittings=[]
for i in range(9):
    bare=Image.open(P/f'bare/frames/land-swim-north/{i:03}.png').convert('RGBA');b=np.array(bare);yy,xx=np.indices(b.shape[:2])
    if i in [0,8]:
        path=R/('bill-shared-helmet-runtime-v2/frames/idle-north/000.png' if i==0 else 'bill-swim-helmet-north-coherent-v1/frames/swim-north/000.png')
        im=Image.open(path).convert('RGBA');shift=(68,52) if i==0 else (56,152)
        assert im.size==((184,184) if i==0 else (208,224))
        out=Image.new('RGBA',(320,352));out.paste(im,shift)
        assert out.crop((shift[0],shift[1],shift[0]+im.width,shift[1]+im.height)).tobytes()==im.tobytes()
    else:
        x,y=records[i-1]['headAnchor'];pos=(x-20,y-9)
        erase=(xx>=x-12)&(xx<=x+12)&(yy>=y-2)&(yy<y+19)
        a=b.copy();a[erase]=0;out=Image.fromarray(a);out.alpha_composite(head,pos);a=np.array(out)
        fg=(b[:,:,3]>0)&((xx<x-12)|(xx>x+12))&(yy<y+21)
        a[fg]=b[fg]
        mask=Image.new('L',(320,352));mask.paste(head.getchannel('A'),pos)
        allowed=erase|(np.array(mask)>0)
        assert np.array_equal(a[~allowed],b[~allowed])
        assert np.array_equal(a[fg],b[fg])
        assert np.array_equal(a[yy>=y+25],b[yy>=y+25])
        out=Image.fromarray(a)
        fittings.append({'pose':i,'headAnchor':[x,y],'shellPosition':pos,'scale':1,'rotation':0,'bodyOutsideHeadExact':True,'foregroundExact':True,'protectedBodyFromY':y+25})
    out.save(F/f'{i:03}.png');frames.append(out)
m=copy.deepcopy(json.loads((P/'bare/manifest.json').read_text()));m['name']='Bill North entry canonical rear helmet candidate';m['equipment']='diving-helmet'
(P/'helmet/manifest.json').write_text(json.dumps(m,indent=2)+'\n')
times=m['states'][0]['frameDurationsMs'];frames[0].save(P/'helmet/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'helmet/source-enter.png') as ap:
    assert ap.n_frames==9
    for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(2880,810),'#182932');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for i in range(9):
        im=Image.open(P/f'{gear}/frames/land-swim-north/{i:03}.png').convert('RGBA');board.paste(im,(i*320,row*405+25),im);d.text((i*320+8,row*405+5),f'{gear} {i}',fill='white')
board.save(P/'paired-entry-contact.png')
close=Image.new('RGB',(1960,660),'#182932');d=ImageDraw.Draw(close)
for col,rec in enumerate(fittings):
    x,y=rec['headAnchor']
    for row,gear in enumerate(['bare','helmet']):
        im=Image.open(P/f'{gear}/frames/land-swim-north/{rec["pose"]:03}.png').convert('RGBA');crop=im.crop((x-35,y-12,x+35,y+65)).resize((280,308),Image.Resampling.NEAREST);close.paste(crop,(col*280,row*330+20),crop);d.text((col*280+5,row*330+4),f'{gear} {rec["pose"]}',fill='white')
close.save(P/'helmet-neck-details.png')
e=json.loads((P/'entry-review.json').read_text());e.update(helmetFittings=fittings,decodedPairedAPNGFramesExact=18,pairedFrames=18,canonicalShellSHA256=hashlib.sha256(head.tobytes()).hexdigest(),helmetVisualReview='pending collar/foreground board')
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({'pairedFrames':18,'decodedAPNGExact':18,'protectedFittings':7,'timelineMs':sum(times)}))
