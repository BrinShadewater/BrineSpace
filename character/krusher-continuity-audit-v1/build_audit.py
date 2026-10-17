from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,math
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v9';B=R/'character/krusher-style-neck-bank-v1';read=lambda p:json.loads(p.read_text());idx=read(P/'package.json');records=read(B/'revision.json')['records'];byoutput={q['output']:q for q in records};crops={};drawings=[];states={};font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),15)
(H/'crops').mkdir(exist_ok=True);(H/'sheets').mkdir(exist_ok=True)
for key,state in idx['states'].items():
 mp=P/state['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']==key.split(':',1)[1]);refs=[]
 for i,(file,source) in enumerate(zip(s['frameFiles'],state['sourceFrames'])):
  q=byoutput[Path(source).relative_to(B.relative_to(R)).as_posix()];im=Image.open(mp.parent/file).convert('RGBA')
  if q.get('newHead'):
   head=Image.open(R/q['newHead']);angle=q.get('rotationDegrees',0);head=head.rotate(angle,expand=True) if angle else head;x,y=q['newPaste'];cx=x+head.width/2;cy=y+head.height/2+8;box=(round(cx-28),round(cy-30),round(cx+28),round(cy+30));crop=im.crop(box)
  else:
   box=im.getbbox();body=im.crop(box);crop=Image.new('RGBA',(56,60));body.thumbnail((56,60),Image.Resampling.LANCZOS);crop.alpha_composite(body,((56-body.width)//2,0))
  digest=hashlib.sha256(crop.tobytes()).hexdigest()
  if digest not in crops:
   n=len(crops);crop.save(H/'crops'/f'{n:04d}.png');crops[digest]={'id':n,'example':key,'frame':i,'cropBox':box,'head':q.get('newHead'),'rotation':q.get('rotationDegrees',0),'mode':q.get('mode','Original sealed rear helmet'),'sourceDrawing':q['source'],'uses':[]}
  row=crops[digest];row['uses'].append([key,i]);refs.append(row['id'])
 states[key]={'cropIds':refs,'durations':s['frameDurationsMs'],'loop':s.get('loop',False),'files':s['frameFiles'],'manifest':state['manifest'],'pivot':m['pivot']}
rows=list(crops.values())
for start in range(0,len(rows),42):
 board=Image.new('RGBA',(6*180,7*210),'#252d31');d=ImageDraw.Draw(board)
 for j,q in enumerate(rows[start:start+42]):
  x=j%6*180;y=j//6*210;im=Image.open(H/'crops'/f"{q['id']:04d}.png");board.alpha_composite(im.resize((168,180),Image.Resampling.NEAREST),(x+6,y+28));d.text((x+3,y+1),f"{q['id']:04d} {q['example'].replace('helmet:','H:').replace('bare:','B:')[:20]}",font=font,fill='white');d.text((x+3,y+15),f"frame {q['frame']} / uses {len(q['uses'])}",font=font,fill='#b9d0d2')
 board.save(H/'sheets'/f'poses-{start//42:02d}.png')
# Each turn is shown in chronological order, including matching source/destination facing masters.
turns=[(k,s) for k,s in states.items() if '-turn-' in k];turnrows=[]
for page in range(math.ceil(len(turns)/6)):
 board=Image.new('RGBA',(1400,6*230),'#252d31');d=ImageDraw.Draw(board)
 for j,(key,s) in enumerate(turns[page*6:page*6+6]):
  gear,action=key.split(':');parts=action.split('-turn-');family=parts[0];a,b=parts[1].split('-');base='carry' if family=='carry' else 'swim-carry' if family=='swim-carry' else 'swim';left=states[gear+':'+base+'-'+a]['cropIds'][0];right=states[gear+':'+base+'-'+b]['cropIds'][0];ids=[left]+s['cropIds']+[right];unique=[]
  for n in ids:
   if not unique or n!=unique[-1]:unique.append(n)
  width=min(140,1360//len(unique));z=min(2,(width-4)/56);d.text((8,j*230),key,font=font,fill='white')
  for n,cid in enumerate(unique):
   im=Image.open(H/'crops'/f'{cid:04d}.png');im=im.resize((round(56*z),round(60*z)),Image.Resampling.NEAREST);board.alpha_composite(im,(n*width+8,j*230+30));d.text((n*width+8,j*230+155),str(cid),font=font,fill='#bed0d0')
  turnrows.append({'key':key,'chronologicalCropIds':ids,'uniqueConsecutive':unique,'sheet':f'turns-{page:02d}.png'})
 board.save(H/'sheets'/f'turns-{page:02d}.png')
(H/'audit-index.json').write_text(json.dumps({'baseline':'krusher-animation-package-v9','states':states,'crops':rows,'turns':turnrows,'scope':'All frame holds mapped to exact head/collar crops; duplicate pixel-identical crops share visual review. Rear sealed helmets shown as miniature full body. Chronological turns include directional context.'},indent=2)+'\n');print(json.dumps({'states':len(states),'frameHolds':sum(len(s['cropIds']) for s in states.values()),'uniqueHeadCollarViews':len(rows),'poseSheets':math.ceil(len(rows)/42),'turnStates':len(turns),'turnSheets':math.ceil(len(turns)/6)}))
