from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];old=r/'character/james-floor-case-west-v1'
s=(old/'full_return_upper_v16.gd').read_text()
s=s.replace('const OUT := "res://character/james-floor-case-west-v1/"','const OUT := "res://character/james-west-donor-comparison-v1/"')
s=s.replace('res://character/james-cargo-return-bridges-v1/bare-joined-manifest-v16.json','res://character/james-west-donor-comparison-v1/bare-upper-manifest.json').replace('res://character/james-cargo-return-bridges-v1/helmet-joined-manifest-v16.json','res://character/james-west-donor-comparison-v1/helmet-upper-manifest.json')
s=s.replace('full_return_upper_v16','full_return_donor').replace('full-return-upper-v16','full-return-donor')
start=s.index('\tif not FileAccess.file_exists(OUT+"full_return_donor.gd.uid")');end=s.index('\tvar f:=FileAccess.open',start);s=s[:start]+s[end:]
s=s.replace('Paired bare15/helmet16 generated upper-crop single-interior trial.','Paired existing coherent upper donors4/3/3/actualExit on original V9 body intermediates, exact endpoints and timing; no new raster source/scale/translation/grade.')
(p/'full_return_donor.gd').write_text(s,encoding='utf-8');(p/'full_return_donor.gd.uid').write_text('uid://djamesdonor1\n')
review=(old/'review_full_return_upper_v16.py').read_text().replace('full_return_upper_v16','full_return_donor').replace('full-return-upper-v16','full-return-donor').replace("case=Image.open(p/'floor-case-west-v7.png')","case=Image.open(r/'character/james-floor-case-west-v1/floor-case-west-v7.png')").replace('paired upper trial16 bridge','paired source-donor upper bridge')
(p/'review_native.py').write_text(review)
paths={r/key for key in json.loads((old/'full_return_v6-inputs.json').read_bytes())}
paths.update([p/'full_return_donor.gd',p/'full_return_donor.gd.uid',p/'bare-upper-manifest.json',p/'helmet-upper-manifest.json'])
for gear in ['bare','helmet']:
    m=json.loads((p/(gear+'-upper-manifest.json')).read_bytes())
    for file in m['states'][0]['frameFiles']:paths.add(r/file[6:])
    for d in json.loads((p/'upper-review.json').read_bytes())['gears'][gear]['donors']:paths.add(r/d['source']);paths.add(r/d['original'])
for key in ['actor','player','workshop','checkpoint']:paths.add(r/f'scripts/james_cargo_{key}.gd')
paths.update([r/'scripts/main.gd',r/'scripts/run_save.gd',r/'scripts/grid_canvas.gd'])
(p/'full_return_donor-inputs.json').write_text(json.dumps({path.relative_to(r).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)},indent=2)+'\n')
print(f'Full staged paired return prepared with{len(paths)}targeted pre-launch hashes; normal V9 retained.')
