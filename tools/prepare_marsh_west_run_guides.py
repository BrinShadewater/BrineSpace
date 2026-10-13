"""Freeze West's own selected body and motion; never mirror East identity."""
from pathlib import Path
import hashlib,json,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert not (BASE/'guide-provenance.json').exists(),'preserve existing guide review'
    BASE.mkdir(parents=True,exist_ok=True);catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve();data=json.loads(manifest.read_text())
        for state in data['states']:selected[state['id']]={'paths':[ROOT/p.removeprefix('res://') if p.startswith('res://') else (manifest.parent/p).resolve() for p in state['frameFiles']],'metadata':{k:data.get(k) for k in ['pivot','standingHeight','frameWidth','frameHeight']},'state':state,'manifest':manifest}
    records={}
    for kind,items in [('primary',[('idle-west',0),('idle-west',1),('walk-west',0),('walk-west',3)]),('motion',[('run-west',i) for i in range(6)])]:
        board=Image.new('RGB',(len(items)*512,572),'#293b40');draw=ImageDraw.Draw(board);records[kind]=[]
        for col,(key,slot) in enumerate(items):
            entry=selected[key];p=entry['paths'][slot];f=Image.open(p).convert('RGBA');pivot=entry['metadata']['pivot'];registered=Image.new('RGBA',(256,256));offset=(128-int(pivot[0]),224-int(pivot[1]));registered.alpha_composite(f,offset);assert np.count_nonzero(np.array(registered)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);large=registered.resize((512,512),Image.Resampling.NEAREST);board.paste(large,(col*512,50),large);draw.text((col*512+5,5),key+' '+str(slot),fill='white');draw.text((col*512+5,25),'PRIMARY body/camera/grade' if kind=='primary' else 'MOTION ONLY; not anatomy',fill='#b1d5c6');records[kind].append({'key':key,'slot':slot,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'metadata':entry['metadata'],'guideWholeTranslation':offset,'manifest':entry['manifest'].relative_to(ROOT).as_posix()})
        board.save(BASE/('selected-west-idle-gait.png' if kind=='primary' else 'run-pose-guide.png'))
    idle=Image.open(selected['idle-west']['paths'][0]).getbbox();data={'normalAdmission':False,'fullGoalComplete':False,'primarySourceFrames':records['primary'],'guideSourceFrames':records['motion'],'selectedIdleOccupiedSize':[idle[2]-idle[0],idle[3]-idle[1]],'runTiming':selected['run-west']['state']['frameDurationsMs'],'runLoop':selected['run-west']['state']['loop'],'identity':'Own original West master, visible near temple BARE; implant on far right temple. Never mirror East or add visible temple hardware.','operations':'Complete whole256canvas/p128224 registered guides at nearest2x, no anatomy edits or perpose fit.'};(BASE/'guide-provenance.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'frozenWestFrames':10,'selectedIdle':data['selectedIdleOccupiedSize'],'runTiming':data['runTiming']}))
if __name__=='__main__':main()
