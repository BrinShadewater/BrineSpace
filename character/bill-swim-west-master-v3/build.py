"""Six authored whole poses, fixed source density and explicit head registration."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
master=R/'crew-side-masters-v1/bill-side-master-01.png';donor=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
jobs=[('Extend',P/'sources/extend-controls-v3.png',[280,170,490,420]),('Sweep',R/'bill-swim-west-master-v2/sources/stroke-sweep-identity-v2.png',[250,170,480,420]),('Pull',P/'sources/pull-head-v3.png',[110,170,360,450]),('Recover',P/'sources/recover-v1.png',[210,170,420,410]),('Reach',P/'sources/reach-v1.png',[280,170,490,410]),('Glide',P/'sources/glide-v1.png',[280,170,490,420])]
inputs=[master,donor,P/'build.py',P/'generation-jobs.json',R/'bill-land-water-west-v9/sources/master-head-reference.png',R/'bill-swim-west-master-v2/sources/stroke-extend-v1.png',R/'bill-swim-west-master-v2/sources/stroke-sweep-identity-v2.png',R/'bill-swim-west-master-v2/sources/stroke-sweep-identity-prompt-v2.txt',R/'bill-land-water-west-v11/bare/frames/land-swim-west/005.png',R/'bill-land-water-west-v11/helmet/frames/land-swim-west/005.png']+[f for f in (P/'sources').iterdir() if f.is_file()]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
density=148/956
def head_bounds(im,roi):
    x0,y0,x1,y1=roi;c=np.array(im)[y0:y1,x0:x1];rgb=c[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    mask=(c[:,:,3]>180)&(r>=40)&(r<=160)&(r>g*1.15)&(g>b*1.2);lab,_=label(mask);counts=np.bincount(lab.ravel());part=lab==np.argmax(counts[1:])+1;y,x=np.where(part)
    bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
    assert bounds[0]>0 and bounds[1]>0 and bounds[2]<c.shape[1] and bounds[3]<c.shape[0],(roi,bounds)
    axis=int(np.median(x[y<y.min()+5]))+x0;top=int(y.min())+y0
    return dict(roi=roi,bounds=bounds,width=bounds[2]-bounds[0],height=bounds[3]-bounds[1],componentTouchesROIEdge=False,sourceCrown=[axis,top],scope='Bounded brown head proxy, not complete anatomical acceptance.')
head=Image.open(donor).convert('RGBA');assert head.size==(40,40)
frames={'bare':[],'helmet':[]};records=[]
for i,(name,path,roi) in enumerate(jobs):
    raw=Image.open(path).convert('RGBA');assert raw.size==(1536,1024)
    bounds=head_bounds(raw,roi)
    anchor=bounds
    if i==2:anchor=head_bounds(Image.open(P/'sources/pull-v2.png').convert('RGBA'),roi)
    axis,top=anchor['sourceCrown'];shift=(134-round(axis*density),200-round(top*density))
    a=np.array(raw);lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
    small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
    bare=Image.new('RGBA',(352,320));bare.alpha_composite(small,shift)
    assert np.count_nonzero(np.array(bare)[:,:,3])==np.count_nonzero(np.array(small)[:,:,3]),name
    x=round(bounds['sourceCrown'][0]*density)+shift[0];y=round(bounds['sourceCrown'][1]*density)+shift[1]
    b=np.array(bare);yy,xx=np.indices(b.shape[:2]);pos=(x-15,y-4);poly=[(x-17,y-3),(x+18,y-3),(x+19,y+23),(x+8,y+33),(x-17,y+33),(x-18,y+22)]
    erase=Image.new('L',bare.size);ImageDraw.Draw(erase).polygon(poly,fill=255);e=np.array(erase)>0
    body=b.copy();body[e]=0;helmet=Image.fromarray(body);helmet.alpha_composite(head,pos);h=np.array(helmet)
    fg=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(b[:,:,3]>0);h[fg]=b[fg]
    area=Image.new('L',bare.size);area.paste(head.getchannel('A'),pos);allowed=e|(np.array(area)>0)
    assert np.array_equal(h[~allowed],b[~allowed]) and np.array_equal(h[fg],b[fg]) and np.array_equal(h[yy>=pos[1]+40],b[yy>=pos[1]+40])
    frames['bare'].append(bare);frames['helmet'].append(Image.fromarray(h))
    records.append(dict(index=i,name=name,source=path.relative_to(R).as_posix(),headProxy=bounds,translation=shift,registeredCrown=[x,y],anchorScope='Prior pull2 whole-source translation retained after head shrink' if i==2 else 'Whole-figure translation from bounded head crown',canonicalHelmetPosition=pos,helmetSize=[40,40],helmetScale=1,helmetRotationDegrees=0,bodyOutsideFittingMaskExact=True,foregroundExact=True,allPaintedSupportPreserved=True))
for gear,bank in frames.items():
    files=[]
    for i,im in enumerate(bank):
        dest=P/gear/f'frames/swim-west/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files.append(dest.relative_to(P/gear).as_posix())
    manifest=dict(name='Bill West original-master six-phase swim candidate',frameWidth=352,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,status='source_candidate_unselected',strideDistanceCells={'swim':.16},states=[dict(id='swim-west',frameFiles=files,frameDurationsMs=[160]*6,loop=True,facings=['west']*6,waterKinds=['swim']*6,waterPoses=[True]*6,depthOffsets=[0]*6,provenance='Six complete authored poses, original148/956 density. New master stroke candidate, not normal runtime admission or visual acceptance.')])
    if gear=='helmet':manifest['equipment']='diving-helmet'
    (P/gear/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    bank[0].save(P/gear/'source-swim.png',save_all=True,append_images=bank[1:],duration=[160]*6,loop=0,disposal=0,blend=0)
    with Image.open(P/gear/'source-swim.png') as ap:
        assert ap.n_frames==6 and ap.info['loop']==0
        for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==160
original=Image.open(master).convert('RGBA').crop((850,0,1280,1024));small=original.resize((round(original.width*density),round(original.height*density)),Image.Resampling.LANCZOS);reference=Image.new('RGBA',(352,320));reference.alpha_composite(small,(125,round(224-977*density)))
board=Image.new('RGB',(2464,720),'#182932');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for col,(title,im) in enumerate([('Original bare master',reference)]+[(records[i]['name'],im) for i,im in enumerate(frames[gear])]):
        board.paste(im,(col*352,row*360+25),im);d.text((col*352+4,row*360+4),gear+' /'+title,fill='white')
board.save(P/'full-stroke-review.png')
detail=Image.new('RGB',(2400,700),'#182932');d=ImageDraw.Draw(detail)
for row,gear in enumerate(['bare','helmet']):
    for i,(im,rec) in enumerate(zip(frames[gear],records)):
        x,y=rec['registeredCrown'];crop=im.crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST);detail.paste(crop,(i*400,row*350+30),crop);d.text((i*400+5,row*350+5),gear+' '+rec['name']+' /same4x',fill='white')
detail.save(P/'neck-review.png')
join=Image.new('RGB',(1408,720),'#182932');d=ImageDraw.Draw(join)
for row,gear in enumerate(['bare','helmet']):
    near=Image.open(R/f'bill-land-water-west-v11/{gear}/frames/land-swim-west/005.png').convert('RGBA')
    for col,(title,im) in enumerate([('V11 entry near-prone',near),('Extend0',frames[gear][0]),('Glide5',frames[gear][5]),('Wrap to extend0',frames[gear][0])]):
        join.paste(im,(col*352,row*360+25),im);d.text((col*352+4,row*360+4),gear+' /'+title,fill='white')
join.save(P/'entry-wrap-review.png')
after={f.relative_to(R).as_posix():sha(f) for f in inputs};assert before==after
review=dict(scope='Full six-phase source candidate, not native/visual acceptance.',inputSHA256=before,frozenInputsStable=len(before),density=density,physicalStandingHeight=148,canvas=[352,320],pivot=[160,224],frames=records,decodedAPNGFramesExact=12,loopMs=960,APNGLoop=0,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending complete master/body/head/grade/neck/wrap review')
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill West master swim loop</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}section{display:flex;gap:20px}canvas{background:#14242e;max-width:45vw}img{width:100%;max-width:1600px;display:block;margin:20px 0}button,select{font:inherit;margin:12px 6px}</style><h1>Bill  west master swim loop study</h1><p>Six authored phases, bare and helmeted. Original body, grade, smoothness and native moving acceptance remain pending.</p><section><div>Bare<br><canvas id="bare" width="352" height="320"></canvas></div><div>Helmet<br><canvas id="helmet" width="352" height="320"></canvas></div></section><button id="play">Play</button><button id="prev">Previous pose</button><button id="next">Next pose</button><select id="speed"><option value="1">Normal speed</option><option value=".25">Quarter speed</option></select><span id="status"></span><h2>Master and complete stroke</h2><img src="full-stroke-review.png"><h2>Head and collar</h2><img src="neck-review.png"><h2>Entry and loop wrap</h2><img src="entry-wrap-review.png"><script>const names=['Extend','Sweep','Pull','Recover','Reach','Glide'],banks={},ctx={};let phase=0,playing=false,last=0,time=0;function draw(){for(const g of ['bare','helmet']){ctx[g].clearRect(0,0,352,320);ctx[g].drawImage(banks[g][phase],0,0)}document.querySelector('#status').textContent=names[phase]+'  pose '+(phase+1)+' of 6'}Promise.all(['bare','helmet'].map(async g=>{ctx[g]=document.querySelector('#'+g).getContext('2d');banks[g]=await Promise.all(names.map((_,i)=>new Promise(resolve=>{const im=new Image;im.onload=()=>resolve(im);im.src=g+'/frames/swim-west/'+String(i).padStart(3,'0')+'.png'})))})).then(draw);document.querySelector('#play').onclick=()=>{playing=!playing;last=performance.now();document.querySelector('#play').textContent=playing?'Pause':'Play'};function step(delta){playing=false;document.querySelector('#play').textContent='Play';phase=(phase+delta+6)%6;time=phase*160;draw()}document.querySelector('#next').onclick=()=>step(1);document.querySelector('#prev').onclick=()=>step(-1);function tick(now){if(playing){time=(time+(now-last)*Number(document.querySelector('#speed').value))%960;phase=Math.floor(time/160);draw()}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),decodedFrames=12,ms=960,headProxies=[(r['name'],r['headProxy']['width'],r['headProxy']['height']) for r in records])))
