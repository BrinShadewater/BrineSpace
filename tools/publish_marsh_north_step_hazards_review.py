"""Publish discrete native hazard takeovers; never imply a continuous route test."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/north-step-hazards-v1-2026-10-02'
DEST=ROOT/'character/marsh-north-step-v1/hazard-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text())
    assert report['failures']==0 and report['cases']==28 and len(report['captures'])==56
    inputs=json.loads((RUN/'inputs-before.json').read_text())
    assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in inputs.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    for n in ['unit.log','native.log']:assert 'ERROR:' not in (RUN/n).read_text(encoding='utf-8-sig')
    assert '1525 checks,0 failures' in (RUN/'unit.log').read_text(encoding='utf-8-sig')
    DEST.mkdir(exist_ok=True);groups={};captures=[];crop=(400,200,550,355)
    for r in report['captures']:
        native=Image.open(RUN/r['file']).convert('RGB').crop(crop)
        source=Image.open(RUN/r['sourceFile']).convert('RGBA')
        if r['key']=='walk-step-north':
            expected=Image.open(ROOT/'character/marsh-north-step-v1/sequence-v1'/('%03d.png'%r['slot'])).convert('RGBA')
            assert source.size==expected.size and source.tobytes()==expected.tobytes()
        groups.setdefault(r['phase'],[]).append((r,native,source))
        captures.append({**r,'nativeSha256':sha(RUN/r['file']),'submittedSourceSha256':sha(RUN/r['sourceFile']),'crop':crop})
    names=[]
    for phase,entries in groups.items():
        assert len(entries)==14
        board=Image.new('RGB',(720,1750),'#293b40');draw=ImageDraw.Draw(board)
        for i,(r,native,source) in enumerate(entries):
            x=(i%2)*360;y=(i//2)*250
            board.paste(native,(x,y+40));matte=Image.new('RGBA',source.size,'#293b40');matte.alpha_composite(source)
            board.paste(matte.convert('RGB'),(x+160,y+40))
            draw.text((x+3,y+3),f"{r['kind']} @{phase:.2f} {r['moment']}",fill='white')
            draw.text((x+3,y+19),f"{r['key']} #{r['slot']} / {r['goal']}",fill='white')
        name='phase-'+str(round(phase*100))+'.png';board.save(DEST/name);names.append(name)
    evidence={**report,'controllerChecks':1525,'targetedInputs':inputs,'targetedInputsUnchanged':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'captures':captures,'normalAdmission':False,'visualMotionAcceptance':False,'scopeFreeze':'24 targeted inputs before/after/publication, not recursive dependency freeze.','logs':{n:sha(RUN/n) for n in ['unit.log','native.log']}}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step hazard study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1100px}img{max-width:100%;image-rendering:pixelated}</style><h1>North short step: staged hazard takeovers</h1><p>'+str(report['checks'])+' native checks;1525 controller checks;28 cases/56 source-native captures;0 failures. Fire, medium/high water, low battery, impact, death and supplied crew obstruction at four prescribed clip phases. Pending pause preserves root/clock; each takeover releases the authored pose and offset without completing old work.</p><p>Marsh remains on the flooded floor. Actual RoomFlooding.step_crew supplies water slowdown; the dry-step clock yields immediately. Actual fire/injury/charge/death controllers and crew_clear retain precedence. Normal failure flags retained, explicit furnished cold-store fixture and paused world/peers. Discrete comparisons, not continuous motion or natural traffic/coordinator/whole escape routes. Normal admission and save/title Continue remain open.</p><p>Each cell pairs unscaled native context and exact submitted texture on matte.24 targeted inputs unchanged;2931 owner files unchanged.</p>'
    for n in names:html+='<h2>'+n.removesuffix('.png')+'</h2><img src="'+n+'">'
    html+='<p><a href="verification.json">Bound evidence</a></p>'; (DEST/'index.html').write_text(html)
    print(report['checks'],'native checks;28 cases;56 submitted source/native comparisons')
if __name__=='__main__':main()
