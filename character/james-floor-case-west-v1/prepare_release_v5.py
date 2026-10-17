from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'release.gd').read_text()
s=s.replace('release_workshop.gd','release_workshop_v5.gd').replace('release.gd','release_v5.gd')
s=s.replace('release-evidence.json','release_v5-evidence.json').replace('-release-','-release-v5-')
s=s.replace('check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")','check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")\n\t\tif failures:quit(1);return')
s=s.replace('"Staged automatic room-owned West floor case','"V5 authored smaller/duller pads and44x26 alpha footprint. Staged automatic room-owned West floor case')
(p/'release_v5.gd').write_text(s)
prior=json.loads((p/'release-inputs.json').read_bytes())
paths=[r/k for k in prior if Path(k).name!='release.gd']+[p/'release_v5.gd',p/'release_workshop_v5.gd',p/'floor-case-west-v5.png']
(p/'release_v5-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
review=(p/'review_release.py').read_text().replace('floor-case-west.png','floor-case-west-v5.png')
for name in ['evidence','inputs','registration-evidence','review']:
    review=review.replace('release-'+name,'release_v5-'+name)
review=review.replace('-release-terminal','-release-v5-terminal').replace('-release-review.png','-release-v5-review.png')
(p/'review_release_v5.py').write_text(review)
print('V5 release/room review prepared;'+str(len(paths))+' targeted inputs frozen;previous source/evidence retained.')
