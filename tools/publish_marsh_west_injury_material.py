"""Publish exact body/effect and actual controller evidence, still staged art."""
from pathlib import Path
import json,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-injury-material-v1'
AUDIT=ROOT/'output/marsh-animation-audit/west-injury-actor-01-2026-10-02'
BODY=ROOT/'character/marsh-west-collapse-material-v1/candidate-02'

def main():
    report=json.loads((AUDIT/'report.json').read_text())
    assert report['checks']==404 and report['failures']==0 and report['actorRestores']==12
    assert report['firstNormalIdleMatchesAuthoredEndpoint'] and len(report['captures'])==14
    assert (AUDIT/'native-exit.txt').read_text().strip()=='0'
    assert 'ERROR:' not in (AUDIT/'native.log').read_text()
    stable={}
    for name in ['inputs','owner']:
        before=json.loads((AUDIT/f'{name}-before.json').read_text());after=json.loads((AUDIT/f'{name}-after.json').read_text())
        assert before==after;stable[name]=len(before)
    recipe=json.loads((BASE/'candidate-01/recipe.json').read_text());assert len(recipe['records'])==12 and not recipe['normalAdmission']
    for r in recipe['records']:
        original=np.array(Image.open(ROOT/r['bodySource']).convert('RGBA'))
        new=np.array(Image.open(BASE/'candidate-01'/r['frame']).convert('RGBA'))
        assert np.array_equal(original[original[:,:,3]>0],new[original[:,:,3]>0])
    for name,action in [('injury','injury-ground-west'),('recovery','injury-rise-west')]:
        animation=Image.open(BASE/f'candidate-01/{name}.apng')
        assert animation.n_frames==6 and animation.info['loop']==1
        for i in range(6):
            animation.seek(i);expected=Image.open(BASE/f'candidate-01/{action}/{i:03d}.png').convert('RGBA')
            assert animation.info['duration']==180 and np.array_equal(np.array(animation.convert('RGBA')),np.array(expected))
    review=BASE/'actor-review-v1';review.mkdir(exist_ok=True)
    paths=[BODY/'000.png']+[BASE/f'candidate-01/{action}/{i:03d}.png' for action in ['injury-ground-west','injury-rise-west'] for i in range(6)]+[BODY/'000.png']
    boards=[];crops=[]
    for i,(capture,expected_path) in enumerate(zip(report['captures'],paths)):
        source=Image.open(AUDIT/capture['sourceFile']).convert('RGBA');expected=Image.open(expected_path).convert('RGBA')
        assert np.array_equal(np.array(source),np.array(expected))
        for key in ['file','sourceFile']:shutil.copy2(AUDIT/capture[key],review/capture[key])
        native=Image.open(AUDIT/capture['file']).convert('RGB')
        x=round(capture['canvasPosition'][0]*native.width/1920);y=round(capture['canvasPosition'][1]*native.height/1080)
        cropbox=(x-100,y-110,x+110,y+30)
        assert 0<=cropbox[0]<cropbox[2]<=native.width and 0<=cropbox[1]<cropbox[3]<=native.height
        crop=native.crop(cropbox);crop.save(review/f'crop-{i:03d}.png');crops.append(crop)
        board=Image.new('RGB',(530,260),'#293b40');draw=ImageDraw.Draw(board)
        board.paste(source,(20,48),source);board.paste(crop,(265,55))
        label=['Selected idle before','Injury pose0','Injury pose1','Injury pose2','Injury pose3','Injury pose4','Injury pose5','Recovery pose0','Recovery pose1','Recovery pose2','Recovery pose3','Recovery pose4','Recovery pose5','First normal idle after'][i]
        draw.text((10,8),label,fill='white');draw.text((10,27),'Exact whole source / exact framebuffer crop',fill='#b1d5c6');boards.append(board)
    for group in range(4):
        board=Image.new('RGB',(1060,520),'#293b40')
        for i,tile in enumerate(boards[group*4:group*4+4]):board.paste(tile,((i%2)*530,(i//2)*260))
        board.save(review/f'paired-{group}.png')
    crops[1].save(review/'finite-native-poses.apng',save_all=True,append_images=crops[2:13],duration=[180]*12,loop=1,disposal=1,blend=0)
    animation=Image.open(review/'finite-native-poses.apng');assert animation.n_frames==12 and animation.info['loop']==1
    for i in range(12):animation.seek(i);assert np.array_equal(np.array(animation.convert('RGB')),np.array(crops[i+1]))
    assessment=review/'visual-assessment.json'
    evidence={'checks':404,'failures':0,'engineErrors':0,'exitCode':0,'nativeSourcePairs':14,'exactSources':14,'actorPlayerRestores':12,'wholeBodyOpaquePixelMatches':12,'decodedSourceApngFrames':12,'decodedNativeApngFrames':12,'firstNormalIdleExact':True,'injuryRecoveryHandoffExact':True,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'normalAdmission':False,'productionRendererChange':'None in this West interval; existing simulation-owned injury playback resets cosmetic key for fresh idle.','visualReviewed':assessment.exists() and json.loads(assessment.read_text())['allFourteenPairedViewsInspected'],'scope':report['scope'],'limits':'Staged West source art only. Native APNG is captured pose illustration, not realtime recording/browser moving review. No full RunSave/Title Continue, other-facing material acceptance or articulated limb contact proof.','retainedFailedIntervals':[]}
    (review/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (review/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Marsh West white-fluid injury/recovery</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;max-width:1300px;margin:25px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Marsh West staged injury/recovery material</h1><p>Exact complete dry source body in twelve poses. Independently authored white-fluid inserts behind the body; common36px mature-puddle calibration. Fixed floor puddle, last two recovery phases half-alpha/none. No anatomy painting or palette changes.</p><p>404 actual actor/grid checks, fourteen exact sources, twelve actor/player restores. Injury-to-recovery and first normal idle exact.Bounded inputs stable;2931owner files unchanged. Existing renderer idle join verified for West; artwork remains unselected.</p><p><a href="../candidate-01/comparison.png">Whole source family</a> · <a href="finite-native-poses.apng">Finite native pose illustration</a> · <a href="verification.json">Scoped evidence</a></p>'''+''.join(f'<img src="paired-{i}.png">' for i in range(4)),encoding='utf-8')
    print(json.dumps(evidence))
if __name__=='__main__':main()
