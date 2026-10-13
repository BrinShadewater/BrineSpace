"""Re-export frozen authored pixels with fixed material/contour calibration."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion
from prepare_marsh_full_polish import material_mask,family,grade
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v4'
DIRS=('south','north','east','west')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def visual(im):
 crop=im.crop(im.getbbox());return hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest()
def policy(key):
 if key.startswith(('idle-','walk','crew-chat-','injury-','death-','torch-','weld')):return 'protected'
 return family(key)
def main():
 states=json.loads((BASE/'baseline-contract.json').read_text())['states'];images={};identities={};donors={};refs={};entries={}
 for rel in json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())['body']:
  data=json.loads((ROOT/'character/marsh-v2'/rel).read_text())
  for entry in data['states']:entries[entry['id']]=entry
 priority={'protected':0,'reference':0,'run':1,'cargo':2,'diagnostic':3,'seated':4,'galley':5,'rest':6,'recovery':6,'water':7,'loaded-water':8}
 for k,s in states.items():
  d=k.rsplit('-',1)[-1];group=policy(k)
  for i,(f,h) in enumerate(zip(s['files'],s['hashes'])):
   assert sha(ROOT/f)==h,f
   im=images.setdefault(f,Image.open(ROOT/f).convert('RGBA'));v=visual(im);m,l,_=material_mask(im)
   if v not in identities or priority[group]<priority[identities[v][0]]:identities[v]=(group,d)
   if '-turn-' not in k and m.sum()>80:donors.setdefault((group,d),[]).append(float(l[m].mean()))
   if k.startswith('idle-') and i==0:refs[d]=float(l[m].mean())
 fits={}
 for (group,d),values in donors.items():
  target=refs[d];median=float(np.median(values));gap=median-target
  gain=1.0
  if group in ('diagnostic','rest','seated','galley','water','loaded-water') and abs(gap)>=9:gain=float(np.clip(target/median,.94,1.06))
  fits[group+'-'+d]={'reference':target,'sourceMedian':median,'gain':gain}
 mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
 cache={};records={};outstates=[];selections={};changes=0
 for k,s in states.items():
  files=[]
  for i,f in enumerate(s['files']):
   orig=images[f];v=visual(orig);group,d=identities[v];gain=fits.get(group+'-'+d,{}).get('gain',1.0)
   # Cache actual artwork, independently of transparent turn padding.
   if v not in cache:
    crop=orig.crop(orig.getbbox());out=grade(crop,gain,mapper)[0] if group!='protected' else crop.copy()
    a=np.array(out);before=np.array(crop);_,_,head=material_mask(crop)
    opacity=a[:,:,3]>0;edge=opacity&~binary_erosion(opacity,iterations=2)
    contour=edge&(a[:,:,:3].mean(2)<18)&~head if group!='protected' else np.zeros(edge.shape,bool)
    # Quiet charcoal contour from the existing palette; geometry/detail stays.
    lifted=a.copy();lifted[contour,:3]=[27,31,33]
    mapped=np.array(mapper(Image.fromarray(lifted)));a[contour]=mapped[contour]
    if group=='diagnostic':
     y=np.arange(crop.height)[:,None]+orig.getbbox()[1]
     locked=np.broadcast_to((y<58)|(y>=145),a.shape[:2])
     a[locked]=before[locked]
    assert np.array_equal(a[:,:,3],before[:,:,3])
    cache[v]=(Image.fromarray(a),gain,int(contour.sum()))
   crop,gain,edgepixels=cache[v];out=orig.copy();out.paste(crop,orig.getbbox()[:2]);changed=not np.array_equal(np.array(out),np.array(orig))
   if changed:
    p=BASE/f'frames/{k}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);out.save(p);rel=p.relative_to(ROOT).as_posix();files.append(rel)
    records[rel]={'sha256':sha(p),'actor':'marsh','source':f,'sourceSha256':sha(ROOT/f),'gain':gain,'contourPixels':edgepixels,'visualIdentity':v}
    changes+=1
   else:files.append(f)
  selections[k]=files
  if files!=s['files']:
   entry=dict(entries[k]);entry['frameFiles']=[Path('../../'+f).as_posix() for f in files]
   outstates.append((entry,s['pivot'],s['standingHeight']))
 # Paths in a sibling manifest resolve relative to that manifest.
 groups={}
 for entry,pivot,height in outstates:groups.setdefault((tuple(pivot),height),[]).append(entry)
 manifest_paths=[]
 for (pivot,height),group in groups.items():
  name='manifest-p'+str(pivot[0]).replace('.','_')+'-'+str(pivot[1]).replace('.','_')+'.json'
  manifest={'revision':'marsh-fullset-v4','pivot':pivot,'standingHeight':height,'textureFilter':'nearest','states':group}
  (BASE/name).write_text(json.dumps(manifest,indent=2)+'\n');manifest_paths.append('../marsh-quality-pass-v4/'+name)
 (BASE/'manifest-list.json').write_text(json.dumps(manifest_paths,indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'fits':fits,'changedStates':len(outstates),'changedSlots':changes,'policy':'Fixed family/direction material gain, restrained existing-palette contour lift. Identical cropped poses share one result; no resizing, alpha changes, new texture or fabricated detail. Idle/walk/crew chat/injury/shutdown/welding protected.'},indent=2)+'\n')
 (BASE/'selection.json').write_text(json.dumps({'states':selections,'changedStates':[entry['id'] for entry,_,_ in outstates]},indent=2)+'\n')
 frozen_entries=BASE/'original-state-entries.json'
 if not frozen_entries.exists():frozen_entries.write_text(json.dumps(entries,indent=2)+'\n')
 print(len(outstates),'changed states;',changes,'graded frame slots;',len(states),'states reviewed')
 print('Material fits:',[(k,round(v['gain'],3)) for k,v in fits.items() if v['gain']!=1])
if __name__=='__main__':main()
