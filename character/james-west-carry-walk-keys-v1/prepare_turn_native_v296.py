from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose4-v296';base=p/'arrival-turn-refine-v290'
gd=(base/'native_probe.gd').read_text().replace('arrival-turn-refine-v290','arrival-turn-pose4-v296')
(o/'native_probe.gd').write_text(gd,encoding='utf-8')
m=json.loads((base/'bare-review-manifest.json').read_bytes());m['states'][1]['frameFiles']=['res://character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/004.png'];m['states'][2]['frameFiles']=['res://character/james-west-carry-walk-keys-v1/arrival-turn-pose4-v296/fixed-canvas-source.png']
(o/'bare-review-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
paths=[r/'scripts/crew_sprite_player.gd',o/'native_probe.gd',o/'bare-review-manifest.json']+[r/s['frameFiles'][0][6:] for s in m['states']]
(o/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},normalChanged=False),indent=2)+'\n')
print('Prepared three-source native material/geometry comparison.')
