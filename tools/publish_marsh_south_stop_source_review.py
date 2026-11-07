"""Bind phase4 stop artwork to source-only native presentation, not gameplay."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw
from build_marsh_south_start import sole

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-stop-v1'
RUN=ROOT/'output/marsh-animation-audit/south-stop-source-native-v1-2026-10-02'
DEST=BASE/'source-motion-review-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report=json.loads((RUN/'report.json').read_text());assert report['failures']==0 and len(report['captures'])==56
    inputs=json.loads((RUN/'inputs-before.json').read_text());assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for path,digest in inputs.items():assert sha(ROOT/path)==digest,path
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    recipe=json.loads((BASE/'candidate-07/phase-4/recipe.json').read_text())
    request=json.loads((BASE/'sources/stop-phase4-07.request.json').read_text())
    assert sha(BASE/'sources/stop-phase4-07.raw.png')==request['rawSha256']
    assert sha(BASE/'sources/stop-phase4-07.prompt.txt')==request['promptSha256']
    for reference in request['orderedReferences']:assert sha(ROOT/reference['path'])==reference['sha256']
    assert sha(BASE/'candidate-07/phase-4/000.png')==recipe['gaitSha256']
    assert sha(BASE/'candidate-07/phase-4/004.png')==recipe['idleSha256']
    DEST.mkdir(exist_ok=True);source_board=Image.new('RGB',(1472,7*218),'#293b40');native_board=Image.new('RGB',(1200,7*218),'#293b40')
    sd=ImageDraw.Draw(source_board);nd=ImageDraw.Draw(native_board);sources=[];native=[];records=[]
    for index,record in enumerate(report['captures']):
        folder=BASE/'candidate-07/phase-4' if record['key']=='walk-stop-phase4-south' else ROOT/'character/marsh-south-idle-material-v1/candidate-01'
        expected=Image.open(folder/f'{record["slot"]:03d}.png').convert('RGBA')
        source=Image.open(RUN/record['sourceFile']).convert('RGBA');assert source.size==expected.size and source.tobytes()==expected.tobytes()
        image=Image.open(RUN/record['file']).convert('RGB').crop((400,200,550,400))
        sources.append(source);native.append(image)
        for board,draw,panel,width in [(source_board,sd,source,184),(native_board,nd,image,150)]:
            x=index%8*width;y=index//8*218;board.paste(panel,(x,y+18),panel if panel.mode=='RGBA' else None)
            draw.text((x+2,y+2),f'{record["time"]:.2f}s #{record["slot"]}',fill='white')
        records.append({**record,'sourceSha256':sha(RUN/record['sourceFile']),'nativeSha256':sha(RUN/record['file'])})
    source_board.save(DEST/'source-board.png');native_board.save(DEST/'native-board.png')
    durations=[20]*55+[600]
    for name,frames in [('source-motion.png',sources),('native-motion.png',native)]:
        frames[0].save(DEST/name,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
        cursor=0
        with Image.open(DEST/name) as decoded:
            for index in range(decoded.n_frames):
                decoded.seek(index);remaining=round(decoded.info['duration'])
                while remaining:
                    assert decoded.convert(frames[0].mode).tobytes()==frames[cursor].tobytes()
                    remaining-=durations[cursor];cursor+=1
                assert remaining==0
        assert cursor==56
    poses=[Image.open(BASE/f'candidate-07/phase-4/{slot:03d}.png').convert('RGBA') for slot in range(5)]
    contacts=[{'left':sole(pose,True),'right':sole(pose,False)} for pose in poses]
    evidence={**report,'captures':records,'targetedInputs':inputs,'targetedInputsUnchanged':True,
              'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'decodedNativeSourcePairs':56,
              'normalAdmission':False,'actualStoppingControllerVerified':False,'contacts':contacts,
              'terminalRightLateralSeamDense':contacts[3]['right'][0]-contacts[4]['right'][0],
              'terminalRightDepthSeamDense':contacts[3]['right'][1]-contacts[4]['right'][1],
              'earlyRightSupportLateralResidualDense':contacts[1]['right'][0]-contacts[0]['right'][0],
              'leftRecoveryExtraLiftDense':contacts[0]['left'][1]-contacts[1]['left'][1],
              'inputFreezeScope':'22 targeted source/runtime inputs, not recursive dependency inventory; extra provenance refs checked at publication',
              'nativeLogSha256':sha(RUN/'native.log'),'publisherSha256':sha(Path(__file__)),
              'visualReview':'Pending source/native board inspection',
              'limits':'Prescribed source clock/stationary actor, fixture idle reset at.4s. No actual route stop/root/controller/priority/safety/snapshots/save/title Continue or natural traffic acceptance.'}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    html=f'''<!doctype html><meta charset="utf-8"><title>Marsh South phase4 stop source study</title>
<style>body{{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px;padding:16px}}img{{max-width:100%;image-rendering:pixelated}}.motion{{width:300px}}a{{color:#b8ddd5}}</style>
<h1>South phase4 stopping artwork — source-only native study</h1>
<p>{report['checks']} native checks,56 exact decoded source/native pairs. Five80ms holds, then exact staged idle0 and its650ms hold before idle1. Explicit fixture clock and stationary root; no actual stopping controller or normal admission.</p>
<p>{report['scope']}</p><p>22targeted inputs stable;{len(owner)} owner files unchanged under scratch APPDATA. First green175check interval retained; inspection found inherited idle phase, so fixture now resets idle playback at.4s and checks the650ms hold. No normal actor logic changed.</p>
<p>At sharedH148/184/p92,172 the terminal right sole is only.5dense pixel from exact idle laterally, with0depth gap; left support exact. Early right support has.5dense lateral residual. Left recovering boot rises3dense beyond its starting location; a small recovery arc, not the requested pure descent. These are source measurements at a fixed root, not verified controller contact.</p>
<img class="motion" src="native-motion.png"><img class="motion" src="source-motion.png">
<h2>Whole-figure source comparison</h2><img src="../candidate-07/phase-4/comparison-2x.png">
<h2>All native samples</h2><img src="native-board.png"><h2>Submitted sources</h2><img src="source-board.png">
<p><a href="verification.json">Bound evidence</a> · <a href="../sources/stop-phase4-07.raw.png">Source07</a> · <a href="../sources/stop-phase4-07.prompt.txt">Exact prompt</a> · <a href="../sources/stop-phase4-07.request.json">Provenance</a> · <a href="../../marsh-south-idle-material-v1/motion-review-v1/index.html">Matched idle/start/gait review</a></p>'''
    (DEST/'index.html').write_text(html,encoding='utf-8')
    print(f'{report["checks"]} native source-only checks;56exact APNG/source pairs;22inputs/{len(owner)} owner files unchanged')

if __name__=='__main__':
    main()
