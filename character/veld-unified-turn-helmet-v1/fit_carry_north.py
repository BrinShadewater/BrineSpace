"""Fix rear carry helmet crown/axis against bare gait and shared idle master."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from registration import CLEAR_BOX,PROTECTED_BOX
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=ROOT/'character/veld-carry-north-consistent-v1'
master=Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA');landmarks=json.loads((OLD/'checks.json').read_text())['helmet_head_landmarks'];checks=0;positions=[];paths=[];contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact)
for i in range(6):
    bare=Image.open(OLD/f'frames/bare/{i:03}.png').convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);crown=int(y.min());center=landmarks[i][0]
    base=Image.open(OLD/f'frames/helmet/{i:03}.png').convert('RGBA');out=base.copy();out.paste((0,0,0,0),CLEAR_BOX);pos=(center-16,crown-7);out.alpha_composite(master,pos)
    before=np.array(base);after=np.array(out);mask=np.ones((256,256),bool);mask[65:109,96:169]=False
    assert np.array_equal(before[mask],after[mask]);checks+=1
    yy,xx=np.where(after[:,:,3]>200);assert int(yy.min())==crown-7;checks+=1
    assert not np.any(np.concatenate([after[0,:,3],after[-1,:,3],after[:,0,3],after[:,-1,3]])>20);checks+=1
    path=f'frames/helmet/carry-north/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);out.save(HERE/path);paths.append(path);positions.append({'slot':i,'bareCrown':crown,'position':pos,'bodySha256':hashlib.sha256((OLD/f'frames/helmet/{i:03}.png').read_bytes()).hexdigest()})
    for row,im in enumerate([base,out]):contact.alpha_composite(im,(i*256,row*280+24));draw.text((i*256+4,row*280+4),f'{"previous" if row==0 else "master crown"} / {i}',fill='white')
m=json.loads((OLD/'helmet-manifest.json').read_text());m.update(name='Veld rear carry master helmet registration',status='installed_master_registration_pending_owner_review');m['states'][0]['frameFiles']=paths
(HERE/'carry-north-helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');(HERE/'carry-north-registration-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'positions':positions,'bodyBelow109Exact':True,'masterRelativeCrownDelta':-7,'noScalingOrGradeChange':True,'installed':True},indent=2)+'\n');contact.save(HERE/'carry-north-registration-v2.png')
print(f'{checks} rear-carry head/body/alpha checks, 0 failures.')
