"""Bind the unselected whole-pose shuffle audition to exact source/native hashes."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-step-v1'
RUN=ROOT/'output/marsh-animation-audit/north-step-native-2026-10-02'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    master='character/marsh-motion-polish-v1/sources/north-standing-identity-01.png'
    idle='character/marsh-v2/frames/bare/idle-north/000.png'
    gait='character/marsh-north-walk-material-v1/candidate-01/001.png'
    runs=[('01','exec-320d391a-aa15-4970-90d9-5d08e45cb432',[master,idle,gait,'character/marsh-north-stop-v1/sources/north-stop-09.png'],'rejected: high knee/full sole, repeated left lift rather than right follow'),('02','exec-9a52e7fc-e74a-4b3e-bd4b-1abed43a08e9',[master,idle],'rejected choreography: opening right boot lifts and third pose repeats right lift; neutral-ruler widths54-55'),('03','exec-72845e8f-2e85-4988-aee6-4fa1af749708',['character/marsh-north-step-v1/sources/north-step-02.png',master,idle],'rejected: third right boot still lifts, fourth cell expands to62px; intermediate edit target retained'),('04','exec-fada2ac1-6b9d-46c6-aafe-66e0b36d69c1',['character/marsh-north-step-v1/sources/north-step-03.png'],'unselected source audition: grounded landing repaired; widths55-56; motion/contact/world acceptance pending')]
    sources=[]
    for version, generation, refs, decision in runs:
        raw=BASE/'sources'/('north-step-'+version+'.png'); prompt=raw.with_suffix('.prompt.txt')
        sources.append({'version':version,'provider':'built-in imagegen','generation':generation,'raw':raw.relative_to(ROOT).as_posix(),'rawSha256':sha(raw),'prompt':prompt.relative_to(ROOT).as_posix(),'promptSha256':sha(prompt),'orderedReferences':[{'path':p,'sha256':sha(ROOT/p)} for p in refs],'decision':decision})
    existing_path=BASE/'sources/provenance.json'
    if existing_path.exists():
        later=[entry for entry in json.loads(existing_path.read_text())['trials'] if entry['version'] not in {r[0] for r in runs}]
        sources.extend(later)
    sources[3]['decision']='rejected for moving step: zero forward landing depth; historical166check source-clock audition remains scoped to stationary presentation'
    (BASE/'sources/provenance.json').write_text(json.dumps({'normalAdmission':False,'trials':sources},indent=2)+'\n')
    candidate=BASE/'candidate-04'; frames=[Image.open(candidate/('%03d.png'%i)).convert('RGBA') for i in range(7)]
    assert frames[0].tobytes()==frames[-1].tobytes()==Image.open(ROOT/idle).convert('RGBA').tobytes()
    for im in frames:
        a=np.array(im); assert set(np.unique(a[:,:,3])) <= {0,255}; assert not np.any(a[a[:,:,3]==0,:3])
    report=json.loads((RUN/'report.json').read_text()); assert report['failures']==0 and len(report['captures'])==7
    before=json.loads((RUN/'owner-before.json').read_text()); after=json.loads((RUN/'owner-after.json').read_text()); assert before==after
    log=(RUN/'native.log').read_text(encoding='utf-8-sig'); assert 'ERROR:' not in log and 'SCRIPT ERROR:' not in log
    review=BASE/'review'; review.mkdir(exist_ok=True)
    board=Image.new('RGB',(900,7*460))
    captures=[]; images=[]
    for i, record in enumerate(report['captures']):
        assert record['slot']==i
        p=RUN/record['file']; im=Image.open(p).convert('RGB'); board.paste(im,(0,i*460)); images.append(im)
        captures.append({**record,'nativeSha256':sha(p),'sourceSha256':sha(candidate/('%03d.png'%i))})
    board.save(review/'native-board.png')
    # Lossless native motion preview: no palette reduction or color change.
    images[0].save(review/'motion.png',save_all=True,append_images=images[1:],duration=[120]*6+[480],loop=0)
    decoded=Image.open(review/'motion.png'); assert decoded.n_frames==7
    for i, im in enumerate(images):
        decoded.seek(i); assert decoded.convert('RGB').tobytes()==im.tobytes()
    verification={'normalAdmission':False,'nativeChecks':report['checks'],'failures':0,'nativeCaptures':captures,'losslessPreviewFramesVerified':7,'ownerNonLogFiles':len(before),'ownerUnchanged':True,'sourceClockOnly':True,'rootContactVerified':False,'continueVerified':False,'inputs':{p:sha(ROOT/p) for p in ['tools/review_marsh_north_step.gd','tools/build_marsh_north_step.py','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','character/marsh-v2/catalog.json','character/marsh-north-step-v1/candidate-04/manifest.json']},'logSha256':sha(RUN/'native.log'),'scope':report['scope']}
    prior_path=review/'verification.json'
    if prior_path.exists():
        prior=json.loads(prior_path.read_text())
        if prior.get('logSha256')==verification['logSha256']:
            verification['inputs']=prior['inputs']
    verification['currentFixtureMatchesCaptured']=verification['inputs']['tools/review_marsh_north_step.gd']==sha(ROOT/'tools/review_marsh_north_step.gd')
    verification['motionDecision']='rejected: zero forward landing depth; source-clock checks are historical presentation evidence only'
    (review/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    (review/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh North short step — unselected audition</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;max-width:1000px;margin:32px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>North short step — unselected</h1><p>Seven120ms source holds; exact selected idle entrance and exit. Candidate04 repairs the left-foot landing after three retained rejected studies. Shared neutral ruler, whole figures, no grading.</p><p>Native source-clock review at148 and65.28 density. '+str(report['checks'])+'checks,7captures,0failures. Owner profile unchanged. Root travel/contact, natural routes, production selection and Continue remain unverified.</p><p>Lossless motion preview repeats with480ms final viewer hold; authored clip remains840ms.</p><img src="motion.png"><h2>Native captures</h2><img src="native-board.png"><p><a href="verification.json">Exact evidence</a> · <a href="../sources/provenance.json">Four source trials</a></p>')
    html=(review/'index.html').read_text(); html=html.replace('<h1>North short step — unselected</h1>','<h1>North short step — rejected for movement</h1><p>The later contact audit found zero forward landing depth. These historical stationary source-clock checks do not qualify this candidate for a moving step. See the <a href="../landing-review/index.html">revised landing study</a>.</p>')
    (review/'index.html').write_text(html)
    print(report['checks'],'historical native checks; seven captures;',len(sources),'retained trials;',len(before),'owner files unchanged')
if __name__=='__main__': main()
