"""Owner-authorized Bill recolour/head replacement trial; existing artwork only."""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label, binary_dilation, binary_fill_holes

P = Path(__file__).resolve().parent
R = P.parent.parent
BASE = R / 'character/crew-runtime-matte-v1/bill/manifest.json'
ACTION = R / 'character/bill-bare-south-selected-v1/manifest.json'
CONCEPT = R / 'character/krusher-concept-v1/concept-04-krusher-dom.png'
for folder in ['sources', 'frames', 'masks', 'review']:
    (P/folder).mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source_hashes = {str(p.relative_to(R)): sha(p) for p in [BASE, ACTION, CONCEPT]}
sheet = Image.open(CONCEPT).convert('RGBA')
head = sheet.crop((630, 274, 720, 383))
h = np.array(head); rgb = h[:,:,:3].astype(float)
warm = (rgb[:,:,0] > rgb[:,:,1]*1.035) & (rgb[:,:,0] > rgb[:,:,2]*1.045)
labs, n = label(warm)
part = max(range(1,n+1), key=lambda k: int((labs==k).sum()))
mask = binary_dilation(binary_fill_holes(labs==part), iterations=2)
h[:,:,3] = mask.astype('uint8')*255
head = Image.fromarray(h)
head.save(P/'sources/krusher-head-concept-crop.png')
head = head.crop(head.getbbox())
head = head.resize((round(head.width*28/head.height),28), Image.Resampling.LANCZOS)
head.save(P/'sources/krusher-head-native.png')
yy, xx = np.mgrid[:184,:184]
records=[]; previews={}; states=[]; failures=[]
base=json.loads(BASE.read_text()); action=json.loads(ACTION.read_text())
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20) if (R/'assets/fonts/BarlowSemiCondensed-Regular.ttf').exists() else ImageFont.load_default()
def resolve(manifest,path):
    return R/path[6:] if path.startswith('res://') else manifest.parent/path

for manifest,m,state_id in [(BASE,base,'idle-south'),(BASE,base,'walk-south')]:
    state=copy.deepcopy(next(s for s in m['states'] if s['id']==state_id))
    (P/'frames'/state_id).mkdir(exist_ok=True)
    originals=[]; outputs=[]; files=[]
    for i,path in enumerate(state['frameFiles']):
        src=resolve(manifest,path); source_hashes[str(src.relative_to(R))]=sha(src)
        original=Image.open(src).convert('RGBA'); a=np.array(original); rgb=a[:,:,:3].astype(float)
        top=int(np.where((a[:,:,3]>180)&(xx>74)&(xx<110)&(yy<60))[0].min())
        crown=(a[:,:,3]>180)&(xx>74)&(xx<110)&(yy>=top)&(yy<top+14)
        cy,cx=np.where(crown);axis=round((int(cx.min())+int(cx.max()))/2)
        warm=(a[:,:,3]>150)&(xx>=axis-12)&(xx<=axis+12)&(yy<top+27)&(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.04)
        labs,n=label(warm); part=max(range(1,n+1),key=lambda k:int((labs==k).sum()))
        headmask=labs==part; ys,xs=np.where(headmask)
        chin=int(ys.max())
        erase=binary_dilation(binary_fill_holes(headmask),iterations=1)&(yy<=chin+1)&(yy<top+27)
        # Neutral collar fabric remains protected below the face.
        erase &= ~((rgb.max(2)-rgb.min(2)<10)&(yy>chin-3))
        markings=(a[:,:,3]>0)&(yy>52)&(yy<112)&(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,0]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>35)
        out=a.copy(); target=np.array([82.,124.,128.])
        lum=rgb@np.array([.2126,.7152,.0722]); targetlum=float(target@np.array([.2126,.7152,.0722]))
        colours=np.minimum(255,np.rint(lum[:,:,None]/targetlum*target)).astype('uint8')
        out[markings,:3]=colours[markings]; out[erase]=0
        outim=Image.fromarray(out); destx=axis-head.width//2; desty=chin+1-head.height
        outim.alpha_composite(head,(destx,desty)); final=np.array(outim)
        allowed=erase|markings; allowed[desty:desty+head.height,destx:destx+head.width]=True
        unchanged=np.array_equal(a[~allowed],final[~allowed])
        if not unchanged: failures.append(f'{state_id}/{i}: pixels outside permitted regions changed')
        if outim.size!=(184,184): failures.append('Canvas mismatch')
        file=f'frames/{state_id}/{i:03}.png';outim.save(P/file);files.append(file)
        Image.fromarray(erase.astype('uint8')*255).save(P/f'masks/{state_id}-{i:03}-head.png')
        Image.fromarray(markings.astype('uint8')*255).save(P/f'masks/{state_id}-{i:03}-markings.png')
        records.append({'state':state_id,'frame':i,'source':str(src.relative_to(R)),'headAxis':axis,'chinY':chin,'headPaste':[destx,desty],'pixelsOutsideEditsExact':unchanged,'output':file})
        originals.append(original);outputs.append(outim)
    state['frameFiles']=files;state['frameCount']=len(files);state['provenance']='Bill original body/motion; muted cyan marking recolour; Krusher accepted concept head fitted per frame'
    states.append(state);previews[state_id]=(originals,outputs,state['frameDurationsMs'])
manifest={k:copy.deepcopy(base[k]) for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed']}
manifest.update(name='Krusher Dom / Bill base reuse trial',states=states,status='unselected visual trial',scope='south idle/walk only')
if 'strideDistanceCells' in base: manifest['strideDistanceCells']=base['strideDistanceCells']
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for state_id,(originals,outputs,timings) in previews.items():
    views=[]
    for i,(old,new) in enumerate(zip(originals,outputs)):
        view=Image.new('RGB',(760,444),'#272b2e'); d=ImageDraw.Draw(view)
        d.text((20,12),'BILL BASE',font=font,fill='white');d.text((395,12),'KRUSHER DOM / REUSE TEST',font=font,fill='white')
        for sprite,x in [(old,5),(new,385)]:
            large=sprite.resize((368,368),Image.Resampling.NEAREST);view.paste(large,(x,38),large)
        d.text((20,416),f'{state_id}   {i+1}/{len(outputs)}   Original timing; fixed source foot pivot',fill='#bbc5ca')
        views.append(view)
    views[0].save(P/f'review/{state_id}.gif',save_all=True,append_images=views[1:],duration=timings,loop=0,disposal=2)
    outputs[0].save(P/f'review/{state_id}.png',save_all=True,append_images=outputs[1:],duration=timings,loop=0,disposal=1,blend=0)
board=Image.new('RGB',(920,480),'#272b2e');d=ImageDraw.Draw(board)
d.text((20,15),'KRUSHER DOM — BILL BODY REUSE TRIAL',font=font,fill='white')
for x,caption,sprite in [(30,'Original Bill',previews['idle-south'][0][0]),(325,'Krusher / idle',previews['idle-south'][1][0]),(620,'Krusher / walk',previews['walk-south'][1][15])]:
    large=sprite.resize((276,276),Image.Resampling.NEAREST);board.paste(large,(x,65),large);d.text((x,355),caption,font=font,fill='white')
    small=sprite.resize((92,92),Image.Resampling.LANCZOS);board.paste(small,(x+90,380),small)
board.save(P/'review/standing-comparison.png')
changed=[p for p,digest in source_hashes.items() if sha(R/p)!=digest]
if changed:failures.append('Source inputs changed during build: '+str(changed))
report={'frames':len(records),'states':len(states),'failures':failures,'sourcesUnchanged':not changed,'records':records,'sourceHashes':source_hashes,'headCrop':[630,274,720,383],'nativeHeadSize':list(head.size),'method':'Existing accepted concept head extraction; deterministic recolour/pose fitting; no new generation','visualReview':'Pending','limitations':['Inherited Bill equipment; no new terminal action','South only; no helmet fitting','Preview only; no Godot actor integration']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'frames':len(records),'states':len(states),'failures':failures,'nativeHead':head.size,'sourcesUnchanged':not changed}))
assert not failures,failures
