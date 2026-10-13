"""Freeze selected East identity and whole running poses for own-master review."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    BASE.mkdir(parents=True,exist_ok=True);catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve();data=json.loads(manifest.read_text())
        for s in data['states']:selected[s['id']]={'paths':[ROOT/p.removeprefix('res://') if p.startswith('res://') else (manifest.parent/p).resolve() for p in s['frameFiles']],'metadata':{k:data.get(k) for k in ['pivot','standingHeight','frameWidth','frameHeight']},'state':s,'manifest':manifest}
    primary=[('idle-east',0),('idle-east',1),('walk-east',0),('walk-east',3)];records={}
    for kind,items in [('primary',primary),('motion',[('run-east',i) for i in range(6)])]:
        board=Image.new('RGB',(len(items)*512,572),'#293b40');draw=ImageDraw.Draw(board);records[kind]=[]
        for col,(key,slot) in enumerate(items):
            entry=selected[key];p=entry['paths'][slot];im=Image.open(p).convert('RGBA');pivot=entry['metadata']['pivot'];registered=Image.new('RGBA',(256,256));offset=(128-int(pivot[0]),224-int(pivot[1]));registered.alpha_composite(im,offset)
            assert np.count_nonzero(np.array(registered)[:,:,3])==np.count_nonzero(np.array(im)[:,:,3]),'whole guide clipped'
            large=registered.resize((512,512),Image.Resampling.NEAREST);board.paste(large,(col*512,50),large);draw.text((col*512+8,8),key+' '+str(slot),fill='white');draw.text((col*512+8,28),'PRIMARY identity/body/material' if kind=='primary' else 'MOTION ONLY; not anatomy authority',fill='#a4d4c3')
            records[kind].append({'key':key,'slot':slot,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'metadata':entry['metadata'],'guideWholeTranslation':offset,'manifest':entry['manifest'].relative_to(ROOT).as_posix()})
        board.save(BASE/('selected-east-idle-gait.png' if kind=='primary' else 'run-pose-guide.png'))
    idle=Image.open(selected['idle-east']['paths'][0]).getbbox();data={'normalAdmission':False,'primarySourceFrames':records['primary'],'guideSourceFrames':records['motion'],'selectedIdleOccupiedSize':[idle[2]-idle[0],idle[3]-idle[1]],'runTiming':selected['run-east']['state']['frameDurationsMs'],'runLoop':selected['run-east']['state']['loop'],'operations':'Whole figures registered to common256/p128224 for guide only, nearest2x. No anatomical edits or size normalization.'}
    (BASE/'guide-provenance.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'frozenEastFrames':10,'selectedIdle':data['selectedIdleOccupiedSize'],'runTiming':data['runTiming']}))
if __name__=='__main__':main()
