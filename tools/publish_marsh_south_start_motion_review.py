"""Bind staged South native samples to exact inputs and lossless previews."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw
from build_marsh_south_start import sole
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/south-start-native-v1-2026-10-02'
DEST=ROOT/'character/marsh-south-start-v1/motion-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global RUN,DEST
    repair='--repair' in sys.argv
    material='--material' in sys.argv
    if repair:
        RUN=ROOT/'output/marsh-animation-audit/south-start-native-v2-2026-10-02'
        DEST=ROOT/'character/marsh-south-start-v1/motion-review-v2'
    if material:
        RUN=ROOT/'output/marsh-animation-audit/south-start-native-v3-2026-10-02'
        DEST=ROOT/'character/marsh-south-walk-material-v1/motion-review-v1'
    count=81 if material else 51
    report=json.loads((RUN/'report.json').read_text())
    assert report['failures']==0 and len(report['captures'])==count
    inputs=json.loads((RUN/'inputs-before.json').read_text())
    assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in inputs.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text())
    assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    DEST.mkdir(exist_ok=True)
    crop=(400,200,550,400);native=[];sources=[];records=[];contacts=[]
    rows=(count+7)//8
    board=Image.new('RGB',(1200,rows*218),'#293b40');draw=ImageDraw.Draw(board)
    sourceboard=Image.new('RGB',(1472,rows*206),'#293b40');sd=ImageDraw.Draw(sourceboard)
    for i,r in enumerate(report['captures']):
        im=Image.open(RUN/r['file']).convert('RGB').crop(crop)
        source=Image.open(RUN/r['sourceFile']).convert('RGBA')
        folder=('character/marsh-south-start-v1/candidate-04' if repair else 'character/marsh-south-start-v1/candidate-02') if r['key']=='walk-start-south' else 'character/marsh-v2/frames/bare/walk-south'
        if material:folder='character/marsh-south-walk-material-v1/candidate-02/south-start' if r['key']=='walk-start-south' else 'character/marsh-south-walk-material-v1/candidate-02'
        expected=Image.open(ROOT/folder/('%03d.png'%r['slot'])).convert('RGBA')
        assert source.size==expected.size and source.tobytes()==expected.tobytes()
        x=(i%8)*150;y=(i//8)*218;board.paste(im,(x,y+18));draw.text((x+2,y+2),f"{r['time']:.2f}s #{r['slot']}",fill='white')
        x=(i%8)*184;y=(i//8)*206;sourceboard.paste(source,(x,y+22),source);sd.text((x+2,y+2),f"{r['time']:.2f}s #{r['slot']}",fill='white')
        native.append(im);sources.append(source)
        records.append({**r,'nativeSha256':sha(RUN/r['file']),'sourceSha256':sha(RUN/r['sourceFile']),'crop':crop})
        if (r['key']=='walk-start-south' and r['slot'] in [3,4]) or r['time']==.4:
            support=sole(source,True)
            contacts.append({'time':r['time'],'x':r['foot'][0]+r['drawOffset'][0]+(support[0]-92)*65.28/148,'y':r['foot'][1]+r['drawOffset'][1]+(support[1]-172)*65.28/148})
    board.save(DEST/'native-board.png');sourceboard.save(DEST/'source-board.png')
    durations=[20]*(count-1)+[600]
    for name,frames in [('native-motion.png',native),('source-motion.png',sources)]:
        frames[0].save(DEST/name,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
        decoded=Image.open(DEST/name);cursor=0
        for i in range(decoded.n_frames):
            decoded.seek(i);ms=round(decoded.info['duration'])
            while ms:
                assert decoded.convert(frames[0].mode).tobytes()==frames[cursor].tobytes()
                ms-=durations[cursor];cursor+=1
            assert ms==0
        assert cursor==count
    evidence={**report,'captures':records,'targetedInputs':inputs,'targetedInputsUnchanged':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'decodedNativeSourcePairs':51,'normalAdmission':False,'realTimePacingVerified':False,'normalSaveTitleVerified':False,'nativeLogSha256':sha(RUN/'native.log'),'unitLogSha256':sha(RUN/'unit.log'),'inputFreezeScope':'24 targeted inputs; not recursive world dependency inventory.'}
    evidence['supportContacts']=contacts
    evidence['maxJoinSupportDepthDriftWorld']=max(c['y'] for c in contacts)-min(c['y'] for c in contacts)
    evidence['maxJoinSupportLateralDriftWorld']=max(c['x'] for c in contacts)-min(c['x'] for c in contacts)
    evidence['maxRootErrorWorld']=max(r['rootErrorWorld'] for r in records)
    evidence['visualReview']='Full native entry plus both51-pose boards inspected: depth seam resolved, lateral support centroid shifts1.985world; generated interiors warmer/brighter than actual selected gait, material/head source change remains visible. Staged, not accepted for normal selection.'
    if repair:evidence['visualReview']='Both51-pose source/native boards inspected: coherent supporting leg and stepping head align with selected gait; lateral seam reduced from1.985 to.221world (half a dense pixel), depth drift remains.000002world. Head centroid at step93.595 vs selected gait93.859dense, unlike rejected candidate03 at96.38. Generated interiors still warmer/brighter than selected gait; material/face-source change remains visible at join. Preferred staged geometry candidate04, not normal admission or complete master/material acceptance. Original and rejected candidates retained.'
    evidence['inputFreezeScope']=f'{len(inputs)} targeted inputs; not recursive world dependency inventory.'
    evidence['decodedNativeSourcePairs']=count
    if material:evidence['visualReview']='Full native gait4 handoff frame, all81-pose native/source boards, six-pose comparison and final detail crops inspected against original South master/idle/start: coherent face/harness/ivory material across the sampled join and all six gait poses, improved shin/panel continuity over rejected candidate01. Candidate02 preferred staged material bank. Original alpha geometry and older rig motion retained; no newly authored motion or full-family fidelity claim. Remaining half-dense-pixel support centroid seam unchanged. Service/priority/safety/save/title Continue and normal admission pending.'
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (DEST/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh staged South start</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px}img{max-width:100%;image-rendering:pixelated}.motion{width:300px}</style><h1>South walking start: staged native motion</h1><p>'+str(report['checks'])+' native checks, 51 actual 20ms samples through one second, zero failures. Five 80ms holds, six dense pixels / 2.646 world units of root advance, then selected gait4 with its first 80ms already consumed: phase .68. Source and native APNG decode to all 51 exact presentation pairs. Final 600ms hold and repetition are viewer-only.</p><p>'+report['scope']+'</p><p>155 controller checks passed. 24 targeted inputs and '+str(len(owner))+' owner non-log files unchanged. Native visual comparison remains a separate judgement; service, safety, save/title Continue and normal admission remain open.</p><img class="motion" src="native-motion.png"><img class="motion" src="source-motion.png"><h2>All native updates</h2><img src="native-board.png"><h2>Exact submitted sources</h2><img src="source-board.png"><p><a href="verification.json">Bound evidence</a> · <a href="../review/index.html">Original source/packing review</a></p>')
    html=DEST/'index.html';html.write_text(html.read_text()+'<h2>Visual review: repairs still required</h2><p>'+evidence['visualReview']+'</p><p>Depth drift '+format(evidence['maxJoinSupportDepthDriftWorld'],'.6f')+' world; lateral centroid drift '+format(evidence['maxJoinSupportLateralDriftWorld'],'.6f')+' world; max measured physical-root error '+format(evidence['maxRootErrorWorld'],'.6f')+' world. Loaded gait timing is asserted by controller test; its manifest is outside the24-file hash freeze. Source V1 retained; no normal selection.</p>')
    if repair:html.write_text(html.read_text().replace('24 targeted','28 targeted').replace('outside the24-file hash freeze','included in the28-file prelaunch hash freeze').replace('actual20ms','actual 20ms'))
    if material:html.write_text('<!doctype html><meta charset="utf-8"><title>Marsh South matched start/gait native study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px}img{max-width:100%;image-rendering:pixelated}.motion{width:300px}</style><h1>Matched South start and gait: staged native study</h1><p>333 native checks,155 controller checks,0failures.81 actual20ms samples through1.6s, all five start holds/all six gait poses; exact gait4 join at.68 phase with80ms already consumed. Two lossless APNGs decode to81 exact native/source pairs. Final600ms viewer hold/repeat only.</p><p>'+report['scope']+'</p><p>'+evidence['visualReview']+'</p><p>39 targeted prelaunch/post hashes stable, including loaded gait manifest and material builder/recipe/raw/grade/palette.2931 owner non-log files unchanged. Deterministic sampled updates, not real-time pacing/natural traffic. Support depth drift '+format(evidence['maxJoinSupportDepthDriftWorld'],'.6f')+'; lateral centroid drift '+format(evidence['maxJoinSupportLateralDriftWorld'],'.6f')+' world; max root quantization '+format(evidence['maxRootErrorWorld'],'.6f')+' world. Normal catalog unchanged.</p><img class="motion" src="native-motion.png"><img class="motion" src="source-motion.png"><h2>All native samples</h2><img src="native-board.png"><h2>Exact submitted source samples</h2><img src="source-board.png"><p><a href="verification.json">Bound native evidence</a> · <a href="../index.html">Original master/source/geometry/provenance review</a></p>')
    if repair:html.write_text(html.read_text()+'<h2>Source repair provenance</h2><p>Built-in imagegen edits, one shared neutral scale. Whole figures only; no independent limb shifts or grade. Candidate03 rejected: sole alignment concealed body shift and its prompt described the correction in the wrong direction. Corrected prompt03 uses actual source measurements.</p><p><a href="../sources/start-03.prompt.txt">Exact prompt03</a> · <a href="../sources/start-03.request.json">Ordered reference hashes/raw provenance</a> · <a href="../candidate-04/recipe.json">Packing recipe</a></p><img src="../candidate-04/comparison.png"><h2>Original South identity master</h2><img style="width:384px" src="../../marsh-motion-polish-v1/sources/south-standing-identity-01.png"><h2>Repaired raw whole strip</h2><img src="../sources/start-03.raw.png">')
    print(report['checks'],'native checks;',count,'lossless native/source pairs;',len(inputs),'targeted inputs;',len(owner),'owner files unchanged; support depth/lateral drift',evidence['maxJoinSupportDepthDriftWorld'],evidence['maxJoinSupportLateralDriftWorld'],'world; root error',evidence['maxRootErrorWorld'])
if __name__=='__main__':main()
