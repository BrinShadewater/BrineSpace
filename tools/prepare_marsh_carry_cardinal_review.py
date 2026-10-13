"""Compare complete staged cargo bodies against actual selected cardinal idles."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'character/marsh-carry-cardinal-review-2026-10-02';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
for n in json.loads(cat.read_text())['body']:
    m=resolve(cat,n)
    for s in json.loads(m.read_text())['states']:selected[s['id']]=[resolve(m,f) for f in s['frameFiles']]
rows=[]
for facing,revision,review in [('south','01','actor-review-v1'),('north','01','actor-review-v1'),('east','03','actor-review-v2'),('west','03','actor-review-v1')]:
    b=ROOT/f'character/marsh-{facing}-carry-material-v1';p=b/f'candidate-{revision}/manifest.json';m=json.loads(p.read_text());s=m['states'][0];assert s['id']==f'carry-{facing}' and s['frameDurationsMs']==[180.0]*4 and s['loop']
    ev=json.loads((b/review/'verification.json').read_text());assert ev['checks']==523 and ev['captures']==6 and ev['failures']==0
    paths=[selected[f'idle-{facing}'][0]]+[resolve(p,n) for n in s['frameFiles']]
    row={'facing':facing,'stagedManifest':p.relative_to(ROOT).as_posix(),'manifestSha256':sha(p),'independentStageEvidence':(b/review/'verification.json').relative_to(ROOT).as_posix(),'normalAdmission':False,'wholeFrames':[]}
    for slot,q in enumerate(paths):
        f=Image.open(q).convert('RGBA');assert f.size==(184,184);row['wholeFrames'].append({'role':'selected idle' if slot==0 else f'staged carry {slot-1}','path':q.relative_to(ROOT).as_posix(),'sha256':sha(q),'occupiedBounds':f.getbbox()})
    rows.append(row)
for group in range(2):
    board=Image.new('RGB',(1840,820),'#293b40');d=ImageDraw.Draw(board)
    for ri,row in enumerate(rows[group*2:group*2+2]):
        for ci,r in enumerate(row['wholeFrames']):
            f=Image.open(ROOT/r['path']).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);board.paste(f,(ci*368,ri*410+35),f);d.text((ci*368+4,ri*410+5),row['facing']+' / '+r['role'],fill='white')
    board.save(O/f'whole-cardinals-{group}.png')
(O/'provenance.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rows':rows,'operations':'Twenty complete unchanged184canvas frames; nearest2x board display only, no anatomy edits/registration/rescaling. Four selected idles plus sixteen staged carry poses.','limits':'Independent native stage evidence per facing only. This comparison is not normal Save/Continue,carry-turn/held join,continuous physical contact or full-set acceptance.'},indent=2)+'\n')
print('Four own cardinal idles plus sixteen staged cargo poses; two complete whole-figure boards retained.')
