from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-chronology-v298';o.mkdir(exist_ok=True)
script=(p/'build_arrival_review_v295.py').read_text().replace("o=p/'arrival-turn-chronology-v295'","o=p/'arrival-turn-chronology-v298'")
script=script.replace("p/'arrival-turn-pose1-v292/fixed-canvas-source.png'","old/'001.png'").replace('arrival-turn-pose2-v293','arrival-turn-pose2-v297').replace('arrival-turn-pose4-v294','arrival-turn-pose4-v296').replace("'New turn1'","'Old turn1'")
exec(compile(script,str(p/'build_arrival_review_v295.py'),'exec'))
inp=json.loads((o/'inputs.json').read_bytes());m=dict(frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',states=[])
for key,files in [('original',[f'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/{i:03}.png' for i in range(6)]),('candidate',[x['file'] for x in inp['sources'][1:7]])]:
 m['states'].append(dict(id=key,frameCount=6,frameFiles=['res://'+f for f in files],frameDurationsMs=inp['clockMs'],loop=False))
m['states'].append(dict(id='master',frameCount=1,frameFiles=['res://character/james-west-master-carry-v1/registered-original-master.png'],frameDurationsMs=[140],loop=False))
(o/'bare-review-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
paths=[r/'scripts/crew_sprite_player.gd',o/'native_probe.gd',o/'bare-review-manifest.json']+[r/f[6:] for s in m['states'] for f in s['frameFiles']]
(o/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},normalChanged=False),indent=2)+'\n')
