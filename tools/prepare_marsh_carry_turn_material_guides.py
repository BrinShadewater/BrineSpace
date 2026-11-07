"""Freeze actual old turn selection and staged whole endpoints/body rulers."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources';S.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n);m=json.loads(p.read_text())
    for s in m['states']:selected[s['id']]=(p,m,s)
turns=[]
for key,(p,m,s) in selected.items():
    if not key.startswith('carry-turn-'):continue
    frames=[resolve(p,n) for n in s['frameFiles']];turns.append({'key':key,'manifest':p.relative_to(ROOT).as_posix(),'manifestSha256':sha(p),'timing':{k:s[k] for k in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets'] if k in s},'metadata':{k:m.get(k) for k in ['frameWidth','frameHeight','pivot','standingHeight']},'frames':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in frames]})
assert len(turns)==12
staged={};idles={};masters={}
for f,rev in [('east','03'),('west','03'),('south','01'),('north','01')]:
    p=ROOT/f'character/marsh-{f}-carry-material-v1/candidate-{rev}/000.png';idle=resolve(selected[f'idle-{f}'][0],selected[f'idle-{f}'][2]['frameFiles'][0]);master=ROOT/f'character/marsh-motion-polish-v1/sources/{f}-standing-identity-01.png'
    for target,q in [(staged,p),(idles,idle),(masters,master)]:target[f]={'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q),'occupiedBounds':Image.open(q).convert('RGBA').getbbox()}
for pair in ['east-south','east-north','west-south','west-north']:
    faces=pair.split('-')
    for kind,records in [('body-primary',idles),('cargo-endpoints',staged)]:
        board=Image.new('RGBA',(1472,736))
        for i,f in enumerate(faces):board.alpha_composite(Image.open(ROOT/records[f]['path']).convert('RGBA').resize((736,736),Image.Resampling.NEAREST),(i*736,0))
        board.save(S/f'{pair}-{kind}.png')
    old=next(t for t in turns if t['key']==f'carry-turn-{pair}');board=Image.new('RGB',(len(old['frames'])*368,410),'#293b40');d=ImageDraw.Draw(board)
    for i,r in enumerate(old['frames']):
        q=ROOT/r['path'];f=Image.open(q).convert('RGBA');assert f.size==(184,184);large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,35),large);d.text((i*368+4,5),pair+f' old slot{i} / motion only',fill='white')
    board.save(S/f'{pair}-old-motion-review.png')
out={'normalAdmission':False,'fullGoalComplete':False,'selectedTurns':turns,'stagedEndpoints':staged,'primaryIdles':idles,'ownOriginalMasters':masters,'guideArtifacts':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(S.glob('*.png'))],'operations':'Whole unchanged184figures,nearest4x transparent pairs/nearest2x old motion review;no anatomy edits/mirror/recolour. Current ordered catalog selection and metadata retained.','limits':'Old selected turns supply motion only; staging endpoints does not admit normal carries or joins.'}
p=S/'guide-provenance.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'currentSelectedTurns':12,'stagedCardinalEndpoints':4,'primarySelectedIdles':4,'turnTiming':{r['key']:r['timing']['frameDurationsMs'] for r in turns}}))
