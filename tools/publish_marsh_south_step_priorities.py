"""Bind native priority captures to exact selected source frames and frozen inputs."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
RUN=ROOT/'output/marsh-animation-audit/south-step-priorities-v1-2026-10-02'
OUT=BASE/'priorities-review-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=read(RUN/'report.json')
    assert report['failures']==0 and report['availableCases']==4 and report['serviceLosses']==32 and report['hazards']==28
    assert report['stagedActorRestores']==36 and len(report['captures'])==156
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
        assert Image.open(source).convert('RGBA').tobytes()==Image.open(canonical).convert('RGBA').tobytes(),row['label']
        im=Image.open(native).convert('RGB');assert im.size==(1600,900)
        tile=im.crop(crop)
        record=dict(row,crop=crop,nativeSha256=sha(native),sourceSha256=sha(source),canonical=canonical.relative_to(ROOT).as_posix(),canonicalSha256=sha(canonical))
        records.append(record)
        label=row['label'];group='available' if ' available ' in label else label.split()[0] if label.split()[0] in ['curiosity','hunger','fatigue','maintenance'] else 'hazard-'+label.split()[0]
        groups.setdefault(group,[]).append((record,tile))
    boards=[]
    for group,entries in groups.items():
        columns=4 if group=='available' else 2 if group.startswith('hazard-') else 3
        rows=(len(entries)+columns-1)//columns
        board=Image.new('RGB',(300*columns,405*rows),'#293b40');draw=ImageDraw.Draw(board)
        for i,(row,tile) in enumerate(entries):
            y,x=divmod(i,columns)
            board.paste(tile.resize((300,370),Image.Resampling.NEAREST),(300*x,405*y+35))
            draw.text((300*x+3,405*y+3),row['label'],fill='white')
            draw.text((300*x+3,405*y+18),row['key']+' /'+str(row['slot'])+' goal:'+row['goal'],fill='#c3d8d3')
        name=group+'-board.png';board.save(OUT/name);boards.append(name)
    evidence={'normalAdmission':False,'checks':report['checks'],'failures':0,'engineErrors':0,'exitCode':0,'availableServiceGoals':4,'realServiceLossCases':32,'hazardCases':28,'actorOnlyRestores':36,'exactSourceNativePairs':records,'targetedInputs':frozen,'inputsStable':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'scope':report['scope'],'visualReview':'pending','boards':boards,'logSha256':sha(RUN/'godot.log'),'limits':['Takeover sources traced to selected catalog at publication;106 bounded pre/post inputs do not freeze every loaded catalog artwork.','Prescribed supplied peer collision; live coordinator and removed topology still pending.','Actor-only restores are not normal full RunSave or Title Continue.','Mixed source body/face/arm/material joins remain provisional.']}
    (OUT/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh South step priorities</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1200px}img{image-rendering:pixelated;max-width:100%}</style><h1>Unselected South step: service and priority study</h1><p>'+str(report['checks'])+'checks,156exact native/source pairs,36actor-only restores,zero failures.106targeted inputs stable;2931owner files unchanged. Actual furnished Cold Store, parent FireSafety/flood/charge/injury/death. Four available goals,32power/suspension losses,28priority cases at four prescribed phases. World/other actors paused; normal catalog unselected.</p><p>Work clears immediately after service loss; finite physical step settles without its old callback, including after actor restoration. Urgent priorities release the step and whole-sprite offset. Sources remain provisional in width/detail/grade. Live coordinator/floor removal, normal RunSave/Title Continue and cross-family polish remain pending.</p>'
    for board in boards:html+='<h2>'+board.removesuffix('-board.png')+'</h2><img src="'+board+'">'
    html+='<p><a href="verification.json">Exact captures, selected source provenance and scope limits</a></p>'
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps({'checks':report['checks'],'pairs':156,'actorRestores':36,'inputsStable':len(frozen),'ownerUnchanged':len(owner)}))
if __name__=='__main__':main()
