from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
files=['scripts/branforth_npc.gd','scripts/ward_repair.gd','scripts/james_construction_motion.gd','scripts/james_hull_resume.gd','scripts/james_hull_return.gd','scripts/station_effects.gd','scripts/grid_canvas.gd','character/james-torch-material-residue-v2/bare-manifest.json','character/james-repair-contact-v1/torch-tip-offsets.json']
(P/'runtime-input-startup.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Nine runtime/source hashes recorded during initial West validation startup, before compatibility launches')
