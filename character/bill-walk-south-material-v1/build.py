"""Clip-wide material chroma correction; native pose/alpha/luminance retained."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_fill_holes,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];audit=json.loads((R/'character/bill-selected-source-audit-2026-10-01-locomotion-v7/source-inventory.json').read_text());refs={g:audit['selectedStateSources'][g]['walk-south'] for g in ['bare','helmet']};yy,xx=np.indices((256,256));L=np.array([.2126,.7152,.0722]);rows=[];states={};planes={}
for gear,s in refs.items():
 planes[gear]=[]
 for f in s['sourceFiles']:
  im=Image.open(R/f[6:]).convert('RGBA');plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,(round(128-s['pivot'][0]),round(224-s['pivot'][1])));planes[gear].append(np.array(plane))
master=np.array(Image.open(R/'character/bill-seated-south-coherent-v1/frames/sit-down-south/000.png').convert('RGBA'))
def material(a,kind):
 rgb=a[:,:,:3].astype(float);lum=rgb@L
 if kind=='neutral':return (a[:,:,3]>0)&(yy>=98)&(np.ptp(rgb,axis=2)<30)&(lum>20)&(lum<120)
 roi=(a[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=105)&(xx<145);top=int(np.where(roi)[0].min())
 return (a[:,:,3]>0)&(yy>=top)&(yy<top+7)&(xx>=105)&(xx<145)&(rgb.max(2)<130)&(lum>10)
def chroma(a,mask):
 r=a[:,:,:3].astype(float)[mask];return r/(r@L)[:,None]
gains={}
for kind in ['neutral']:
 region=((yy<125)&(xx>=108)&(xx<148)) if kind=='neutral' else np.ones((256,256),bool)
 target=np.median(chroma(master,material(master,kind)&region),axis=0);source=np.median(np.concatenate([chroma(a,material(a,kind)&region) for a in planes['bare']]),axis=0);gains[kind]=target/source;assert np.all(np.isfinite(gains[kind]))
headreg=json.loads((P.parent/'bill-run-head-locked-v1/head-registration.json').read_text());headref=next(d for d in headreg['directions'] if d['direction']=='south');head=Image.open(P.parent/'bill-run-head-locked-v1'/headref['componentFile']).convert('RGBA');headarray=np.array(head);headbottom=int(np.where(headarray[:,:,3]>160)[0].max());(P/'sources').mkdir(exist_ok=True);head.save(P/'sources/south-master-head.png')
mastertop=int(np.where((master[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166))[0].min());masterxs=np.where((master[:,:,3]>180)&(yy>=mastertop)&(yy<mastertop+14)&(xx>=100)&(xx<166))[1];masteraxis=(int(masterxs.min())+int(masterxs.max()))/2
# The earlier warm-silhouette component omitted four gray crown rows in this view.
full=np.zeros_like(master);bx,by,bx1,by1=headref['sourceBox'];full[by:by1,bx:bx1]=headarray;crown=(master[:,:,3]>0)&(yy>=mastertop-2)&(yy<mastertop+14)&(xx>=105)&(xx<145);full[crown]=master[crown];ys,xs=np.where(full[:,:,3]>0);headref['sourceBox']=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];head=Image.fromarray(full).crop(headref['sourceBox']);headarray=np.array(head);headbottom=int(np.where(headarray[:,:,3]>160)[0].max());head.save(P/'sources/south-master-head.png')
targetneutral=np.median(chroma(master,material(master,'neutral')&(yy<125)&(xx>=108)&(xx<148)),axis=0)
for gear,s in refs.items():
 manifest=json.loads((R/s['manifest']).read_text());state=copy.deepcopy(next(x for x in manifest['states'] if x['id']=='walk-south'));files=[]
 for i,a in enumerate(planes[gear]):
  rgb=a[:,:,:3].astype(float);lum=rgb@L;out=a.copy();masks={}
  for kind in ['neutral']:
   mask=material(a,kind)&(np.minimum(rgb[:,:,0],rgb[:,:,2])>rgb[:,:,1]*1.04)
   if gear=='helmet':mask&=np.all(a==planes['bare'][i],axis=2)
   graded=rgb*.25+(lum[:,:,None]*targetneutral)*.75;graded*=np.divide(lum,graded@L,out=np.ones_like(lum),where=(graded@L)>0)[:,:,None];out[:,:,:3][mask]=np.clip(np.rint(graded[mask]),0,255).astype('uint8');masks[kind]=mask
  headposition=None;erase=np.zeros((256,256),bool)
  fabricdelta=float(np.abs((out[:,:,:3].astype(float)@L)-lum)[masks['neutral']].max(initial=0))
  if gear=='bare':
   roi=(a[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166);ys=np.where(roi)[0];top=int(ys.min());crown=roi&(yy<top+14);xs=np.where(crown)[1];left=int(xs.min())-4;right=int(xs.max())+4;axis=(int(xs.min())+int(xs.max()))/2
   tinted=(a[:,:,3]>0)&(rgb[:,:,0]>rgb[:,:,1]*1.03)&(rgb[:,:,0]>rgb[:,:,2]*1.02)&(xx>=left)&(xx<right)&(yy>=top)&(yy<top+25)
   for y in range(top,top+25):
    x=np.where(tinted[y])[0]
    if len(x):erase[y,int(x.min()):int(x.max())+1]=True
   erase=(binary_dilation(binary_fill_holes(erase),iterations=1)|((yy>=top-2)&(yy<top+16)))&(a[:,:,3]>0)&(xx>=left)&(xx<right)&(yy>=top-2)&(yy<top+25)
   headposition=[round(axis-(masteraxis-headref['sourceBox'][0])),top+24-headbottom];out[erase]=0;stamp=Image.fromarray(out);stamp.alpha_composite(head,headposition);out=np.array(stamp)
  masks['hair']=erase
  dest=P/f'frames/{gear}/walk-south/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(dest);files.append('res://'+dest.relative_to(R).as_posix());maskfile=P/f'sources/mask-{gear}-{i:03}.png';maskfile.parent.mkdir(exist_ok=True);Image.fromarray((masks['neutral']|masks['hair']).astype('uint8')*255).save(maskfile)
  Image.fromarray(erase.astype('uint8')*255).save(P/f'sources/erase-{gear}-{i:03}.png')
  rows.append({'gear':gear,'frame':i,'originalFile':s['sourceFiles'][i],'originalSha256':hashlib.sha256((R/s['sourceFiles'][i][6:]).read_bytes()).hexdigest(),'originalPivot':s['pivot'],'canvasTranslation':[round(128-s['pivot'][0]),round(224-s['pivot'][1])],'mask':maskfile.relative_to(P).as_posix(),'eraseMask':f'sources/erase-{gear}-{i:03}.png','headPosition':headposition,'changedPixels':int(np.any(out!=a,axis=2).sum()),'fabricLuminanceDifference':fabricdelta})
 state['frameFiles']=files;state['provenance']={'originalManifest':s['manifest'],'materialPass':'Fixed75% master neutral chroma on magenta gray fabric only, luminance retained; exact native accepted bare head scale1; gear changes only body pixels exactly shared with bare source'}
 result={'name':'Bill south walk pooled master material consistency','status':'selected_runtime','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'walk-south':manifest['strideDistanceCells']['walk-south']},'states':[state]}
 if gear=='helmet':result['equipment']='diving-helmet'
 (P/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(result,indent=2)+'\n');states[gear]=state
(P/'material-registration.json').write_text(json.dumps({'diagnosticGains':{k:v.tolist() for k,v in gains.items()},'targetNeutralChroma':targetneutral.tolist(),'neutralBlend':.75,'headSourceBox':headref['sourceBox'],'sourceInventory':'character/bill-selected-source-audit-2026-10-01-locomotion-v7/source-inventory.json','master':'character/bill-seated-south-coherent-v1/frames/sit-down-south/000.png','frames':rows},indent=2)+'\n')
board=Image.new('RGB',(1792,1024),(34,52,62));draw=ImageDraw.Draw(board)
for row in range(2):
 choices=[master]+[planes['bare'][i] if row==0 else np.array(Image.open(R/states['bare']['frameFiles'][i][6:])) for i in [0,8,16,24,32,40]]
 for col,a in enumerate(choices):
  im=Image.fromarray(a);board.paste(im,(col*256,row*512),im);crop=im.crop((100,65,166,125)).resize((198,180),Image.Resampling.NEAREST);board.paste(crop,(col*256+29,row*512+300),crop)
 draw.text((10,row*512+270),'Master + original' if row==0 else 'Master + shared material pass',fill='white')
board.save(P/'material-review.png');print(json.dumps({'frames':len(rows),'fabricLuminanceMax':max(r['fabricLuminanceDifference'] for r in rows)}))
