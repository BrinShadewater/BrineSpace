"""Assemble four unchanged complete poses; retain source/native review limits."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'character/marsh-east-carry-material-v1'; O=B/'candidate-02'; O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[B/'near-06-unselected/near-contact.png',B/'near-06-unselected/near-passing.png',B/'contact-04-unselected/far-contact.png',B/'passing-05-unselected/far-passing.png']
names=['near contact','near passing','far contact','far passing']; records=[]; frames=[]
for i,p in enumerate(sources):
    q=O/f'{i:03}.png';shutil.copy2(p,q);assert sha(p)==sha(q)
    f=Image.open(q).convert('RGBA');assert f.size==(184,184);frames.append(f)
    records.append({'slot':i,'pose':names[i],'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'occupiedBounds':f.getbbox()})
m=json.loads((B/'candidate-01/manifest.json').read_text());m['revision']='marsh-east-carry-material-02-unselected';(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
frames[0].save(O/'cycle.png',save_all=True,append_images=frames[1:],duration=[180]*4,loop=0,disposal=0,blend=0)
decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(O/'cycle.png'))];assert len(decoded)==4
for a,b in zip(frames,decoded):assert a.tobytes()==b.tobytes()
board=Image.new('RGB',(1472,860),'#293b40');d=ImageDraw.Draw(board)
for row,fs in enumerate([[Image.open(B/'candidate-01'/f'{i:03}.png').convert('RGBA') for i in range(4)],frames]):
    for i,f in enumerate(fs):
        large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,row*430+45),large);d.text((i*368+4,row*430+5),('Rejected repeated near half' if row==0 else names[i]),fill='white')
board.save(O/'comparison.png')
(O/'assembly.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'sources':records,'operations':'Byte-identical complete source PNG copies; no added scaling, mirroring, limb or crate edits. Source sheets each use one own neutral calibration.','apngExactDecodedFrames':4,'nativeReviewed':False,'visualReviewed':False,'remaining':'Review complete four-pose body/cargo joins, then actual East workshop carry native fixture. No normal admission.'},indent=2)+'\n')
print(json.dumps({'completeFrames':4,'byteIdenticalSources':4,'exactDecodedApngFrames':4,'normalAdmission':False}))
