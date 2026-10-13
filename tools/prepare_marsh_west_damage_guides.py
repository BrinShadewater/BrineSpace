"""Prepare selected West master-density and motion-only guides for inspection."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    catalog=ROOT/'character/marsh-v2/catalog.json';states={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        data=json.loads(manifest.read_text())
        for state in data['states']:
            states[state['id']]=([ROOT/p.removeprefix('res://') if p.startswith('res://') else manifest.parent/p for p in state['frameFiles']],data)
    idle=states['idle-west'][0][0]
    primary=[idle,states['idle-west'][0][1],states['walk-west'][0][0],states['walk-west'][0][3]]
    board=Image.new('RGB',(4*512,565),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(primary):
        im=Image.open(path).convert('RGBA')
        shown=Image.new('RGBA',(256,256));metadata=states['idle-west' if i<2 else 'walk-west'][1]
        pivot=metadata['pivot'];shown.alpha_composite(im,(128-int(pivot[0]),224-int(pivot[1])))
        assert sum(shown.getchannel('A').histogram()[1:])==sum(im.getchannel('A').histogram()[1:])
        shown=shown.resize((512,512),Image.Resampling.NEAREST);board.paste(shown,(i*512,40),shown)
        draw.text((i*512+8,8),['SELECTED West idle0','SELECTED West idle1','SELECTED West gait0','SELECTED West gait3'][i],fill='white')
        draw.text((i*512+8,24),'PRIMARY material, identity, proportions, camera',fill='#a4d4c3')
    board.save(sources/'selected-west-idle-gait.png')
    guide=states['death-ground-west'][0][1:]+[idle]
    board=Image.new('RGB',(6*256,300),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(guide):
        im=Image.open(path).convert('RGBA');metadata=states['death-ground-west' if i<5 else 'idle-west'][1]
        pivot=metadata['pivot'];registered=Image.new('RGBA',(256,256));registered.alpha_composite(im,(128-int(pivot[0]),224-int(pivot[1])))
        assert sum(registered.getchannel('A').histogram()[1:])==sum(im.getchannel('A').histogram()[1:])
        board.paste(registered,(i*256,40),registered)
        draw.text((i*256+5,6),['1 soften','2 crouch','3 knees/hands','4 chest lowers','5 prone','6 selected neutral'][i],fill='white')
        draw.text((i*256+5,22),'POSE ONLY' if i<5 else 'PRIMARY ruler',fill='#a4d4c3')
    board.save(sources/'collapse-pose-guide.png')
    bounds=Image.open(idle).getbbox()
    records={'normalAdmission':False,'status':'guides frozen for visual inspection before authoring prompt','selectedIdleOccupiedSize':[bounds[2]-bounds[0],bounds[3]-bounds[1]],'selectedMetadata':{k:states['idle-west'][1].get(k) for k in ['frameWidth','frameHeight','pivot','standingHeight']},'primarySourceFrames':[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in primary],'guideSourceFrames':[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in guide]}
    (sources/'guide-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({k:records[k] for k in ['selectedIdleOccupiedSize','selectedMetadata']}))
if __name__=='__main__':main()
