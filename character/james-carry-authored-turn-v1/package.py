from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
for name in ['early','late']:
    info=json.loads((p/(name+'-inputs.json')).read_bytes())
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in info['preCallSha256'].items())
    raw=Image.open(p/(name+'-raw.png')).convert('RGBA');assert raw.width==raw.height
    raw.resize((256,256),Image.Resampling.LANCZOS).save(p/(name+'-pose.png'))
sources=[r/'character/james-south-master-carry-v1/carry-pose.png',p/'early-pose.png',r/'character/james-carry-authored-midpoint-v1/midpoint-lower-v2.png',p/'late-pose.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
ims=[Image.open(s).convert('RGBA') for s in sources];labels=['South reused','early22.5 intended','mid45 intended reused','late67.5 intended','West reused']
frames=p/'frames';frames.mkdir(exist_ok=True)
for i,im in enumerate(ims):im.save(frames/f'{i:03}.png')
def board(name,crops,scale):
    w=crops[0].width*scale;h=crops[0].height*scale;out=Image.new('RGBA',(5*w,h+26),(48,59,63,255));d=ImageDraw.Draw(out)
    for i,(im,label) in enumerate(zip(crops,labels)):
        out.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+4,7),label,fill='white')
    out.convert('RGB').save(p/name)
board('whole-chronology.png',ims,1)
board('upper-chronology.png',[im.crop((80,64,176,160)) for im in ims],3)
board('legs-chronology.png',[im.crop((88,160,168,232)) for im in ims],3)
station=[]
for im in ims:
    out=Image.new('RGBA',(600,210),(48,59,63,255));d=ImageDraw.Draw(out)
    for i,height in enumerate([82,54,27]):
        sz=round(256*height/148);out.alpha_composite(im.resize((sz,sz),Image.Resampling.LANCZOS),(i*200+100-sz//2,180-round(224*height/148)));d.text((i*200+20,16),f'{height}px standing ruler',fill='white')
    station.append(out.convert('RGB'))
station[0].save(p/'station-preview.apng',save_all=True,append_images=station[1:],duration=[100,200,200,200,600],loop=0)
im=Image.open(p/'station-preview.apng');assert im.n_frames==5
for i,expected in enumerate(station):
    im.seek(i);assert im.convert('RGB').tobytes()==expected.tobytes()
    assert im.info['duration']==[100,200,200,200,600][i]
gallery=Image.new('RGB',(600,5*210))
for i,item in enumerate(station):gallery.paste(item,(0,i*210))
gallery.save(p/'station-chronology.png')
paths=['res://'+(frames/f'{i:03}.png').relative_to(r).as_posix() for i in range(5)]
states=[]
for name,files,facing in [('carry-turn-south-west',paths,'west'),('carry-turn-west-south',list(reversed(paths)),'south')]:
    states.append({'id':name,'frameCount':5,'frameFiles':files,'frameDurationsMs':[100,200,200,200,100],'loop':False,'facings':[facing]*5,'waterKinds':['carry']*5})
manifest={'name':'James authored carrying turn provisional bare','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'candidate_unselected_source_review_pending','states':states}
(p/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
report={'sourceFiles':[s.relative_to(r).as_posix() for s in sources],'sourceSha256':{s.relative_to(r).as_posix():hashlib.sha256(s.read_bytes()).hexdigest() for s in sources},'nativeAlpha128Bounds':[im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for im in ims],'standingRuler':148,'pivot':[128,224],'perPoseFit':False,'runtimeDurationsMs':[100,200,200,200,100],'previewDurationsMs':[100,200,200,200,600],'previewDecodeChecks':10,'visualReviewPending':True,'selected':False,'sourceAcceptance':False,'scope':'Five bare whole-body poses, reused cardinal endpoints/midpoint and two new source poses. Chronology evidence only until reviewed; reversed state is same poses reversed, not new art. Preview endpoint hold/replay is viewer only, no native or actual lifecycle proof.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'bounds':report['nativeAlpha128Bounds'],'previewDecodeChecks':10,'selected':False}))
