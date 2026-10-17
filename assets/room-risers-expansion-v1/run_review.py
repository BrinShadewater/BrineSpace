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
card_mode='--cards' in sys.argv
scope=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--rooms=')),None)
tag=('cards' if card_mode else 'native')+('-'+scope.replace(',','-') if scope else '')
before=fingerprint()
(PACK/f'evidence/{tag}-owner-before.json').write_text(json.dumps(before,indent=2))
env=os.environ.copy();env['APPDATA']=str(PACK/'scratch-appdata');env['BRINE_RISER_EXPANSION_TEST']='isolated'
(PACK/'scratch-appdata').mkdir(exist_ok=True)
script='res://tools/review_riser_expansion.gd'
arguments=sys.argv[1:]
if card_mode:
    scratch_profile=PACK/'scratch-appdata/Godot/app_userdata/BrineSpace'
    scratch_profile.mkdir(parents=True,exist_ok=True)
    if (OWNER/'room_layouts.json').exists():shutil.copy2(OWNER/'room_layouts.json',scratch_profile/'room_layouts.json')
    script='res://tools/bake_room_cards_v2.gd'
    ids=scope.split(',') if scope else list(json.loads((PACK/'briefs.json').read_text()))
    arguments=['--rooms='+','.join(ids),'--output=res://assets/room-risers-expansion-v1/cards']
with (PACK/f'evidence/{tag}-review.log').open('w') as log:
    result=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
        '--path',str(ROOT),'--rendering-method','gl_compatibility','-s',script,
        '--',*arguments],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240)
after=fingerprint()
(PACK/f'evidence/{tag}-owner-after.json').write_text(json.dumps(after,indent=2))
summary=dict(exit_code=result.returncode,owner_unchanged=before==after,
    owner_changed_paths=[k for k in before if k in after and before[k]!=after[k]],
    owner_added_paths=[k for k in after if k not in before],owner_removed_paths=[k for k in before if k not in after],
    captures=len(list((PACK/'review').glob('*.png'))))
(PACK/f'evidence/{tag}-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
for line in (PACK/f'evidence/{tag}-review.log').read_text(errors='replace').splitlines():
    if any(t in line for t in ['ERROR','Error','RISER_EXPANSION','ROOM CARDS']):print(line)
raise SystemExit(result.returncode)
