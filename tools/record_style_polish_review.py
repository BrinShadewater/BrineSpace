"""Record the reviewed native polish batch; independently verify current provenance."""
import hashlib,json
from pathlib import Path
from PIL import Image
from init_material_scale_review import initialize,ROOT
PACK=ROOT/'assets/room-style-polish-v1'
OUT=ROOT/'output/room-style-polish-2026-09-08'
manifest=json.loads((PACK/'manifest.json').read_text())
jobs={r['id']:r for r in json.loads((PACK/'generation.json').read_text())}
for row in manifest:
    identity=row['id'];job=jobs[identity]
    export=PACK/'exports'/(identity+'.png')
    record=initialize(ROOT,row['registration'],export,PACK/(identity+'.prompt.txt'),'polished-south-'+identity,width=344,references=[(ROOT/row['previous_source'].removeprefix('res://'),'camera, silhouette and functional layout'),(ROOT/'assets/material-polish-v1/tidal-south.png','owner-approved material quality; not universal palette'),(ROOT/job['reference'],'department materials and function; not camera')])
    registration=json.loads((ROOT/row['registration']).read_text())
    x,y,w,h=registration['region']
    with Image.open(export) as image:
        alpha=image.getchannel('A')
        corners=[alpha.getpixel(p) for p in [(0,0),(image.width-1,0),(0,image.height-1),(image.width-1,image.height-1)]]
        body_point=(int(x+w*.5),int(y+h*.88))
        body_alpha=alpha.getpixel(body_point)
        assert corners==[0,0,0,0] and body_alpha==255,(identity,corners,body_alpha)
    comparison=OUT/'comparisons'/(identity+'.png')
    assert comparison.exists()
    record.update(department=job['department'],condition='Maintained functional equipment; no generalized grime',attachment_class='south-wall fitted bank',functional_bays=[job['direction']],runtime_behavior='Existing furnishing behavior retained',camera_and_facing='Overhead rear view; backing at image bottom, operating side north',proposed_ground_footprint_world=[344,344*h/w],placement_exclusions=['Room doors and existing furnishings; no placement frame or owner layout changes'])
    record['review']['materials']={'verdict':'pass','findings':['Native comparison reviewed against stable Tidal finish and departmental north source.',job['direction'],'Construction detail added through recessed service panels; no new machinery or geometry enlargement.']}
    record['review']['native_scale']={'verdict':'pass','evidence':comparison.relative_to(ROOT).as_posix(),'findings':['Both revisions drawn at 344 world units beside Bill at runtime scale.','Native comparison is static; no new route acceptance claimed.']}
    record['review']['alpha']={'verdict':'pass','findings':['Source raster unchanged by registration; native polygon export removes neutral exterior.','All four export corners transparent; named rear-body probe retained.'], 'probes':{'corners':corners,'retained_rear_body':{'point':body_point,'alpha':body_alpha}}}
    default=identity not in ['radio-signal-wall','quarantine-specimen-wall']
    record['review']['integration']={'stage':'runtime_registered','evidence':'output/room-style-polish-2026-09-08/catalog/runtime.json','findings':['Native default south-wall placement visually reviewed.' if default else 'Selectable tray view; current default chooses another mounting wall.']}
    record['owner_acceptance']=None
    record['lessons']=['Generic cabinet colors weaken department identity even when facing is correct.','Pair unchanged camera/geometry with a separate material-quality master and department reference.']
    (PACK/(identity+'-review.json')).write_text(json.dumps(record,indent=2)+'\n')
    row['status']='native material and scale reviewed; '+('default south placement reviewed; ' if default else 'tray variant; ')+'owner acceptance pending'
(PACK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'{len(manifest)} records: source/export/reference hashes, transparent corners and retained rear-body alpha verified')
