"""Reuse complete authored coolant behind exact complete East bodies."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-injury-material-v1'
BODY=ROOT/'character/marsh-east-collapse-material-v1/candidate-01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    request_path=BASE/'sources/reuse-request.json';request=json.loads(request_path.read_text())
    for ref in request['bodyGuideFrames']+request['reusedAuthoredEffects']:
        assert sha(ROOT/ref['path'])==ref['sha256'],ref['path']
    out=BASE/'candidate-01';out.mkdir(exist_ok=True)
    effects=[Image.open(ROOT/f'character/marsh-south-injury-material-v1/candidate-01/effect-{i:02d}.png').convert('RGBA') for i in range(4)]
    records=[];states=[];sequences=[];puddle_center=(122,172);anchors={1:(106,124),2:(106,134)}
    for action in ['injury-ground-east','injury-rise-east']:
        directory=out/action;directory.mkdir(exist_ok=True);files=[];frames=[]
        for i in range(6):
            index=i if action=='injury-ground-east' else 5-i
            source=BODY/f'{index:03d}.png';body=Image.open(source).convert('RGBA')
            frame=Image.new('RGBA',(184,184));effect_index=None;origin=None;opacity=255
            if action=='injury-ground-east' and i in [1,2]:
                effect_index=i-1;effect=effects[effect_index];center,top=anchors[i];origin=(center-effect.width//2,top)
            elif (action=='injury-ground-east' and i>=3) or (action=='injury-rise-east' and i<=4):
                effect_index=2 if action=='injury-ground-east' and i==3 else 3
                effect=effects[effect_index];origin=(puddle_center[0]-effect.width//2,puddle_center[1]-effect.height//2)
                if action=='injury-rise-east' and i==4:opacity=127
            if effect_index is not None:
                effect=effects[effect_index].copy()
                if opacity!=255:effect.putalpha(effect.getchannel('A').point(lambda a:a*opacity//255))
                x,y=origin;assert x>=0 and y>=0 and x+effect.width<=184 and y+effect.height<=184
                frame.alpha_composite(effect,origin)
            frame.alpha_composite(body)
            old=np.array(body);new=np.array(frame);mask=old[:,:,3]>0
            assert np.array_equal(old[mask],new[mask]),'body pixels altered'
            path=directory/f'{i:03d}.png'
            if effect_index is None:shutil.copy2(source,path)
            else:frame.save(path)
            files.append(path.relative_to(out).as_posix());frames.append(frame)
            records.append({'frame':files[-1],'bodySource':source.relative_to(ROOT).as_posix(),'bodySha256':sha(source),'bodyPixelsExact':True,'effectIndex':effect_index,'wholeEffectOrigin':origin,'effectAlpha':opacity,'visibleEffectPixels':int(np.sum((new[:,:,3]>0)&~mask)),'sha256':sha(path)})
        states.append({'id':action,'frameFiles':files,'frameDurationsMs':[180]*6,'loop':False});sequences.append(frames)
    assert (out/'injury-ground-east/005.png').read_bytes()==(out/'injury-rise-east/000.png').read_bytes()
    assert (out/'injury-rise-east/005.png').read_bytes()==(BODY/'000.png').read_bytes()
    manifest={'revision':'marsh-east-injury-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'reuseRequestSha256':sha(request_path),'records':records,'puddleCenter':puddle_center,'gloveAnchors':anchors,'operations':'Exact complete candidate02 East bodies, existing complete authored148-density coolant swatches behind body, whole translations only. Reverse whole body recovery policy. Final fade127 then no effect; floor handoff byte-exact. No body scaling, patch, recolor, mirroring or old-guide subtraction.','pending':'Source and native material/effect registration review, actual impact/recovery/restoration, normal admission and family polish.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(1104,660),'#293b40');draw=ImageDraw.Draw(board)
    for row,(label,frames) in enumerate([('Complete dry',[Image.open(BODY/f'{i:03d}.png').convert('RGBA') for i in range(6)]),('White-fluid injury',sequences[0]),('Whole-body recovery',sequences[1])]):
        for i,frame in enumerate(frames):
            board.paste(frame,(i*184,row*220+30),frame);draw.text((i*184+3,row*220+5),label+' '+str(i),fill='white')
    board.save(out/'comparison.png')
    for name,frames in zip(['injury','recovery'],sequences):frames[0].save(out/f'{name}.apng',save_all=True,append_images=frames[1:],duration=[180]*6,loop=1,disposal=1,blend=0)
    print(json.dumps({'bodyPixelsExact':12,'visibleEffectPixels':[r['visibleEffectPixels'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
