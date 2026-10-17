"""Validate registration/endpoints/reverse playback; owner motion review is separate."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'manifest.json').read_text());r=json.loads((HERE/'registration.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0
def check(value,message):
 global checks
 assert value,message
 checks+=1
check((p['frameWidth'],p['frameHeight'],p['pivot'],p['standingHeight'])==(256,256,[128,224],148),'profile')
a,b=p['states'];arrays=[]
for s in p['states']:
 check(not s['loop'] and not s['water'],'one-shot dry')
 check(sum(s['frameDurationsMs'])==800,'retained quarter duration')
 check(len(s['frameFiles'])==len(s['frameDurationsMs'])==len(s['facings'])==6,'metadata lengths')
 for file in s['frameFiles']:
  path=HERE/file;im=Image.open(path).convert('RGBA');data=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas')
  check(box is not None and min(box[0],box[1],256-box[2],256-box[3])>=4,'not clipped')
  check(int((data[:,:,3]>180).sum())>3000,'figure alpha')
  check(hashlib.sha256(path.read_bytes()).hexdigest()==hashes[file],'hash')
  check(220<=box[3]<=227,'foot registration')
  fy,fx=np.where(data[195:,:,3]>180);check(int(fx.max()-fx.min())<=58,'boots under body rather than extended stride')
for i in range(6):check(np.array_equal(np.array(Image.open(HERE/a['frameFiles'][i])),np.array(Image.open(HERE/b['frameFiles'][5-i]))),'exact reverse')
for i,index in enumerate([0,5]):check(np.array_equal(np.array(Image.open(HERE/a['frameFiles'][index])),np.array(Image.open(HERE.parent/r['endpointAuthorities'][i]))),'exact loaded neutral endpoints')
check(len(set(hashes.values()))==6,'six distinct poses')
check(all(f['scale']==r['scale'] for f in r['frames']),'frozen scale')
check(all(f['scaleX']==r['scaleX'] for f in r['frames']),'frozen horizontal anatomy calibration')
for i in range(1,5):
 arr=np.array(Image.open(HERE/a['frameFiles'][i]));xs=np.where(arr[110,:,3]>180)[0]
 check(int(np.ptp(xs)+1)<=48,'intermediate shoulders do not exceed frontal authority')
check([f['sourceCell'] for f in r['frames']]==[1,2,3,4],'selected intermediates')
from turn_material import cloth_samples
target=float(np.mean([np.median(cloth_samples(Image.open(HERE/a['frameFiles'][i]))) for i in [0,5]]))
for i in range(1,5):
 file=a['frameFiles'][i];im=Image.open(HERE/file);arr=np.array(im);old=np.array(Image.open(HERE/'review-ungraded-master-v3'/file))
 check(np.array_equal(arr[:,:,3],old[:,:,3]),'color pass retains alpha/geometry')
 check(np.array_equal(arr[:104],old[:104]),'face/hair retain original pixels')
 check(abs(float(np.median(cloth_samples(im)))-target)<=4,'suit midtones remain near endpoint grade')
(HERE/'color-verification.json').write_text(json.dumps({'endpointClothMedian':target,'turnClothMedians':[float(np.median(cloth_samples(Image.open(HERE/f)))) for f in a['frameFiles']],'maxAllowedDifference':4,'geometryPreserved':True},indent=2)+'\n')
(HERE/'verification.json').write_text(json.dumps({'checksPassed':checks,'status':'pass','scope':'packaging,registration,endpoint and reverse continuity;not native or owner visual acceptance'},indent=2)+'\n')
print(checks,'checks passed')
