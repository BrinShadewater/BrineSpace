"""Register raw seated source for anatomical review before grade or selection."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=P/'sources/badge-edit-v2.png';image=Image.open(raw).convert('RGBA');array=np.array(image)
labels,count=label(array[:,:,3]>180);sizes=np.bincount(labels.ravel());sizes[0]=0
parts=[]
for number in np.argsort(sizes)[-6:]:
    yy,xx=np.where(labels==number);parts.append((int(yy.min())//512,int(xx.mean())//512,number))
parts.sort();assert [(row,col) for row,col,_ in parts]==[(row,col) for row in range(2) for col in range(3)]
yy,xx=np.where(labels==parts[0][2]);height=int(yy.max()-yy.min()+1);ruler=148/height
records=[];frames=[]
for slot,(_,_,part) in enumerate(parts):
    yy,xx=np.where(labels==part);floor=int(yy.max())
    foot_x=float(xx[yy>=floor-8].mean())
    box=[int(xx.min()-3),int(yy.min()-3),int(xx.max()+4),int(yy.max()+4)]
    keep=binary_dilation(labels==part,iterations=3)&(array[:,:,3]>0)
    cut=array.copy();cut[~keep]=0
    cropped=Image.fromarray(cut).crop(box)
    cropped=cropped.resize((round(cropped.width*ruler),round(cropped.height*ruler)),Image.Resampling.LANCZOS)
    position=[round(128-(foot_x-box[0])*ruler),round(223-(floor-box[1])*ruler)]
    frame=Image.new('RGBA',(256,256));frame.alpha_composite(cropped,position);frames.append(frame)
    records.append({'pose':slot,'box':box,'position':position,'size':list(cropped.size),'sourceFloorY':floor,'sourceFootCenterX':foot_x,'floorTarget':223})
master_path=R/'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png'
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52))
board=Image.new('RGB',(1792,310),'#202a30');draw=ImageDraw.Draw(board)
for column,frame in enumerate([master]+frames):
    board.paste(frame,(column*256,24),frame);draw.text((column*256+6,5),'Selected master' if column==0 else f'Raw seated {column-1}',fill='white')
board.save(P/'source-scale-review.png')
original=np.array(Image.open(P/'sources/seated-v1.png').convert('RGBA'))
report={'status':'staged ungraded geometry diagnostic, not fitted/selected animation','source':raw.relative_to(P).as_posix(),'sourceSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'master':master_path.relative_to(R).as_posix(),'masterSha256':hashlib.sha256(master_path.read_bytes()).hexdigest(),'executionId':'46f46718-fd10-4141-9a2f-2bd63b35fadb','prompt':'sources/badge-prompt-v2.txt','originalExecutionId':'13863aad-88c3-42e9-ad58-831fcd78f721','originalPrompt':'sources/prompt-v1.txt','editChangedPixels':int(np.any(array!=original,axis=2).sum()),'editScope':'new complete source revision; edit changed pixels beyond badges, so no exact protected-body claim','fixedRuler':ruler,'standingOpaqueHeight':height,'frames':records,'pending':['grade/material/head anatomy review','canonical equipped hardware and seated joins','actual seated motion/furniture contact']}
(P/'source-scale-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'poses':len(frames),'opaqueStandingHeight':height,'fixedRuler':ruler,'status':'ungraded diagnostic'}))
