from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v13'
template=p/'paired-v12/native_probe.gd'
source=template.read_text().replace('paired-v12','paired-v13').replace('[0,12,24,36,48]','[0,12,24,36,46,48]').replace('five observed paired captures','six observed paired captures')
(out/'native_probe.gd').write_text(source,encoding='utf-8')
files=[template,Path(__file__),out/'native_probe.gd',out/'bare-manifest.json',out/'helmet-manifest.json',r/'scripts/crew_sprite_player.gd',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for kind in ('bare','helmet'):
 m=json.loads((out/(kind+'-manifest.json')).read_bytes());assert m['strideDistanceCells']['carry-west']==0.1796875
 files.extend(r/f[6:] for f in m['states'][0]['frameFiles'])
(out/'native-inputs.json').write_text(json.dumps({'preLaunchSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Contact candidate distance probe prepared; six paired captures including repaired46.')
