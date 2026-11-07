"""Bind six source-only native phase studies without claiming actor acceptance."""
from pathlib import Path
import hashlib,json,collections
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/south-stop-six-source-native-v1-2026-10-02'
DEST=ROOT/'character/marsh-south-stop-v1/six-source-motion-review-v1'
VERSIONS={0:'06',1:'06',2:'06',3:'01',4:'07',5:'01'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_motion(path,frames,durations):
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
    cursor=0
    with Image.open(path) as decoded:
        for index in range(decoded.n_frames):
            decoded.seek(index);remaining=round(decoded.info['duration'])
            while remaining:
                assert decoded.convert(frames[0].mode).tobytes()==frames[cursor].tobytes()
                remaining-=durations[cursor];cursor+=1
            assert remaining==0
    assert cursor==len(frames)
def main():
    report=json.loads((RUN/'report.json').read_text());assert report['failures']==0 and len(report['captures'])==336
    inputs=json.loads((RUN/'inputs-before.json').read_text());after=json.loads((RUN/'inputs-after.json').read_text())
    changed=[p for p in inputs if inputs[p]!=after[p]]
    assert set(changed)<={'scripts/grid_canvas.gd'},changed
    for p,d in after.items():assert sha(ROOT/p)==d,p
    loaded_renderer=sha(RUN/'loaded-grid-source.txt')
    assert loaded_renderer==sha(RUN/'frozen-grid-source.txt'), 'loaded renderer must match frozen bytes'
    assert loaded_renderer==inputs['scripts/grid_canvas.gd']
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    grouped=collections.defaultdict(list)
    for cap in report['captures']:grouped[cap['phase']].append(cap)
    assert sorted(grouped)==list(range(6))
    DEST.mkdir(exist_ok=True);records=[];previews=[]
    for phase,captures in grouped.items():
        assert len(captures)==56
        native=[];sources=[];nb=Image.new('RGB',(1200,7*218),'#293b40');sb=Image.new('RGB',(1472,7*218),'#293b40');nd=ImageDraw.Draw(nb);sd=ImageDraw.Draw(sb)
        for i,cap in enumerate(captures):
            folder=ROOT/f'character/marsh-south-stop-v1/candidate-{VERSIONS[phase]}/phase-{phase}' if cap['key'].startswith('walk-stop') else ROOT/'character/marsh-south-idle-material-v1/candidate-01'
            expected=folder/f'{cap["slot"]:03d}.png';source=Image.open(RUN/cap['sourceFile']).convert('RGBA');canonical=Image.open(expected).convert('RGBA')
            assert source.size==canonical.size and source.tobytes()==canonical.tobytes()
            shot=Image.open(RUN/cap['file']).convert('RGB').crop((400,200,550,400));sources.append(source);native.append(shot)
            for board,draw,panel,width in [(nb,nd,shot,150),(sb,sd,source,184)]:
                x=i%8*width;y=i//8*218;board.paste(panel,(x,y+18),panel if panel.mode=='RGBA' else None);draw.text((x+2,y+2),f'{cap["time"]:.2f}s #{cap["slot"]}',fill='white')
            records.append({**cap,'sourcePath':expected.relative_to(ROOT).as_posix(),'sourceFileSha256':sha(expected),'capturedSourceSha256':sha(RUN/cap['sourceFile']),'nativeSha256':sha(RUN/cap['file'])})
        for key in ['native','source']:
            (nb if key=='native' else sb).save(DEST/f'phase-{phase}-{key}-board.png')
            verify_motion(DEST/f'phase-{phase}-{key}-motion.png',native if key=='native' else sources,[20]*55+[600])
        previews.append({'phase':phase,'sourceBoard':f'phase-{phase}-source-board.png','nativeBoard':f'phase-{phase}-native-board.png','sourceMotion':f'phase-{phase}-source-motion.png','nativeMotion':f'phase-{phase}-native-motion.png'})
    evidence={**report,'captures':records,'targetedInputs':inputs,'targetedInputsAfter':after,'targetedDiskInputsStable':len(inputs)-len(changed),'changedDiskInputs':changed,'loadedRendererSha256':loaded_renderer,'loadedRendererMatchesFrozen':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'exactSourceNativePairs':336,'decodedApngIntervals':672,'previews':previews,'normalAdmission':False,'actualStoppingControllerVerified':False,'visualReview':'Pending all six native/source board pairs and motion inspection','inputFreezeScope':str(len(inputs))+' targeted pre/post controller/runtime/source/manifest/recipe inputs, not recursive dependency inventory. Loaded renderer source snapshot also matches frozen source bytes. Prescribed stationary source clock; explicit fixture idle seed at.4s.','nativeLogSha256':sha(RUN/'native.log'),'publisherSha256':sha(Path(__file__))}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    html='<!doctype html><meta charset="utf-8"><title>Marsh six South stop source motion</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;max-width:1500px;margin:30px auto}img{max-width:100%;image-rendering:pixelated}.motion{width:300px}</style><h1>Six South stop branches: source-only native motion</h1><p>'+str(report['checks'])+' native checks,336 exact captured source/native pairs,672 decoded APNG capture-interval matches. '+str(len(inputs)-len(changed))+'/'+str(len(inputs))+' targeted disk inputs stable; loaded renderer matches retained frozen bytes. '+str(len(owner))+' owner files unchanged under scratchAPPDATA.</p><p>'+report['scope']+'</p>'
    for p in previews:html+='<h2>Phase'+str(p['phase'])+'</h2><img class="motion" src="'+p['nativeMotion']+'"><img class="motion" src="'+p['sourceMotion']+'"><img src="'+p['nativeBoard']+'"><img src="'+p['sourceBoard']+'">'
    html+='<p>'+evidence['visualReview']+'</p><a href="verification.json">Bound evidence</a>'
    (DEST/'index.html').write_text(html,encoding='utf-8');print(report['checks'],'checks;336pairs;672decoded intervals;',len(inputs)-len(changed),'stable disk inputs; loaded renderer bound;',len(owner),'owner files unchanged')
if __name__=='__main__':main()
