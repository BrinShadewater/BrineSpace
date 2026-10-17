"""Validate the current directional set and its separable transition layers."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy import ndimage
from PIL import Image
R=Path(__file__).resolve().parent;d=json.loads((R/'manifest.json').read_text());clips={e['id']:e for e in d['states']}
assert len(clips)==92 and len(d['headings'])==8
selected=sys.argv[1:] or list(d['headings']);assert set(selected)<=set(d['headings'])
states=[e for e in d['states'] if e['heading'] in selected]
hashes={};alpha={};checks=[];count=0;seams={}
def digest(path,body=False):
 if path not in hashes:
  im=Image.open(R/path).convert('RGBA');assert im.size==(512,512);hashes[path]=hashlib.sha256(im.tobytes()).digest();alpha[path]=hashlib.sha256(im.getchannel('A').tobytes()).digest()
  bb=im.getbbox();assert bb is None or (min(bb[:2])>0 and max(bb[2:])<512),(path,bb)
  if body:
   assert bb is not None
   ar=np.array(im);labels,_=ndimage.label(ar[:,:,3]>128);sizes=np.bincount(labels.ravel())[1:]
   assert int((sizes>=80).sum())==1,(path,'detached substantial component',sizes[sizes>=80].tolist())
 return hashes[path]
for e in states:
 assert len(e['frameFiles'])==len(e['cargoFiles'])==len(e['phases'])==e['frameCount']
 atlas=Image.open(R/e['atlas']['path']).convert('RGBA');cargo=Image.open(R/e['cargoAtlas']['path']).convert('RGBA')
 for n,(bp,cp) in enumerate(zip(e['frameFiles'],e['cargoFiles'])):
  box=(n%6*512,n//6*512,(n%6+1)*512,(n//6+1)*512)
  assert digest(bp,True)==hashlib.sha256(atlas.crop(box).tobytes()).digest(),(e['id'],n,'body parity')
  assert digest(cp)==hashlib.sha256(cargo.crop(box).tobytes()).digest(),(e['id'],n,'cargo parity')
  count+=1
 assert len(e['lampSamples'])==e['frameCount'] and all(0<=x<=1 for x in e['lampSamples'])
 spin=e['rotorPhaseSamples'];assert len(spin)==e['frameCount']
 steps=np.diff(spin)
 assert all(steps<=1e-8) if e['state']=='reverse' else all(steps>=-1e-8),(e['id'],'spin reversed unexpectedly')
 if e['state']=='power-off':assert max(abs(x) for x in steps[-10:])<1e-8
 if e['state']=='power-on':assert e['lampSamples'][0]==0 and e['lampSamples'][-1]==1
 if e['state']=='power-off':assert e['lampSamples'][0]==1 and e['lampSamples'][-1]==0
 checks.append({'clip':e['id'],'frames':e['frameCount'],'result':'pass'})
for h,m in d['headings'].items():
 if h not in selected:continue
 assert digest(m['pose'])==digest(clips['idle-'+h]['frameFiles'][0]),(h,'resting pixels changed')
 rotor=Image.open(R/m['rotorAtlas']['path']).convert('RGBA');reference=None;rotor_frames=[]
 for n in range(60):
  a=rotor.crop((n%6*512,n//6*512,(n%6+1)*512,(n//6+1)*512)).getchannel('A').tobytes()
  if reference is None:reference=a
  assert a==reference,(h,n,'rotor silhouette')
  rotor_frames.append(np.array(rotor.crop((n%6*512,n//6*512,(n%6+1)*512,(n//6+1)*512)),dtype=np.int16))
 diffs=[float(np.abs(rotor_frames[(n+1)%60]-rotor_frames[n]).mean()) for n in range(60)]
 assert diffs[-1]<=max(diffs[:-1])*1.5+1e-6,(h,'rotor loop seam',diffs[-1],max(diffs[:-1]))
 seams[h]={'wrapMeanDifference':diffs[-1],'largestInteriorDifference':max(diffs[:-1])}
 for state in ['idle','swim','reverse','carry','start','stop','power-on','power-off','charging','disabled']:assert state+'-'+h in clips
 if h in ['north','east','south','west']:
  grab=clips['retrieve-'+h];release=clips['release-'+h];carry=clips['carry-'+h];blocked=clips['blocked-'+h]
  assert alpha[grab['frameFiles'][-1]]==alpha[carry['frameFiles'][0]]==alpha[release['frameFiles'][0]],h
  assert digest(grab['cargoFiles'][-1])==digest(carry['cargoFiles'][0])==digest(release['cargoFiles'][0]),h
  assert alpha[blocked['frameFiles'][0]]==alpha[blocked['frameFiles'][-1]],h
for source in d['sourceFiles']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256']
result={'clips':len(states),'headings':len(selected),'selectedHeadings':selected,'manifestClips':len(clips),'bodyFrameReferences':count,'cargoFrameReferences':count,'uniqueImageFilesChecked':len(hashes),'atlasParity':'all selected frames','bounds':'pass','connectedBodySilhouettes':'pass','rotorLayerPhases':60*len(selected),'clawCargoJoins':'pass','powerLampEndpoints':'pass','sourceHashes':'pass','checks':checks}
result['rotorLoopSeams']=seams
report='full-validation.json' if not sys.argv[1:] else 'validation-'+ '-'.join(selected)+'.json'
(R/'review'/report).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','rotorLoopSeams']}))
