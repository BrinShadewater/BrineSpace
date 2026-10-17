"""Pack authored gather with existing calibrated heads; preserve all six V7 poses."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,ast
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent;V=R/'bill-swim-west-master-v7'
helper=V/'prepare_body.py'
# Reuse the inspected technical landmark detectors without executing another bank build.
module=ast.parse(helper.read_text(encoding='utf-8'))
for node in module.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['head_bounds','hip_marker']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(helper),'exec'))
rawPath=P/'sources/low-elbow-controls-v2.png'
headPath=R/'bill-swim-west-master-v6/sources/canonical-bare-head-v1.png'
helmetPath=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
inputs=[Path(__file__),helper,rawPath,headPath,helmetPath,P/'sources/low-elbow-controls-prompt-v2.txt',P/'control-provenance.json',V/'review.json']+[V/g/'manifest.json' for g in ['bare','helmet']]+[V/g/f'frames/swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(6)]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs += [R/'crew-side-masters-v1/bill-side-master-01.png',R/'bill-swim-west-master-v3/sources/master-control-reference.png',R/'bill-water-exit-west-v1/sources/low-elbow-canvas-v2.png',P/'sources/low-elbow-master-v1.png',P/'sources/low-elbow-master-prompt-v1.txt',P/'generation-job.json',P/'generation-provenance.json',P/'control-job.json']
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
raw=Image.open(rawPath).convert('RGBA');assert raw.size==(1536,1024)
rec=head_bounds(raw,[100,170,370,450]);density=148/956
opaque=np.array(raw)[:,:,3]>180
contact=int(np.where(opaque)[0].max())+1
shift=(134-round(rec['sourceCrown'][0]*density),224-round(contact*density))
a=np.array(raw);labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel());keep=binary_dilation(labs==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
body=Image.new('RGBA',(352,320));body.alpha_composite(small,shift)
assert np.count_nonzero(np.array(body)[:,:,3])==np.count_nonzero(np.array(small)[:,:,3])
x=round(rec['sourceCrown'][0]*density)+shift[0];y=round(rec['sourceCrown'][1]*density)+shift[1]
b=np.array(body);yy,xx=np.indices(b.shape[:2]);donor=Image.open(headPath).convert('RGBA');assert donor.size==(21,23)
position=(x-6,y+7);polygon=[(x-25,y-3),(x+18,y-3),(x+18,y+11),(x+3,y+35),(x-25,y+35)]
mask=Image.new('L',body.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);erase=np.array(mask)>0
clean=b.copy();clean[erase]=0;bare=Image.fromarray(clean);bare.alpha_composite(donor,position);ba=np.array(bare)
rgb=b[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
fg=(yy>=y+11)&(xx>=x+2)&(b[:,:,3]>0)&(gg>=rr*.8)&(bb>=rr*.8)&(rgb.mean(axis=2)>30)&erase
ba[fg]=b[fg];area=Image.new('L',body.size);area.paste(donor.getchannel('A'),position);allowed=erase|(np.array(area)>0)
assert np.array_equal(ba[~allowed],b[~allowed]) and np.array_equal(ba[fg],b[fg]) and np.array_equal(ba[yy>=y+37],b[yy>=y+37])
opaque=np.array(donor)[:,:,3]==255;local=ba[position[1]:position[1]+23,position[0]:position[0]+21];lfg=fg[position[1]:position[1]+23,position[0]:position[0]+21]
assert np.array_equal(local[opaque&~lfg],np.array(donor)[opaque&~lfg])
ll,_=label(ba[:,:,3]>180);cc=np.bincount(ll.ravel());assert np.count_nonzero(cc[1:]>40)==1
bare=Image.fromarray(ba)
helmetDonor=Image.open(helmetPath).convert('RGBA');assert helmetDonor.size==(40,40)
hpos=(x-15,y-4);hpoly=[(x-17,y-3),(x+18,y-3),(x+19,y+23),(x+8,y+33),(x-17,y+33),(x-18,y+22)]
hmask=Image.new('L',body.size);ImageDraw.Draw(hmask).polygon(hpoly,fill=255);he=np.array(hmask)>0
clean=b.copy();clean[he]=0;helmet=Image.fromarray(clean);helmet.alpha_composite(helmetDonor,hpos);ha=np.array(helmet)
hfg=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(b[:,:,3]>0);ha[hfg]=b[hfg]
harea=Image.new('L',body.size);harea.paste(helmetDonor.getchannel('A'),hpos);hallowed=he|(np.array(harea)>0)
assert np.array_equal(ha[~hallowed],b[~hallowed]) and np.array_equal(ha[hfg],b[hfg]) and np.array_equal(ha[yy>=hpos[1]+40],b[yy>=hpos[1]+40])
helmet=Image.fromarray(ha)
names=['Swimming context','Low elbow'];durations=[60,50];banks={}
for g,new in [('bare',bare),('helmet',helmet)]:
 bank=[Image.open(V/g/'frames/swim-west/000.png').convert('RGBA'),new];banks[g]=bank;files=[]
 for i,im in enumerate(bank):
  dest=P/g/f'frames/swim-land-west/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files.append(dest.relative_to(P/g).as_posix())
 m=dict(name='Bill West original-master low-elbow exit study',status='partial_source_candidate_unselected',frameWidth=352,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,states=[dict(id='swim-land-west',frameFiles=files,frameDurationsMs=durations,loop=False,facings=['west']*2,provenance='Two-pose partial exit study only. Independently authored low elbow at original148/956 density, fixed calibrated head components. Not full exit or normal adoption.')])
 if g=='helmet':m['equipment']='diving-helmet'
 (P/g/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 bank[0].save(P/g/'source-leave.png',save_all=True,append_images=bank[1:],duration=durations,loop=1,disposal=0,blend=0)
 with Image.open(P/g/'source-leave.png') as ap:
  assert ap.n_frames==2 and ap.info['loop']==1
  for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i]
board=Image.new('RGB',(1408,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 old=Image.open(R/f'bill-water-exit-west-v1/{g}/frames/swim-land-west/001.png').convert('RGBA')
 nextOld=Image.open(R/f'bill-water-exit-west-v1/{g}/frames/swim-land-west/002.png').convert('RGBA')
 for i,(title,im) in enumerate([('New swimmer',banks[g][0]),('Old low elbow',old),('New low elbow',banks[g][1]),('Old next palm push /pending',nextOld)]):
  board.paste(im,(i*352,row*360+25),im);d.text((i*352+5,row*360+5),g+' / '+title,fill='white')
board.save(P/'master-exit-review.png')
neck=Image.new('RGB',(800,340),'#182932');d=ImageDraw.Draw(neck)
for i,(g,im) in enumerate([('bare',bare),('helmet',helmet)]):
 crop=im.crop((x-45,y-10,x+55,y+75)).resize((400,340),Image.Resampling.NEAREST);neck.paste(crop,(i*400,0),crop);d.text((i*400+4,4),g+' Low elbow /same4x',fill='white')
neck.save(P/'neck-review.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
report=dict(inputSHA256=before,frozenInputsStable=len(before),decodedAPNGFramesExact=4,durationsMs=durations,totalMs=110,APNGLoop=1,canvas=[352,320],pivot=[160,224],standingHeight=148,density=density,translation=shift,sourceHeadProxy=rec,registeredCrown=[x,y],sourceLowestOpaqueSupport=contact,registeredLowestOpaqueSupport=224,bareDonor=[21,23],bareDonorPosition=position,bareErasePolygon=polygon,bareBelowProtectedRow=y+37,helmetDonor=[40,40],bodyOutsideHeadRegionsProtected=True,foregroundProtected=True,normalSelected=False,nativeAcceptance=False,visualAcceptance='Partial two-pose source study only; master anatomy/material/contact/next-phase and moving acceptance pending. Lowest painted support is not proof both palms/toes share physical contact.')
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill West low-elbow exit study</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}section{display:flex;gap:20px}canvas{background:#14242e;max-width:45vw}img{width:100%;max-width:1600px;display:block;margin:20px 0}button{font:inherit;margin:12px 6px}</style><h1>Bill west - first exit pose</h1><p>Two-pose study: the revised swimmer and an independently authored low-elbow support pose. Remaining exit poses, floor contact and full motion still need review.</p><section><div>Bare<br><canvas id="bare" width="352" height="320"></canvas></div><div>Helmet<br><canvas id="helmet" width="352" height="320"></canvas></div></section><button id="prev">Swimming</button><button id="next">Low elbow</button><span id="status"></span><h2>Master-scale exit comparison</h2><img src="master-exit-review.png"><h2>Head and collar</h2><img src="neck-review.png"><script>const names=[\'Swimming context\',\'Low elbow\'],banks={},ctx={};let phase=0;function draw(){for(const g of [\'bare\',\'helmet\']){ctx[g].clearRect(0,0,352,320);ctx[g].drawImage(banks[g][phase],0,0)}document.querySelector(\'#status\').textContent=names[phase]+\' /pose \'+(phase+1)+\' of 2\'}Promise.all([\'bare\',\'helmet\'].map(async g=>{ctx[g]=document.querySelector(\'#\'+g).getContext(\'2d\');banks[g]=await Promise.all(names.map((_,i)=>new Promise(resolve=>{const im=new Image;im.onload=()=>resolve(im);im.src=g+\'/frames/swim-land-west/\'+String(i).padStart(3,\'0\')+\'.png\'})))})).then(draw);document.querySelector(\'#prev\').onclick=()=>{phase=0;draw()};document.querySelector(\'#next\').onclick=()=>{phase=1;draw()};</script>'
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),APNGDecodedExact=4,ms=110,headProxy=[rec['width'],rec['height']],crown=[x,y],translation=shift)))
