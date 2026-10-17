from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];b=r/'character/james-cargo-return-bridges-v1'
for mode,candidate in [('bare','upper-v15-bare.png'),('helmet','upper-v16-helmet.png')]:
    m=json.loads((b/(mode+'-joined-manifest-v9.json')).read_bytes())
    for i,ref in enumerate(m['states'][0]['frameFiles']):
        if not ref.startswith('res://'):m['states'][0]['frameFiles'][i]='res://character/james-cargo-return-bridges-v1/'+ref
    m['states'][0]['frameFiles'][3]='res://character/james-cargo-return-bridges-v1/'+candidate
    m['name']='James paired upper crop trial16 '+mode;m['status']='unselected_paired_upper_body_trial_native_review_pending'
    path=b/(mode+'-joined-manifest-v16.json');assert not path.exists();path.write_text(json.dumps(m,indent=2)+'\n')
s=(p/'full_return_collar_v12.gd').read_text().replace('bare-joined-manifest-v12.json','bare-joined-manifest-v16.json').replace('helmet-joined-manifest-v9.json','helmet-joined-manifest-v16.json')
s=s.replace('full-return-collar-v12','full-return-upper-v16').replace('full_return_collar_v12','full_return_upper_v16')
s=s.replace('One new bare collar interior only; helmet V9 unchanged. No normal selection/Continue/natural scheduling, paired repair or full master acceptance.','Paired bare15/helmet16 generated upper-crop single-interior trial. Staged injected actor/player/view, current main/native renderer. No new normal selection/Continue/natural scheduling or full master acceptance.')
path=p/'full_return_upper_v16.gd';assert not path.exists();path.write_text(s)
review=(p/'review_full_return_collar_v12.py').read_text().replace('full_return_collar_v12','full_return_upper_v16').replace('full-return-collar-v12','full-return-upper-v16')
review=review.replace('Full prescribed East-to-West carry return, V9 bridge','Full prescribed East-to-West carry return, paired upper trial16 bridge')
(p/'review_full_return_upper_v16.py').write_text(review)
paths={r/k for k in json.loads((p/'full_return_v6-inputs.json').read_bytes())}
paths.update([path,b/'bare-joined-manifest-v16.json',b/'helmet-joined-manifest-v16.json',b/'upper-v15-bare.png',b/'upper-v16-helmet.png',b/'package-upper-v15.gd',b/'package-upper-v16.gd'])
for key in ['actor','player','workshop','checkpoint']:paths.add(r/f'scripts/james_cargo_{key}.gd')
for name in ['main.gd','run_save.gd']:paths.add(r/'scripts'/name)
for version in [15,16]:
    folder=b/f'upper-crop-v{version}'
    paths.update([folder/'raw.png',folder/'prompt.txt',folder/'references.json'])
    ref=json.loads((folder/'references.json').read_bytes())
    for item in ref['sources']:paths.add(r/item['source']);paths.add(r/item['reference'])
(p/'full_return_upper_v16-inputs.json').write_text(json.dumps({str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(paths)},indent=2)+'\n')
print(f'Paired trial16 complete native return prepared; {len(paths)} targeted input hashes frozen; preferred V9 unchanged.')
