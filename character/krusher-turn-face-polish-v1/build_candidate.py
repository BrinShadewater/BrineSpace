from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib,copy,shutil
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;V=R/'character/krusher-animation-package-v11';P=R/'character/krusher-animation-package-v12'
read=lambda p:json.loads(p.read_text())
style={q['source']:q for q in read(R/'character/krusher-style-neck-bank-v1/revision.json')['records']};bank=read(R/'character/krusher-continuity-bank-v1/revision.json')['records'];idx=read(V/'package.json')
visors={Path(q['source']).name:q for q in read(R/'character/krusher-continuous-playback-v1/visor-pilot.json')}
refined={q['view']:q for q in read(H/'head-extraction.json')};patches={};records=[]
(H/'frames').mkdir(exist_ok=True);(H/'masks').mkdir(exist_ok=True)
for q in bank:
 if '-turn-' not in q['example']:continue
 s=style[q['sourceRaw']];name=Path(s.get('newHead','')).name;view={'style-se-native.png':'se','style-sw-native.png':'sw'}.get(name)
 if not view:continue
 oldname=(q['outputHash']+'.png') if q['changedPixels'] else Path(q['source']).name
 visor=visors.get(oldname)
 current=(R/visor['output']) if visor else V/'frames'/oldname
 if not current.exists():continue
 current_hash=hashlib.sha256(current.read_bytes()).hexdigest()
 if 'frames/'+current_hash+'.png' not in idx['files']:continue
 before=np.array(Image.open(current).convert('RGBA'));old=Image.open(R/s['newHead']).convert('RGBA');new=Image.open(R/refined[view]['output']).convert('RGBA');mask=Image.open(R/refined[view]['mask']).convert('L')
 angle=s.get('rotationDegrees',0)
 if angle:
  old=old.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);new=new.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);mask=mask.rotate(angle,resample=Image.Resampling.NEAREST,expand=True)
 at=visor['newPaste'] if visor else s['newPaste'];old_layer=Image.new('RGBA',(before.shape[1],before.shape[0]));new_layer=old_layer.copy();ml=Image.new('L',old_layer.size)
 old_layer.alpha_composite(old,tuple(at));new_layer.alpha_composite(new,tuple(at));ml.paste(mask,tuple(at));oa=np.array(old_layer);na=np.array(new_layer)
 m=(np.array(ml)>0)&(oa[:,:,3]>220)&(before[:,:,3]>220)
 if visor:
  ap=Image.new('L',old_layer.size);ImageDraw.Draw(ap).polygon([tuple(p) for p in visor['polygon']],fill=255);m &= np.array(ap)>0
 else:
  # Only pixels still occupied by the authored portrait can change; preserve rim/collar foreground.
  difference=np.max(np.abs(before[:,:,:3].astype(int)-oa[:,:,:3].astype(int)),axis=2);m &= difference<=16
 if m.sum()<12:continue
 after=before.copy();delta=na[:,:,:3].astype(int)-oa[:,:,:3].astype(int);after[m,:3]=np.clip(before[m,:3].astype(int)+delta[m],0,255)
 changed=np.any(after!=before,axis=2);assert np.array_equal(before[:,:,3],after[:,:,3]);assert not np.any(changed&~m)
 if not changed.any():continue
 dest=H/'frames'/(current_hash+'.png');Image.fromarray(after).save(dest);Image.fromarray((m*255).astype('uint8')).save(H/'masks'/(current_hash+'.png'))
 patches[current_hash]=dest
 records.append({'source':'character/krusher-animation-package-v11/frames/'+current_hash+'.png','output':dest.relative_to(R).as_posix(),'example':q['example'],'frame':q['exampleFrame'],'view':view,'at':at,'changedPixels':int(changed.sum()),'mask':(H/'masks'/(current_hash+'.png')).relative_to(R).as_posix(),'alphaExact':True,'bodyAndEquipmentOutsideFaceExact':True})
for folder in ['frames','packs','references','verification']:(P/folder).mkdir(parents=True,exist_ok=True)
out=copy.deepcopy(idx);out['status']='V12 refined turn faces; original body, neck and helmet geometry retained; owner visual review pending';out['files']={};out['verification']='res://character/krusher-animation-package-v12/verification/face-validation.json';out['candidatePacks']={'bare':[],'helmet':[]};changed_states=[];holds=0
for gear in ['bare','helmet']:
 for path in idx['candidatePacks'][gear]:
  source=R/path[6:];data=read(source);destination=P/'packs'/source.name
  for state in data['states']:
   inputs=[];count=0
   for i,f in enumerate(state['frameFiles']):
    original=(source.parent/f).resolve();replacement=patches.get(original.stem,original);content=replacement.read_bytes();digest=hashlib.sha256(content).hexdigest();dest=P/'frames'/(digest+'.png')
    if not dest.exists():dest.write_bytes(content)
    state['frameFiles'][i]='../frames/'+dest.name;out['files']['frames/'+dest.name]={'sha256':digest,'bytes':len(content)};inputs.append(replacement.relative_to(R).as_posix());count+=replacement!=original
   entry=out['states'][gear+':'+state['id']];entry['manifest']='packs/'+destination.name;entry['sourceManifest']=source.relative_to(R).as_posix();entry['sourceFrames']=inputs
   if count:changed_states.append({'key':gear+':'+state['id'],'holds':count});holds+=count
  destination.write_text(json.dumps(data,indent=2));out['candidatePacks'][gear].append('res://'+destination.relative_to(R).as_posix())
for p in (V/'references').glob('*'):
 if p.is_file():shutil.copy2(p,P/'references'/p.name)
(P/'package.json').write_text(json.dumps(out,indent=2));summary={'drawings':len(records),'states':len(changed_states),'holds':holds,'stateChanges':changed_states,'records':records,'frameHolds':sum(len(v['sourceFrames']) for v in out['states'].values()),'totalStates':len(out['states']),'indexedPng':len(out['files'])}
(H/'face-validation.json').write_text(json.dumps(summary,indent=2));shutil.copy2(H/'face-validation.json',P/'verification/face-validation.json')
for page in range((len(records)+15)//16):
 board=Image.new('RGB',(1200,4*220),'#273239');d=ImageDraw.Draw(board)
 for j,q in enumerate(records[page*16:page*16+16]):
  x=j%4*300;y=j//4*220;d.text((x+3,y+3),q['example'].replace('swim-carry','loaded')+' / '+str(q['frame']),fill='white')
  mask=np.array(Image.open(R/q['mask']));ys,xs=np.where(mask>0);cx=(xs.min()+xs.max())/2;cy=(ys.min()+ys.max())/2;box=(round(cx-18),round(cy-21),round(cx+18),round(cy+25))
  for col,p in enumerate([q['source'],q['output']]):
   im=Image.open(R/p).convert('RGBA').crop(box);bg=Image.new('RGBA',im.size,'#273239');bg.alpha_composite(im);im=bg.convert('RGB').resize((144,184),Image.Resampling.NEAREST);board.paste(im,(x+col*150,y+25))
 board.save(H/('face-comparison-%02d.png'%page))
print({k:summary[k] for k in ['drawings','states','holds','frameHolds','totalStates','indexedPng']})
