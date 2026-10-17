from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
sources=[P.with_name('west-sample-family-v1'),P];results={}
for folder in sources:
 if not (folder/'SOURCE_REVIEW.json').exists():continue
 report=json.loads((folder/'SOURCE_REVIEW.json').read_bytes());rows=[]
 for item in report['frames']:
  a=np.array(Image.open(folder/f'frames/bare/{item["frame"]:03}.png').convert('RGBA'))
  # Fixed ground band and original front-foot side. Not an inferred contact solver.
  yy,xx=np.where(a[218:226,:133,3]>200)
  rows.append({'frame':item['frame'],'visibleFrontGroundLeft':int(xx.min()) if len(xx) else None,'visibleFrontGroundRight':int(xx.max()) if len(xx) else None,'floor':item['floor']})
 vals=[x['visibleFrontGroundLeft'] for x in rows if x['visibleFrontGroundLeft'] is not None];baseline=rows[0]['visibleFrontGroundLeft']
 results[folder.name]={'baselineFrontGroundLeft':baseline,'visibleFrontGroundLeftRange':[min(vals),max(vals)],'maximumLeftShiftFromStart':baseline-min(vals),'rows':rows,'scope':'Fixed218..225 native ground band,x<133,alpha>200. Visible pixels only; does not establish pressure/contact or separate feet under occlusion.'}
(P/'CONTACT_REVIEW.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:{x:v[x] for x in ['baselineFrontGroundLeft','visibleFrontGroundLeftRange','maximumLeftShiftFromStart']} for k,v in results.items()}))
