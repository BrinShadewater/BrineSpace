"""Bind discrete Main coordinator/topology captures to their native interval."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/north-step-traffic-v1-2026-10-02'
DEST=ROOT/'character/marsh-north-step-v1/traffic-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text())
    assert report['checks']==163 and report['failures']==0 and report['cases']==12 and len(report['captures'])==24
    frozen=json.loads((RUN/'inputs-before.json').read_text());assert frozen==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in frozen.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
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
        assert len(entries)==6
        board=Image.new('RGB',(720,750),'#293b40');draw=ImageDraw.Draw(board)
        for i,(r,native,source) in enumerate(entries):
            x=(i%2)*360;y=(i//2)*250;board.paste(native,(x,y+40))
            matte=Image.new('RGBA',source.size,'#293b40');matte.alpha_composite(source);board.paste(matte.convert('RGB'),(x+160,y+40))
            draw.text((x+3,y+3),f"{r['kind']} @{phase:.2f} {r['moment']}",fill='white')
            draw.text((x+3,y+19),f"{r['key']} #{r['slot']} / {r['goal']}",fill='white')
        name='phase-'+str(round(phase*100))+'.png';board.save(DEST/name);names.append(name)
    evidence={**report,'captures':captures,'targetedInputs':frozen,'targetedInputsUnchanged':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'normalAdmission':False,'naturalMovingTrafficVerified':False,'continuousMotionVerified':False,'normalSaveTitleVerified':False,'inputFreezeScope':'24 targeted inputs before/after/publication; not recursive dependency freeze.','nativeLogSha256':sha(RUN/'native.log')}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step coordinator study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1100px}img{max-width:100%;image-rendering:pixelated}</style><h1>North short step: live peer collection and topology</h1><p>163 native checks;12 cases/24 exact source-native captures;0 failures. Main._update_test_walker collects an actual active stationary Bill root and updates selected Marsh. Blocking roots release the finite source without passing through; nonblocking controls keep one clock advance. Removing occupied/placed floor invokes the real topology rebuild and stops without teleport or old callback. Non-running actor guard passes.</p><p>Four prescribed clip phases in furnished cold store, normal failure flags retained, explicit fixture placement, staged actor/renderer/manifest. Bill is not recovered/scheduled; this tests live peer collection, not natural moving traffic or a complete yield route. Discrete before/after captures do not establish continuous motion or normal save/title acceptance.24 targeted inputs unchanged;2931 owner files unchanged.</p>'
    for n in names:html+='<h2>'+n.removesuffix('.png')+'</h2><img src="'+n+'">'
    html+='<p>Each cell: unscaled native context and exact submitted source on matte. <a href="verification.json">Bound evidence</a></p>'
    (DEST/'index.html').write_text(html);print('163 native checks;12 coordinator/topology cases;24 source/native pairs')
if __name__=='__main__':main()
