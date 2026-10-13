"""Publish exact isolated native evidence for the staged South idle/start/gait family."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from build_marsh_south_start import sole

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-idle-material-v1'
RUN=ROOT/'output/marsh-animation-audit/south-idle-material-native-v1-2026-10-02'
DEST=BASE/'motion-review-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report=json.loads((RUN/'report.json').read_text())
    assert report['failures']==0 and len(report['captures'])==83
    inputs=json.loads((RUN/'inputs-before.json').read_text())
    assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for path,digest in inputs.items():assert sha(ROOT/path)==digest,path
    owner=json.loads((RUN/'owner-before.json').read_text())
    assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    request=json.loads((BASE/'sources/idle-01.request.json').read_text())
    assert sha(BASE/'sources/idle-01.raw.png')==request['rawSha256']
    assert sha(BASE/'sources/idle-01.prompt.txt')==request['promptSha256']
    for ref in request['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
    baseline=json.loads((BASE/'baseline.json').read_text());alpha_compared=0
    for original in baseline['frames']:
        old=np.array(Image.open(ROOT/original['path']).convert('RGBA'))
        new=np.array(Image.open(BASE/f'candidate-01/{original["slot"]:03d}.png').convert('RGBA'))
        assert sha(ROOT/original['path'])==original['sha256']
        assert np.array_equal(old[:,:,3],new[:,:,3]);alpha_compared+=old.shape[0]*old.shape[1]
    assert (BASE/'candidate-01/000.png').read_bytes()==(BASE/'candidate-01/south-start/000.png').read_bytes()
    for slot in range(1,5):
        assert (BASE/f'candidate-01/south-start/{slot:03d}.png').read_bytes()==(ROOT/f'character/marsh-south-walk-material-v1/candidate-02/south-start/{slot:03d}.png').read_bytes()
    DEST.mkdir(exist_ok=True)
    boards=[Image.new('RGB',(1472,11*218),'#293b40'),Image.new('RGB',(1200,11*218),'#293b40')]
    draws=[ImageDraw.Draw(board) for board in boards]
    sources=[];native=[];records=[];contacts=[];unique={}
    for index,record in enumerate(report['captures']):
        key=record['key'];slot=record['slot']
        folder=BASE/'candidate-01' if key=='idle-south' else BASE/'candidate-01/south-start' if key=='walk-start-south' else ROOT/'character/marsh-south-walk-material-v1/candidate-02'
        expected=Image.open(folder/f'{slot:03d}.png').convert('RGBA')
        source=Image.open(RUN/record['sourceFile']).convert('RGBA')
        assert source.tobytes()==expected.tobytes() and source.size==expected.size
        image=Image.open(RUN/record['file']).convert('RGB').crop((400,200,550,400))
        sources.append(source);native.append(image);unique.setdefault((key,slot),(source,image))
        for board,draw,panel,width in zip(boards,draws,[source,image],[184,150]):
            x=index%8*width;y=index//8*218
            board.paste(panel,(x,y+18),panel if panel.mode=='RGBA' else None)
            draw.text((x+2,y+2),f'{record["time"]:.2f}s #{slot}',fill='white')
        records.append({**record,'sourceSha256':sha(RUN/record['sourceFile']),'nativeSha256':sha(RUN/record['file'])})
        if (key=='walk-start-south' and slot in [3,4]) or record['time']==.4:
            support=sole(source,True)
            contacts.append([record['foot'][0]+record['drawOffset'][0]+(support[0]-92)*65.28/148,
                             record['foot'][1]+record['drawOffset'][1]+(support[1]-172)*65.28/148])
    assert len(unique)==13
    for board,name in zip(boards,['source-board.png','native-board.png']):board.save(DEST/name)
    details=Image.new('RGB',(184*7,440),'#293b40');dd=ImageDraw.Draw(details)
    for index,((key,slot),(source,_)) in enumerate(unique.items()):
        x=index%7*184;y=index//7*220;details.paste(source,(x,y+24),source);dd.text((x+2,y+4),f'{key} {slot}',fill='white')
    details.resize((details.width*2,details.height*2),Image.Resampling.NEAREST).save(DEST/'unique-source-2x.png')
    durations=[650,650]+[20]*80+[600]
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
        assert cursor==83
    evidence={**report,'captures':records,'targetedInputs':inputs,'ownerNonLogFiles':len(owner),
              'targetedInputsUnchanged':True,'ownerUnchanged':True,'decodedNativeSourcePairs':83,
              'uniqueSourcePoses':13,'alphaPixelsCompared':alpha_compared,'normalAdmission':False,
              'inputFreezeScope':f'{len(inputs)} targeted source/runtime inputs; not a recursive world dependency freeze',
              'maxRootErrorWorld':max(record['rootErrorWorld'] for record in records),
              'maxJoinSupportLateralDriftWorld':max(point[0] for point in contacts)-min(point[0] for point in contacts),
              'maxJoinSupportDepthDriftWorld':max(point[1] for point in contacts)-min(point[1] for point in contacts),
              'nativeLogSha256':sha(RUN/'native.log'),
              'visualReview':'Pending inspection of native/source boards; static source comparison alone is insufficient.',
              'limits':'Explicit staged banks and fixture, deterministic actor updates/world/peers paused. Not continuous real-time pacing, natural traffic, updated safety/save/title Continue, ordinary stops or full-family fidelity.'}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    html=f'''<!doctype html><meta charset="utf-8"><title>Marsh staged South idle material</title>
<style>body{{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px;padding:16px}}img{{max-width:100%;image-rendering:pixelated}}a{{color:#b8ddd5}}.motion{{width:300px}}</style>
<h1>South idle material and start/gait handoff — staged</h1>
<p>{report['checks']} native checks,83 exact captured native/source pairs,13 unique poses. Both650ms breathing poses, all five80ms start holds and all six gait frames. No normal admission.</p>
<p>{len(inputs)} targeted inputs stable;{len(owner)} owner files unchanged under scratch APPDATA. Both idle alpha outlines exactly retained ({alpha_compared}pixels), including pivot/foot contacts and breathing silhouette. Whole generated material mapping covers97–98%, standard palette/no extra gain; not newly authored breathing motion.</p>
<p>{report['scope']}</p><p>{evidence['limits']}</p>
<img class="motion" src="native-motion.png"><img class="motion" src="source-motion.png">
<h2>All distinct submitted source poses</h2><img src="unique-source-2x.png">
<h2>Native samples</h2><img src="native-board.png"><h2>Submitted sources</h2><img src="source-board.png">
<h2>Old/new idle and family comparison</h2><img src="../candidate-01/comparison-3x.png">
<p><a href="verification.json">Bound evidence</a> · <a href="../sources/idle-01.raw.png">Generated source</a> · <a href="../sources/idle-01.prompt.txt">Exact prompt</a> · <a href="../sources/idle-01.request.json">Provenance</a> · <a href="../../marsh-south-stop-v1/index.html">Rejected stop studies</a></p>'''
    (DEST/'index.html').write_text(html,encoding='utf-8')
    print(f'{report["checks"]} native checks;83 exact decoded source/native pairs;13 poses;{alpha_compared} exact alpha pixels;{len(inputs)} inputs/{len(owner)} owner files stable')

if __name__=='__main__':
    main()
