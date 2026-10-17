from pathlib import Path
import json,numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation,label
P=Path(__file__).resolve().parent;R=P.parent.parent;rows=[]
for q in json.loads((P/'revision.json').read_text())['records']:
 if q['gear']!='bare' or 'paste' not in q['details']:continue
 b=np.array(Image.open(P/q['output']).convert('RGBA'));head=np.array(Image.open(R/q['details']['headSource'][6:]).convert('RGBA'));x,y=q['details']['paste'];hm=np.zeros(b.shape[:2],bool);hm[y:y+head.shape[0],x:x+head.shape[1]]=head[:,:,3]>180
 if q['details'].get('foregroundFromRow') is not None:hm[q['details']['foregroundFromRow']:]=False
 contact_region=hm.copy();up=q['state'].endswith('-south') and q['details'].get('foregroundFromRow') is not None
 if up:contact_region[y+head.shape[0]//4:]=False
 else:contact_region[:y+head.shape[0]*3//4]=False
 body=(b[:,:,3]>180)&~hm;contact=int((binary_dilation(contact_region)&body).sum());lab,n=label(b[:,:,3]>180);largest=np.bincount(lab.ravel())[1:].argmax()+1;joined=bool(np.all(lab[hm]==largest));rows.append({'state':q['state'],'frame':q['frame'],'neckSide':'upper/back crown toward body' if up else 'lower jaw/neck toward body','headAdjacentRetainedBodyPixels':contact,'opaqueHeadInMainBodyComponent':joined})
result={'scope':'Pose-aware original-body edge adjacency and silhouette connected component; raster contact does not certify anatomical quality. In South prone swimming the body is above head, so neck-side test uses upper/back crown.','records':rows,'errors':[q for q in rows if not q['opaqueHeadInMainBodyComponent'] or not q['headAdjacentRetainedBodyPixels']]};(P/'neck-edge-contact.json').write_text(json.dumps(result,indent=2)+'\n');print({'barePoses':len(rows),'minimumEdgeContact':min(q['headAdjacentRetainedBodyPixels'] for q in rows),'errors':result['errors']});assert not result['errors']
