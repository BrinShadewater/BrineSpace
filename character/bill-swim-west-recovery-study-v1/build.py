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
rawPath=P/'sources/recover-from-pull-v1.png'
headPath=R/'bill-swim-west-master-v6/sources/canonical-bare-head-v1.png'
helmetPath=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
inputs=[Path(__file__),helper,rawPath,headPath,helmetPath,P/'sources/recover-from-pull-prompt-v1.txt',P/'generation-provenance.json',V/'review.json']+[V/g/'manifest.json' for g in ['bare','helmet']]+[V/g/f'frames/swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(6)]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
raw=Image.open(rawPath).convert('RGBA');assert raw.size==(1536,1024)
rec=head_bounds(raw,[100,170,370,450]);marker=hip_marker(raw);mx,my=marker['sourceCenter'];density=148/956
shift=(192-round(mx*density),237-round(my*density))
a=np.array(raw);labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel());keep=binary_dilation(labs==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
body=Image.new('RGBA',(352,320));body.alpha_composite(small,shift)
assert np.count_nonzero(np.array(body)[:,:,3])==np.count_nonzero(np.array(small)[:,:,3])
x=round(rec['sourceCrown'][0]*density)+shift[0];y=round(rec['sourceCrown'][1]*density)+shift[1]
b=np.array(body);yy,xx=np.indices(b.shape[:2]);donor=Image.open(headPath).convert('RGBA');assert donor.size==(21,23)
position=(x-7,y+4);polygon=[(x-18,y-3),(x+18,y-3),(x+18,y+8),(x+3,y+25),(x-18,y+25)]
mask=Image.new('L',body.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);erase=np.array(mask)>0
clean=b.copy();clean[erase]=0;bare=Image.fromarray(clean);bare.alpha_composite(donor,position);ba=np.array(bare)
rgb=b[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
fg=(yy>=y+11)&(xx>=x+2)&(b[:,:,3]>0)&(gg>=rr*.8)&(bb>=rr*.8)&(rgb.mean(axis=2)>30)&erase
ba[fg]=b[fg];area=Image.new('L',body.size);area.paste(donor.getchannel('A'),position);allowed=erase|(np.array(area)>0)
assert np.array_equal(ba[~allowed],b[~allowed]) and np.array_equal(ba[fg],b[fg]) and np.array_equal(ba[yy>=y+27],b[yy>=y+27])
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
names=['Extend','Sweep','Pull','Gather','Recover','Reach','Glide'];durations=[160,160,80,80,160,160,160];assert sum(durations)==960
banks={};exact=0
for g,new in [('bare',bare),('helmet',helmet)]:
 bank=[Image.open(V/g/f'frames/swim-west/{i:03}.png').convert('RGBA') for i in range(6)];bank.insert(3,new);banks[g]=bank;files=[]
 for i,im in enumerate(bank):
  dest=P/g/f'frames/swim-west/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files.append(dest.relative_to(P/g).as_posix())
  if i!=3:
   prior=i if i<3 else i-1;assert im.tobytes()==Image.open(V/g/f'frames/swim-west/{prior:03}.png').convert('RGBA').tobytes();exact+=1
 m=json.loads((V/g/'manifest.json').read_text(encoding='utf-8'));m['name']='Bill West gathered recovery timing study';s=m['states'][0];s.update(frameFiles=files,frameDurationsMs=durations,facings=['west']*7,waterKinds=['swim']*7,waterPoses=[True]*7,depthOffsets=[0]*7,provenance='Six V7 poses exact plus one authored compact gather. Fixed body density and calibrated donors. Provisional chronology, not normal selection.')
 (P/g/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 bank[0].save(P/g/'source-swim.png',save_all=True,append_images=bank[1:],duration=durations,loop=0,disposal=0,blend=0)
 with Image.open(P/g/'source-swim.png') as ap:
  assert ap.n_frames==7 and ap.info['loop']==0
  for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i]
board=Image.new('RGB',(2464,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 for i,im in enumerate(banks[g]):board.paste(im,(i*352,row*360+25),im);d.text((i*352+5,row*360+5),g+' / '+names[i],fill='white')
board.save(P/'paired-stroke-review.png')
neck=Image.new('RGB',(800,340),'#182932');d=ImageDraw.Draw(neck)
for i,(g,im) in enumerate([('bare',bare),('helmet',helmet)]):
 crop=im.crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST);neck.paste(crop,(i*400,30),crop);d.text((i*400+4,4),g+' Gather / same4x',fill='white')
neck.save(P/'gather-neck-review.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
report=dict(inputSHA256=before,frozenInputsStable=len(before),priorV7DecodedFramesExact=exact,decodedAPNGFramesExact=14,durationsMs=durations,loopMs=960,APNGLoop=0,canvas=[352,320],pivot=[160,224],standingHeight=148,density=density,translation=shift,sourceHeadProxy=rec,registeredHipMarker=[192,237],registeredCrown=[x,y],bareDonor=[21,23],bareDonorPosition=position,bareCollarRegistrationOffset=[4,4],helmetDonor=[40,40],bodyOutsideHeadRegionsProtected=True,foregroundProtected=True,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending master anatomy/material/chronological motion review; only source packing verified.')
(P/'paired-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html=(V/'body-source/index.html').read_text(encoding='utf-8')
html=html.replace('Bill West master swim loop','Bill West gathered recovery study').replace('Bill  west master swim loop study','Bill west - gathered recovery study')
html=html.replace('Six authored phases, bare and helmeted. Original body, grade, smoothness and native moving acceptance remain pending.','Seven phases retain the six matte poses and add a compact hands-gathered beat. Master anatomy, colour and in-game motion remain under review.')
html=html.replace("['Extend','Sweep','Pull','Recover','Reach','Glide']","['Extend','Sweep','Pull','Gather','Recover','Reach','Glide']")
html=html.replace('phase=(phase+delta+6)%6;time=phase*160','phase=(phase+delta+7)%7;time=[0,160,320,400,480,640,800][phase]')
html=html.replace('phase=Math.floor(time/160)','phase=[0,160,320,400,480,640,800].filter(t=>t<=time).length-1').replace("+' of 6'","+' of 7'")
html=html.replace('<h2>Master and complete stroke</h2><img src="full-stroke-review.png">','<h2>Paired seven-phase stroke</h2><img src="paired-stroke-review.png">').replace('neck-review.png','gather-neck-review.png')
html=html.replace('<h2>Entry and loop wrap</h2><img src="entry-wrap-review.png">','<h2>Source chronology</h2><img src="chronology-review.png">')
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),priorFramesExact=exact,APNGDecodedExact=14,loopMs=960,headProxy=[rec['width'],rec['height']],crown=[x,y])))
