from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-original-motion-v1';D=P/'motion-review-v1'
data=json.loads((O/'records.json').read_text());runs=[]
for gear in ['bare','helmet']:
    current=[];side=''
    for row in [r for r in data['records'] if r['gear']==gear]:
        # Original source support order after phase rotation2,3,4,5,0,1.
        nextside={1:'right',2:'right',4:'left',5:'left'}.get(row['slot'],'') if row['action']=='carry-north' else ''
        if side and side!=nextside:
            if len(current)>1:
                drift=max(r['worldToeY'] for r in current)-min(r['worldToeY'] for r in current)
                runs.append({'gear':gear,'support':side,'start':current[0]['time'],'end':current[-1]['time'],'sampleCount':len(current),'supportWorldYDrift':round(drift,4),'screenDriftAt93':round(drift*93/65.28,3),'records':current})
            current=[]
        side=nextside
        if not side:continue
        a=np.array(Image.open(O/(row['name']+'-source.png')).convert('RGBA'))
        x0,x1=(96,128) if side=='left' else (128,166)
        yy,xx=np.where(a[195:230,x0:x1,3]>200);assert len(yy)>0
        toeY=int(yy.max()+195)
        current.append({'name':row['name'],'time':row['time'],'slot':row['slot'],'toeNativeY':toeY,'worldToeY':-row['travel']+(toeY-224)*65.28/148})
    if side and len(current)>1:raise AssertionError('Final support segment should end before stop')
maximum=max(r['supportWorldYDrift'] for r in runs)
report={'scope':'Diagnostic sole-bottom support trace on prescribed movement study, not anatomical/contact controller proof. Source slots1/2 screenRIGHT support;4/5 screenLEFT support. Toe proxy uses bottom opaque boot in fixed side region.','runs':runs,'maxSupportWorldYDrift':maximum,'contactConsistency':'failed' if maximum>2 else 'within2worldUnits','finding':'Distance phase and monotonic travel tests passed, but the grounded boot travels with the body during its support segment. Source floor equality does not establish world foot planting. Whole-source gait/contact or stride/cadence must be revised before contact acceptance.'}
(D/'contact-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'runs':len(runs),'maxSupportWorldYDrift':maximum,'screenDriftAt93':max(r['screenDriftAt93'] for r in runs),'contactConsistency':report['contactConsistency']}))
