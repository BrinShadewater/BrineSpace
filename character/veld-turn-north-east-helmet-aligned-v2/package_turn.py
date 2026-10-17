from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent;R=P.parents[1]
B=R/'character/veld-turn-north-east-original-master-v2'
H=R/'character/veld-helmet-original-turntable-v1/v3-study/shells'
S=R/'character/veld-turn-north-east-helmet-aligned-v1'
checks=0;fits=[];bindings={};refs={}
bare=json.loads((B/'bare-manifest.json').read_text());old_helmet=json.loads((B/'helmet-manifest.json').read_text())
bare_files=bare['states'][0]['frameFiles'];old_files=old_helmet['states'][0]['frameFiles']
assert bare['states'][0]['id']=='carry-turn-north-east'
board=Image.new('RGB',(1536,870),'#202a30');d=ImageDraw.Draw(board)
refs['bare']=list(bare_files);refs['helmet']=[]
for i in range(6):
    body=Image.open(R/bare_files[i][6:]).convert('RGBA');old=Image.open(R/old_files[i][6:]).convert('RGBA')
    if i in (0,1,5):
        ref=old_files[i];helmet=old;fits.append({'phase':i,'exactPreviouslyFittedWholeAlias':ref})
    else:
        shellpath={2:H/'004.png',3:S/'intermediate-v5-shell.png',4:H/'005.png'}[i]
        shell=Image.open(shellpath).convert('RGBA');a=np.array(body);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());hx=np.where(a[top:top+16,:,3]>128)[1]
        _,sx=np.where(np.array(shell)[-4:,:,3]>160);center=(sx.min()+sx.max())/2
        pos=(round((hx.min()+hx.max())/2-center),104-shell.height)
        clear=(int(hx.min())-3,top,int(hx.max())+4,103)
        helmet=body.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
        protected=np.ones((256,256),bool)
        protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
        assert np.array_equal(a[protected],np.array(helmet)[protected]);checks+=1
        dest=P/f'frames/helmet/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);helmet.save(dest)
        ref='res://'+dest.relative_to(R).as_posix()
        fits.append({'phase':i,'wholeSource':shellpath.relative_to(R).as_posix(),'shellSize':list(shell.size),'position':pos,'clearBox':clear,'protectedBodyExact':True})
        bindings[shellpath.relative_to(R).as_posix()]=hashlib.sha256(shellpath.read_bytes()).hexdigest()
    refs['helmet'].append(ref)
    for row,(label,im) in enumerate([('exact bare',body),('previous helmet',old),('yaw candidate',helmet)]):
        board.paste(im,(i*256,row*285+22),im);d.text((i*256+4,row*285+4),f'{label} phase{i}',fill='white')
        z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
for gear in refs:
    m=json.loads((B/f'{gear}-manifest.json').read_text());m.update(name='Veld North-East original body helmet yaw study '+gear,status='staged_not_installed')
    for state in m['states']:
        state['frameFiles']=refs[gear] if state['id']=='carry-turn-north-east' else list(reversed(refs[gear]))
        original=next(s for s in (bare if gear=='bare' else old_helmet)['states'] if s['id']==state['id'])
        assert state['frameDurationsMs']==original['frameDurationsMs'] and sum(state['frameDurationsMs'])==800 and not state['loop'];checks+=1
        images=[]
        for ref in state['frameFiles']:
            path=R/ref[6:];bindings[ref[6:]]=hashlib.sha256(path.read_bytes()).hexdigest()
            bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(path).convert('RGBA'));images.append(bg)
        movie=P/f'{gear}-{state["id"]}.apng';images[0].save(movie,format='PNG',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
        with Image.open(movie) as source:
            assert source.n_frames==6;checks+=1
            for j,expected in enumerate(images):source.seek(j);assert source.convert('RGBA').tobytes()==expected.tobytes();checks+=1
    (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
assert refs['bare']==bare_files and refs['helmet'][0]==old_files[0] and refs['helmet'][5]==old_files[5];checks+=3
for path in [B/'registration.json',S/'intermediate-v5-registration.json',S/'raw-intermediate-v5.png']:
    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
board.save(P/'paired-yaw-source.png')
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'fits':fits,'bindings':bindings,'exactBareFrameAliases':True,'exactNorthAndEastEquippedEndpoints':True,'durationMs':800,'scope':'Whole helmet yaw fit only. Body and finite timing unchanged. Late actual-head correspondence reuses exact original profile at phase4; no normal adoption, gather/gait/world/save acceptance.'},indent=2)+'\n')
print(f'{checks} whole source/protection/alias/timing/APNG checks, 0 failures')
