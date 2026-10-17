from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'south-arrival-v325';o.mkdir(exist_ok=True)
manifest=r/'character/james-cargo-half-turns-v1/bare-manifest.json';m=json.loads(manifest.read_bytes());state=next(s for s in m['states'] if s['id']=='carry-turn-south-north');files=[manifest.parent/f for f in state['frameFiles']]
board=Image.new('RGB',(1536,720),(47,58,62));draw=ImageDraw.Draw(board);metrics=[]
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');ys,xs=np.where(np.asarray(im)[:,:,3]>=128);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];x=(i%6)*256;y=(i//6)*360;board.paste(im,(x,y+40),im);draw.text((x+8,y+8),f'south-north{i} {state["frameDurationsMs"][i]}ms',fill='white');draw.text((x+8,y+315),str(bounds),fill='white');metrics.append(dict(file=f.relative_to(r).as_posix(),boundsAlpha128=bounds))
board.save(o/'south-north-source-review.png');(o/'source-measurements.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
text=(p/'arrival-join-v324/native_probe.gd').read_text(encoding='utf-8').replace('arrival-join-v324','south-arrival-v325').replace('arrival324','arrival325').replace('james-arrival324','james-arrival325')
text=text.replace('var from:=at+Vector2(96,0)','var from:=at-Vector2(0,96)').replace('"west"','"south"').replace('carry-west','carry-south').replace('carry-turn-west-north','carry-turn-south-north')
text=text.replace('var checkpoint:String="turn" if clock>=.405 and clock<.8 else "unload" if clock>=1.105 else ""','var checkpoint:String="turn" if clock>=.405 and clock<1.48 else "unload" if clock>=1.705 else ""')
text=text.replace('"All authored normal turn/unload slots observed"','"All11half-turn and6unload slots observed"')
(o/'native_probe.gd').write_text(text,encoding='utf-8')
sources=[o/'native_probe.gd',r/'scripts/james_workshop_arrival.gd',r/'scripts/james_cargo_player.gd',r/'scripts/branforth_npc.gd',manifest]+files
(o/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},normalHalfTurnMs=1600,arrivalHalfTurnMs=1480,unloadMs=520,middleHoldBeforeMs=200,middleHoldAfterMs=80),indent=2)+'\n',encoding='utf-8')
print('325 existing half-turn all11source poses and south movement/restore probe prepared.')
