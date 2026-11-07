"""Rebuild the connected Branforth south repair chain without writing live frames."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from prepare_branforth_repair_study import main as repair_study
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-repair-polish-v1'
OUT=BASE/'review/branforth-south-chain-02'
def rgba(path):return Image.open(path).convert('RGBA')
def pad_idle(variant):
 im=Image.new('RGBA',(256,256));im.alpha_composite(rgba(BASE/f'sources/branforth-idle-south-{variant}-endpoint.png'),(36,52));return im
def build():
 repair_study();OUT.mkdir(parents=True,exist_ok=True)
 path=BASE/'sources/branforth-kneel-south-02.png';raw=rgba(path);w,h=raw.size
 poses=[];records=[];scale=.23
 for i in range(4):
  rect=(i%2*w//2,i//2*h//2,(i%2+1)*w//2,(i//2+1)*h//2)
  tile=raw.crop(rect);tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=192 else 0));box=tile.getbbox()
  _,xs=np.where(np.asarray(tile)[box[3]-8:box[3],:,3]>0)
  # Screen-right boot stays planted. Exclude the rear/right leg during descent.
  xs=xs[xs>(box[0]+box[2])/2];support=float(np.median(xs))
  dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
  dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
  offset=(round(148-support*scale),round(224-box[3]*scale))
  out=Image.new('RGBA',(256,256));out.alpha_composite(dense,offset);poses.append(out)
  records.append(dict(crop=rect,scale=scale,support=[support,box[3]],offset=offset))
 work=[rgba(BASE/f'review/branforth-repair-south-01/source-{i:03}.png') for i in [0,1,2,3,4,0]]
 kneel=[pad_idle('bare')]+poses+[work[0].copy()]
 rows={'kneel-south':kneel,'repair-south':work,'stand-south':list(reversed(kneel))}
 # Reuse canonical south helmet head, preserving the new body's pixels below collar.
 helmet=rgba(BASE/'sources/branforth-idle-south-helmet-endpoint.png').crop((72,20,112,61))
 fits={};equipment={}
 for state,row in rows.items():
  equipment[state]=[];fits[state]=[]
  for i,frame in enumerate(row):
   if (state=='kneel-south' and i==0) or (state=='stand-south' and i==5):
    worn=pad_idle('helmet');fits[state].append({'exactIdle':True})
   else:
    box=frame.getbbox();top=box[1];alpha=np.asarray(frame)[:,:,3]
    _,xs=np.where(alpha[top+3:top+13]>0);cx=round(float(np.median(xs)))
    at=(cx-20,top-4);worn=frame.copy()
    worn.paste((0,0,0,0),(cx-20,top-4,cx+20,top+32));worn.alpha_composite(helmet,at)
    fits[state].append({'headTop':top,'helmetPosition':at})
   equipment[state].append(worn)
 for variant,clips in [('bare',rows),('helmet',equipment)]:
  for state,row in clips.items():
   for i,frame in enumerate(row):frame.save(OUT/f'{variant}-{state}-{i:03}.png')
  assert clips['kneel-south'][-1].tobytes()==clips['repair-south'][0].tobytes()
  assert clips['repair-south'][-1].tobytes()==clips['stand-south'][0].tobytes()
  assert clips['kneel-south'][0].tobytes()==clips['stand-south'][-1].tobytes()
 sheet=Image.new('RGB',(1536,560),'#17212a');draw=ImageDraw.Draw(sheet)
 for col,f in enumerate(kneel):sheet.paste(f,(col*256,24),f);draw.text((col*256+8,5),f'kneel {col}',fill='white')
 for col,f in enumerate(equipment['kneel-south']):sheet.paste(f,(col*256,304),f)
 sheet.save(OUT/'contact.png')
 sequence=[('kneel-south',i) for i in range(6)]+[('repair-south',i) for _ in range(3) for i in range(6)]+[('stand-south',i) for i in range(6)]
 preview=[];times=[]
 for state,i in sequence:
  board=Image.new('RGB',(512,280),'#17212a');d=ImageDraw.Draw(board);d.text((8,6),state+' / bare',fill='white');d.text((264,6),'helmet',fill='white')
  for col,clips in enumerate([rows,equipment]):board.paste(clips[state][i],(col*256,24),clips[state][i])
  preview.append(board);times.append(140 if state=='repair-south' else [70,90,100,100,90,70][i])
 preview[0].save(OUT/'chain.gif',save_all=True,append_images=preview[1:],duration=times,loop=0)
 report=dict(status='prepared_runtime_chain',selection='tools/branforth_repair_revision.py',source=path.relative_to(ROOT).as_posix(),sourceSha256=hashlib.sha256(path.read_bytes()).hexdigest(),registration=records,helmetFits=fits,derived='Stand reverses the kneel. Exact frozen idle endpoints and exact repair joins. Repair loop reuses first pose as last.',limits=['Generation and joins do not establish owner acceptance.','Native and live review evidence is recorded separately in the dated handoff.'])
 (OUT/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
 print('36 candidate frames; exact joins pass; no runtime writes')
 return rows,equipment
if __name__=='__main__':build()
