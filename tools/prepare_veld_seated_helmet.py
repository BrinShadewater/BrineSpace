"""Pose-fit canonical Veld helmet heads to the unselected east seating study."""
import json
import numpy as np
from PIL import Image
from prepare_veld_seated_identity import BASE,main as prepare_body
from prepare_veld_east_identity_chain import head_layer
from rebuild_bill_art import binary,chroma

def main():
    prepare_body()
    raw=binary(chroma(BASE/'sources/east-sample-heads-01.png'))
    folder=BASE/'review/seated-east-body-01';records=[];rows={}
    for key in ['sit-down-east','sit-idle-east']:
        poses=[]
        for i in range(6):
            body=Image.open(folder/f'{key}-{i:03}.png').convert('RGBA');top=body.getbbox()[1]
            _,xs=np.where(np.asarray(body)[top:top+12,:,3]>0);center=float(xs.min()+xs.max())/2
            anchor=(round(center+3),top+27)
            slot=2 if key=='sit-down-east' and i in [2,3] else 0
            layer=head_layer(raw,1,slot,anchor);pose=body.copy()
            pose.paste((0,0,0,0),(round(center-18),top-5,round(center+19),top+22))
            pose.paste((0,0,0,0),(round(center-10),top+22,round(center+14),top+28))
            pose.alpha_composite(layer)
            assert np.array_equal(np.asarray(body)[top+29:],np.asarray(pose)[top+29:]),'Preserve body below collar'
            poses.append(pose);records.append(dict(state=key,frame=i,anchor=anchor,slot=slot))
        rows[key]=poses
    rows['sit-down-east'][0]=Image.open(BASE/'review/east-chain-01/helmet-idle-east-000.png').convert('RGBA')
    rows['sit-idle-east'][0]=rows['sit-down-east'][5].copy()
    rows['sit-idle-east'][5]=rows['sit-down-east'][5].copy()
    rows['sit-rise-east']=list(reversed(rows['sit-down-east']))
    sheet=Image.new('RGB',(1536,1536),'#293b40')
    for row,(key,poses) in enumerate(rows.items()):
        for i,pose in enumerate(poses):
            pose.save(folder/f'helmet-{key}-{i:03}.png')
            body=Image.open(folder/f'{key}-{i:03}.png');sheet.paste(body,(i*256,row*512),body);sheet.paste(pose,(i*256,row*512+256),pose)
    sheet.save(folder/'paired-contact.png')
    (folder/'helmet-registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger',source='sources/east-sample-heads-01.png',records=records,limits=['Review collar masks and pose fit at native scale before selection.']),indent=2)+'\n')
    print('Prepared 18 fitted helmet poses; exact idle/seated/rise endpoints.')
if __name__=='__main__':main()
