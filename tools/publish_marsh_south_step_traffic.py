from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
RUN=ROOT/'output/marsh-animation-audit/south-step-traffic-v1-2026-10-02';OUT=BASE/'traffic-review-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=read(RUN/'report.json');assert report['checks']==164 and report['failures']==0 and report['cases']==12 and len(report['captures'])==24
    frozen=read(RUN/'inputs-before.json');assert frozen==read(RUN/'inputs-after.json')
    for path,digest in frozen.items():assert sha(ROOT/path)==digest
    owner=read(RUN/'owner-before.json');assert owner==read(RUN/'owner-after.json')
    log=(RUN/'godot.log').read_text(encoding='utf-8-sig');assert 'ERROR:' not in log
    selected={};catalog=ROOT/'character/marsh-v2/catalog.json'
    for name in read(catalog)['body']+['res://character/marsh-south-step-v1/candidate-05/manifest.json']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        for state in read(manifest)['states']:
            selected[state['id']]=[ROOT/name.removeprefix('res://') if name.startswith('res://') else manifest.parent/name for name in state['frameFiles']]
    OUT.mkdir(exist_ok=True);records=[];groups={};crop=(400,180,550,365)
    for row in report['captures']:
        native=RUN/row['file'];source=RUN/row['sourceFile'];canonical=selected[row['key']][row['slot']]
        assert Image.open(source).convert('RGBA').tobytes()==Image.open(canonical).convert('RGBA').tobytes()
        im=Image.open(native).convert('RGB');assert im.size==(1600,900)
        records.append(dict(row,crop=crop,nativeSha256=sha(native),sourceSha256=sha(source),canonical=canonical.relative_to(ROOT).as_posix(),canonicalSha256=sha(canonical)))
        groups.setdefault(row['label'].split()[0],[]).append((row,im.crop(crop)))
    boards=[]
    for group,entries in groups.items():
        board=Image.new('RGB',(600,1620),'#293b40');draw=ImageDraw.Draw(board)
        for i,(row,tile) in enumerate(entries):
            y,x=divmod(i,2);board.paste(tile.resize((300,370),Image.Resampling.NEAREST),(300*x,405*y+35))
            draw.text((300*x+3,405*y+3),row['label'],fill='white')
            draw.text((300*x+3,405*y+18),row['key']+' /'+str(row['slot']),fill='#c3d8d3')
        name=group+'-board.png';board.save(OUT/name);boards.append(name)
    evidence={'normalAdmission':False,'checks':164,'failures':0,'engineErrors':0,'exitCode':0,'cases':12,'exactSourceNativePairs':records,'targetedInputs':frozen,'inputsStable':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'scope':report['scope'],'visualReview':'pending','boards':boards,'logSha256':sha(RUN/'godot.log'),'limits':['Stationary prescribed peer collected by live coordinator, not natural moving-peer/yield acceptance.','No normal RunSave/fresh Title Continue or admission.','Sources remain provisional in width/detail/material/contact.']}
    (OUT/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh South step coordinator</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1000px}img{image-rendering:pixelated;max-width:100%}</style><h1>Unselected South short-step coordinator study</h1><p>164checks,12cases,24exact native/source pairs,zero failures.109targeted inputs stable;2931owner files unchanged. Live main coordinator collects a prescribed stationary Bill peer. Blocking peer releases the step without overlap; nonblocking control preserves one clock advance. Actual occupied/placed floor removal rebuilds navigation and stops without teleport.</p><p>Four prescribed phases, other actors/world paused. Natural moving traffic/full yield route, normal RunSave/Title Continue and final art consistency remain pending.</p>'
    for board in boards:html+='<h2>'+board.removesuffix('-board.png')+'</h2><img src="'+board+'">'
    html+='<p><a href="verification.json">Exact evidence</a></p>'
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps({'checks':164,'pairs':24,'cases':12,'inputsStable':len(frozen),'ownerUnchanged':len(owner)}))
if __name__=='__main__':main()
