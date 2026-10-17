from pathlib import Path
import json, hashlib, shutil, os
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent; R=P.parents[1]
S=R/'character/james-meal-service-south-open-v1'
N=R/'character/james-meal-interrupt-north-v1'
runs={}
for folder,base,target in [(S,'native-north-open-review','native-open'),(N,'native-return','native-return')]:
    v=json.loads((folder/(base+'-validation.json')).read_text())
    e=json.loads((folder/(base+'-evidence.json')).read_text())
    assert v['exitCode']==0 and not v['timedOut'] and e['failures']==0
    assert 'ERROR:' not in (folder/(base+'.log')).read_text(encoding='utf-8')
    for suffix in ['-validation.json','-evidence.json','.log']:
        shutil.copy2(folder/(base+suffix),P/(target+suffix))
    runs[target]={'checks':e['checks'],'failures':0,'scratch':v['scratch'],'realProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta']}

m=json.loads((P/'manifest.json').read_text());m['status']='selected_production_native_verified_owner_review_pending'
(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
b=(P/'build.py').read_text(encoding='utf-8').replace("'production_bound_native_review_pending'","'selected_production_native_verified_owner_review_pending'").replace("'productionInstalled':False","'productionInstalled':True,'ownerVisualAcceptance':False")
(P/'build.py').write_text(b,encoding='utf-8')
reg=json.loads((P/'registration.json').read_text());reg.update(productionInstalled=True,ownerVisualAcceptance=False)
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
a=R/'character/ACTIVE_ASSETS.json';active=json.loads(a.read_text());active['actionOverrides']['branforth-drink-north-hand-continuity']='character/james-drink-north-hand-continuity-v1/manifest.json'
a.write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')

# Recompute diagnostics from current registered exports, not the archived first pass.
rows=[]
for i in range(6):
    arr=np.array(Image.open(P/'frames'/f'{i:03d}.png').convert('RGBA')); yy,xx=np.where(arr[:,:,3]>180);top=int(yy.min());rgb=arr[:,:,:3].astype(float)
    head=(arr[:,:,3]>180)&(np.indices(arr.shape[:2])[0]<top+14)
    rows.append({'index':i,'crown':top,'sole':int(yy.max()),'alphaWidth':int(xx.max()-xx.min()+1),'upper14Width':int(np.where(head)[1].max()-np.where(head)[1].min()+1),'headMedianRGB':np.median(rgb[head],0).tolist()})
assert all(x['crown']==23 and x['sole']==170 for x in rows)
(P/'source-master-diagnostics.json').write_text(json.dumps({'rows':rows,'scope':'Current fixed-ruler exports; bounds and head medians are diagnostics. Anatomy/material require visual review.'},indent=2),encoding='utf-8')

# Source-event native captures at the actual nine-second producer clocks.
states={}
for path in ['character/james-meal-family-v1/bare-manifest.json','character/james-meal-pickup-north-v1/manifest.json','character/james-cup-pickup-north-v1/handoffs-manifest.json','character/james-meal-interrupt-north-v1/manifest.json','character/james-drink-north-hand-continuity-v1/manifest.json']:
    states.update({s['id']:s for s in json.loads((R/path).read_text())['states']})
views=[];times=[]
for action,repeats,budget in [('meal-acquire',1,900),('eat',3,1400),('meal-deposit',1,900),('cup-acquire',1,900),('drink',1,1200),('cup-deposit',1,900)]:
    ds=states[action+'-north']['frameDurationsMs'];durations=[round(x*budget/sum(ds)) for x in ds];durations[-1]+=budget-sum(durations)
    for repeat in range(repeats):
        for i,duration in enumerate(durations):
            im=Image.open(S/'north-open-captures'/f'q0-p0-{action}-{i:02d}.png').convert('RGB');view=Image.new('RGB',(im.width,im.height+26),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),f'North meal / {action} {i}',fill='white');views.append(view);times.append(duration)
assert sum(times)==9000
# Quantize cumulative boundaries so GIF centiseconds do not shorten the course.
boundaries=np.rint(np.cumsum([0]+times)/10).astype(int)*10
gif_times=np.diff(boundaries).tolist()
assert sum(gif_times)==9000
views[0].save(P/'native-course-review.gif',save_all=True,append_images=views[1:],duration=gif_times,loop=0)
shutil.copy2(P/'native-course-review.gif',S/'north-open-course-review.gif')
board=Image.new('RGB',(1620,624),'#303b40');draw=ImageDraw.Draw(board)
for row,action in enumerate(['eat','drink']):
    for i in range(6):
        im=Image.open(S/'north-open-captures'/f'q0-p0-{action}-{i:02d}.png').convert('RGB');crop=im.crop((96,70,336,340));board.paste(crop,(i*270+15,row*312+26));draw.text((i*270+6,row*312+8),f'{action} {i}',fill='white')
board.save(S/'north-open-loops-review.png')
selection={'status':m['status'],'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'prompt':'prompt.txt','registration':'registration.json','newWholeInteriorPoses':4,'exactHeldEndpoints':[0,5],'derivedSourceIndexReturns':6,'ruler':{'scale':reg['fixedWholeScale'],'rigidSoleCorrection':reg['wholeSourceSoleCorrection'],'crown':23,'sole':170},'sourceMaterial':'Pooled neutral/ochre and fixed cap chroma calibration; no per-pose fitting, limb splice or mirroring.','nativeRuns':runs,'packageChecks':28,'physicalReview':'Eight North open-prep courses, two placements across four room rotations. Native pickup/deposit/source loops reviewed. Rear body occludes exact grip; visual contact plausible, no numeric hidden-grip proof.','preview':'native-course-review.gif','previewScope':'Actual selected native source-event captures at producer clocks, not direct frame-rate recording.','ownerVisualAcceptance':False,'remaining':['Full head identity/anatomy and cross-family consistency','Actual locker/crowd journeys and arbitrary scale/flip/off-grid/neighbor furniture contexts']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
note='''

## James North cup hand continuity — October 1, 2026

North open-prep physical review caught a hand switch: pickup uses image-left hand,
old sip uses image-right. Selected james-drink-north-hand-continuity-v1 supplies
four new whole interior sip poses and exact original held endpoints, with six
derived interruption returns. Same cup hand throughout; wrench stays on belt.
One whole-source ruler, pooled matte/cap material calibration, rigid +1px source
sole correction; all six crown23/sole170. Never infer matching sprite registration
from fixed actor foot or passing lifecycle checks alone. Review prop hand across
the complete pickup/use/deposit sequence, including exact held joints.

Current native eight North open-prep courses9160pass and six actual interrupted
return/disk-Continue journeys1041pass; package28pass. Both engines0/no timeout,
scratch APPDATA. Strict profile guards false,last_session.json only; attribution
unproven, no owner rollback. Native nine-second course preview uses source-event
captures, not direct video. New normal North override and matching return clocks
selected; owner visual acceptance pending. North pickup/deposit/worktop review
finished for these two placements/four rotations, with exact grip occluded by rear
torso. Other scale/flip/off-grid/neighbor, actual locker/crowd journeys and full
head/anatomy/material/motion cross-family polish remain. Full James goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes();encoded=note.encode('utf-8')
    if b'## James North cup hand continuity' not in data:
        updated=encoded.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+encoded
        temp=path.with_name(path.name+'.north-cup.tmp');temp.write_bytes(updated);os.replace(temp,path)
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: James North cup continuity

## Objective and acceptance
Full James set and continual master/style/perspective/height/proportion/grade checks,
then cross-family polish. Goal active; this pack is one milestone.

## Accepted decisions and constraints
Matte master palette, stable head/feet, wrench on belt. Keep the cup in its pickup
hand. Whole source authoring and one ruler; preserve exact held endpoints.

## Current state
New source/prompt/build/manifest/registration and four interior sip poses selected
in normal grid_canvas/NPC paths; six derived returns. ACTIVE_ASSETS updated.
Original sources and before-sole-registration evidence retained. New native-course
preview replaces stale opposite-hand sip. Documentation and installed skill mirror
record hand continuity and source registration lessons.

## Verification
28 package checks; 9160 native checks across eight North open-prep courses;
1041 return checks with six actual journeys and disk Continue. Engines0/no timeout.
Strict owner profile fingerprints false for last_session.json only, cause unproven.
Native pickup/deposit, six sip poses and whole ruler reviewed. Exact rear grip
occluded; no hidden-grip proof. Owner visual acceptance pending.

## Next action
Refresh selected-source comparison boards, then continue physical contexts and
full head/anatomy/perspective/material/motion consistency. No owned job remains live.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
south=S/'HANDOFF.md';text=south.read_text(encoding='utf-8');text=text.replace('Next: North open-prep actual hand/worktop contact review, then remaining physical furniture/gear/crowd/Continue contexts and full head/face/anatomy/perspective/motion consistency. No owned native job remains live.','Next: North open-prep physical review finished for two placements/four rotations; left-cup sip continuity selected and verified (see ../james-drink-north-hand-continuity-v1/HANDOFF.md). Continue remaining physical furniture/gear/crowd/Continue contexts and full head/face/anatomy/perspective/motion consistency. No owned native job remains live.');south.write_text(text,encoding='utf-8')
print(json.dumps({'nativeChecks':sum(x['checks'] for x in runs.values()),'packageChecks':28,'selected':True,'fullGoal':'active'}))
