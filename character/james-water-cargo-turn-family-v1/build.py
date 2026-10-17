"""Stage independent water quarters, exact endpoint seams, reversed and composed turns."""
from pathlib import Path
import copy,json,hashlib,shutil,os
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
CONFIG=json.loads((P/'anatomy-config.json').read_text())
ANCHORS={'east':[142,118],'south':[128,143],'west':[114,118],'north':[128,110]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mask_gold(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 return (a[:,:,3]>180)&(r-b>35)&(g-b>20)
def color_gain(source,reference,point):
 a=np.array(source); b=np.array(reference); yy,xx=np.indices(a.shape[:2]); protect=((xx-point[0])/14)**2+((yy-point[1])/16)**2<1
 ag=mask_gold(a)&~protect; bg=mask_gold(b)
 an=(a[:,:,3]>180)&~ag&~protect; bn=(b[:,:,3]>180)&~bg
 # Uniform source-level material gains, never independent per-pose equalization.
 gold=np.median(b[:,:,:3][bg],axis=0)/np.maximum(1,np.median(a[:,:,:3][ag],axis=0))
 neutral=float(np.median(b[:,:,:3][bn])/max(1,np.median(a[:,:,:3][an])))
 return gold,neutral
def grade(im,point,gold,neutral):
 a=np.array(im); yy,xx=np.indices(a.shape[:2]); protected=((xx-point[0])/14)**2+((yy-point[1])/16)**2<1; gm=mask_gold(a)&~protected
 rgb=a[:,:,:3].astype(float); rgb[gm]*=gold; rgb[(a[:,:,3]>0)&~gm&~protected]*=neutral
 a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8'); return Image.fromarray(a)
def endpoint(d,mode):
 folder=P.parent/('james-water-cargo-'+d+'-v1'); m=json.loads((folder/(mode+'-manifest.json')).read_bytes()); s=next(s for s in m['states'] if s['id']=='swim-carry-'+d)
 return folder/s['frameFiles'][0]
def main():
 retained=json.loads((P/'retained-contracts.json').read_bytes()); collections={}; hashes={}; quarter_rows={}; allrecords={}
 status=json.loads((P/'selection.json').read_bytes()).get('status','staged_cargo_turns_anatomy_review_pending') if (P/'selection.json').exists() else 'staged_cargo_turns_anatomy_review_pending'
 for pair,c in CONFIG.items():
  p=P.parent/('james-water-cargo-turn-'+pair+'-v1'); a,b=pair.split('-'); audit=json.loads((p/'source-audit.json').read_text())['poses']; points=[]; raw=[]
  for i in range(6):
   target=np.array(ANCHORS[a])*(1-i/5)+np.array(ANCHORS[b])*(i/5); local=np.array(c['heads'][i]); sc=c['scale']; im=Image.open(p/'source-crops'/f'{i:03d}.png').convert('RGBA'); small=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.LANCZOS); pos=np.rint(target-local*sc).astype(int); actual=local*sc+pos
   out=Image.new('RGBA',(256,276)); out.alpha_composite(small,tuple(pos)); raw.append(out); points.append(actual)
  gold,neutral=color_gain(raw[0],Image.open(endpoint(a,'bare')).convert('RGBA'),points[0]); body=[grade(im,point,gold,neutral) for im,point in zip(raw,points)]
  body[0]=Image.open(endpoint(a,'bare')).convert('RGBA'); body[5]=Image.open(endpoint(b,'bare')).convert('RGBA')
  donor_folder=p/c.get('helmetDonorFolder','source-crops'); donor_audit=json.loads((p/c.get('helmetDonorAudit','source-audit.json')).read_bytes())['poses']; hscale={'east':35,'south':39,'west':35,'north':33}[a]/donor_audit[6]['opaqueWidth']; equipped=[]; head_records=[]
  offsets={d:json.loads((P.parent/('james-water-'+d+'-v1')/'helmet-registration.json').read_bytes())['centerOffset'] for d in [a,b]}
  for i in range(6):
   if i in [0,5]:equipped.append(Image.open(endpoint(a if i==0 else b,'helmet')).convert('RGBA')); head_records.append({'exactEndpoint':True});continue
   patch=Image.open(donor_folder/f'{i+6:03d}.png').convert('RGBA'); patch=patch.resize((round(patch.width*hscale),round(patch.height*hscale)),Image.Resampling.LANCZOS)
   pa=np.array(patch); rgb=pa[:,:,:3].astype(float); rr,gg,bb=rgb.transpose(2,0,1); nm=(pa[:,:,3]>0)&(abs(rr-gg)<13)&(abs(gg-bb)<17); rgb[nm]*=.9; pa[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');patch=Image.fromarray(pa)
   target=points[i]+np.array(offsets[a])*(1-i/5)+np.array(offsets[b])*(i/5); pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int)
   arr=np.array(body[i]); yy,xx=np.indices(arr.shape[:2]); erase=((xx-points[i][0])/14)**2+((yy-(points[i][1]-1))/14)**2<=1; arr[erase]=0; out=Image.fromarray(arr); out.alpha_composite(patch,tuple(pos)); equipped.append(out)
   head_records.append(dict(sourceHead=i+6,sourceFile=c.get('helmetDonorSource','source.png'),sourceSha256=sha(p/c.get('helmetDonorSource','source.png')),sourceBox=donor_audit[i+6]['sourceBox'],fixedScale=hscale,position=pos.tolist(),editRegion=[min(int(points[i][0]-14),int(pos[0])),min(int(points[i][1]-15),int(pos[1])),max(int(points[i][0]+15),int(pos[0])+patch.width),max(int(points[i][1]+14),int(pos[1])+patch.height)]))
  records=dict(fixedScale=c['scale'],cranialRuler=c['ruler'],registration='Manually inspected cranial centers; interpolated world head anchor, not measured shoulder registration',sourceSha256=sha(p/'source.png'),goldGain=gold.tolist(),neutralGain=neutral,helmetFixedScale=hscale,tracking=[dict(sourceCropHead=c['heads'][i],sourceBox=audit[i]['sourceBox'],headAnchor=points[i].tolist(),helmet=head_records[i]) for i in range(6)],status='staged_cargo_turns_anatomy_review_pending')
  (p/'registration.json').write_text(json.dumps(records,indent=2)+'\n');allrecords[pair]=records
  for mode,rows in [('bare',body),('helmet',equipped)]:
   quarter_rows[(mode,pair)]=rows
   for forward,order in [(pair,list(range(6))),(b+'-'+a,list(reversed(range(6))))]:
    key='swim-carry-turn-'+forward; st=copy.deepcopy(retained[key]['state']); files=[]
    for j,i in enumerate(order):
     f=p/'frames'/mode/key/f'{j:03d}.png'; f.parent.mkdir(parents=True,exist_ok=True);rows[i].save(f); rel=Path(os.path.relpath(f,P)).as_posix();files.append(rel); hashes[rel]=sha(f)
    st.update(frameFiles=files,frameCount=6,provenance=dict(source='Independent quarter body/head sheet',quarter=pair,sourcePoses=order,endpointSources=[str(endpoint(d,mode).relative_to(R).as_posix()) for d in [a,b]],derivation='Exact staged cargo endpoints; fixed anatomical source scale; fixed material gains; reverse exact; no mirrored pose'))
    collections[(mode,key)]=st
 routes={'east-west':['east-south','south-west'],'west-east':['west-south','south-east'],'north-south':['north-east','east-south'],'south-north':['south-east','east-north']}
 for mode in ['bare','helmet']:
  for pair,parts in routes.items():
   old=copy.deepcopy(retained['swim-carry-turn-'+pair]['state']); seq=[]; donors=[]
   for n,part in enumerate(parts):
    paths=collections[(mode,'swim-carry-turn-'+part)]['frameFiles']
    if n:assert Image.open(P/seq[-1]).tobytes()==Image.open(P/paths[0]).tobytes();paths=paths[1:]
    seq+=paths;donors+=paths
   # A half turn traverses two quarters at their authored speed. The exact
   # shared endpoint occurs once, with both quarter endpoint holds preserved.
   first=collections[(mode,'swim-carry-turn-'+parts[0])]['frameDurationsMs']
   second=collections[(mode,'swim-carry-turn-'+parts[1])]['frameDurationsMs']
   old['frameDurationsMs']=first[:-1]+[first[-1]+second[0]]+second[1:]
   for field in ['facings','waterKinds','waterPoses','depthOffsets']:del old[field][6]
   old.update(frameFiles=seq,frameCount=11,provenance=dict(derivation='Exact independent quarter donors; duplicate shared pose merged, holds summed; composed 1600ms clock',sourceFrames=donors,timingQuarterSources=parts,previousRetainedDurationMs=680))
   collections[(mode,'swim-carry-turn-'+pair)]=old
  m=dict(name='James underwater cargo turns '+mode,frameWidth=256,frameHeight=276,pivot=[128,128],standingHeight=148,precomposed=True,textureFilter='linear',status=status,states=[st for (mo,key),st in collections.items() if mo==mode])
  (P/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
 (P/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(P/'registration.json').write_text(json.dumps(allrecords,indent=2)+'\n')
 boards=[];times=[]; contact=Image.new('RGB',(1536,4*600),'#303b40');dr=ImageDraw.Draw(contact)
 for row,pair in enumerate(CONFIG):
  for i in range(6):
   for mo,y in [('bare',row*600+35),('helmet',row*600+320)]:
    im=quarter_rows[(mo,pair)][i];contact.paste(im,(i*256,y),im);dr.text((i*256+5,y-23),pair+' '+mo+' '+str(i),fill='white')
   board=Image.new('RGB',(1140,345),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James swimming turn '+pair+' / bare + shared helmet / 82px / 54px / 27px',fill='white')
   for j,mo in enumerate(['bare','helmet']):
    im=quarter_rows[(mo,pair)][i];board.paste(im,(j*256,38),im)
    for h,x in [(82,525),(54,830),(27,1025)]:
     sc=h/148;small=im.resize((round(256*sc),round(276*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+j*(round(256*sc)+3),160-round(128*sc)),small)
   boards.append(board);times.append(int(retained['swim-carry-turn-'+pair]['state']['frameDurationsMs'][i])+(350 if i in [0,5] else 0))
 contact.save(P/'contact.png');boards[0].save(P/'review.gif',save_all=True,append_images=boards[1:],duration=times,loop=0)
 print('12 states / 92 refs per mode / exact cargo endpoints / 800ms quarters, 1600ms halves')
if __name__=='__main__':main()
