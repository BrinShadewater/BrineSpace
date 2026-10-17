"""Independent full-crown completeness audit, including gray hair and soft edges."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'head-registration.json').read_text());yy,xx=np.indices((256,256));rows=[]
for d in reg['directions']:
 master=np.array(Image.open(R/d['master']).convert('RGBA'));head=np.array(Image.open(P/d['componentFile']).convert('RGBA'));x0,y0,x1,y1=d['sourceBox'];full=np.zeros_like(master);full[y0:y1,x0:x1]=head;top=int(np.where((master[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166))[0].min());crown=(master[:,:,3]>0)&(yy>=top)&(yy<top+14)&(xx>=105)&(xx<145);missing=crown&np.any(master!=full,axis=2);ys=np.where(missing)[0]
 rows.append({'direction':d['direction'],'masterTopY':top,'componentTopY':y0,'missingCrownPixels':int(missing.sum()),'missingOpaqueCrownPixels':int((missing&(master[:,:,3]>160)).sum()),'missingRows':sorted(set(int(y) for y in ys)),'componentSha256':hashlib.sha256((P/d['componentFile']).read_bytes()).hexdigest()})
report={'scope':'Full14-row master crown coverage, native source pixels and alpha; not face/collar/whole motion acceptance','directions':rows};(P/'crown-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows))
