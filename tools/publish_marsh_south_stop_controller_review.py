"""Bind actual staged phase4 arrival to isolated native artwork/controller evidence."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/south-stop-controller-v1-2026-10-02'
DEST=ROOT/'character/marsh-south-stop-v1/controller-review-v1'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report=json.loads((RUN/'report.json').read_text());assert report['failures']==0
    inputs=json.loads((RUN/'inputs-before.json').read_text());assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for path,digest in inputs.items():assert sha(ROOT/path)==digest,path
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert json.loads((RUN/'owner-before-unit.json').read_text())==json.loads((RUN/'owner-after-unit.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    unit=(RUN/'unit.log').read_text(encoding='utf-8-sig');assert '91 checks,0 failures' in unit and 'ERROR:' not in unit
    records=report['captures'];count=len(records);assert count>25
    folders={'walk-start-south':'character/marsh-south-idle-material-v1/candidate-01/south-start',
             'walk-south':'character/marsh-south-walk-material-v1/candidate-02',
             'walk-stop-phase4-south':'character/marsh-south-stop-v1/candidate-07/phase-4',
             'idle-south':'character/marsh-south-idle-material-v1/candidate-01'}
    rows=(count+7)//8;source_board=Image.new('RGB',(1472,rows*218),'#293b40');native_board=Image.new('RGB',(1200,rows*218),'#293b40')
    sd=ImageDraw.Draw(source_board);nd=ImageDraw.Draw(native_board);sources=[];native=[];bound=[]
    DEST.mkdir(exist_ok=True)
    for index,record in enumerate(records):
        expected_path=ROOT/folders[record['key']]/f'{record["slot"]:03d}.png'
        expected=Image.open(expected_path).convert('RGBA');source=Image.open(RUN/record['sourceFile']).convert('RGBA')
        assert source.size==expected.size and source.tobytes()==expected.tobytes()
        image=Image.open(RUN/record['file']).convert('RGB').crop((400,200,550,400))
        sources.append(source);native.append(image)
        for board,draw,panel,width in [(source_board,sd,source,184),(native_board,nd,image,150)]:
            x=index%8*width;y=index//8*218;board.paste(panel,(x,y+18),panel if panel.mode=='RGBA' else None)
            draw.text((x+2,y+2),f'{record["time"]:.2f}s #{record["slot"]}',fill='white')
        bound.append({**record,'sourceSha256':sha(RUN/record['sourceFile']),'nativeSha256':sha(RUN/record['file']),'canonicalSource':expected_path.relative_to(ROOT).as_posix()})
    source_board.save(DEST/'source-board.png');native_board.save(DEST/'native-board.png')
    durations=[round((records[index+1]['time']-record['time'])*1000) for index,record in enumerate(records[:-1])]+[600]
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
        assert cursor==count
    evidence={**report,'captures':bound,'targetedInputs':inputs,'targetedInputsUnchanged':True,
              'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'decodedNativeSourcePairs':count,
              'controllerChecks':91,'unitLogSha256':sha(RUN/'unit.log'),'nativeLogSha256':sha(RUN/'native.log'),
              'normalAdmission':False,'visualReview':'Pending native/source board inspection',
              'inputFreezeScope':f'{len(inputs)} targeted inputs before/after native interval; not recursive dependency inventory. Unit/controller hashes captured before subsequent native run; unit run had owner fingerprints but no independent prelaunch source freeze.',
              'limits':'Only one actual ordinary straight route/phase4. Unit-context priority/cancellation assertions do not prove actual hazards/service/coordinator traffic/save/title Continue or remaining5branches. Artwork widths/master full-family polish remain.'}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    html=f'''<!doctype html><meta charset="utf-8"><title>Marsh staged South phase4 stop controller</title>
<style>body{{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px;padding:16px}}img{{max-width:100%;image-rendering:pixelated}}.motion{{width:300px}}a{{color:#b8ddd5}}</style>
<h1>Actual South arrival and phase4 stop — staged</h1>
<p>91controller checks and{report['checks']}native checks,0failures;{count}exact decoded native/source pairs across134actual20ms actor updates. Native captures every update during start/stop and every5updates during locomotion/idle. One loaded gait cycle after authored start chooses actual phase4 at arrival; no phase forcing or scripted stop clock.</p>
<p>{report['scope']}</p><p>{evidence['limits']}</p><p>{len(inputs)}targeted native inputs stable and{len(owner)}owner files unchanged; unit owner interval also unchanged. Idle1 observed{report['firstIdle1Seconds']:.3f}s, expected{report['expectedIdle1Seconds']:.3f}s, within20ms sampling.</p>
<img class="motion" src="native-motion.png"><img class="motion" src="source-motion.png">
<h2>Native captured updates</h2><img src="native-board.png"><h2>Exact submitted sources</h2><img src="source-board.png">
<p><a href="verification.json">Bound evidence</a> · <a href="../source-motion-review-v1/index.html">Source-only artwork review</a> · <a href="../stop_controller.gd">Staged controller</a></p>'''
    (DEST/'index.html').write_text(html,encoding='utf-8')
    print(f'91controller/{report["checks"]}native checks;{count}exact source-native pairs;{len(inputs)}inputs/{len(owner)}owner stable')

if __name__=='__main__':main()
