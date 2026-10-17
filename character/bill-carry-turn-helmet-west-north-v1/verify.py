"""Check packaging and narrow fitting invariants; no visual acceptance claim."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
def main():
 pack=json.loads((HERE/'manifest.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());registration=json.loads((HERE/'helmet-registration.json').read_text());checks=0
 assert pack['pivot']==[128,224] and pack['frameWidth']==256 and pack['frameHeight']==256;checks+=1
 assert len(pack['states'])==2;checks+=1
 forward,reverse=pack['states'];images=[]
 for state in pack['states']:
  assert len(state['frameFiles'])==6 and sum(state['frameDurationsMs'])==800 and not state['loop'];checks+=1
  for file in state['frameFiles']:
   path=HERE/file;im=Image.open(path);a=np.array(im)
   assert im.size==(256,256) and im.mode=='RGBA';checks+=1
   assert hashlib.sha256(path.read_bytes()).hexdigest()==hashes[file];checks+=1
   assert np.any(a[:,:,3]==0) and np.any(a[:,:,3]>180);checks+=1
 for f,r in zip(forward['frameFiles'],reversed(reverse['frameFiles'])):
  assert np.array_equal(np.array(Image.open(HERE/f)),np.array(Image.open(HERE/r)));checks+=1
 for index,authority in zip([0,5],registration['endpointAuthorities']):
  assert np.array_equal(np.array(Image.open(HERE/forward['frameFiles'][index])),np.array(Image.open(HERE.parent/authority)));checks+=1
 for record in registration['frames']:
  file=forward['frameFiles'][record['frame']];protected=record['protectedBodyFromY'];result=np.array(Image.open(HERE/file));original=np.array(Image.open(HERE.parent/'bill-carry-turn-west-north-v1'/file))
  assert np.array_equal(result[protected:],original[protected:]);checks+=1
  # Lanczos edges are partly transparent; compare qualified sole contact to
  # the accepted original instead of requiring an opaque pixel on row223.
  ys=np.where(result[:,:,3]>180)[0];original_ys=np.where(original[:,:,3]>180)[0]
  assert ys.max()==original_ys.max() and 220<=ys.max()<=224 and result[225:,:,3].max()==0;checks+=1
 assert reverse['frameDurationsMs']==list(reversed(forward['frameDurationsMs']));checks+=1
 report={'passed':True,'checks':checks,'scope':'frames,alpha,hashes,800ms timing,pivot,exact equipped endpoints,reverse equality,protected original body/boots','ownerVisualAcceptance':False,'installed':False,'nativePlayback':False}
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(f'{checks} checks PASS;staged candidate;visual/native acceptance separate')
if __name__=='__main__':main()
