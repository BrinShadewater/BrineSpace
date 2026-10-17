from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-bunk-east-master-v1'
board=Image.new('RGB',(8*256,4*280),'#303b40');d=ImageDraw.Draw(board);checks=[];records=[]
for gi,mode in enumerate(['bare','helmet']):
    manifest=json.loads((S/(mode+'-manifest.json')).read_bytes());states={s['id']:s for s in manifest['states']}
    frames={action:[Image.open(S/rel).convert('RGBA') for rel in states[action+'-east']['frameFiles']] for action in ['bunk-enter','bunk-sleep','bunk-exit']}
    master=frames['bunk-enter'][0]
    checks += [{'mode':mode,'label':'reverse exit','pass':all(a.tobytes()==b.tobytes() for a,b in zip(frames['bunk-enter'],reversed(frames['bunk-exit'])))},{'mode':mode,'label':'exact sleep joins','pass':frames['bunk-enter'][-1].tobytes()==frames['bunk-sleep'][0].tobytes()==frames['bunk-exit'][0].tobytes()},{'mode':mode,'label':'entry exit clock1840ms','pass':all(sum(states[a+'-east']['frameDurationsMs'])==1840 for a in ['bunk-enter','bunk-exit'])}]
    for ai,action in enumerate(['bunk-enter','bunk-exit']):
        row=gi*2+ai
        for col,im in enumerate([master,*frames[action]]):
            at=(col*256,row*280+24);board.paste(im,at,im);d.text((at[0]+4,at[1]-19),mode+' '+('master' if col==0 else action+' '+str(col-1)),fill='white')
    for action,imgs in frames.items():
        for i,im in enumerate(imgs):records.append({'mode':mode,'action':action,'index':i,'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'bounds':im.getchannel('A').getbbox()})
board.save(P/'paired-selected-bunk-source.png')
(P/'source-evidence.json').write_text(json.dumps({'checks':checks,'failures':sum(not c['pass'] for c in checks),'records':records,'sleepSourceFramesPerGear':1,'scope':'Thirty actual selected East bunk references, fixed canonical source canvas. Static bunk sleep hold, exact reverse exits and shared joins; visual furniture contact must be judged from actual native journeys.'},indent=2)+'\n')
print(len(records),'selected bunk refs;',len(checks),'source clock/join checks;',sum(not c['pass'] for c in checks),'failures.')
