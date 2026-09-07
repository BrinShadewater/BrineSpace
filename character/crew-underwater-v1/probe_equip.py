"""Measure overhead clearance without shrinking the actor to an old canvas."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
source = ROOT/'generated/bill-equip-helmet-east-candidate-05.png'
im = Image.open(source).convert('RGBA')
a = np.array(im)
# Candidate 04 has white letterboxing outside its magenta sprite band.
band_top=round(152/683*im.height); band_bottom=round(531/683*im.height)
a[:band_top]=0; a[band_bottom:]=0
key = (a[:,:,0].astype(int)>a[:,:,1].astype(int)+35)&(a[:,:,2].astype(int)>a[:,:,1].astype(int)+35)
a[key] = 0
im = Image.fromarray(a)
occupied = (a[:,:,3]>0).sum(axis=0)>3
runs=[]; start=None
for x,on in enumerate(list(occupied)+[False]):
    if on and start is None: start=x
    if not on and start is not None:
        if x-start>25: runs.append((start,x))
        start=None
assert len(runs)==6
# Candidate 04 measurements on 2048x683 preview: crown239, boot511.
scale=74/((511-239)/683*im.height)
out=ROOT/'pilot/bill-equip-helmet-east'; out.mkdir(exist_ok=True)
sheet=Image.new('RGB',(1104,230),'#1d252a'); draw=ImageDraw.Draw(sheet)
records=[]
for i,(left,right) in enumerate(runs):
    crop=im.crop((left,0,right,im.height)); box=crop.getbbox()
    crop=crop.crop(box)
    frame=Image.new('RGBA',(92,104))
    sprite=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.BOX)
    sprite.putalpha(sprite.getchannel('A').point(lambda v:255 if v>=128 else 0))
    # Original source boot centers, registered independently of hand/helmet width.
    boot_x=[187,528,853,1205,1534,1870][i]/2048*im.width
    x=46-round((boot_x-left-box[0])*scale); y=98-sprite.height
    frame.alpha_composite(sprite,(x,y)); frame.save(out/f'frame_{i:03}.png')
    big=frame.resize((184,208),Image.Resampling.NEAREST); sheet.paste(big,(i*184,22),big)
    records.append({'sourceBounds':[left+box[0],box[1],left+box[2],box[3]],'bounds':frame.getbbox(),'wouldExceed92Foot86':sprite.height>85})
draw.text((5,4),'Bill donning / 74px bare body calibration / clearance study only',fill='white')
sheet.save(out/'contact.png')
(out/'clearance.json').write_text(json.dumps({'status':'clearance_study_not_runtime','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'canvas':[92,104],'pivot':[46,98],'frames':records},indent=2)+'\n')
print(json.dumps(records))
manifest={'status':'donning_pilot_not_runtime','frameWidth':92,'frameHeight':104,'pivot':[46,98],
 'states':[{'id':'equip-helmet-east','frameCount':6,'frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[180,180,220,220,260,240],'loop':False}]}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'contract.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)).replace('\\','/'),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'status':'pilot; endpoint matching and locker integration pending'},indent=2)+'\n')
comparison=Image.new('RGB',(552,244),'#1d252a'); labels=ImageDraw.Draw(comparison)
for i,(label,path,pivot) in enumerate([
    ('Existing equipped idle',ROOT/'equipment/dry/bill-idle-east/frame_000.png',86),
    ('Donning endpoint',out/'frame_005.png',98),
    ('Existing bare idle',ROOT.parent/'major-bill-v2/frames/idle-east/frame_000.png',86)]):
    sprite=Image.open(path).convert('RGBA'); sprite=sprite.resize((sprite.width*2,sprite.height*2),Image.Resampling.NEAREST)
    comparison.paste(sprite,(i*184,220-pivot*2),sprite); labels.text((i*184+4,5),label,fill='white')
comparison.save(out/'endpoint-comparison.png')
