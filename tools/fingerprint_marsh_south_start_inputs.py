"""Targeted South start source/runtime freeze; not recursive world dependency inventory."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
paths=['character/marsh-south-start-v1/start_controller.gd','tools/review_marsh_south_start.gd','tests/test_marsh_south_start_controller.gd','tools/build_marsh_south_start.py','character/marsh-south-start-v1/candidate-02/manifest.json','scripts/main.gd','scripts/marsh_npc.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/marsh_ground_motion.gd','scripts/marsh_west_motion.gd','scripts/bill_npc.gd','character/marsh-v2/catalog.json']
paths += ['character/marsh-south-start-v1/candidate-02/%03d.png'%i for i in range(5)]
paths += ['character/marsh-v2/frames/bare/walk-south/%03d.png'%i for i in range(6)]
if '--repair' in sys.argv:
    paths=[p.replace('candidate-02','candidate-04') for p in paths]
    paths+=['character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json','tools/build_marsh_south_start_repair.py','character/marsh-south-start-v1/sources/start-03.raw.png','character/marsh-south-start-v1/candidate-04/recipe.json']
if '--material' in sys.argv or '--idle-material' in sys.argv:
    paths=[p.replace('character/marsh-south-start-v1/candidate-02','character/marsh-south-walk-material-v1/candidate-02/south-start') for p in paths]
    paths+=['character/marsh-south-walk-material-v1/candidate-02/%03d.png'%i for i in range(6)]
    paths+=['character/marsh-south-walk-material-v1/candidate-02/manifest.json','character/marsh-south-walk-material-v1/candidate-02/recipe.json','character/marsh-south-walk-material-v1/baseline.json','character/marsh-south-walk-material-v1/sources/south-walk-02.raw.png','tools/build_marsh_south_walk_material.py','tools/prepare_marsh_full_polish.py','tools/prepare_marsh_carry_chain.py','character/palette-standard-v1/palettes/marsh.json','character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json']
if '--idle-material' in sys.argv:
    paths=[p.replace('character/marsh-south-walk-material-v1/candidate-02/south-start','character/marsh-south-idle-material-v1/candidate-01/south-start') for p in paths]
    paths+=['character/marsh-south-idle-material-v1/candidate-01/%03d.png'%i for i in range(2)]
    paths+=['character/marsh-v2/frames/bare/idle-south/%03d.png'%i for i in range(2)]
    paths+=['character/marsh-south-idle-material-v1/candidate-01/manifest.json','character/marsh-south-idle-material-v1/candidate-01/recipe.json','character/marsh-south-idle-material-v1/baseline.json','character/marsh-south-idle-material-v1/sources/idle-01.raw.png','character/marsh-south-idle-material-v1/sources/idle-01.request.json','character/marsh-south-idle-material-v1/sources/idle-01.prompt.txt','tools/build_marsh_south_idle_material.py']
out={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(len(out),'targeted South inputs saved')
