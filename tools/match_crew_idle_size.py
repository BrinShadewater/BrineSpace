from pathlib import Path
import json,numpy as np,re
from PIL import Image,ImageDraw
P=Path('character/crew-idle-size-match-v1');P.mkdir(exist_ok=True);reports={};tracks=[];sheet=Image.new('RGB',(1104,880),'#303b40');draw=ImageDraw.Draw(sheet)
def skin(a):
 r=a[:,:,:3].astype(float);y=np.indices(a.shape[:2])[0];top=np.where(a[:,:,3]>127)[0].min();return (a[:,:,3]>240)&(y>=top+6)&(y<top+27)&(r[:,:,0]>100)&(r[:,:,1]>55)&(r[:,:,2]>35)&(r[:,:,0]>r[:,:,1]*1.12)&(r[:,:,1]>r[:,:,2]*1.08)
for col,who in enumerate(['bill','veld','branforth']):
 root=Path('character/bill-walk-head-v1') if who=='bill' else Path('character/crew-runtime-matte-v1')/who;m=json.loads((root/'manifest.json').read_text());idleRoot=Path('character/crew-idle-match-v1')/who;idleM=json.loads((idleRoot/'manifest.json').read_text());skinGain=np.ones(3)
 if who=='bill':
  sides=[];south=[]
  for d in ['east','west','south']:
   st=next(s for s in m['states'] if s['id']=='walk-'+d)
   for f in st['frameFiles']:
    a=np.array(Image.open(root/f).convert('RGBA'));(south if d=='south' else sides).append(a[:,:,:3][skin(a)])
  target=np.median(np.concatenate(sides),axis=0);base=np.median(np.concatenate(south),axis=0);skinGain=target/base;print('Bill skin:',base.tolist(),'target',target.tolist(),'gain',skinGain.tolist())
 for row,d in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']=='walk-'+d);idle=next(s for s in idleM['states'] if s['id']=='idle-'+d);ii=Image.open(idleRoot/idle['frameFiles'][0]).convert('RGBA');a=np.array(ii);ih=172-np.where(a[:,:,3]>127)[0].min();arr=[np.array(Image.open(root/f).convert('RGBA')) for f in s['frameFiles']];wh=np.median([172-np.where(a[:,:,3]>127)[0].min() for a in arr]);scale=float(ih/wh);files=[];heights=[];clipped=0
  for i,a in enumerate(arr):
   if who=='bill' and d=='south':
    sel=skin(a);b=a.copy();b[:,:,:3][sel]=np.clip(np.rint(a[:,:,:3][sel]*skinGain),0,255).astype('uint8');assert np.array_equal(a[~sel],b[~sel]);a=b
   im=Image.fromarray(a).transform((184,184),Image.Transform.AFFINE,(1/scale,0,92*(1-1/scale),0,1/scale,172*(1-1/scale)),Image.Resampling.BICUBIC);b=np.array(im);ys,xs=np.where(b[:,:,3]>127);heights.append(int(172-ys.min()));clipped+=int(xs.min()==0 or xs.max()==183 or ys.min()==0 or ys.max()==183);rel=f'frames/walk-{d}/{i:03}.png';out=P/who/rel;out.parent.mkdir(parents=True,exist_ok=True);im.save(out);files.append(rel)
   if i==0:
    x=col*368;y=row*220;sheet.paste(ii,(x,y+25),ii);sheet.paste(im,(x+184,y+25),im);draw.text((x+5,y+3),f'{who} {d} idle / matched walk',fill='white')
  s['frameFiles']=files;s['provenance']=dict(source=str(root),fixedScale=scale,anchor=[92,172],skinGain=skinGain.tolist() if who=='bill' and d=='south' else None);reports[who+'-'+d]=dict(scale=scale,idleHeight=int(ih),oldWalkMedian=float(wh),newWalkMedian=float(np.median(heights)),clippedFrames=clipped,timingUnchanged=True)
  prefix=who+'/';tracks.append(dict(label=who.title()+' '+d,row=row,col=col,idle='../crew-idle-match-v1/'+who+'/'+idle['frameFiles'][0],idleFiles=['../crew-idle-match-v1/'+who+'/'+f for f in idle['frameFiles']],idleDurations=idle['frameDurationsMs'],files=[prefix+f for f in files],durations=s['frameDurationsMs']))
 m['states']=[s for s in m['states'] if s['id'].startswith('walk-')];(P/who/'manifest.json').write_text(json.dumps(m,indent=2))
sheet.save(P/'contact.png');(P/'validation.json').write_text(json.dumps(reports,indent=2));html=Path('character/crew-idle-match-v1/index.html').read_text();html=re.sub(r'const tracks=.*?;let ready=',lambda _: 'const tracks='+json.dumps(tracks)+';let ready=',html);html=html.replace('Matched idle preview','Idle size and Bill skin matching').replace('Each pair shows colour-matched idle on the left and installed walk on the right.','Matched idle left; revised walk right. Fixed per-clip scaling matches idle height without flattening walking bob. Bill south skin matched to side views; 3% side-head reduction retained.');(P/'index.html').write_text(html);print(reports)
