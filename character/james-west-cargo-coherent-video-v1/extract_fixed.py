from pathlib import Path
import hashlib,json
import imageio.v2 as iio
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw

p=Path(__file__).resolve().parent;r=p.parents[1]
out=p/'fixed-review';out.mkdir(exist_ok=True)
frames_dir=out/'frames';frames_dir.mkdir(exist_ok=True)
source=r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'
reference=Image.open(source).convert('RGBA')
assert reference.size==(256,256)
reader=iio.get_reader(str(p/'source.mp4'));meta=reader.get_meta_data()
assert tuple(meta['size'])==(768,768)
frames=[];stats=[]
for index,raw in enumerate(reader):
    rgb=np.asarray(raw)[:,:,:3].astype(float)
    # White key only on border-connected background. No interior recolouring.
    white=np.min(rgb,axis=2)>=240
    seed=np.zeros(white.shape,bool);seed[0,:]=white[0,:];seed[-1,:]=white[-1,:]
    seed[:,0]=white[:,0];seed[:,-1]=white[:,-1]
    background=ndimage.binary_propagation(seed,mask=white)
    fringe=ndimage.binary_dilation(background,iterations=1)&~background
    alpha=np.ones(white.shape);alpha[background]=0
    alpha[fringe]=np.clip((255-np.min(rgb[fringe],axis=1))/35,0,1)
    corrected=rgb.copy();edge=fringe&(alpha>0)
    corrected[edge]=np.clip((rgb[edge]-255*(1-alpha[edge,None]))/alpha[edge,None],0,255)
    rgba=np.dstack((corrected,alpha*255)).round().astype('uint8')
    # Same whole-canvas 1/3 scale every frame, no shift or pose/bounds fitting.
    im=Image.fromarray(rgba).resize((256,256),Image.Resampling.LANCZOS)
    im.save(frames_dir/f'{index:03d}.png');frames.append(im)
    mask=np.asarray(im)[:,:,3]>=128
    ys,xs=np.where(mask[205:230]);stats.append({'index':index,'time':index/meta['fps'],
        'lowerFootUnionBounds':[int(xs.min()),int(ys.min()+205),int(xs.max()+1),int(ys.max()+206)]})
reader.close()
def tile(im):
    bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im);return bg.convert('RGB')
pages=[]
for start in range(0,len(frames),24):
    board=Image.new('RGB',(1536,1160),'#303b40');d=ImageDraw.Draw(board)
    board.paste(tile(reference),(0,22));d.text((4,4),'original endpoint | 256 | pivot128,224',fill='white')
    for k,im in enumerate(frames[start:start+24]):
        x=k%6*256;y=280+k//6*220
        board.paste(tile(im).crop((0,40,256,256)),(x,y+20));d.text((x+4,y+2),f'{start+k:03d}',fill='white')
    name=f'whole-{start:03d}.png';board.save(out/name);pages.append(name)
chosen=[0,24,48,70,96,120,len(frames)-1]
board=Image.new('RGB',(8*256,2*230),'#303b40');d=ImageDraw.Draw(board)
for k,(name,im) in enumerate([('original',reference)]+[(str(i),frames[i]) for i in chosen]):
    d.text((k*256+4,4),name,fill='white')
    # Common foot and upper windows, enlarged 4x. Mark same root on every crop.
    for row,box in enumerate([(80,192,144,240),(72,64,136,112)]):
        crop=tile(im).crop(box).resize((256,192),Image.Resampling.NEAREST)
        board.paste(crop,(k*256,row*230+26))
    x=k*256+(128-80)*4;y=26+(224-192)*4
    d.line((x-5,y,x+5,y),fill='#55ffff');d.line((x,y-5,x,y+5),fill='#55ffff')
board.save(out/'contact-upper.png')
report={'sourceSha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),
 'referenceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'recipe':'Border-connected minRGB>=240 white key; one-pixel soft fringe/white unmix; interior RGB unchanged; whole768->256 Lanczos uniformly1/3; no translation/pose fitting or matte grade.',
 'canvas':[256,256],'pivot':[128,224],'standingReferenceHeight':148,
 'frames':len(frames),'fps':meta['fps'],'durationSeconds':len(frames)/meta['fps'],
 'pages':pages,'sampleIndices':chosen,'lowerFootDiagnostics':stats,
 'selected':False,'visualReviewPending':True,'scope':'Source extraction/contact study only. Lower-foot union bounds do not establish individual ankle contacts or anatomical height. Not native playback, paired helmet, endpoint admission or continuous watched cadence.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['frames','fps','durationSeconds','pages']}))
