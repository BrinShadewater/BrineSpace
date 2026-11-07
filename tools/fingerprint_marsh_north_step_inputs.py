"""Freeze targeted inputs for the staged North-step interval, not all world assets."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
PATHS=[
 'character/marsh-north-step-v1/step_controller.gd','tools/review_marsh_north_step_world.gd',
 'tools/build_marsh_north_step_sequence.py','tests/test_marsh_north_step_controller.gd',
 'character/marsh-north-step-v1/sequence-v1/manifest.json',
 'character/marsh-north-step-v1/sequence-v1/000.png','character/marsh-north-step-v1/sequence-v1/001.png',
 'character/marsh-north-step-v1/sequence-v1/002.png','character/marsh-north-step-v1/sequence-v1/003.png',
 'character/marsh-north-step-v1/sequence-v1/004.png','character/marsh-north-step-v1/sequence-v1/005.png',
 'character/marsh-north-step-v1/sequence-v1/006.png','character/marsh-v2/catalog.json',
 'character/marsh-v2/frames/bare/idle-north/000.png',
 'scripts/main.gd','scripts/marsh_npc.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd',
 'scripts/marsh_ground_motion.gd','scripts/marsh_west_motion.gd','scripts/bill_npc.gd',
 'scripts/fire_safety.gd','scripts/flood_safety.gd','rooms/underwater/corridor_dressing.gd']
PATHS += ['character/marsh-north-step-v1/sequence-v2/manifest.json',
 'character/marsh-north-step-v1/sequence-v2/000.png','character/marsh-north-step-v1/sequence-v2/001.png',
 'character/marsh-north-step-v1/sequence-v2/002.png','character/marsh-north-step-v1/sequence-v2/003.png',
 'character/marsh-north-step-v1/sequence-v2/004.png','character/marsh-north-step-v1/sequence-v2/005.png',
 'character/marsh-north-step-v1/sequence-v2/006.png']
result={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PATHS}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(len(result),'targeted input hashes saved')
