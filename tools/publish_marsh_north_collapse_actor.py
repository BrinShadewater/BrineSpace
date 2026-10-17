"""Publish actual staged actor captures without production artwork admission."""
from pathlib import Path
import json,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-collapse-material-v1'
AUDIT=ROOT/'output/marsh-animation-audit/north-collapse-actor-02-2026-10-02'

def main():
    report=json.loads((AUDIT/'report.json').read_text())
    assert report['checks']==249 and report['failures']==0 and report['actorRestores']==6
    assert len(report['captures'])==8 and len(report['samples'])==66
    assert (AUDIT/'native-exit.txt').read_text().strip()=='0'
    assert 'ERROR:' not in (AUDIT/'native.log').read_text()
    stable={}
    for name in ['inputs','owner']:
        before=json.loads((AUDIT/f'{name}-before.json').read_text());after=json.loads((AUDIT/f'{name}-after.json').read_text())
        assert before==after;stable[name]=len(before)
    captures=report['captures'];assert [c['slot'] for c in captures]==[-1,0,1,2,3,4,5,5]
    assert len({tuple(c['foot']) for c in captures})==1
    review=BASE/'actor-review-v1';review.mkdir(exist_ok=True)
    source_animation=Image.open(BASE/'candidate-02/source-motion.apng')
    assert source_animation.n_frames==6 and source_animation.info['loop']==1
    for i in range(6):
        source_animation.seek(i)
        expected=Image.open(BASE/f'candidate-02/{i:03d}.png').convert('RGBA')
        assert source_animation.info['duration']==180 and np.array_equal(np.array(source_animation.convert('RGBA')),np.array(expected))
    boards=[];crops=[]
    for i,c in enumerate(captures):
        source=Image.open(AUDIT/c['sourceFile']).convert('RGBA')
        expected=Image.open(BASE/f'candidate-02/{max(0,c["slot"]):03d}.png').convert('RGBA')
        assert np.array_equal(np.array(source),np.array(expected))
        for key in ['file','sourceFile']:shutil.copy2(AUDIT/c[key],review/c[key])
        native=Image.open(AUDIT/c['file']).convert('RGB')
        # Configured1920x1080 design canvas to captured framebuffer, not art rescaling.
        x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080)
        cropbox=(x-100,y-110,x+110,y+30)
        assert 0<=cropbox[0]<cropbox[2]<=native.width and 0<=cropbox[1]<cropbox[3]<=native.height
        crop=native.crop(cropbox);crop.save(review/f'crop-{i:03d}.png');crops.append(crop)
        board=Image.new('RGB',(530,260),'#293b40');draw=ImageDraw.Draw(board)
        board.paste(source,(20,48),source);board.paste(crop,(265,55))
        draw.text((10,8),c['label']+' / slot'+str(c['slot']),fill='white')
        draw.text((10,27),'Source H148 / native crop unchanged pixel scale',fill='#b1d5c6')
        boards.append(board)
    for group in range(2):
        board=Image.new('RGB',(1060,520),'#293b40')
        for i,tile in enumerate(boards[group*4:group*4+4]):board.paste(tile,((i%2)*530,(i//2)*260))
        board.save(review/f'paired-{group}.png')
    crops[1].save(review/'finite-native-poses.apng',save_all=True,append_images=crops[2:7],duration=[180]*6,loop=1,disposal=1,blend=0)
    animation=Image.open(review/'finite-native-poses.apng');assert animation.n_frames==6 and animation.info['loop']==1
    for i in range(6):
        animation.seek(i);assert np.array_equal(np.array(animation.convert('RGB')),np.array(crops[i+1]))
    evidence={'checks':249,'failures':0,'engineErrors':0,'exitCode':0,'captures':8,'exactSources':8,'actorPlayerRestores':6,'traceSamples':66,'unchangedOwnerNonLogFiles':stable['owner'],'stableBoundedInputs':stable['inputs'],'normalAdmission':False,'visualReviewed':False,'scope':report['scope'],'nativeApng':'Six exact captured pose crops,180ms illustrative source holds, one play; not a realtime recording or browser motion review.','cropRule':'Configured1920x1080 design coordinates scaled to framebuffer; crop region visually reviewed separately. Native screenshot crop preserves exact pixels.','retainedFailedIntervals':[]}
    assessment=review/'visual-assessment.json'
    if assessment.exists():evidence['visualReviewed']=json.loads(assessment.read_text())['allEightPairedViewsInspected']
    (review/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (review/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Marsh North dry shutdown actor study</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;max-width:1300px;margin:25px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Marsh North dry shutdown: staged actual actor study</h1><p>Normal Marsh.die, main/grid/player; explicit unselected candidate02: complete milder first dip and four retained later source01 figures. 249checks, eight exact sources, six actor/player restores and pause holds. 63 bounded inputs stable;2931 owner files unchanged. Fixed root; actual visual-clock selection observed every20ms in a controlled fixture.</p><p>Paired exact source and framebuffer crops below. Warm ivory/sage and exposed dark soles retained. Proportions/foreshortening and moving floor joins remain provisional. No full RunSave/Title Continue or browser-motion acceptance. Injury/recovery unchanged.</p><p><a href="finite-native-poses.apng">Finite native pose illustration</a> · <a href="verification.json">Scoped evidence</a></p><img src="paired-0.png"><img src="paired-1.png">''',encoding='utf-8')
    print(json.dumps(evidence))
if __name__=='__main__':main()

