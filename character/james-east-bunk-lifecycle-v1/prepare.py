from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];inputs={}
def freeze(p):inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for mode in ['bare','helmet']:
    path=R/'character/james-bunk-east-master-v1'/(mode+'-manifest.json');freeze(path)
    for state in json.loads(path.read_bytes())['states']:
        for rel in state['frameFiles']:freeze(path.parent/rel)
for rel in ['scripts/grid_canvas.gd','scripts/branforth_npc.gd','scripts/bill_npc.gd','scripts/crew_life.gd','scripts/crew_room_activity.gd','scripts/room_layout_store.gd','scripts/run_save.gd','scripts/main.gd','character/ACTIVE_ASSETS.json']:
    freeze(R/rel)
(P/'inputs-before.json').write_text(json.dumps(inputs,indent=2)+'\n');shutil.copy2(R/'character/james-selected-rest-review-2026-10-01/run_validation.py',P/'run_validation.py')
print(len(inputs),'bunk source/controller inputs frozen; strict scratch runner ready.')
