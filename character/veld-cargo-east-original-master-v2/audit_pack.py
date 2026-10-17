from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;rows=[]
case=np.array(Image.open(P/'shared-floor-case.png').convert('RGBA'));reg=json.loads((P/'shared-case-registration.json').read_text(encoding='utf-8'));cx,cy=reg['sharedCompleteCase']['position'];shared=Image.new('RGBA',(256,256));shared.alpha_composite(Image.fromarray(case),(cx,cy));shared=np.array(shared)
for gear in ['bare','helmet']:
 pack=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));states={s['id']:s for s in pack['states']}
 held=np.array(Image.open(R/f'character/veld-east-held-original-master-v1/frames/{gear}/000.png').convert('RGBA'));assert np.array_equal(np.array(Image.open(P/f'frames/{gear}/000.png')),held);checks+=1
 assert sum(states['unload-east']['frameDurationsMs'])==520;checks+=1
 assert states['pickup-east']['frameFiles']==states['unload-east']['frameFiles'][::-1];checks+=1
 for i in range(3,6):
  out=np.array(Image.open(P/f'frames/{gear}/{i:03}.png').convert('RGBA'));exposed=(shared[:,:,3]==255)&(out[:,:,3]==255)&np.all(out[:,:,:3]==shared[:,:,:3],axis=2);rows.append({'gear':gear,'pose':i,'exposedExactCasePixels':int(exposed.sum())});assert exposed.sum()>0;checks+=1
original=Image.new('RGBA',(256,256));original.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52));old=np.array(original);end=np.array(Image.open(P/'frames/bare/005.png').convert('RGBA'));outside_case=shared[:,:,3]==0;assert np.array_equal(old[outside_case],end[outside_case]);checks+=1
contact=[]
for i in range(6):
 a=np.array(Image.open(P/f'frames/bare/{i:03}.png').convert('RGBA'));y,x=np.where(a[216:225,90:137,3]>200);sel=y>=y.max()-1;contact.append({'pose':i,'nearFloor':int(y.max()+216),'nearBottomMeanX':float((x[sel]+90).mean())})
paths=[P/'build_shared_case.py',P/'register_contacts.py',P/'contact-registration.json',P/'shared-case-registration.json',P/'shared-floor-case.png',P/'whole-floor-case-reference.png',P/'whole-deep-pose-reference.png',R/'character/veld-side-foundation-v1/east-standing.png',R/'character/veld-cargo-turns-master-family-v1/original-east-density-reference.png'];paths+=list(P.glob('raw-*.png'))+list(P.glob('prompt-*.txt'))+list(P.glob('*-manifest.json'))+list((P/'frames').rglob('*.png'))
report={'checks':checks,'failures':0,'casePixels':rows,'nearContacts':contact,'originalEmptyBodyOutsideCompleteCaseExact':True,'bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'Exact held entry and original empty body, complete repeated deposited equipment/source reversals. Contact occlusion and held-to-deposited physical case scale require visual proof. Pixel equality cannot accept grip/anatomy/material.'};(P/'source-record.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='bindings'}))
