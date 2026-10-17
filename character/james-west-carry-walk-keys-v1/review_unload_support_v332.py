from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-low-support-v332'
im=Image.open(o/'raw.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);im.save(o/'fixed-canvas-source.png')
original=Image.open(p/'north-unload-low-source-v314/fixed-canvas-source.png').convert('RGBA')
standing=Image.open(r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png').convert('RGBA')
def measure(frame):
    a=np.array(frame)[:,:,3]>128;y,x=np.where(a);spans=[]
    for lo,hi in [(0,128),(128,256)]:
        yy,xx=np.where(a[210:225,lo:hi]);spans.append([int(xx.min()+lo),int(xx.max()+lo)] if len(xx) else [])
    return dict(bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],bootBandSpans=spans)
images=[standing,original,im];metrics=[measure(f) for f in images]
board=Image.new('RGB',(1152,430),(48,59,64));d=ImageDraw.Draw(board)
for j,(frame,m,label) in enumerate(zip(images,metrics,['Standing support','Earlier bent source314','New source332'])):
    x=j*384;board.paste(frame,(x+64,20),frame);d.text((x+4,3),f'{label} {m["bootBandSpans"]}',fill='white');pos=x+10
    for h in [82,54,27]:
        n=round(256*h/148);small=frame.resize((n,n),Image.Resampling.LANCZOS);board.paste(small,(pos,420-n),small);pos+=n+6
board.save(o/'support-comparison.png')
inputs=json.loads((o/'inputs.json').read_bytes())
for ref in inputs['refs']:assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()==ref['sha256']
inputs.update(submittedPromptSha256=hashlib.sha256((o/'submitted-prompt.txt').read_bytes()).hexdigest(),generationFile='exec-1819c4d1-b94a-4ab9-8258-7aa7717a6faf.png')
(o/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
report=dict(metrics=metrics,normalChanged=False,selected=False,nativeRun=False,sourceAcceptance=False,fullGoalComplete=False,status='rejected_requested_support_alignment_not_achieved',findings=['bent pose floor retained closely, but knee/boot span remains spread relative to standing support','curved cloth visible, yet body/equipment/head continuity still unproven','a boot-reference image does not constrain output joint placement'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
