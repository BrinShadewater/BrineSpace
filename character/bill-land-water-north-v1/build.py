from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;S=P/'sources'
F=P/'bare/frames/land-swim-north';F.mkdir(parents=True,exist_ok=True)
idle_path=R/'crew-runtime-matte-v1/bill/frames/idle-north-transition-matte-v1/000.png'
swim_path=R/'bill-swim-north-coherent-v1/frames/swim-north/000.png'
idle=Image.open(idle_path).convert('RGBA');swim=Image.open(swim_path).convert('RGBA')
assert idle.size==(184,184) and swim.size==(208,224)
frames=[];records=[]
def context(im,shift):
    out=Image.new('RGBA',(320,352));out.paste(im,shift)
    assert out.crop((shift[0],shift[1],shift[0]+im.width,shift[1]+im.height)).tobytes()==im.tobytes()
    return out
frames.append(context(idle,(68,52)))
def isolate(raw):
    a=np.array(raw);labs,count=label(a[:,:,3]>250);sizes=np.bincount(labs.ravel())
    assert count>0 and sizes[1:].max()>10000
    keep=binary_dilation(labs==np.argmax(sizes[1:])+1,iterations=3)&(a[:,:,3]>0)
    a[~keep]=0
    return Image.fromarray(a)
def register(im,scale,axis,crown,anchor=None):
    native=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    a=np.array(native);y,x=np.where(a[:,:,3]>180)
    shift=(160-round(axis*scale),224-int(y.max())-1) if anchor is None else (anchor[0]-round(axis*scale),anchor[1]-round(crown*scale))
    out=Image.new('RGBA',(320,352));out.paste(native,shift)
    assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(a[:,:,3]),'No alpha clipping'
    return out,{'scale':scale,'wholeFigureTranslation':shift,'headAnchor':[round(axis*scale)+shift[0],round(crown*scale)+shift[1]],'opaqueSole':int(y.max())+shift[1]+1,'alphaBounds':out.getchannel('A').getbbox()}
crouch=isolate(Image.open(S/'crouch-canvas-v2.png').convert('RGBA'))
frame,rec=register(crouch,148/976,627,328)
frames.append(frame);records.append(dict(rec,source='sources/crouch-canvas-v2.png',phase='early crouch'))
atlas=Image.open(S/'entry-atlas-v1.png').convert('RGBA');assert atlas.size==(1536,1024)
head=[(273,60),(767,110),(1247,82),(294,601),(775,618),(1275,589)]
anchors=[None,None,(160,145),(160,169),(160,184),(160,198)]
for i in range(6):
    col=i%3;row=i//3;box=(col*512,row*512,(col+1)*512,(row+1)*512)
    pose=isolate(atlas.crop(box));hx,hy=head[i];hx-=col*512;hy-=row*512
    frame,rec=register(pose,.25,hx,hy,anchors[i]);frames.append(frame)
    records.append(dict(rec,source='sources/entry-atlas-v1.png',cell=i,sourceCell=box,phase=['crouch','deep crouch','push','lift','near-prone','extend'][i]))
frames.append(context(swim,(56,152)))
times=[40,50,55,55,60,60,60,60,60];assert len(frames)==9 and sum(times)==500
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
m={'name':'Bill North articulated entry source candidate','frameWidth':320,'frameHeight':352,'pivot':[160,224],'standingHeight':148,'precomposed':True,'status':'source_visual_review_pending','states':[{'id':'land-swim-north','frameFiles':[f'frames/land-swim-north/{i:03}.png' for i in range(9)],'frameDurationsMs':times,'loop':False,'facings':['north']*9,'provenance':'Exact padded selected idle/swim contexts; seven independently authored intermediates from single crouch and shared-density six-pose atlas. Source-only; master/motion/helmet/native acceptance pending.'}]}
(P/'bare/manifest.json').write_text(json.dumps(m,indent=2)+'\n')
frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
    assert ap.n_frames==9
    for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(2880,405),'#182932');d=ImageDraw.Draw(board)
names=['selected idle','early crouch','crouch','deep crouch','push-off','lift','near-prone','extend','selected swim']
for i,im in enumerate(frames):
    board.paste(im,(i*320,25),im);d.text((i*320+8,7),f'{i} {names[i]}',fill='white')
    if i<=3:d.line((i*320,249,i*320+319,249),fill='#6aa39e')
board.save(P/'entry-contact.png')
e={'scope':'Nine-frame500ms bare source candidate, no helmet/native integration or full visual acceptance. Endpoint contexts static, not actual normal phase handoffs.',
   'sharedAtlasDrawingScale':.25,'scaleReason':'One fixed anatomical density for all six atlas cells against native rear-head/equipment ruler; not per-pose height/width fitting. Source canvas dimensions alone do not establish character drawing density.',
   'registrations':records,'endpointExactToSelectedSources':True,'decodedAPNGFramesExact':9,'timelineMs':500,
   'generation':'exec-cc306187-9f78-4e39-ad55-67b08baf571e','poseReferenceGeneration':'exec-03f2b8d7-7eb4-4ce6-a2c3-12927d641de4',
   'sourceHashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [S/'entry-atlas-v1.png',S/'entry-atlas-prompt-v1.txt',S/'near-prone-canvas-v2.png',S/'near-prone-prompt-v2.txt']},
   'visualReview':'pending complete source sequence and master comparison'}
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
data=json.dumps({'frames':[f'bare/frames/land-swim-north/{i:03}.png' for i in range(9)],'times':times})
(P/'entry.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill North entry source</title><style>body{background:#182932;color:#eef;font:16px sans-serif}canvas{background:#182932}img{max-width:100%}</style><h1>Bill North entry — bare source candidate</h1><p>Source-only500ms candidate. Helmet, complete master/motion review and native integration pending.</p><button id="play">Play once</button><button id="step">Next pose</button><select id="speed"><option value="1">Normal speed</option><option value="4">Quarter speed</option></select><span id="pose"></span><br><canvas width="640" height="704"></canvas><br><img src="entry-contact.png"><script>const data='''+data+''';const images=data.frames.map(src=>{const im=new Image();im.src=src;return im});const c=document.querySelector('canvas'),ctx=c.getContext('2d');let index=0,run=0;function draw(){ctx.clearRect(0,0,640,704);if(images[index].complete)ctx.drawImage(images[index],0,0,640,704);document.querySelector('#pose').textContent='Pose '+index}images.forEach(im=>im.onload=draw);document.querySelector('#step').onclick=()=>{run++;index=(index+1)%images.length;draw()};document.querySelector('#play').onclick=async()=>{const token=++run;for(index=0;index<images.length;index++){if(run!==token)return;draw();await new Promise(r=>setTimeout(r,data.times[index]*Number(document.querySelector('#speed').value)))}index=images.length-1;draw()};draw()</script>''',encoding='utf-8')
print(json.dumps({'frames':9,'timelineMs':500,'decodedAPNGExact':9,'registrations':records}))
