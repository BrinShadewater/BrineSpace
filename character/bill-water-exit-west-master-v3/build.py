"""Package five independent West exit interiors at original density; no pose-size fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,ast
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent;V=R/'bill-swim-west-master-v7';OLD=R/'bill-water-exit-west-v1';LOW=R/'bill-water-exit-west-master-v2'
helper=V/'prepare_body.py';module=ast.parse(helper.read_text(encoding='utf-8'))
for node in module.body:
 if isinstance(node,ast.FunctionDef) and node.name=='head_bounds':exec(compile(ast.Module(body=[node],type_ignores=[]),str(helper),'exec'))
headPath=R/'bill-swim-west-master-v6/sources/canonical-bare-head-v1.png';helmetPath=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
jobs=[('Low elbow',LOW/'sources/low-elbow-controls-v2.png',[100,170,370,450],134),('Palm push',P/'sources/palm-push-master-v1.png',[50,80,350,440],134),('Knee tuck',P/'sources/knee-tuck-original-v2.png',[150,50,500,420],140),('Half kneel',P/'sources/half-kneel-master-v1.png',[350,10,670,300],150),('Rise',P/'sources/rise-master-v1.png',[500,10,760,260],157)]
inputs=[Path(__file__),helper,headPath,helmetPath,R/'crew-side-masters-v1/bill-side-master-01.png',P/'generation-jobs.json',P/'generation-provenance.json',LOW/'review.json',LOW/'control-provenance.json']+[raw for _,raw,_,_ in jobs]+[P/f'sources/{name}-master-prompt-v1.txt' for name in ['palm-push','knee-tuck','half-kneel','rise']]+[OLD/f'sources/{name}-canvas-v{2 if name=="rise" else 1}.png' for name in ['palm-push','knee-tuck','half-kneel','rise']]+[V/g/'frames/swim-west/000.png' for g in ['bare','helmet']]+[OLD/g/'frames/swim-land-west/006.png' for g in ['bare','helmet']]+[OLD/g/f'frames/swim-land-west/{i:03}.png' for g in ['bare','helmet'] for i in range(1,6)]
inputs += [P/'sources/knee-tuck-master-v1.png',P/'sources/knee-tuck-original-prompt-v2.txt',P/'knee-repair-job.json',P/'knee-repair-provenance.json',R/'bill-land-water-west-v9/sources/master-head-reference.png',P/'before-knee-refinement.json']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();before={f.relative_to(R).as_posix():sha(f) for f in inputs}
interiors={'bare':[],'helmet':[]};records=[]
for name,rawPath,roi,headX in jobs:
 raw=Image.open(rawPath).convert('RGBA');assert raw.size==(1536,1024)
 rec=head_bounds(raw,roi);density=148/956
 opaque=np.array(raw)[:,:,3]>180
 contact=int(np.where(opaque)[0].max())+1
 shift=(headX-round(rec['sourceCrown'][0]*density),224-round(contact*density))
 a=np.array(raw);labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel());keep=binary_dilation(labs==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
 small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
 body=Image.new('RGBA',(352,320));body.alpha_composite(small,shift)
 assert np.count_nonzero(np.array(body)[:,:,3])==np.count_nonzero(np.array(small)[:,:,3])
 x=round(rec['sourceCrown'][0]*density)+shift[0];y=round(rec['sourceCrown'][1]*density)+shift[1]
 b=np.array(body);yy,xx=np.indices(b.shape[:2]);donor=Image.open(headPath).convert('RGBA');assert donor.size==(21,23)
 headDepth=round(rec['height']*density);position=(x-6,y+headDepth-23);polygon=[(x-30,y-3),(x+25,y-3),(x+25,y+11),(x+5,y+headDepth+5),(x-30,y+headDepth+5)]
 mask=Image.new('L',body.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);erase=np.array(mask)>0
 clean=b.copy();clean[erase]=0;bare=Image.fromarray(clean);bare.alpha_composite(donor,position);ba=np.array(bare)
 rgb=b[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 fg=(yy>=y+11)&(xx>=x+2)&(b[:,:,3]>0)&(gg>=rr*.8)&(bb>=rr*.8)&(rgb.mean(axis=2)>30)&erase
 ba[fg]=b[fg];area=Image.new('L',body.size);area.paste(donor.getchannel('A'),position);allowed=erase|(np.array(area)>0)
 assert np.array_equal(ba[~allowed],b[~allowed]) and np.array_equal(ba[fg],b[fg]) and np.array_equal(ba[yy>=y+headDepth+7],b[yy>=y+headDepth+7])
 opaque=np.array(donor)[:,:,3]==255;local=ba[position[1]:position[1]+23,position[0]:position[0]+21];lfg=fg[position[1]:position[1]+23,position[0]:position[0]+21]
 assert np.array_equal(local[opaque&~lfg],np.array(donor)[opaque&~lfg])
 ll,_=label(ba[:,:,3]>180);cc=np.bincount(ll.ravel());assert np.count_nonzero(cc[1:]>40)==1
 bare=Image.fromarray(ba)
 helmetDonor=Image.open(helmetPath).convert('RGBA');assert helmetDonor.size==(40,40)
 hpos=(x-15,y+headDepth-36);hpoly=polygon
 hmask=Image.new('L',body.size);ImageDraw.Draw(hmask).polygon(hpoly,fill=255);he=np.array(hmask)>0
 clean=b.copy();clean[he]=0;helmet=Image.fromarray(clean);helmet.alpha_composite(helmetDonor,hpos);ha=np.array(helmet)
 hfg=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(b[:,:,3]>0);hfg &= (~he)|((gg>=rr*.8)&(bb>=rr*.8))
 ha[hfg]=b[hfg]
 harea=Image.new('L',body.size);harea.paste(helmetDonor.getchannel('A'),hpos);hallowed=he|(np.array(harea)>0)
 assert np.array_equal(ha[~hallowed],b[~hallowed]) and np.array_equal(ha[hfg],b[hfg]) and np.array_equal(ha[yy>=max(hpos[1]+40,y+headDepth+7)],b[yy>=max(hpos[1]+40,y+headDepth+7)])
 helmet=Image.fromarray(ha)
 interiors['bare'].append(bare);interiors['helmet'].append(helmet)
 records.append(dict(name=name,source=rawPath.relative_to(R).as_posix(),headProxy=rec,translation=shift,crown=[x,y],bareDonorPosition=position,helmetDonorPosition=hpos,erasePolygon=polygon,sourceLowestPaintedSupport=contact,registeredSupport=224,physicalContactAccepted=False,bareDonorSize=[21,23],helmetDonorSize=[40,40],donorScale=1,donorRotation=0,bodyOutsideHeadRegionsExact=True,foregroundExact=True,belowHeadRegionExact=True,opaqueBareDonorExact=True))
names=['Swimming']+[r['name'] for r in records]+['Standing'];durations=[60,50,60,70,100,100,60];assert sum(durations)==500
banks={};endpointExact=0
for g in ['bare','helmet']:
 first=Image.open(V/g/'frames/swim-west/000.png').convert('RGBA');standing=Image.open(OLD/g/'frames/swim-land-west/006.png').convert('RGBA');last=Image.new('RGBA',(352,320));last.alpha_composite(standing,(0,0))
 bank=[first]+interiors[g]+[last];banks[g]=bank
 assert first.tobytes()==Image.open(V/g/'frames/swim-west/000.png').convert('RGBA').tobytes();assert last.crop((0,0,320,320)).tobytes()==standing.tobytes();endpointExact+=2
 files=[]
 for i,im in enumerate(bank):
  dest=P/g/f'frames/swim-land-west/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files.append(dest.relative_to(P/g).as_posix())
 manifest=dict(name='Bill West complete master exit candidate',status='source_candidate_unselected',frameWidth=352,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,states=[dict(id='swim-land-west',frameFiles=files,frameDurationsMs=durations,loop=False,facings=['west']*7,provenance='Five independently authored whole-body interiors at148/956; shared calibrated heads. Full sequence candidate, master/contact/motion acceptance pending.')])
 if g=='helmet':manifest['equipment']='diving-helmet'
 (P/g/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 bank[0].save(P/g/'source-leave.png',save_all=True,append_images=bank[1:],duration=durations,loop=1,disposal=0,blend=0)
 with Image.open(P/g/'source-leave.png') as ap:
  assert ap.n_frames==7 and ap.info['loop']==1
  for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i]
board=Image.new('RGB',(2464,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 for i,im in enumerate(banks[g]):board.paste(im,(i*352,row*360+25),im);d.text((i*352+4,row*360+4),g+' / '+names[i],fill='white')
board.save(P/'full-exit-review.png')
neck=Image.new('RGB',(2000,700),'#182932');d=ImageDraw.Draw(neck)
for row,g in enumerate(['bare','helmet']):
 for i,rec in enumerate(records):
  x,y=rec['crown'];im=banks[g][i+1];crop=im.crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST);neck.paste(crop,(i*400,row*350+30),crop);d.text((i*400+4,row*350+4),g+' / '+rec['name'],fill='white')
neck.save(P/'neck-review.png')
comparison=Image.new('RGB',(1760,1440),'#182932');d=ImageDraw.Draw(comparison)
for row,g in enumerate(['bare','helmet']):
 for i,rec in enumerate(records):
  old=Image.open(OLD/g/f'frames/swim-land-west/{i+1:03}.png').convert('RGBA');new=banks[g][i+1]
  comparison.paste(old,(i*352,row*720+25),old);comparison.paste(new,(i*352,row*720+385),new);d.text((i*352+4,row*720+4),g+' prior / '+rec['name'],fill='white');d.text((i*352+4,row*720+364),g+' new / '+rec['name'],fill='white')
comparison.save(P/'prior-comparison.png')
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA').crop((850,0,1280,1024));density=148/956;master=master.resize((round(master.width*density),round(master.height*density)),Image.Resampling.LANCZOS);ref=Image.new('RGBA',(352,320));ref.alpha_composite(master,(125,round(224-977*density)))
mb=Image.new('RGB',(1408,360),'#182932');d=ImageDraw.Draw(mb)
for i,(title,im) in enumerate([('Original master',ref),('New knee tuck',banks['bare'][3]),('New half kneel',banks['bare'][4]),('New rise',banks['bare'][5])]):mb.paste(im,(i*352,25),im);d.text((i*352+4,4),title,fill='white')
mb.save(P/'master-build-review.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
review=dict(inputSHA256=before,frozenInputsStable=len(before),frames=records,decodedAPNGFramesExact=14,endpointChecksExact=endpointExact,durationsMs=durations,totalMs=500,APNGLoop=1,canvas=[352,320],pivot=[160,224],standingHeight=148,bodyDensity=148/956,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending full master/build/grade/collar/contact/moving review; generated head component proxy does not prove body dimensions.')
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill West master exit candidate</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}section{display:flex;gap:20px}canvas{background:#14242e;max-width:45vw}img{width:100%;max-width:1600px;display:block;margin:20px 0}button{font:inherit;margin:12px 6px}</style><h1>Bill west - complete exit candidate</h1><p>Five independently authored exit poses, bare and helmeted. Original proportions, grade, floor contact and in-game motion remain under review.</p><section><div>Bare<br><canvas id="bare" width="352" height="320"></canvas></div><div>Helmet<br><canvas id="helmet" width="352" height="320"></canvas></div></section><button id="play">Play exit</button><button id="prev">Previous pose</button><button id="next">Next pose</button><span id="status"></span><h2>Complete exit</h2><img src="full-exit-review.png"><h2>Original master and build</h2><img src="master-build-review.png"><h2>Head and collar</h2><img src="neck-review.png"><h2>Previous and new poses</h2><img src="prior-comparison.png"><script>const names=[\'Swimming\',\'Low elbow\',\'Palm push\',\'Knee tuck\',\'Half kneel\',\'Rise\',\'Standing\'],starts=[0,60,110,170,240,340,440],banks={},ctx={};let phase=0,playing=false,last=0,time=0;function draw(){for(const g of [\'bare\',\'helmet\']){ctx[g].clearRect(0,0,352,320);ctx[g].drawImage(banks[g][phase],0,0)}document.querySelector(\'#status\').textContent=names[phase]+\' /pose \'+(phase+1)+\' of 7\'}Promise.all([\'bare\',\'helmet\'].map(async g=>{ctx[g]=document.querySelector(\'#\'+g).getContext(\'2d\');banks[g]=await Promise.all(names.map((_,i)=>new Promise(resolve=>{const im=new Image;im.onload=()=>resolve(im);im.src=g+\'/frames/swim-land-west/\'+String(i).padStart(3,\'0\')+\'.png\'})))})).then(draw);document.querySelector(\'#play\').onclick=()=>{playing=!playing;if(playing){time=0;phase=0;last=performance.now()}document.querySelector(\'#play\').textContent=playing?\'Pause\':\'Play exit\';draw()};function step(delta){playing=false;document.querySelector(\'#play\').textContent=\'Play exit\';phase=Math.max(0,Math.min(6,phase+delta));time=starts[phase];draw()}document.querySelector(\'#next\').onclick=()=>step(1);document.querySelector(\'#prev\').onclick=()=>step(-1);function tick(now){if(playing){time=Math.min(500,time+now-last);phase=starts.filter(t=>t<=time).length-1;if(time>=500){playing=false;document.querySelector(\'#play\').textContent=\'Play exit\'}draw()}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'
(P/'index.html').write_text(html,encoding='utf-8');print(json.dumps(dict(inputs=len(before),APNGExact=14,ms=500,heads=[(r['name'],r['headProxy']['width'],r['headProxy']['height']) for r in records])))
