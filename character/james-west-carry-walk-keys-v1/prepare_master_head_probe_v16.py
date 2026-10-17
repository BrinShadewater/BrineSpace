from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-head-review-v16';template=p/'paired-v14/native_probe.gd'
source=template.read_text().replace('paired-v14','master-head-review-v16')
(out/'native_probe.gd').write_text(source,encoding='utf-8')
files=[template,Path(__file__),out/'native_probe.gd',out/'bare-manifest.json',out/'helmet-manifest.json',p/'build_master_heads_v16.py',r/'scripts/crew_sprite_player.gd',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for mode in ('bare','helmet'):
 m=json.loads((out/(mode+'-manifest.json')).read_bytes());files.extend(r/f[6:] for f in m['states'][0]['frameFiles'])
(out/'native-inputs.json').write_text(json.dumps({'preLaunchSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Master-head candidate native distance probe inputs frozen.')
