"""Package neutral-calibrated knee tuck; preserve seven other poses for explicit mixed-scale comparison."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib,ast
P=Path(__file__).resolve().parent;R=P.parent;PREV=R/'bill-water-exit-west-master-v7'
helper=R/'bill-swim-west-master-v7/prepare_body.py';module=ast.parse(helper.read_text(encoding='utf-8'))
for node in module.body:
 if isinstance(node,ast.FunctionDef) and node.name=='head_bounds':exec(compile(ast.Module(body=[node],type_ignores=[]),str(helper),'exec'))
headPath=R/'bill-swim-west-master-v6/sources/canonical-bare-head-v1.png';helmetPath=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
jobs=[('Knee tuck',P/'sources/knee-tuck-calibrated-v2.png',[700,370,920,590],140)]
inputs=[Path(__file__),helper,PREV/'build.py',headPath,helmetPath,R/'crew-side-masters-v1/bill-side-master-01.png',P/'generation-job-v2.json',P/'generation-provenance-v2.json',P/'sources/knee-tuck-calibrated-prompt-v2.txt',jobs[0][1],R/'bill-water-exit-west-master-v7/sources/palm-push-master-v1.png',R/'bill-water-exit-west-master-v3/sources/knee-tuck-original-v2.png']+[PREV/g/f'frames/swim-land-west/{i:03}.png' for g in ['bare','helmet'] for i in range(8)]+[PREV/g/'manifest.json' for g in ['bare','helmet']]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();before={f.relative_to(R).as_posix():sha(f) for f in inputs}
interiors={'bare':[],'helmet':[]};records=[]
def hip_marker(raw):
 roi=[1020,610,1110,690];x0,y0,x1,y1=roi;a=np.array(raw)[y0:y1,x0:x1];rr,gg,bb=a[:,:,:3].astype(float).transpose(2,0,1)
 mask=(a[:,:,3]>180)&(gg>rr*1.5)&(bb>rr*1.5)&(gg>100)&(bb>100);labs,n=label(mask);parts=[]
 for i in range(1,n+1):
  yy,xx=np.where(labs==i)
  if len(xx)<10:continue
  assert xx.min()>0 and yy.min()>0 and xx.max()<x1-x0-1 and yy.max()<y1-y0-1
  parts.append({'pixels':len(xx),'center':[float(xx.mean()+x0),float(yy.mean()+y0)]})
 assert len(parts)==2;parts.sort(key=lambda r:r['center'][0]);return {'roi':roi,'components':parts,'sourceCenter':np.mean([v['center'] for v in parts],axis=0).tolist(),'scope':'Equipment proxy; not anatomical or floor-contact acceptance'}
for name,rawPath,roi,headX in jobs:
 sheet=Image.open(rawPath).convert('RGBA');assert sheet.size==(1536,1024)
 # One standing calibration sets BOTH figures' whole-source scale; no pose-height fitting.
 sa=np.array(sheet);neutralROI=[130,0,530,1000];actionROI=[620,350,1500,1000]
 nx0,ny0,nx1,ny1=neutralROI;neutralAlpha=sa[ny0:ny1,nx0:nx1,3];nys,nxs=np.where(neutralAlpha>180)
 neutralBounds=[int(nxs.min()+nx0),int(nys.min()+ny0),int(nxs.max()+nx0+1),int(nys.max()+ny0+1)]
 assert min(nxs)>0 and max(nxs)<nx1-nx0-1 and min(nys)>0 and max(nys)<ny1-ny0-1
 neutralHeight=neutralBounds[3]-neutralBounds[1];density=148/neutralHeight
 neutralHead=head_bounds(sheet,[240,0,440,190])
 ax0,ay0,ax1,ay1=actionROI;ays,axs=np.where(sa[ay0:ay1,ax0:ax1,3]>180)
 assert min(axs)>0 and max(axs)<ax1-ax0-1 and min(ays)>0 and max(ays)<ay1-ay0-1
 action=np.zeros_like(sa);action[ay0:ay1,ax0:ax1]=sa[ay0:ay1,ax0:ax1];raw=Image.fromarray(action)
 assert np.array_equal(np.array(raw)[ay0:ay1,ax0:ax1],sa[ay0:ay1,ax0:ax1])
 rec=head_bounds(raw,roi)
 calibration={'neutralROI':neutralROI,'neutralOpaqueBounds':neutralBounds,'neutralHeight':neutralHeight,'neutralHeadProxy':neutralHead,'actionROI':actionROI,'oneWholeSourceScale':density,'neutralFacing':'east/right-facing, calibration only, not accepted West idle','actionFacing':'west','scope':'Shared sheet standing denominator; action anatomy/perspective still visually provisional.'}
 opaque=np.array(raw)[:,:,3]>180
 contact=int(np.where(opaque)[0].max())+1
 marker=hip_marker(raw);shift=(headX-round(rec['sourceCrown'][0]*density),224-round(contact*density))
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
 records.append(dict(name=name,source=rawPath.relative_to(R).as_posix(),headProxy=rec,translation=shift,crown=[x,y],bareDonorPosition=position,helmetDonorPosition=hpos,erasePolygon=polygon,sourceLowestPaintedSupport=contact,registeredSupport=224,hipMarker=marker,registeredHipMarker=[round(mx*density)+shift[0] for mx in [marker['sourceCenter'][0]]]+[round(marker['sourceCenter'][1]*density)+shift[1]],registrationScope="Whole-figure crown-X and lowest painted support translation; articulated palm/knee/toe contact pending",physicalContactAccepted=False,bareDonorSize=[21,23],helmetDonorSize=[40,40],donorScale=1,donorRotation=0,bodyOutsideHeadRegionsExact=True,foregroundExact=True,belowHeadRegionExact=True,opaqueBareDonorExact=True))

names=['Swimming','Lower hands','Low elbow','Palm push','Knee tuck','Half kneel','Rise','Standing'];durations=[60,40,50,60,70,80,80,60];assert sum(durations)==500
banks={};preserved=0;decoded=0
for g in ['bare','helmet']:
 previous=[Image.open(PREV/g/f'frames/swim-land-west/{i:03}.png').convert('RGBA') for i in range(8)]
 bank=previous[:4]+[interiors[g][0]]+previous[5:];banks[g]=bank;files=[]
 for i,im in enumerate(bank):
  if i!=4:assert im.tobytes()==previous[i].tobytes();preserved+=1
  f=P/g/f'frames/swim-land-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P/g).as_posix())
 manifest=json.loads((PREV/g/'manifest.json').read_text(encoding='utf-8'));manifest['name']='Bill West master-calibrated knee comparison candidate';manifest['status']='mixed_scale_comparison_unselected';state=manifest['states'][0];state['frameFiles']=files;state['frameDurationsMs']=durations;state['facings']=['west']*8;state['provenance']='Seven other complete poses exact for comparison; knee uses one shared neutral148/958 calibration and crown-X/lowest painted support registration. Older neighbor scale remains mismatched; not final motion or normal admission.'
 (P/g/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 bank[0].save(P/g/'source-leave.png',save_all=True,append_images=bank[1:],duration=durations,loop=1,disposal=0,blend=0)
 with Image.open(P/g/'source-leave.png') as ap:
  assert ap.n_frames==8 and ap.info['loop']==1
  for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i];decoded+=1
board=Image.new('RGB',(2816,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 for i,im in enumerate(banks[g]):board.paste(im,(i*352,row*360+25),im);d.text((i*352+4,row*360+4),g+' / '+names[i],fill='white')
board.save(P/'full-exit-review.png')
neck=Image.new('RGB',(800,350),'#182932');d=ImageDraw.Draw(neck)
x,y=records[0]['crown']
for i,g in enumerate(['bare','helmet']):
 im=banks[g][4].crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST);neck.paste(im,(i*400,25),im);d.text((i*400+4,4),g+' / calibrated knee tuck',fill='white')
neck.save(P/'neck-review.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
review={'inputSHA256':before,'frozenInputsStable':len(before),'frames':records,'priorCompletePosesExact':preserved,'decodedAPNGFramesExact':decoded,'durationsMs':durations,'totalMs':500,'loop':1,'density':density,'calibration':calibration,'canvas':[352,320],'pivot':[160,224],'standingHeight':148,'normalSelected':False,'nativeAcceptance':False,'scope':'Shared neutral-calibrated knee source; seven earlier-scale comparison poses unchanged. Mixed sequence is diagnostic, not final motion. No body/limb fitting; full master/articulation/contact/grade acceptance pending.'}
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
# Retain finite timing, explicitly identify mixed-scale diagnostic sequence.
html=(PREV/'index.html').read_text(encoding='utf-8').replace('Corrected lowering, elbow support and palm push, bare and helmeted. Five other complete poses retained.','New knee pose compared with the original master and a shared standing reference. Older surrounding poses still need size and finish corrections.').replace('Bill west - complete exit candidate','Bill West - master scale comparison').replace('Push transition comparison','Knee transition comparison')
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'stableInputs':len(before),'priorPosesExact':preserved,'APNGFramesExact':decoded,'headProxy':records[0]['headProxy'],'hip':records[0]['registeredHipMarker'],'crown':records[0]['crown'],'bareDonor':records[0]['bareDonorPosition']}))
