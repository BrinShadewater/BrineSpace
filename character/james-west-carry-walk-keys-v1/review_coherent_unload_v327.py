from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-coherent-v327'
raw=Image.open(o/'raw.png').convert('RGBA');assert raw.width==raw.height
sheet=raw.resize((768,768),Image.Resampling.NEAREST);sheet.save(o/'whole-normalized.png')
old=Image.open(r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png').convert('RGBA')
board=Image.new('RGB',(1536,810),(48,59,64));d=ImageDraw.Draw(board);measure=[]
for i in range(9):
    x=(i%3)*256;y=(i//3)*256;frame=sheet.crop((x,y,x+256,y+256));frame.save(o/f'{i:03}.png')
    bounds=frame.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    measure.append(dict(pose=i,bounds=bounds,height=bounds[3]-bounds[1]))
    bx=(i%3)*512;by=(i//3)*270
    board.paste(old,(bx,by+14),old);board.paste(frame,(bx+256,by+14),frame)
    d.text((bx+4,by+2),f'endpoint | trial {i} H{bounds[3]-bounds[1]} sole{bounds[3]-1}',fill='white')
board.save(o/'endpoint-comparison.png')
report=dict(generationId='01a0ef89-fc47-7e22-953f-3c02a051b0f6',mode='built-in imagegen',rawSize=list(raw.size),
    promptFile='submitted-prompt.txt',promptSha256=hashlib.sha256((o/'submitted-prompt.txt').read_bytes()).hexdigest(),
    geometry=measure,referenceHeight=148,referenceSole=224,normalChanged=False,nativeRun=False,selected=False,
    status='rejected_before_native_scale_registration_and_stance',
    findings=['nine-slot sheet exceeds standing scale; full-sheet registration not preserved','floor height varies across rows','lowest pose still widens knees and boots','master curve/material not fully matched; gear and backpack redrawn'],
    nextAction='Use a temporally coherent first/last-source video trial with equal whole-source registration; inspect entire clip, preserving original masters as fidelity authority. Do not fit this rejected sheet pose by pose.')
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(rawSize=raw.size,geometry=measure,selected=False)))
