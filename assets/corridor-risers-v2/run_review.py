"""Run scoped native captures with isolated APPDATA and fingerprint the owner profile."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys

PACK=Path(__file__).resolve().parent
ROOT=PACK.parents[1]
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(p.relative_to(OWNER)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OWNER.rglob('*') if p.is_file()}
floor_id=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--floor=')), '')
if floor_id and floor_id not in ['rubber','sage','bronze']: raise ValueError('Unknown floor')
wet_mode='--wet' in sys.argv
nav_mode='--navigation' in sys.argv
prop_mode='--props' in sys.argv
tag='navigation' if nav_mode else 'wet' if wet_mode else 'native'
if floor_id: tag='floor-'+floor_id
if prop_mode: tag='hallway-props'
before=fingerprint()
(PACK/f'evidence/{tag}-owner-before.json').write_text(json.dumps(before,indent=2))
env=os.environ.copy();env['APPDATA']=str(PACK/'scratch-appdata');env['BRINE_RISER_EXPANSION_TEST']='isolated'
(PACK/'scratch-appdata').mkdir(exist_ok=True)
script='res://tests/test_corridor_wall_variants.gd'
arguments=['--out=res://assets/corridor-risers-v2/review','--cards=res://assets/corridor-risers-v2/cards']
if floor_id:
    arguments=['--out=res://assets/corridor-risers-v2/review-'+floor_id,'--cards=res://assets/corridor-risers-v2/cards-'+floor_id,'--floor=res://assets/corridor-risers-v2/floor-'+floor_id+'.png']
if wet_mode:
    script='res://tests/test_corridor_water_variations.gd'
    arguments=['--out=res://assets/corridor-risers-v2/wet-review']
if nav_mode:
    script='res://tests/test_corridor_furnishing.gd'
    arguments=[]
if prop_mode:
    script='res://tests/test_hallway_props.gd'
    arguments=[]
with (PACK/f'evidence/{tag}-review.log').open('w') as log:
    result=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
        '--path',str(ROOT),'--rendering-method','gl_compatibility','-s',script,
        '--',*arguments],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240)
after=fingerprint()
(PACK/f'evidence/{tag}-owner-after.json').write_text(json.dumps(after,indent=2))
summary=dict(exit_code=result.returncode,owner_unchanged=before==after,
    owner_changed_paths=[k for k in before if k in after and before[k]!=after[k]],
    owner_added_paths=[k for k in after if k not in before],owner_removed_paths=[k for k in before if k not in after],
    captures=len(list(((ROOT/'assets/hallway-props-v1/review') if prop_mode else (PACK/('wet-review' if wet_mode else 'review'))).glob('*.png'))))
(PACK/f'evidence/{tag}-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
for line in (PACK/f'evidence/{tag}-review.log').read_text(errors='replace').splitlines():
    if any(t in line for t in ['ERROR','Error','PASS','SCRIPT','PAUSE_DIAGNOSTIC']):print(line)
raise SystemExit(result.returncode)
