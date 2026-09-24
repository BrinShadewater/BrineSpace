"""Register an unselected Branforth south repair study; never modifies live art."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/crew-repair-polish-v1/sources/branforth-repair-south-01.png'
OUT=ROOT/'character/crew-repair-polish-v1/review/branforth-repair-south-01'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 raw=Image.open(SOURCE).convert('RGBA');assert raw.size==(1536,1024)
 frames=[];registration=[]
 # One fixed source scale: the ~100px source head becomes ~23px, matching the
 # detailed standing reference. Never scale each kneeling pose to standing height.
 scale=.23
 for i in range(6):
  box=(i%3*512,i//3*512,(i%3+1)*512,(i//3+1)*512)
  tile=raw.crop(box);tile.putalpha(tile.getchannel('A').point(lambda v:255 if v>=192 else 0))
  bounds=tile.getbbox();assert bounds is not None
  a=np.asarray(tile);ys,xs=np.where(a[bounds[3]-8:bounds[3],:,3]>0)
  sole_x=float(np.median(xs));sole_y=bounds[3]
  dense=tile.resize((round(512*scale),round(512*scale)),Image.Resampling.BOX)
  dense.putalpha(dense.getchannel('A').point(lambda v:255 if v>=128 else 0))
  # This is the planted LEFT boot (screen-right), not the two-foot midpoint.
  # The frozen idle places that support at x148 on the 256px/pivot128 canvas.
  # Centering this one boot on the pivot shifts the whole kneeling body sideways.
  frame=Image.new('RGBA',(256,256));paste=(round(148-sole_x*scale),round(224-sole_y*scale))
  frame.alpha_composite(dense,paste);frames.append(frame)
  registration.append(dict(cell=box,sole=[sole_x,sole_y],scale=scale,paste=paste))
 # Preserve every extracted authored pose; the audition closes on its opening
 # instead of claiming the separately generated last pose is pixel-identical.
 for i,f in enumerate(frames):f.save(OUT/f'source-{i:03}.png')
 order=[0,1,2,3,4,0];row=[frames[i] for i in order]
 oldbase=ROOT/'character/chief-engineer-branforth-v2/frames/bare/repair-south'
 old=[Image.open(oldbase/f'{i:03}.png').convert('RGBA') for i in range(6)]
 preview=[]
 for i,(before,after) in enumerate(zip(old,row)):
  board=Image.new('RGB',(512,282),'#17212a');d=ImageDraw.Draw(board)
  d.text((12,7),'CURRENT SOUTH REPAIR',fill='white');d.text((268,7),'UNSELECTED STUDY',fill='white')
  board.paste(before,(0,26),before);board.paste(after,(256,26),after);preview.append(board)
 preview[0].save(OUT/'comparison.gif',save_all=True,append_images=preview[1:],duration=[140]*6,loop=0)
 preview[2].save(OUT/'comparison.png')
 report=dict(status='unselected_source_study',source=SOURCE.relative_to(ROOT).as_posix(),sourceSha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),registration=registration,playbackOrder=order,durationsMs=[140]*6,pivot=[128,224],standingHeight=148,limits=['New kneeling silhouette is lower than legacy south repair; requires matching kneel/stand chain before integration.','Helmet variant not authored.','North/west and Marsh remain unchanged.','Not a native gameplay or owner acceptance.'])
 (OUT/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'frames':len(frames),'liveAssetsChanged':0,'output':str(OUT)}))
if __name__=='__main__':main()
