from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2];A=R/'character/veld-interact-west-original-master-v1/original-action-video-v1'
source=json.loads((P/'SOURCE_REVIEW.json').read_bytes());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in source['bindings'].items())
bindings=dict(source['bindings']);old=json.loads((A/'full-source-record.json').read_bytes())['bindings'];assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in old.items());bindings.update(old)
for gear in ['bare','helmet']:
 idle=json.loads((P/f'{gear}-source-manifest.json').read_bytes())['states'][0]
 action_manifest=json.loads((A/f'{gear}-source-manifest.json').read_bytes());action=action_manifest['states'][0]
 states=[dict(id='source-interact-west',frameCount=426,frameFiles=idle['frameFiles']+action['frameFiles']+idle['frameFiles'],frameDurationsMs=idle['frameDurationsMs']+action['frameDurationsMs']+idle['frameDurationsMs'],loop=False,facings=['west']*426,waterKinds=['interact']*426,waterPoses=[False]*426,depthOffsets=[0.0]*426)]+action_manifest['states'][1:]
 manifest=P/f'{gear}-joined-manifest.json';manifest.write_text(json.dumps(dict(name='Veld original West full idle scanner idle source '+gear,status='staged_source_clock_join_review_only',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,states=states),indent=2)+'\n');bindings[manifest.relative_to(R).as_posix()]=hashlib.sha256(manifest.read_bytes()).hexdigest()
 images=[Image.open(R/ref[6:]).convert('RGBA') for ref in states[0]['frameFiles']]
 images[0].save(P/f'{gear}-joined-full-source.png',save_all=True,append_images=images[1:],duration=states[0]['frameDurationsMs'],loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-joined-full-source.png');assert replay.n_frames==426
 for i,im in enumerate(images):replay.seek(i);assert np.array_equal(np.asarray(replay.convert('RGBA')),np.asarray(im));assert round(replay.info['duration'])==states[0]['frameDurationsMs'][i]
 board=Image.new('RGB',(2048,560),'#202a30');d=ImageDraw.Draw(board)
 for j,i in enumerate([140,141,142,143,282,283,284,285]):
  im=images[i];board.paste(im,(j*256,24),im);d.text((j*256+4,4),f'Joined source{i}',fill='white');detail=im.crop((100,60,164,124)).resize((256,256),Image.Resampling.NEAREST);board.paste(detail,(j*256,288),detail)
 board.save(P/f'{gear}-joined-details.png')
 for name in [f'{gear}-source-manifest.json']:
  path=P/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
for name in ['SOURCE_REVIEW.json','build_joined_study.py','generation.json','INPUTS.json']:
 path=P/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'joined-source-record.json').write_text(json.dumps(dict(frameCount=426,durationMs=17751,replayChecks=1704,failures=0,bindings=bindings,scope='Complete unchanged idle142/scanner142/idle142 source clocks, paired; no looping/controller/native contact/adoption claim.'),indent=2)+'\n')
test=(R/'tests/test_veld_west_interact_source_v1.gd').read_text()
test=test.replace('character/veld-interact-west-original-master-v1/original-action-video-v1/bare-source-manifest.json','character/veld-idle-west-original-master-v1/blink-only-v2/bare-joined-manifest.json').replace('character/veld-interact-west-original-master-v1/original-action-video-v1/helmet-source-manifest.json','character/veld-idle-west-original-master-v1/blink-only-v2/helmet-joined-manifest.json').replace('veld-west-interact-source','veld-west-idle-scanner-joins').replace('==142','==426').replace('All142','All426').replace('range(142)','range(426)').replace('elapsed-5.917','elapsed-17.751').replace('"source-interact-west",6,','"source-interact-west",18,').replace('full West scanner source','complete West idle/scanner/idle source').replace('Scanner action','Idle / scanner / idle').replace('VELD WEST INTERACT SOURCE','VELD WEST IDLE SCANNER JOINS')
(R/'tests/test_veld_west_idle_scanner_joins_v1.gd').write_text(test);(R/'tests/test_veld_west_idle_scanner_joins_v1.gd.uid').write_text('uid://cveldwestidlescanner1\n')
runner=(R/'tools/run_veld_west_interact_source_v1.py').read_text().replace('veld-west-interact-source','veld-west-idle-scanner-joins').replace('character/veld-interact-west-original-master-v1/original-action-video-v1','character/veld-idle-west-original-master-v1/blink-only-v2').replace('test_veld_west_interact_source_v1','test_veld_west_idle_scanner_joins_v1').replace("P/'full-source-record.json'","P/'joined-source-record.json'").replace("P/'build_source_clip.py'","P/'build_joined_study.py'").replace("P.glob('*-source-manifest.json')","P.glob('*-joined-manifest.json')").replace('Complete paired West interaction source-clock','Complete426paired West idle/scanner/idle source-clock')
(R/'tools/run_veld_west_idle_scanner_joins_v1.py').write_text(runner)
print('Complete426paired source clock joined study/1704replaychecks0 and isolated native fixture prepared')
