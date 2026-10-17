"""Template-authored breathing chest details with exact supported neutral head ownership."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-rest-south-sleep-template-v8'
file=P/'bare-manifest.json';pack=json.loads(file.read_text());reg=json.loads((P/'registration-v2.json').read_text())
neutral=Image.open(P/'frames/lie-down/005.png').convert('RGBA');canonical=np.array(neutral)
box=list(reg['tracking'][5]['protectedHeadBox']);box[3]=159;x0,y0,x1,y1=box
breath_image=Image.new('L',(256,256));ImageDraw.Draw(breath_image).polygon([(101,153),(158,153),(151,167),(110,167)],fill=255)
breath_region=np.array(breath_image)>0;breath_region[y0:y1,x0:x1]=False
# Supported hands, tools, pelvis, soles and outline must stay still during sleep.
breath_region&=canonical[:,:,3]>240
raw=[]
for i in range(6):
    im=Image.open(S/'frames'/f'{i:03}.png').convert('RGBA')
    # One constant source-ruler translation after matching alpha192 reference sole.
    shifted=Image.new('RGBA',(256,256));shifted.alpha_composite(im,(0,1));raw.append(shifted)
for i,im in enumerate(raw):
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
    protect=np.zeros(a.shape[:2],bool);protect[y0:y1,x0:x1]=True
    gold=(a[:,:,3]>0)&~protect&(r-b>35)&(g-b>20);body=(a[:,:,3]>0)&~protect&~gold
    lum=rgb.mean(2);mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170])
    factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[body]*=factor[body,None]
    a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');raw[i]=Image.fromarray(a)
def masks(a):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);protect=np.zeros(a.shape[:2],bool);protect[y0:y1,x0:x1]=True
    opaque=a[:,:,3]>240;gold=opaque&~protect&(r-b>35)&(g-b>20)
    neutral_mask=opaque&~protect&~gold&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<110)&~((r-b>12)&(r-g>5))
    return {'neutral':neutral_mask,'gold':gold}
target=masks(canonical);gains={}
for material in ['neutral','gold']:
    samples=np.concatenate([np.array(raw[i])[:,:,:3][masks(np.array(raw[i]))[material]] for i in [1,2,3,4]])
    source=np.median(samples,0);master=np.median(canonical[:,:,:3][target[material]],0)
    gains[material]={'sourceMedian':source.tolist(),'targetNeutralMedian':master.tolist(),'fixedGain':(master/source).tolist()}
rows=[neutral.copy()];records=[]
for i in [1,2,3,4]:
    a=np.array(raw[i]);regions=masks(a)
    for material,mask in regions.items():a[:,:,:3][mask]=np.rint(a[:,:,:3][mask].astype(float)*gains[material]['fixedGain']).clip(0,255).astype('uint8')
    # Stationary breathing explicitly requires fixed head/neck/pillow contact.
    # Reuse the exact whole supported neutral ownership region; never shrink a head.
    output=canonical.copy();use=breath_region&(a[:,:,3]>240);output[:,:,:3][use]=a[:,:,:3][use]
    rows.append(Image.fromarray(output))
    records.append({'slot':i,'source':'res://character/james-rest-south-sleep-template-v8/frames/'+f'{i:03}.png','sourceSha256':hashlib.sha256((S/'frames'/f'{i:03}.png').read_bytes()).hexdigest(),'wholeSourceTranslation':[0,1],'canonicalHeadBox':box,'breathingRegionPolygon':[(101,153),(158,153),(151,167),(110,167)],'derivation':'Registered authored chest interior RGB inside existing opaque neutral silhouette; all alpha and nonbreathing head/collar/hands/tools/pelvis/soles exact supported neutral. No new limb/head pose or interpolation.'})
rows.append(neutral.copy());state=next(s for s in pack['states'] if s['id']=='sleep-south')
for i,im in enumerate(rows):im.save(P/'frames/sleep'/f'{i:03}.png')
state['provenance'].update(breathingSource='res://character/james-rest-south-sleep-template-v8/source.png',breathingPrompt='res://character/james-rest-south-sleep-template-v8/prompt.txt',breathingFixedScale=json.loads((S/'fixed-ruler-evidence.json').read_text())['fixedScale'],breathingMethod='Four template-authored chest-detail interiors inside the exact supported neutral silhouette; exact neutral0/5 and all nonbreathing supports/head/tools/soles. One shared material gain, constant[0,1]whole-source translation. No per-frame bounds/grade fitting, head/limb shrinking or duplicate authored-frame claim.',breathingHeadOwnership=box)
for i in [6,7,8,9,10,11]:reg['tracking'][i]=copy.deepcopy(reg['tracking'][5])
reg['templateBreathing']={'source':'res://character/james-rest-south-sleep-template-v8/source.png','fixedScale':state['provenance']['breathingFixedScale'],'gains':gains,'records':records,'canonicalHeadBox':box,'alphaAllExact':True,'bodySourceChangesGeometry':False,'matteCurveAppliedOnce':'Original approved non-gold curve, raw template authoring source is ungraded. Fixed pooled gain follows, never another curve on processed frames.','scope':'Registered template-authored chest interiors only; exact canonical alpha/head/collar/hands/tools/pelvis/boots prevent unintended support/detail flashes. No part resizing or newly invented articulated geometry. Four authored chest variants and shared neutral.'}
file.write_text(json.dumps(pack,indent=2)+'\n');(P/'registration-v2.json').write_text(json.dumps(reg,indent=2)+'\n')
board=Image.new('RGB',(6*256,280),'#303b40');d=ImageDraw.Draw(board)
preview=[]
for i,im in enumerate(rows):
    board.paste(im,(i*256,24),im);d.text((i*256+4,4),'South sleep '+str(i),fill='white')
    b=Image.new('RGB',(512,280),'#303b40');b.paste(neutral,(0,24),neutral);b.paste(im,(256,24),im);bd=ImageDraw.Draw(b);bd.text((4,4),'exact supported neutral',fill='white');bd.text((260,4),'authored breathing '+str(i),fill='white');preview.append(b)
board.save(P/'all-revised-sleep-poses.png')
preview[0].save(P/'sleep-supported-head-review.gif',save_all=True,append_images=preview[1:],duration=state['frameDurationsMs'],loop=0,disposal=2)
(P/'sleep-ownership-evidence.json').write_text(json.dumps({'records':records,'gains':gains,'headBox':box,'neutralEndpointsExact':True,'canonicalHeadAllExact':True,'fourAuthoredChestInteriorReferences':True,'runtimeInstalled':bool((P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled'))},indent=2)+'\n')
print(json.dumps({'sleepReferences':6,'authoredInteriorChestReferences':4,'headOwnershipExact':True,'clockMs':sum(state['frameDurationsMs']),'runtimeInstalled':bool((P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled'))}))
