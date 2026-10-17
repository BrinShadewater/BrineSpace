from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
path=r/'scripts/grid_canvas.gd';s=path.read_text()
old='"salvage_workshop":"res://rooms/underwater/salvage-workshop-v1/workshop_view.gd"'
new='"salvage_workshop":"res://scripts/james_cargo_workshop.gd"'
assert s.count(old)==1
path.write_text(s.replace(old,new))
print('Normal shared workshop view selected; no room geometry changes.')
