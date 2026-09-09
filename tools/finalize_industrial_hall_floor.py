"""Install the smaller industrial floor atlas and its native review cards."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/hallway-floor-tiles-v2'
out=ROOT/'output/hallway-floor-tiles-v2'
source=pack/'source.png'
with Image.open(source) as im: size=list(im.size)
manifest={'source':'res://assets/hallway-floor-tiles-v2/source.png','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dimensions':size,'grid':[8,8],'module_world_size':24,'editor_cell_world_size':48,'modules_per_editor_cell':[2,2],'processing':'Original source unchanged; atlas quarter UVs place four modules inside each existing floor cell','direction':'Smaller industrial grating, metal panels and protected recessed pipes; supersedes plain large panels','review':'Native review complete; owner acceptance pending'}
(pack/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name in ['scripts/room_card_art.gd','scripts/grid_canvas.gd']:
    p=ROOT/name
    p.write_text(p.read_text().replace('res://assets/hallway-floor-tiles-v1/cards/','res://assets/hallway-floor-tiles-v2/cards/'))
html=(ROOT/'output/hallway-floor-tiles-v1/index.html').read_text()
html=html.replace('Hallway panel tiles','Industrial hallway deck').replace('hall-floor-notes','industrial-hall-floor-notes').replace('hallway-floor-tiles-v1','hallway-floor-tiles-v2')
html=html.replace('Sixteen matte grey-green floor tiles, fitted to straight corridors, corners and T-junctions. Quiet seams and subtle wear, with no drains, cables, pipes or loose decorations. Tiles cover the existing floor footprint at 48 units per tile. The new finish is the corridor default; explicitly saved finishes remain available.','Smaller dark steel modules mix walkway grating, metal access panels and recessed pipe channels. Each module is 24 units across—half the previous panel width—with four modules inside each existing editor cell. The industrial deck is now the corridor default. Pipes sit below the walking surface; saved finish choices remain available.')
html=html.replace('4 × 4 source tileset','8 × 8 source tileset')
(out/'index.html').write_text(html,encoding='utf-8')
print('Industrial floor recorded: 64 small modules, nine cards, separate review and notes')
