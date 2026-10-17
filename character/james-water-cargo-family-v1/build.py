"""Stage source-authored salvage/pickup/carry and reused accepted prone helmets."""
from pathlib import Path
import sys,copy,json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
STATUS=json.loads((P/'selection.json').read_bytes()).get('status','staged_visual_review_pending') if (P/'selection.json').exists() else 'staged_visual_review_pending'
sys.path.insert(0,str(P.parent/'james-water-family-v1'))
from extract_sources import extract
ANCHORS={'east':[142,118],'south':[128,143],'west':[114,118],'north':[128,110]}
SEQUENCES={'salvage':[0,1,2,3,4,0],'swim-pickup':[0,7,8,9,10,12],'swim-carry':[12,13,14,15,16,12]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def gold_mask(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 return (a[:,:,3]>180)&(r-b>35)&(g-b>20)
def grade(im,point,gold,neutral):
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 protect=(((xx-point[0])/14)**2+((yy-point[1])/16)**2<1)|((b>r+20)&(b>g+10))
 gm=gold_mask(a)&~protect;rgb=a[:,:,:3].astype(float);rgb[gm]*=gold;rgb[(a[:,:,3]>0)&~gm&~protect]*=neutral
 a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');return Image.fromarray(a)
def main():
 retained=json.loads((P/'retained-contracts.json').read_text());combined={m:[] for m in ['bare','helmet']};hashes={};review=[];times=[]
 for d in sys.argv[1:] or ['east','south','west','north']:
  p=P.parent/('james-water-cargo-'+d+'-v1');w=P.parent/('james-water-'+d+'-v1');reg=json.loads((p/'registration-audition.json').read_text());assert reg['sourceSha256']==sha(p/'source.png')
  rows=[Image.open(p/'registered-audition'/f'{i:03d}.png').convert('RGBA') for i in range(18)]
  wm=json.loads((w/'bare-manifest.json').read_text());sw=next(s for s in wm['states'] if s['id']=='swim-'+d);ref=np.array(Image.open(w/sw['frameFiles'][0]).convert('RGBA'));src=np.array(rows[0]);yy,xx=np.indices(src.shape[:2]);point=reg['tracking'][0]['headAnchor'];protect=((xx-point[0])/14)**2+((yy-point[1])/16)**2<1
  gm=gold_mask(src)&~protect;rg=gold_mask(ref);nm=(src[:,:,3]>180)&~gm&~protect;rn=(ref[:,:,3]>180)&~rg
  gold=np.median(ref[:,:,:3][rg],axis=0)/np.maximum(1,np.median(src[:,:,:3][gm],axis=0));neutral=float(np.median(ref[:,:,:3][rn])/max(1,np.median(src[:,:,:3][nm])))
  body=[grade(im,rec['headAnchor'],gold,neutral) for im,rec in zip(rows,reg['tracking'])]
  hr=json.loads((w/'helmet-registration.json').read_text());donors=extract(w/'source-helmet.png',6,6);patch=donors[4][0];pa=np.array(patch);rgb=pa[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);mask=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[mask]*=.9;pa[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS)
  equipped=[];heads=[]
  for i,im in enumerate(body):
   point=np.array(reg['tracking'][i]['headAnchor']);target=point+np.array(hr['centerOffset']);pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int);a=np.array(im);yy,xx=np.indices(a.shape[:2]);erase=((xx-point[0])/14)**2+((yy-(point[1]-1))/14)**2<=1;a[erase]=0;out=Image.fromarray(a);out.alpha_composite(patch,tuple(pos));equipped.append(out)
   heads.append(dict(donorPose=4,donorSourceSha256=sha(w/'source-helmet.png'),sourceBox=donors[4][1],fixedScale=hr['fixedHeadScale'],position=pos.tolist(),editRegion=[min(int(point[0]-14),int(pos[0])),min(int(point[1]-15),int(pos[1])),max(int(point[0]+15),int(pos[0])+patch.width),max(int(point[1]+14),int(pos[1])+patch.height)]))
  reg.update(status=STATUS,goldGain=gold.tolist(),neutralGain=neutral,helmetTracking=heads)
  (p/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
  board=Image.new('RGB',(1536,6*300),'#303b40');dr=ImageDraw.Draw(board)
  for mode,art in [('bare',body),('helmet',equipped)]:
   states=[]
   for action,seq in SEQUENCES.items():
    if d=='west' and action=='salvage':seq=[0,1,2,1,4,0] # Reject downward-aiming source3; preserve it as source evidence.
    key=action+'-'+d;st=copy.deepcopy(retained[key]['state']);files=[]
    for j,i in enumerate(seq):
     f=p/'frames'/mode/action/f'{j:03d}.png';f.parent.mkdir(parents=True,exist_ok=True);art[i].save(f);rel=f.relative_to(p).as_posix();files.append(rel);hashes[Path(os.path.relpath(f,P)).as_posix()]=sha(f)
     y=(list(SEQUENCES).index(action)*2+int(mode=='helmet'))*300+30;at=(j*256,y);board.paste(art[i],at,art[i]);dr.text((at[0]+5,y-22),key+' '+mode+' '+str(j),fill='white')
    st.update(frameFiles=files,frameCount=6,provenance=dict(source='source.png',sourcePoses=seq,derivation='Independent full bodies, fixed cranial source scale and fixed material gains; exact salvage/pickup/carry joins and closed loops; retained clocks',helmet='Accepted prone water donor4 at fixed shell scale' if mode=='helmet' else None));states.append(st)
    cs=copy.deepcopy(st);cs['frameFiles']=[Path(os.path.relpath(p/f,P)).as_posix() for f in files];combined[mode].append(cs)
   manifest=dict(name='James underwater cargo '+d+' '+mode,frameWidth=256,frameHeight=276,pivot=[128,128],standingHeight=148,strideDistanceCells={'swim-carry':retained['swim-carry-'+d]['pack']['strideDistanceCells']['swim-carry']},precomposed=True,status=STATUS,states=states)
   (p/(mode+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
  board.save(p/'paired-contact.png')
  for action,seq in SEQUENCES.items():
   for j,i in enumerate(seq):
    board=Image.new('RGB',(1140,345),'#303b40');dr=ImageDraw.Draw(board);dr.text((8,8),'James '+d+' '+action+' / bare + helmet / 82px / 54px / 27px',fill='white')
    for k,art in enumerate([body,equipped]):
     im=art[i];board.paste(im,(k*256,38),im)
     for h,x in [(82,525),(54,830),(27,1025)]:
      sc=h/148;small=im.resize((round(256*sc),round(276*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+k*(small.width+3),160-round(128*sc)),small)
    review.append(board);times.append(int(retained[action+'-'+d]['state']['frameDurationsMs'][j])+(350 if j in [0,5] else 0))
  print(d,'18 references/mode staged, gold',np.round(gold,3).tolist(),'neutral',round(neutral,3))
 for mode,states in combined.items():
  (P/(mode+'-manifest.json')).write_text(json.dumps(dict(name='James underwater cargo '+mode,frameWidth=256,frameHeight=276,pivot=[128,128],standingHeight=148,strideDistanceCells={'swim-carry':retained['swim-carry-east']['pack']['strideDistanceCells']['swim-carry']},precomposed=True,status=STATUS,states=states),indent=2)+'\n')
 (P/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=times,loop=0,disposal=2,optimize=False)
if __name__=='__main__':main()
