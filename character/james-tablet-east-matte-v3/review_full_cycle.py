from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-tablet-east-belt-fixed-source-v2'
generated=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-3c542e97-20da-45b2-9dfd-4ad0142813ab.png')
shutil.copy2(generated,P/'unselected-material-study.png')
target=np.array(Image.open(P/'material-edit-target.png').convert('RGBA'))
raw=Image.open(generated).convert('RGBA');normalized=np.array(raw.resize((target.shape[1],target.shape[0]),Image.Resampling.LANCZOS))
image_report={'rawSize':list(raw.size),'targetSize':[target.shape[1],target.shape[0]],'normalizedAlphaChangedPixels':int((normalized[:,:,3]!=target[:,:,3]).sum()),'selected':False,'reason':'Generated material study redraws face, cloth and tool details and changes alpha after canvas normalization; only reference evidence, no authored source replacement.','sha256':hashlib.sha256(generated.read_bytes()).hexdigest()}
records=[];modes={}
for mode in ['bare','helmet']:
    p=S/(mode+'-manifest.json');pack=json.loads(p.read_bytes());state=next(s for s in pack['states'] if s['id']=='inspect-east');images=[]
    for i,rel in enumerate(state['frameFiles']):
        f=(p.parent/rel).resolve();im=Image.open(f).convert('RGBA');images.append(im);a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy=np.indices(a.shape[:2])[0];lum=rgb.mean(2)
        green=(a[:,:,3]>0)&(g>r*1.3)&(g>b*1.3)&(g>70)
        cloth=(a[:,:,3]>240)&(yy>=60)&(yy<145)&(np.ptp(rgb,2)<28)&(lum>12)&(lum<140)&~((r-b>12)&(r-g>5))&~((r-b>18)&(g-b>10))
        records.append({'mode':mode,'index':i,'keyGreenPixels':int(green.sum()),'keyGreenOpaquePixels':int((green&(a[:,:,3]>240)).sum()),'keyGreenBounds':list(Image.fromarray(green.astype('uint8')*255).getbbox()) if green.any() else None,'clothMedian':np.median(rgb[cloth],0).tolist(),'alphaSha256':hashlib.sha256(a[:,:,3].tobytes()).hexdigest()})
    for page in range(5):
        subset=list(range(page*32,min((page+1)*32,len(images))));board=Image.new('RGB',(8*184,4*208),'#303b40');draw=ImageDraw.Draw(board)
        for j,i in enumerate(subset):
            at=((j%8)*184,(j//8)*208+24);board.paste(images[i],at,images[i]);draw.text((at[0]+4,at[1]-20),mode+' '+str(i),fill='white')
        board.save(P/(mode+'-full-cycle-'+str(page)+'.png'))
    rr=[r for r in records if r['mode']==mode];modes[mode]={'slots':len(images),'clockMs':sum(state['frameDurationsMs']),'framesWithKeyGreen':sum(r['keyGreenPixels']>0 for r in rr),'maxKeyGreenPixels':max(r['keyGreenPixels'] for r in rr),'maxKeyGreenOpaquePixels':max(r['keyGreenOpaquePixels'] for r in rr),'firstMasterClothMedian':rr[0]['clothMedian'],'lastMasterClothMedian':rr[-1]['clothMedian']}
(P/'full-cycle-evidence.json').write_text(json.dumps({'modes':modes,'records':records,'generation':image_report,'scope':'Actual selected141source frames per gear. RGB key-green criterion g>1.3r, g>1.3b,g>70 is a diagnostic, not a semantic cloth/tool segmentation. Low-chroma opaque cloth median excludes warm/gold, y60..144; not whole-body perceptual identity. No source changes or native test.'},indent=2))
print(json.dumps({'modes':modes,'generation':image_report}))
