from pathlib import Path
import json,copy,hashlib,os,importlib.util
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
spec=importlib.util.spec_from_file_location('james_material_helpers',P.parent/'james-water-cargo-turn-family-v1/build.py');helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
color_gain=helpers.color_gain;grade=helpers.grade
ANCHORS={'east':[142,214],'south':[128,239],'west':[114,214],'north':[128,206]}
def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()
def endpoint(mode,action,d):return Image.open(P/'endpoints'/mode/(action+'-'+d+'.png')).convert('RGBA')
def main():
 configs=json.loads((P/'anatomy-config.json').read_text());retained=json.loads((P/'retained-contracts.json').read_text());collections={m:[] for m in ['bare','helmet']};records={};hashes={};boards=[];durations=[]
 status=json.loads((P/'selection.json').read_text()).get('status','staged_visual_review_pending') if (P/'selection.json').exists() else 'staged_visual_review_pending'
 for d,c in configs.items():
  p=P.parent/('james-air-'+d+'-v1');w=P.parent/('james-water-'+d+'-v1');sourcehead=Image.open(w/'source-helmet.png').convert('RGBA');hreg=json.loads((w/'helmet-registration.json').read_text());records[d]={'sourceSha256':sha(p/'source.png'),'actions':{}}
  for action,indices in [('swim-distress',range(6)),('recover-air',range(6,12))]:
   scale=c[action]['scale'];heads=c['heads'];raw=[];points=[];translations=[];indexlist=list(indices)
   for i in indices:
    im=Image.open(p/c[action].get('cropFolder','source-crops')/f'{i:03d}.png').convert('RGBA');a=np.array(im);small=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    if action=='swim-distress':pos=np.rint(np.array(ANCHORS[d])-np.array(heads[i])*scale).astype(int)
    else:
     y,x=np.where(a[:,:,3]>180);bottom=y.max();feet=x[y>=bottom-14];heel=np.array([(feet.min()+feet.max())/2,bottom]);pos=np.rint(np.array([128,224])-heel*scale).astype(int)
    point=np.array(heads[i])*scale+pos;out=Image.new('RGBA',(256,360));out.alpha_composite(small,tuple(pos));raw.append(out);points.append(point);translations.append(pos.tolist())
   target=endpoint('bare','swim' if action=='swim-distress' else 'idle',d);gold,neutral=color_gain(raw[0],target,points[0]);bare=[grade(im,point,gold,neutral) for im,point in zip(raw,points)];helmet=[];tracked=[]
   for j,i in enumerate(indexlist):
    donor_key='6' if action=='swim-distress' else (('18' if d=='north' else '13') if j<4 else '0');donor=hreg['tracking'][donor_key];box=donor['sourceHeadBox'];patch=sourcehead.crop(box);hscale=hreg['fixedHeadScale'];patch=patch.resize((round(patch.width*hscale),round(patch.height*hscale)),Image.Resampling.LANCZOS)
    pa=np.array(patch);rr,gg,bb=pa[:,:,:3].astype(float).transpose(2,0,1);nm=(pa[:,:,3]>0)&(abs(rr-gg)<13)&(abs(gg-bb)<17);rgb=pa[:,:,:3].astype(float);rgb[nm]*=.9;pa[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');patch=Image.fromarray(pa)
    at=np.rint(points[j]+np.array(hreg['centerOffset'])-[patch.width/2,patch.height/2]).astype(int);a=np.array(bare[j]);yy,xx=np.indices(a.shape[:2]);erase=((xx-points[j][0])/14)**2+((yy-(points[j][1]-1))/14)**2<=1;a[erase]=0;out=Image.fromarray(a);out.alpha_composite(patch,tuple(at));helmet.append(out)
    tracked.append(dict(sourcePose=i,sourceHead=heads[i],worldHead=points[j].tolist(),translation=translations[j],helmetDonor=donor['sourceHead'],helmetBox=box,helmetSourceSha256=sha(w/'source-helmet.png'),helmetScale=hscale,helmetPosition=at.tolist(),editRegion=[min(int(points[j][0]-14),int(at[0])),min(int(points[j][1]-15),int(at[1])),max(int(points[j][0]+15),int(at[0])+patch.width),max(int(points[j][1]+14),int(at[1])+patch.height)]))
   if action=='swim-distress':
    for mode,rows in [('bare',bare),('helmet',helmet)]:rows[0]=endpoint(mode,'swim',d);rows[5]=rows[0].copy()
   else:
    for mode,rows in [('bare',bare),('helmet',helmet)]:rows[5]=endpoint(mode,'idle',d)
   records[d]['actions'][action]=dict(sourceFile=c[action].get('sourceFile','source.png'),sourceSha256=sha(p/c[action].get('sourceFile','source.png')),fixedScale=scale,ruler=c[action]['ruler'],goldGain=gold.tolist(),neutralGain=neutral,tracking=tracked,registration='Reviewed cranial proxy for prone swim; measured bottom boot-contact midpoint for dry recovery; no height fitting')
   for mode,rows in [('bare',bare),('helmet',helmet)]:
    key=action+'-'+d;state=copy.deepcopy(retained[key]['state']);files=[]
    for i,im in enumerate(rows):
     file=p/'frames'/mode/key/f'{i:03d}.png';file.parent.mkdir(parents=True,exist_ok=True);im.save(file);rel=Path(os.path.relpath(file,P)).as_posix();files.append(rel);hashes[rel]=sha(file)
    state.update(frameFiles=files,frameCount=6,provenance=dict(source='Independent two-row facing source',sourcePoses=indexlist,derivation='Fixed anatomical scale per action row; fixed material gains per row; reused selected shared helmets; exact swim loop seam or final idle endpoint'))
    collections[mode].append(state)
   for j in range(6):
    board=Image.new('RGB',(1140,440),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James '+key+' / bare + shared helmet / 82px / 54px / 27px',fill='white')
    for k,rows in enumerate([bare,helmet]):
     im=rows[j];board.paste(im,(k*256,35),im)
     for h,x in [(82,525),(54,830),(27,1025)]:
      sc=h/148;small=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+k*(small.width+3),260-round(224*sc)),small)
    boards.append(board);durations.append(int(retained[key]['state']['frameDurationsMs'][j])+(350 if j in [0,5] else 0))
  (p/'registration.json').write_text(json.dumps(records[d],indent=2)+'\n')
 for mode,states in collections.items():
  (P/(mode+'-manifest.json')).write_text(json.dumps(dict(name='James distress/recovery '+mode,frameWidth=256,frameHeight=360,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,status=status,states=states),indent=2)+'\n')
 (P/'registration.json').write_text(json.dumps(records,indent=2)+'\n');(P/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 boards[0].save(P/'review.gif',save_all=True,append_images=boards[1:],duration=durations,loop=0)
 contact=Image.new('RGB',(1536,len(configs)*740),'#303b40');draw=ImageDraw.Draw(contact)
 for row,d in enumerate(configs):
  for sub,action in enumerate(['swim-distress','recover-air']):
   for mode,y in [('bare',row*740+sub*370),('helmet',row*740+sub*370+180)]:
    state=next(s for s in collections[mode] if s['id']==action+'-'+d)
    for i,rel in enumerate(state['frameFiles']):
     im=Image.open(P/rel).convert('RGBA');im=im.resize((128,180),Image.Resampling.BILINEAR);contact.paste(im,(i*256+30,y+15),im);draw.text((i*256+5,y+5),state['id']+' '+mode+' '+str(i),fill='white')
 contact.save(P/'contact.png');print('Staged8 states/48 refs per mode, exact swim seams/final idle, retained960ms/3sec clocks')
if __name__=='__main__':main()
