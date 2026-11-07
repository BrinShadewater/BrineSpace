"""Replace one whole intermediate; retain all other original PNG bytes."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1'
old=B/'east-north-01-unselected';new=B/'east-north-02-unselected';assert not new.exists();new.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((old/'manifest.json').read_text());m['revision']='marsh-carry-turn-material-east-north-02-unselected'
replacement=B/'east-north-nearback03-unselected/intermediate-3.png';unchanged=0
for state in m['states']:
    for i,name in enumerate(state['frameFiles']):
        p=new/name;p.parent.mkdir(exist_ok=True)
        source=replacement if (state['id']=='carry-turn-east-north' and i==3) or (state['id']=='carry-turn-north-east' and i==1) else old/name
        shutil.copy2(source,p);assert sha(source)==sha(p)
        unchanged+=source!=replacement
(new/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
forward=[Image.open(new/n).convert('RGBA') for n in m['states'][0]['frameFiles']]
reverse=[Image.open(new/n).convert('RGBA') for n in m['states'][1]['frameFiles']]
assert all(a.tobytes()==b.tobytes() for a,b in zip(forward,reversed(reverse)))
for state in m['states']:
    for i in [0,4]:assert sha(new/state['frameFiles'][i])==sha(old/state['frameFiles'][i])
timing=m['states'][0]['frameDurationsMs'];forward[0].save(new/'turn.apng',save_all=True,append_images=forward[1:],duration=timing,loop=0,disposal=0,blend=0)
decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(new/'turn.apng'))];assert len(decoded)==5 and all(a.tobytes()==b.tobytes() for a,b in zip(decoded,forward))
board=Image.new('RGB',(1840,830),'#293b40');d=ImageDraw.Draw(board)
for row,folder in enumerate([old,new]):
    d.text((10,row*415+5),'Original rejected third' if row==0 else 'Whole nearback03 replacement / staged',fill='white')
    for i,n in enumerate(m['states'][0]['frameFiles']):
        f=Image.open(folder/n).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);board.paste(f,(i*368,row*415+35),f)
board.save(new/'comparison.png')
(new/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'replacementSource':replacement.relative_to(ROOT).as_posix(),'replacementSha256':sha(replacement),'unchangedOriginalFrameCopies':unchanged,'exactEndpointCopies':4,'reverseWholeOrderExact':True,'apngExactDecodedFrames':5,'durationMs':sum(timing),'limits':'Nearback03 rear-right head/body and viewerLEFT support checked provisionally;first intermediate remains close to East side and full grade/head/case/foot joins need consistency polish. No mirrored pixels or patches;all eight other frame files unchanged.'},indent=2)+'\n')
print('Assembled two staged five-frame states;8unchanged PNGs,4exact endpoints,5decoded APNG frames.')
