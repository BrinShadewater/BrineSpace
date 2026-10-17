"""Package nonfatal impact and recovery from selected, authored Marsh poses."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-injury-runtime-v1';POLISH=ROOT/'character/marsh-full-polish-v1'

def main():
    BASE.mkdir(parents=True,exist_ok=True);selected=json.loads((POLISH/'selection.json').read_text());states=[];records={};derivations=[]
    for d in ('south','north','east','west'):
        dry=[Image.open(ROOT/f).convert('RGBA') for f in selected['states']['death-ground-'+d]];injury=[Image.open(ROOT/f).convert('RGBA') for f in selected['stagedFrames']['injury-ground-'+d]]
        a=np.asarray(injury[-1]);b=np.asarray(dry[-1]);rgb=a[:,:,:3].astype(float)
        # Existing white fluid outside the body becomes a transient floor effect.
        mask=(a[:,:,3]>0)&(b[:,:,3]==0)&(rgb.max(2)-rgb.min(2)<18)&(rgb.mean(2)>140)
        fluid=np.zeros_like(a);fluid[mask]=a[mask]
        for action in ('injury-ground','injury-rise'):
            files=[]
            for i in range(6):
                p=BASE/f'frames/{action}-{d}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True)
                if action=='injury-ground':shutil.copy2(ROOT/selected['stagedFrames'][action+'-'+d][i],p)
                else:
                    im=dry[5-i].copy();overlay=Image.fromarray(fluid.copy());alpha=np.asarray(overlay.getchannel('A')).copy()
                    # Retain white fluid through recovery; expire the temporary
                    # effect in its last two poses, ending at exact selected idle.
                    if i==4:alpha=(alpha*.5).astype('uint8')
                    if i==5:alpha[:]=0
                    overlay.putalpha(Image.fromarray(alpha));overlay.alpha_composite(im)
                    if i==0:overlay=injury[-1].copy()
                    overlay.save(p)
                rel=p.relative_to(ROOT).as_posix();files.append(p.relative_to(BASE).as_posix());records[rel]={'source':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'actor':'marsh'}
                derivations.append({'frame':rel,'fluidSource':selected['stagedFrames']['injury-ground-'+d][-1],'bodySource':selected['stagedFrames']['injury-ground-'+d][i] if action=='injury-ground' else selected['states']['death-ground-'+d][5-i],'method':'Exact selected injury pose' if action=='injury-ground' else 'Reverse selected dry collapse; composite existing white-fluid floor pixels; transient effect fades at standing endpoint'})
            states.append({'id':action+'-'+d,'frameFiles':files,'frameDurationsMs':[180]*6,'loop':False})
    (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-nonfatal-injury-v1','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
    (BASE/'installation.json').write_text(json.dumps({'frameCount':48,'frames':records,'derivations':derivations},indent=2)+'\n')
    p=ROOT/'character/marsh-v2/catalog.json';catalog=json.loads(p.read_text());entry='../marsh-injury-runtime-v1/manifest.json'
    if entry not in catalog['body']:catalog['body'].append(entry);p.write_text(json.dumps(catalog,indent=2)+'\n')
    print('Packaged eight injury/recovery states / 48 frames from selected sources')

if __name__=='__main__':main()
