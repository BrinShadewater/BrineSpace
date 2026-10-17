from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'release.gd').read_text()
s=s.replace('release_workshop.gd','release_workshop_v6.gd').replace('release.gd','release_v6.gd')
s=s.replace('release-evidence.json','release_v6-evidence.json').replace('-release-','-release-v6-')
s=s.replace('check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")','check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")\n\t\tif failures:quit(1);return')
s=s.replace('"Staged automatic room-owned West floor case','"V6 authored closer original center/corner hardware and44x25 alpha footprint. Staged automatic room-owned West floor case')
(p/'release_v6.gd').write_text(s)
prior=json.loads((p/'release-inputs.json').read_bytes())
paths=[r/k for k in prior if Path(k).name!='release.gd']+[p/'release_v6.gd',p/'release_workshop_v6.gd',p/'floor-case-west-v6.png']
(p/'release_v6-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
review=(p/'review_release.py').read_text().replace('floor-case-west.png','floor-case-west-v6.png')
for name in ['evidence','inputs','registration-evidence','review']:
    review=review.replace('release-'+name,'release_v6-'+name)
review=review.replace('-release-terminal','-release-v6-terminal').replace('-release-review.png','-release-v6-review.png')
(p/'review_release_v6.py').write_text(review)
print('V6 release/room review prepared;'+str(len(paths))+' targeted inputs frozen;previous source/evidence retained.')
