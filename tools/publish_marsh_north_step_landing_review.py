"""Record new source decisions and exact isolated landing evidence."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'character/marsh-north-step-v1'; RUN=ROOT/'output/marsh-animation-audit/north-step-landing-native-2026-10-02'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    master='character/marsh-motion-polish-v1/sources/north-standing-identity-01.png'; idle='character/marsh-v2/frames/bare/idle-north/000.png'
    ledger=json.loads((BASE/'sources/provenance.json').read_text()); ledger['trials']=ledger['trials'][:4]
    ledger['trials'][3]['decision']='rejected for moving short step: zero forward landing depth despite stationary166check source-clock pass'
    records=[('05','exec-138534ca-233e-4e56-a00f-a03dbb4859ab',['character/marsh-north-step-v1/sources/north-step-04.png',master,idle],'rejected: opposite-foot opening,28.94px right-forward landing beyond short-step depth; packaging support/bounds guard failed'),('06','exec-8fb8c906-4f9c-4141-857b-baf6163cbf28',['character/marsh-north-step-v1/sources/north-step-05.png'],'rejected: mixed opening feet/full presented sole;25.10px landing beyond short-step depth'),('07','exec-7d10f66a-ecb1-4c00-8112-20cf5eda7e92',[master,idle,'character/marsh-north-step-v1/sources/north-step-04.png'],'rejected moving depth: third raw pose only2.96dense pixels ahead'),('08','exec-db10b53a-58ef-44a6-906e-a7101ed0d184',[master,idle],'unselected isolated landing study;13dense pixel grounded-forward left contact/5.734world-unit implied depth;86native presentation checks'),('09','exec-66fcea78-2375-4cc3-8899-69e693ad9ecb',['character/marsh-north-step-v1/sources/north-step-08.png',master,idle],'unselected whole transfer/closing study; widths59/56/56, transfer arm spread and full moving joins pending visual/contact review')]
    for version,generation,refs,decision in records:
        raw=BASE/'sources'/('north-step-'+version+'.png'); prompt=raw.with_suffix('.prompt.txt')
        ledger['trials'].append({'version':version,'provider':'built-in imagegen','generation':generation,'raw':raw.relative_to(ROOT).as_posix(),'rawSha256':sha(raw),'prompt':prompt.relative_to(ROOT).as_posix(),'promptSha256':sha(prompt),'orderedReferences':[{'path':p,'sha256':sha(ROOT/p)} for p in refs],'decision':decision})
    (BASE/'sources/provenance.json').write_text(json.dumps(ledger,indent=2)+'\n')
    report=json.loads((RUN/'report.json').read_text()); assert report['failures']==0 and len(report['captures'])==3
    before=json.loads((RUN/'owner-before.json').read_text()); assert before==json.loads((RUN/'owner-after.json').read_text())
    log=(RUN/'native.log').read_text(encoding='utf-8-sig'); assert 'ERROR:' not in log
    recipe=json.loads((BASE/'candidate-08/recipe.json').read_text()); assert recipe['landingDepthPixels']==13 and 5<=recipe['impliedNorthLength']<=7
    review=BASE/'landing-review'; review.mkdir(exist_ok=True); board=Image.new('RGB',(900,1380)); images=[]; captures=[]
    for i,entry in enumerate(report['captures']):
        assert entry['slot']==i
        path=RUN/entry['file']; im=Image.open(path).convert('RGB'); images.append(im); board.paste(im,(0,460*i))
        captures.append({**entry,'nativeSha256':sha(path),'sourceSha256':sha(BASE/'candidate-08'/('%03d.png'%i))})
    board.save(review/'native-board.png'); images[0].save(review/'motion.png',save_all=True,append_images=images[1:],duration=[120,480,480],loop=0)
    decoded=Image.open(review/'motion.png'); assert decoded.n_frames==3
    for i,im in enumerate(images): decoded.seek(i); assert decoded.convert('RGB').tobytes()==im.tobytes()
    for version,count in [('08',3),('09',3)]:
        for i in range(count):
            a=np.array(Image.open(BASE/('candidate-'+version)/('%03d.png'%i)).convert('RGBA')); assert set(np.unique(a[:,:,3])) <= {0,255} and not np.any(a[a[:,:,3]==0,:3])
    verification={'normalAdmission':False,'nativeChecks':report['checks'],'failures':0,'nativeCaptures':captures,'ownerNonLogFiles':len(before),'ownerUnchanged':True,'landingDepthPixels':13,'impliedNorthLength':recipe['impliedNorthLength'],'rootContactVerified':False,'continueVerified':False,'fullStepVerified':False,'losslessDecodedNativePairs':3,'inputs':{p:sha(ROOT/p) for p in ['tools/review_marsh_north_step.gd','tools/build_marsh_north_step_landing.py','character/marsh-north-step-v1/candidate-08/manifest.json','character/marsh-north-step-v1/sources/north-step-08.png','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','character/marsh-v2/catalog.json']},'logSha256':sha(RUN/'native.log'),'scope':report['scope']}
    (review/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    (review/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh North landing study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;max-width:1000px;margin:32px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>North grounded-forward landing — unselected study</h1><p>One whole new pose with shared neutral ruler. Width54px versus55px idle. Left floor contact13dense pixels ahead, equivalent to5.734world units.86native presentation checks,0failures; owner2931files unchanged. Three presentation holds are a comparison, not a completed short step.</p><img src="motion.png"><p>Transfer/closure sources packaged separately;59px transfer arm spread and moving joins need review.</p><img src="../candidate-09/comparison.png"><h2>Native landing comparison</h2><img src="native-board.png"><p><a href="verification.json">Exact scoped evidence</a> · <a href="../sources/provenance.json">Nine raw trials/decisions</a></p><p>Actual moving support/root curve, safety, snapshots, Continue and normal selection remain unverified. The earlier candidate04 is rejected for movement because its landing has zero forward depth.</p>')
    print('Nine retained trials;',report['checks'],'isolated landing checks; three lossless pairs;',len(before),'owner files unchanged')
if __name__=='__main__': main()
