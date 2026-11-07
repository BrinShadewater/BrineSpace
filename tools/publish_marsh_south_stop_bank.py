"""Review staged six-phase South source coverage, without runtime admission."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw
from build_marsh_south_start import sole

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-stop-v1'
VERSIONS={0:'06',1:'06',2:'06',3:'01',4:'07',5:'01'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    dest=BASE/'source-bank-review-v1';dest.mkdir(exist_ok=True)
    board=Image.new('RGB',(184*5,220*6),'#293b40');draw=ImageDraw.Draw(board)
    checks=0;states=[];unique=set()
    for phase,version in VERSIONS.items():
        source=BASE/f'candidate-{version}/phase-{phase}'
        manifest=json.loads((source/'manifest.json').read_text());state=manifest['states'][0]
        assert state['id']==f'walk-stop-phase{phase}-south' and state['frameDurationsMs']==[80]*5 and not state['loop'];checks+=1
        assert manifest['pivot']==[92,172] and manifest['standingHeight']==148;checks+=1
        frames=[];hashes={}
        for i in range(5):
            p=source/f'{i:03d}.png';im=Image.open(p).convert('RGBA');frames.append(im)
            assert im.size==(184,184) and set(im.getchannel('A').tobytes())<={0,255};checks+=1
            hashes[p.name]=sha(p);unique.add(hashlib.sha256(im.tobytes()).hexdigest())
            board.paste(im,(184*i,220*phase+36),im)
            draw.text((184*i+4,220*phase+4),f'phase{phase} '+('exact outgoing' if i==0 else 'exact idle' if i==4 else f'interior{i}'),fill='white')
        for file,target in [('000.png',ROOT/f'character/marsh-south-walk-material-v1/candidate-02/{phase:03d}.png'),('004.png',ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png')]:
            assert (source/file).read_bytes()==target.read_bytes();checks+=1
        apng=Image.open(source/'source-motion.apng');assert apng.n_frames==5;checks+=1
        for i,frame in enumerate(frames):apng.seek(i);assert apng.convert('RGBA').tobytes()==frame.tobytes();checks+=1
        parent=BASE/'candidate-06/phase-0' if phase in [1,2] else BASE/'candidate-01/phase-3' if phase==5 else None
        if parent:
            for file in ['001.png','002.png','003.png']:assert (source/file).read_bytes()==(parent/file).read_bytes();checks+=1
            recipe=json.loads((source/'recipe.json').read_text())
            assert recipe['sourceRecipeSha256']==sha(parent/'recipe.json');checks+=1
        states.append({'phase':phase,'manifest':(source/'manifest.json').relative_to(ROOT).as_posix(),'manifestSha256':sha(source/'manifest.json'),'frameHashes':hashes,'contacts':[[sole(f,True),sole(f,False)] for f in frames],'sharedBank':parent.relative_to(ROOT).as_posix() if parent else None})
    board.save(dest/'all-six-phases.png')
    evidence={'status':'six source branches staged; native/controller acceptance pending','normalAdmission':False,'checks':checks,'failures':0,'declaredStates':6,'declaredSlots':30,'uniqueRgbaPoses':len(unique),'states':states,'visualReview':'All six full source comparisons inspected beside exact gait/idle/original master. Phase1 shares whole phase0 source06 recovery; phase2 same bank, phase5 shares phase3source01. Same recovering-foot sides. No new authored interiors in aliases. Near-contact phase2/5 has2dense support-depth settling at entry, not proven plantar contact. Phase0/1/2 terminal left1dense seam; phase3/5 terminal left0.5/right1.5dense seams. Phase4 keeps existing preferredsource07 with0.5dense terminal seam and3dense initial extra left lift. Width/detail/material joins remain full-family polish. No native/player/controller/save proof for new branches; phase4 historical evidence separate.'}
    (dest/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    (dest/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh six South stop source branches</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;max-width:1250px;margin:30px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Six staged South stop branches</h1><p>'+evidence['visualReview']+'</p><img src="all-six-phases.png"><p>'+str(checks)+' packaging checks;6states/30slots/'+str(len(unique))+'unique RGBA poses. Source coverage only; full objective remains active.</p><a href="verification.json">Bound source evidence</a>',encoding='utf-8')
    print(json.dumps({k:evidence[k] for k in ['checks','failures','declaredStates','declaredSlots','uniqueRgbaPoses']}))
if __name__=='__main__':main()
