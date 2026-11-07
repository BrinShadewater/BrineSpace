from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
paths=['tools/review_marsh_south_step.gd','tools/review_marsh_south_step.gd.uid','tools/build_marsh_south_step.py','tools/prepare_marsh_south_step.py','tools/fingerprint_marsh_south_step_inputs.py','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','character/marsh-v2/catalog.json','character/marsh-south-idle-material-v1/candidate-01/manifest.json','character/marsh-south-idle-material-v1/candidate-01/000.png','character/marsh-south-idle-material-v1/candidate-01/001.png','character/marsh-south-walk-material-v1/candidate-02/000.png','character/marsh-south-walk-material-v1/candidate-02/003.png','character/marsh-motion-polish-v1/sources/south-standing-identity-01.png','character/marsh-south-step-v1/sources/idle-gait-reference.png','character/marsh-south-step-v1/sources/whole-pose-guide-03.png']
for version in ['01','02','03','04','05']:
    paths += [f'character/marsh-south-step-v1/sources/step-{version}.{suffix}' for suffix in ['raw.png','request.json','prompt.txt']]
for version in ['01','02','03','04','05']:
    paths += [f'character/marsh-south-step-v1/candidate-{version}/{file}' for file in ['manifest.json','recipe.json','ruler.png']+[f'{i:03d}.png' for i in range(7)]]
paths += ['tools/build_marsh_south_step_correction.py','tools/build_marsh_south_step_close.py','tools/prepare_marsh_south_step_correction.py','character/marsh-south-step-v1/sources/reach-close-guide-04.png','character/marsh-south-step-v1/sources/close-neutral-guide-05.png']
paths += ['character/marsh-south-step-v1/step_controller.gd','character/marsh-south-step-v1/step_controller.gd.uid','tests/test_marsh_south_step_controller.gd','tests/test_marsh_south_step_controller.gd.uid','tools/review_marsh_south_step_world.gd','tools/review_marsh_south_step_world.gd.uid','scripts/marsh_npc.gd','scripts/marsh_south_snapshot.gd','scripts/main.gd','scripts/run_save.gd','scripts/loading_transition.gd','scripts/marsh_ground_motion.gd','scripts/marsh_west_motion.gd','scripts/bill_npc.gd']
out={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(len(out),'targeted South step inputs saved')
