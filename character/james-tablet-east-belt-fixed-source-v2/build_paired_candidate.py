"""Stage all141 new source poses with the selected common helmet; no install."""
from pathlib import Path
import json,runpy,math,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
helper=runpy.run_path(str(R/'character/james-shared-helmet-interact-east-v1/build.py'))
face=helper['face'];idle=helper['idle']
bare_idle=idle(R/'character/crew-runtime-matte-v1/branforth/manifest.json');helmet_idle=idle(R/'character/james-shared-helmet-runtime-v1/manifest.json')
shellpath=R/'character/james-shared-helmet-east-v1/helmet.png';shell=Image.open(shellpath).convert('RGBA')
source=[Image.open(f).convert('RGBA') for f in sorted((P/'matching-study-frames').glob('*.png'))]
reference,_,_=face(bare_idle);baseline=np.array([73,16]);tracking=[];paired={'bare':[],'helmet':[]}
for i,body in enumerate(source):
    target,box,count=face(body);at=np.rint(baseline+target-reference).astype(int)
    eq=body.copy();ImageDraw.Draw(eq).polygon([tuple(target+point) for point in [(-11,-14),(10,-14),(14,8),(6,15),(-10,10)]],fill=(0,0,0,0));eq.alpha_composite(shell,tuple(map(int,at)))
    tracking.append({'sourceFrame':i,'face':target.round(3).tolist(),'facePixels':count,'helmetPosition':at.tolist(),'shellRotation':0,'bodyTranslation':[0,0]})
    for mode,im,end in [('bare',body,bare_idle),('helmet',eq,helmet_idle)]:
        if i in [0,len(source)-1]:im=end.copy()
        paired[mode].append(im);path=P/'candidate-frames'/mode/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
times=[round((i+1)*5500/len(source))-round(i*5500/len(source)) for i in range(len(source))]
for mode in paired:
    manifest={'name':'James East separate-tablet candidate '+mode,'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'candidate_full_source_native_review_pending','states':[]}
    for key in ['interact-east','inspect-east']:
        dur=times.copy()
        if key=='inspect-east':dur[-1]+=500
        manifest['states'].append({'id':key,'frameCount':len(source),'frameFiles':[f'candidate-frames/{mode}/{i:03}.png' for i in range(len(source))],'frameDurationsMs':dur,'loop':key=='inspect-east','provenance':{'source':'source.mp4','sourceFrames':list(range(len(source))),'derivation':'Complete authored lift/read/stow, one fixed inverse master ruler and pooled neutral gain; exact selected idle endpoints. No reverse lift, frame deletion, interpolated poses or per-pose fitting.'}})
    if mode=='helmet':
        old=json.loads((R/'character/james-inspect-material-continuity-v1/helmet-manifest.json').read_text())
        indices=[0,32,60,86,123,140]
        for key in ['eat-east','drink-east']:
            state=copy.deepcopy(next(s for s in old['states'] if s['id']==key))
            state['frameFiles']=[f'candidate-frames/helmet/{i:03}.png' for i in indices]
            state['provenance'].update(sourceManifest='character/james-tablet-east-belt-fixed-source-v2/helmet-manifest.json',sourcePoses=indices,materialSource='New separate-tablet complete source; existing six-slot compatibility substitute clocks retained. Actual closed-helmet everyday behavior plays full inspect-east.')
            manifest['states'].append(state)
    (P/(mode+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
previews=[]
for i in range(len(source)):
    board=Image.new('RGB',(920,255),'#303b40');d=ImageDraw.Draw(board);d.text((8,6),'James East separate tablet candidate / bare / shared helmet / 82px / 54px / 27px',fill='white')
    for j,mode in enumerate(['bare','helmet']):
        im=paired[mode][i];board.paste(im,(220*j,40),im)
        for h,x in [(82,460),(54,660),(27,800)]:
            side=round(184*h/148);small=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(small,(x+j*(side+8),212-round(172*h/148)),small)
    previews.append(board)
fulltimes=times.copy();fulltimes[-1]+=500;elapsed=rounded=0;dur=[]
for t in fulltimes:
    elapsed+=t;now=round(elapsed/10)*10;dur.append(now-rounded);rounded=now
previews[0].save(P/'paired-candidate.gif',save_all=True,append_images=previews[1:],duration=dur,loop=0)
heads=Image.new('RGB',(16*140,math.ceil(len(source)/16)*140),'#303b40');d=ImageDraw.Draw(heads)
for i,im in enumerate(paired['helmet']):
    crop=im.crop((62,8,128,66)).resize((132,116),Image.Resampling.NEAREST);at=(i%16*140,i//16*140);heads.paste(crop,(at[0],at[1]+22),crop);d.text((at[0]+4,at[1]+3),str(i),fill='white')
heads.save(P/'all-candidate-helmet-heads.png')
report={'sourceFrames':len(source),'pairedFrames':sum(map(len,paired.values())),'sourceSha256':hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),'shellSha256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'sourceIndicesComplete':True,'interactMs':sum(times),'inspectMs':sum(fulltimes),'gifMs':sum(dur),'exactIdleEndpoints':True,'bodyTranslations':[0,0],'shellAngle':0,'productionInstalled':False,'tracking':tracking,'limits':['Existing accepted East common-shell fitting method reused; all-head/source-to-shell review required.','No runtime/native selection. Current sealed-meal substitutes still point to old East diagnostic source.','Package source is complete; numeric bounds and clocks do not prove all anatomy, tool identity or native behavior.']}
(P/'paired-candidate-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['tracking','limits']}))
