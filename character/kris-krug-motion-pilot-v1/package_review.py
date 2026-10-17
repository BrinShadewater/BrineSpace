from pathlib import Path
import hashlib,json,shutil
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
V2=ROOT.parent/'kris-krug-motion-pilot-v2'
(ROOT/'alternate').mkdir(exist_ok=True)
for state in ['walk-east','tablet-east']:
    shutil.copyfile(V2/state/'scale-preview.mp4',ROOT/'alternate'/f'{state}-v2.mp4')
    shutil.copyfile(V2/state/'contact.png',ROOT/'alternate'/f'{state}-v2-contact.png')
action=ROOT.parent/'kris-krug-tablet-east-v1'
shutil.copyfile(action/'key-sequence-preview.mp4',ROOT/'alternate'/'canonical-tablet-keys.mp4')
shutil.copyfile(action/'source-review.png',ROOT/'alternate'/'canonical-tablet-keys.png')
endpoint=ROOT.parent/'kris-krug-tablet-endpoint-east-v1'
shutil.copyfile(endpoint/'scale-preview.mp4',ROOT/'alternate'/'endpoint-draw-trial.mp4')
shutil.copyfile(endpoint/'endpoint-comparison.png',ROOT/'alternate'/'endpoint-comparison.png')
draw=ROOT.parent/'kris-krug-tablet-draw-east-v1'
shutil.copyfile(draw/'action-preview.mp4',ROOT/'alternate'/'complete-draw-candidate.mp4')
shutil.copyfile(draw/'native/output/slot-07.png',ROOT/'alternate'/'draw-native-held.png')
records=[]
for version,folder,states in [(1,ROOT,['idle-east','walk-east','tablet-east']),(2,V2,['walk-east','tablet-east'])]:
    for state in states:
        gen=json.loads((folder/state/'generation.json').read_text())
        check=json.loads((folder/state/'checks.json').read_text())
        assert gen['status']=='Success' and len(check['records'])==141 and not check['clipped_frames']
        records.append({'version':version,'state':state,'task_id':gen['task_id'],
            'source_sha256':hashlib.sha256((folder/state/'source.mp4').read_bytes()).hexdigest(),
            'frame_count':check['frame_count'],'duration_ms':check['duration_ms'],'estimated_usd':gen['estimatedUSD'],
            'status':'source trial; no selected loop or runtime integration'})
gen=json.loads((endpoint/'generation.json').read_text())
check=json.loads((endpoint/'checks.json').read_text())
assert gen['status']=='Success' and check['frame_count']==142 and not check['clipped_frames']
records.append({'version':'endpoint','state':'draw-east','task_id':gen['task_id'],'source_sha256':check['source_sha256'],
    'frame_count':142,'duration_ms':check['duration_ms'],'estimated_usd':gen['estimatedUSD'],'status':'rejected: purple garment and overbright screen'})
(ROOT/'source-audit.json').write_text(json.dumps({'sources':records,'unique_full_source_frames':sum(r['frame_count'] for r in records),
    'estimated_usd_total':round(sum(r['estimated_usd'] for r in records),2),'verified_billing':None,
    'scope':'Full-clip fixed-registration review, not a production animation pack',
    'failures':{'v1_walk':'Frame82 color fault','v2_walk':'Suit drifts toward teal; not selected'},
    'tablet_status':'Draw/inspect/return study; exact source-master joins/handedness not yet accepted'},indent=2),encoding='utf-8')
with ZipFile(ROOT/'Kris-Krug-motion-study.zip','w',ZIP_DEFLATED) as bundle:
    for name in ['index.html','README.md','source-audit.json']:
        if (ROOT/name).exists():bundle.write(ROOT/name,name)
    for state in ['idle-east','walk-east','tablet-east']:
        for name in ['scale-preview.mp4','contact.png']:
            bundle.write(ROOT/state/name,state+'/'+name)
    for path in sorted((ROOT/'alternate').iterdir()):bundle.write(path,'alternate/'+path.name)
print('6 provider sources verified; 847 full-clip frames/no clipped frames; estimated USD1.23; review ZIP saved.')
