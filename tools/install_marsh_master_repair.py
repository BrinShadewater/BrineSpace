"""Stage reviewed unique-pose edits into complete metadata-preserving manifests."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_master_repair import visual
from prepare_marsh_full_polish import material_mask,grade
from prepare_marsh_carry_chain import palette_module

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-master-repair-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 baseline=json.loads((BASE/'baseline-contract.json').read_text())['states'];approved=json.loads((BASE/'approved-sheets.json').read_text());candidates={};provenance={}
 for index,version in approved.items():
  for r in json.loads((BASE/f'candidates/sheet-{int(index):02}-{version}.json').read_text()):
   assert r['poseId'] not in candidates
   candidates[r['poseId']]=r['candidate'];provenance[r['poseId']]=r
 entries={}
 frozen=BASE/'original-state-entries.json'
 if frozen.exists():entries=json.loads(frozen.read_text())
 else:
  for rel in json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())['body']:
   for e in json.loads((ROOT/'character/marsh-v2'/rel).read_text())['states']:entries[e['id']]=e
  frozen.write_text(json.dumps(entries,indent=2)+'\n')
 refs={};donors={};fits={};graded={}
 mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
 for d in ('south','north','east','west'):
  im=Image.open(ROOT/baseline['idle-'+d]['files'][0]).convert('RGBA');m,l,_=material_mask(im);refs[d]=float(l[m].mean())
 for v,r in provenance.items():
  im=Image.open(ROOT/r['candidate']).convert('RGBA');m,l,_=material_mask(im)
  if m.sum()>80 and '-turn-' not in r['key']:donors.setdefault((r['group'],r['key'].split('-')[-1]),[]).append(float(l[m].mean()))
 for (group,d),vals in donors.items():
  median=float(np.median(vals));gain=float(np.clip(refs[d]/median,.90,1.06)) if abs(median-refs[d])>=5 else 1.0
  fits[group+' / '+d]={'target':refs[d],'candidateMedian':median,'gain':gain}
 for v,r in provenance.items():
  gain=fits.get(r['group']+' / '+r['key'].split('-')[-1],{}).get('gain',1.0)
  im=Image.open(ROOT/r['candidate']).convert('RGBA');im=grade(im,gain,mapper)[0];orig=Image.open(ROOT/r['source']).convert('RGBA')
  # Each static pose has one grade reused everywhere. Intermediate turns blend
  # the two directional material anchors; reversed uses give the same target.
  targets=[];ordinary=[u for u in r['uses'] if '-turn-' not in u[0]]
  for key,slot,_ in ordinary or r['uses']:
   dirs=key.split('-')[-2:] if '-turn-' in key else [key.split('-')[-1]]
   fraction=slot/max(1,len(baseline[key]['files'])-1)
   targets.append(refs[dirs[0]]*(1-fraction)+refs[dirs[-1]]*fraction)
  target=float(np.mean(targets));mask,l,_=material_mask(orig)
  if mask.sum()>80:target+=float(np.clip(l[mask].mean()-target,-2,2))
  mask,l,_=material_mask(im)
  if mask.sum()>80 and abs(float(l[mask].mean())-target)>2:
   lo,hi=.75,1.3;best=im;gap=abs(float(l[mask].mean())-target)
   for _ in range(8):
    trial_gain=(lo+hi)/2;trial=grade(im,trial_gain,mapper)[0];tm,tl,_=material_mask(trial)
    if tm.sum()<80:break
    value=float(tl[tm].mean())
    if abs(value-target)<gap:best=trial;gap=abs(value-target)
    if value<target:lo=trial_gain
    else:hi=trial_gain
   im=best
  r['ivoryTarget']=target
  if r['key'].split('-')[0] in ('interact','repair','kneel','stand','inspect','salvage'):
   im.paste(orig.crop((0,0,orig.width,58)),(0,0));im.paste(orig.crop((0,145,orig.width,orig.height)),(0,145))
  if r['key'].startswith('injury-'):
   a=np.array(im);o=np.array(orig);white=(o[:,:,:3].min(2)>=210)&(np.ptp(o[:,:,:3].astype(int),axis=2)<30)&(o[:,:,3]>0);a[white]=o[white];im=Image.fromarray(a)
  graded[v]=im
 # The generated injured south start narrowed the torso. Its dry source has the
 # same registration; use that reviewed body and retain the authored fluid.
 plan=json.loads((BASE/'edit-plan.json').read_text())
 poses=[r for sheet in plan['sheets'] for r in sheet['poses']]
 dry=next(r for r in poses if r['key']=='death-ground-south' and r['slot']==1)
 hurt=next(r for r in poses if r['key']=='injury-ground-south' and r['slot']==1)
 donor=np.array(graded[dry['id']]);old=np.array(Image.open(ROOT/hurt['source']).convert('RGBA'));out=old.copy()
 body=(donor[:,:,3]>0)&(old[:,:,3]>0);white=(old[:,:,:3].min(2)>=210)&(np.ptp(old[:,:,:3].astype(int),axis=2)<30)&(old[:,:,3]>0)
 out[body,:3]=donor[body,:3];out[white]=old[white];graded[hurt['id']]=Image.fromarray(out)
 provenance[hurt['id']]['bodyDonorPoseId']=dry['id']
 selection={};groups={};records={};changes=[]
 for key,s in baseline.items():
  files=[]
  for i,(f,h) in enumerate(zip(s['files'],s['hashes'])):
   assert sha(ROOT/f)==h
   old=Image.open(ROOT/f).convert('RGBA');v=visual(old)
   if v not in candidates:files.append(f);continue
   donor=graded[v];out=old.copy();out.paste(donor.crop(donor.getbbox()),old.getbbox()[:2]);assert np.array_equal(np.array(out)[:,:,3],np.array(old)[:,:,3])
   p=BASE/f'frames/{key}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);out.save(p);rel=p.relative_to(ROOT).as_posix();files.append(rel)
   records[rel]={'sha256':sha(p),'actor':'marsh','source':f,'sourceSha256':h,'poseId':v,'editedSheet':provenance[v]['editedSheet'],'editedSheetSha256':provenance[v]['editedSheetSha256']}
   if 'bodyDonorPoseId' in provenance[v]:
    donor_id=provenance[v]['bodyDonorPoseId'];records[rel]['bodyDonorPoseId']=donor_id
    records[rel]['rejectedEditedSheet']=records[rel]['editedSheet']
    records[rel]['editedSheet']=provenance[donor_id]['editedSheet'];records[rel]['editedSheetSha256']=provenance[donor_id]['editedSheetSha256']
  selection[key]=files
  if files!=s['files']:
   changes.append(key);e=dict(entries[key]);e['frameFiles']=['../../'+f for f in files];groups.setdefault((tuple(s['pivot']),s['standingHeight']),[]).append(e)
 manifests=[]
 for (pivot,height),entries in groups.items():
  name='manifest-p'+str(pivot[0]).replace('.','_')+'-'+str(pivot[1]).replace('.','_')+'.json';p=BASE/name
  p.write_text(json.dumps({'revision':'marsh-master-repair-v1','pivot':pivot,'standingHeight':height,'textureFilter':'nearest','states':entries},indent=2)+'\n');manifests.append('../marsh-master-repair-v1/'+name)
 (BASE/'manifest-list.json').write_text(json.dumps(manifests,indent=2)+'\n');(BASE/'selection.json').write_text(json.dumps({'states':selection,'changedStates':changes},indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'materialFits':fits,'poseIvoryTargets':{v:r['ivoryTarget'] for v,r in provenance.items()},'reviewedSourceSheets':approved,'uniqueEditedPoses':len(candidates),'changedStates':len(changes),'changedSlots':len(records),'policy':'Master-guided source edits; static pose ivory grade from directional idle anchors, blending turn directions; original alpha, white fluid and diagnostic head/boots retained; shared cropped poses reuse one candidate. Original frame timing, pivots, calibration and state metadata copied.'},indent=2)+'\n')
 if '--install' in sys.argv:
  p=ROOT/'character/marsh-v2/catalog.json';c=json.loads(p.read_text())
  for path in manifests:
   if path not in c['body']:c['body'].append(path)
  p.write_text(json.dumps(c,indent=2)+'\n')
 print(len(candidates),'edited poses;',len(changes),'states;',len(records),'slots;', 'installed' if '--install' in sys.argv else 'staged')
if __name__=='__main__':main()
