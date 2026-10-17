from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
P=Path(__file__).resolve().parent;V=P/'continuous-video-v1';V.mkdir(exist_ok=True);reg=json.loads((P/'source-registration-v2.json').read_text(encoding='utf-8'));raw=Image.open(P/'raw-gait-v2.png').convert('RGBA');whole=raw.crop(tuple(reg['rows'][0]['cell']));a=np.array(whole);labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;keep=np.isin(labels,np.where(counts>=50)[0]);a[~ndimage.binary_dilation(keep,iterations=3)]=0;whole=Image.fromarray(a);whole.save(V/'whole-source-reference.png');plate=Image.new('RGBA',(768,1024),(0,255,0,255));offset=(190,130);plate.alpha_composite(whole,offset);plate.convert('RGB').save(V/'master-input.png')
record={'sourceGeneration':'1310316f-87b9-4f29-8b5f-42ca0790e7c0','sourceCell':reg['rows'][0]['cell'],'wholeFigureOffset':list(offset),'sourceRescaling':False,'scope':'Complete source figure on flat chroma plate; no limb/RGB/grade changes. Video must preserve original proportions/material and actual contact progression.','inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [V/'master-input.png',V/'whole-source-reference.png']}};(V/'input-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('Complete source chroma plate saved768x1024; source pixels unscaled')
