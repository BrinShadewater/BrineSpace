"""Keep whole dry body pixels exact; compose separate authored coolant behind."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-injury-material-v1'
BODY=ROOT/'character/marsh-south-collapse-material-v1/candidate-01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sources=BASE/'sources';request_path=sources/'fluid-01.request.json';request=json.loads(request_path.read_text())
    raw_path=sources/'fluid-01.raw.png';assert sha(raw_path)==request['rawSha256']
    assert sha(sources/'fluid-01.prompt.txt')==request['promptSha256']
    for ref in request['orderedReferences']+request['referenceSourceFrames']:assert sha(ROOT/ref['path'])==ref['sha256']
    raw=Image.open(raw_path).convert('RGBA');a=np.array(raw)
    occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=1)
    groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==4
    borders=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(3)]+[raw.width]
    cells=[binary(raw.crop((borders[i],0,borders[i+1],raw.height))) for i in range(4)]
    last=cells[-1].getbbox();scale=36/(last[2]-last[0])
    out=BASE/'candidate-01';out.mkdir(exist_ok=True);effects=[];effect_records=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX))
        dense=dense.crop(dense.getbbox());dense.save(out/f'effect-{i:02d}.png');effects.append(dense)
        effect_records.append({'file':f'effect-{i:02d}.png','sourceCell':[borders[i],0,borders[i+1],raw.height],'size':dense.size,'commonScale':scale,'sha256':sha(out/f'effect-{i:02d}.png')})
    # Effects translate as complete inserts; body is never masked, painted or scaled.
    # Puddle center remains fixed through growth/recovery, not attached to moving arms.
    records=[];states=[];puddle_center=(54,173)
    anchors={1:(62,145),2:(62,143)}
    fall=[];rise=[]
    for action in ['injury-ground-south','injury-rise-south']:
        directory=out/action;directory.mkdir(exist_ok=True);files=[]
        for i in range(6):
            body_index=i if action=='injury-ground-south' else 5-i
            body_path=BODY/f'{body_index:03d}.png';body=Image.open(body_path).convert('RGBA')
            frame=Image.new('RGBA',(184,184));effect_index=None;effect_origin=None;effect_alpha=255
            if action=='injury-ground-south' and i in [1,2]:
                effect_index=i-1;effect=effects[effect_index]
                center,top=anchors[i];effect_origin=(center-effect.width//2,top)
            elif (action=='injury-ground-south' and i>=3) or (action=='injury-rise-south' and i<=4):
                effect_index=2 if action=='injury-ground-south' and i==3 else 3
                effect=effects[effect_index];effect_origin=(puddle_center[0]-effect.width//2,puddle_center[1]-effect.height//2)
                if action=='injury-rise-south' and i==4:effect_alpha=127
            if effect_index is not None:
                effect=effects[effect_index].copy()
                if effect_alpha!=255:effect.putalpha(effect.getchannel('A').point(lambda v:v*effect_alpha//255))
                x,y=effect_origin;assert x>=0 and y>=0 and x+effect.width<=184 and y+effect.height<=184
                frame.alpha_composite(effect,effect_origin)
            frame.alpha_composite(body)
            old=np.array(body);new=np.array(frame);mask=old[:,:,3]>0
            assert np.array_equal(old[mask],new[mask]),'whole body pixels altered'
            path=directory/f'{i:03d}.png'
            if (action=='injury-ground-south' and i==0) or (action=='injury-rise-south' and i==5):shutil.copy2(body_path,path)
            else:frame.save(path)
            files.append(path.relative_to(out).as_posix());records.append({'frame':path.relative_to(out).as_posix(),'bodySource':body_path.relative_to(ROOT).as_posix(),'bodySha256':sha(body_path),'bodyPixelsExact':True,'effectIndex':effect_index,'wholeEffectOrigin':effect_origin,'effectAlpha':effect_alpha,'sha256':sha(path),'visibleEffectPixels':int(np.sum((new[:,:,3]>0)&~mask))})
            (fall if action=='injury-ground-south' else rise).append(frame)
        states.append({'id':action,'frameFiles':files,'frameDurationsMs':[180]*6,'loop':False})
    assert (out/'injury-ground-south/005.png').read_bytes()==(out/'injury-rise-south/000.png').read_bytes(),'floor handoff source must be byte exact'
    manifest={'revision':'marsh-south-injury-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'status':'unselected white-fluid injury/recovery with exact complete dry body','fluidRawSha256':sha(raw_path),'fluidRequestSha256':sha(request_path),'effects':effect_records,'records':records,'puddleCenter':puddle_center,'operations':'ONE effect scale from mature puddle36px; BOX/alpha128; whole effects behind exact complete dry pose bodies. Reverse whole body sequence matches existing recovery motion policy. Last two recovery fluid phases half-alpha then none. No anatomy mask/paint/recolor, per-pose height fit or body reflection.','pending':'Source registration/material/effect shape review, actual injury phase handoffs/restoration, normal admission and family polish.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(1104,660),'#293b40');draw=ImageDraw.Draw(board)
    for row,(label,frames) in enumerate([('Dry body',[Image.open(BODY/f'{i:03d}.png').convert('RGBA') for i in range(6)]),('White-fluid injury',fall),('Recovery exact whole-body reverse',rise)]):
        for i,frame in enumerate(frames):
            board.paste(frame,(184*i,220*row+30),frame);draw.text((184*i+3,220*row+5),label+' '+str(i),fill='white')
    board.save(out/'comparison.png')
    for name,frames in [('injury',fall),('recovery',rise)]:frames[0].save(out/f'{name}.apng',save_all=True,append_images=frames[1:],duration=[180]*6,loop=1,disposal=1,blend=0)
    print(json.dumps({'effectScale':scale,'effectSizes':[im.size for im in effects],'bodyPixelsExact':12,'visibleEffectPixels':[r['visibleEffectPixels'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
