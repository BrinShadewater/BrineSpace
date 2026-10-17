"""Staged generated helmet pitch donors; original seated body and clock retained."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=R/'character/james-seated-family-v1'
src=Image.open(P/'source-v2.png').convert('RGBA');boxes=json.loads((P/'source-boxes.json').read_text())
old=json.loads((OLD/'helmet-manifest.json').read_text());registration=json.loads((OLD/'helmet-registration.json').read_text())
pack=copy.deepcopy(old);pack['states']=[];pack['name']='James staged seated reading helmet pitch';pack['status']=json.loads((P/'selection.json').read_text()).get('status','staged_source_review_pending') if (P/'selection.json').exists() else 'staged_source_review_pending'
# One whole-neutral East ruler shared by every generated figure/head; no per-head fitting.
scale=boxes['neutralRulers'][0]['inverseSourceRuler'];records=[];preview=[];board=Image.new('RGB',(6*184,6*216),'#303b40');draw=ImageDraw.Draw(board)
calibration={t['direction']:np.array(t['oldNeutralHeadMedian'])/np.array(t['candidateNeutralHeadMedian']) for t in json.loads((P/'head-material-calibration.json').read_text())['rows']}
def foot_x(a):
    yy,xx=np.where(a[:,:,3]>180);sole=yy.max();mask=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]>=sole-3);return float(np.where(mask)[1].mean()),int(sole)
for row,d in enumerate(['east','west','south']):
    state=copy.deepcopy(next(s for s in old['states'] if s['id']=='read-seated-'+d));files=[]
    for i,f in enumerate(state['frameFiles']):
        base=Image.open((OLD/f).resolve()).convert('RGBA');canonical=np.array(base);out=base.copy();box=boxes['rows'][row][i]
        raw=src.crop(tuple(box));scaled=raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS)
        target_x,target_y=foot_x(canonical);sx,sy=foot_x(np.array(scaled));at=[round(target_x-sx),target_y-sy];registered=Image.new('RGBA',base.size);registered.alpha_composite(scaled,tuple(at))
        t=registration[state['id']][i];cx=t['bodyCrown'][0];cut=t['headCutoff'];roi=[round(cx-23),0,round(cx+23),cut]
        if i in [1,2,3,4]:
            # Source torso pixels never enter below this explicit upper-head donor limit.
            a=canonical.copy();x0,y0,x1,y1=roi;donor=np.array(registered)[y0:y1,x0:x1].copy();rgb=donor[:,:,:3].astype(float);mask=(donor[:,:,3]>240)&(np.ptp(rgb,2)<20)&(rgb.mean(2)>20)
            rgb[mask]*=calibration[d];donor[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');a[y0:y1,x0:x1]=donor;out=Image.fromarray(a)
        dest=P/'frames'/state['id']/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append(dest.relative_to(P).as_posix())
        records.append({'direction':d,'slot':i,'old':str((OLD/f).resolve()),'oldSha256':hashlib.sha256((OLD/f).resolve().read_bytes()).hexdigest(),'sourceBox':box,'fixedScale':scale,'wholePoseFootRegistration':at,'headROI':roi,'endpointExact':i in [0,5],'output':files[-1]})
        for j,im in enumerate([base,out]):
            y=(row*2+j)*216;board.paste(im,(i*184,y+24),im);draw.text((i*184+4,y+4),d+' '+['selected','candidate'][j]+' '+str(i),fill='white')
    state['frameFiles']=files;state['provenance'].update(helmetSource='res://character/james-seated-read-head-pitch-v2/source-v2.png',helmetPrompt='res://character/james-seated-read-head-pitch-v2/tool-prompt.txt');state['provenance']['helmet']='Generated authored down-pitch donors within upper-head ROI; exact selected torso/tablet/hands/boots and neutral endpoints. Single whole-figure source ruler; staging only.';pack['states'].append(state)
(P/'helmet-manifest.json').write_text(json.dumps(pack,indent=2)+'\n');(P/'registration.json').write_text(json.dumps({'fixedScale':scale,'ruler':'Complete generated East neutral5 sole-to-crown / original selected East neutral5; one shared scale, no per-head resize.','records':records,'fixedMaterialGains':{k:v.tolist() for k,v in calibration.items()},'runtimeInstalled':bool((P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled'))},indent=2)+'\n');board.save(P/'before-after-all-poses.png')
print(json.dumps({'stagedReferences':len(records),'fixedScale':scale,'runtimeInstalled':bool((P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled'))}))
