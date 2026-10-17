from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent
for d in ['east','south','west','north']:
 p=P.parent/('james-water-'+d+'-v1');m=json.loads((p/'bare-manifest.json').read_text());state=next(s for s in m['states'] if s['id']=='swim-'+d)
 im=Image.open(p/state['frameFiles'][0]).convert('RGBA');im=im.crop(im.getbbox());im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(P.parent/('james-air-'+d+'-v1')/'prone-master-reference.png')
