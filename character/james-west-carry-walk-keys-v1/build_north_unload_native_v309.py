from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-start-source-v309'
inputs=json.loads((o/'inputs.json').read_bytes())
paths=[p/'north-unload-join-review-v308/bare-runtime-master-review.png',r/inputs['sourceFile'],r/inputs['destinationOriginalFile'],o/'fixed-canvas-source.png']
m=dict(frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',states=[dict(id=key,frameCount=1,frameFiles=['res://'+f.relative_to(r).as_posix()],frameDurationsMs=[140],loop=False) for key,f in zip(['master','turnend','original','candidate'],paths)])
(o/'bare-review-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
s=(p/'arrival-turn-pose4-v296/native_probe.gd').read_text(encoding='utf-8').replace('arrival-turn-pose4-v296','north-unload-start-source-v309').replace('1200','1600').replace('range(3)','range(4)').replace('["master","original","candidate"]','["master","turnend","original","candidate"]').replace(' / original master and planted turn',' / north unloading start').replace('Three bare static sources at148/82/54/27; not paired helmet, full turn, traveling contact or ordinary arrival.','Four bare static sources at148/82/54/27; runtime North master, turnend, old and new unload1. Not paired helmet, continuous unload or ordinary arrival.').replace('JAMES TURN SOURCE','JAMES UNLOAD SOURCE')
(o/'native_probe.gd').write_text(s,encoding='utf-8')
frozen=[r/'scripts/crew_sprite_player.gd',o/'native_probe.gd',o/'bare-review-manifest.json']+paths
(o/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in frozen},normalChanged=False),indent=2)+'\n',encoding='utf-8')
print('Prepared four-source native comparison; normal selectors unchanged.')
