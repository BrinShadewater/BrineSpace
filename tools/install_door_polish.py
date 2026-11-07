"""Narrow text integration of the shared door skins; no raster transformation."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'rooms/whole-room/room_door.gd'
s=p.read_text()
a=s.index('\tvar rise=',s.index('static func draw_riser_door'))
b=s.index('\nstatic func riser_detail',a)
s=s[:a]+'\tpreload("res://rooms/doors/door_finish.gd").raised(canvas,open_amount,"brine" if ceramic!=null else "generic")\n'+s[b:]
a=s.index('\tfor panel in leaf_rects',s.index('static func draw_door'))
s=s[:a]+'''\tfor i in range(leaf_rects(open_amount).size()):
\t\tvar panel: Rect2=leaf_rects(open_amount)[i]
\t\tpreload("res://rooms/doors/door_finish.gd").low_leaf(canvas,panel,i==0,false,"generic")
\tfor side in [-1,1]:
\t\tcanvas.draw_rect(Rect2(side*39-2,-6,4,12),Color("627e7b"))
\t\tcanvas.draw_rect(Rect2(side*39-1,-2,2,4),Color("91b7ae"))
'''
p.write_text(s)
p=root/'rooms/doors/department_door.gd'
s=p.read_text()
a=s.index('\t\t\tif leaf_art==null:')
b=s.index('\n\t\tif part.get("leaf",false):',a)
s=s[:a]+'''\t\t\tpreload("res://rooms/doors/door_finish.gd").low_leaf(canvas,part.rect,part.get("north",false),not part.get("front_leaf",false),variant)
'''.rstrip()+s[b:]
p.write_text(s)
p=root/'rooms/underwater/brine-core/brine_core_view.gd'
s=p.read_text()
a=s.index('\tfor item in default_door_parts():')
b=s.index('\nstatic func default_door_parts()',a)
s=s[:a]+'\tpreload("res://rooms/doors/door_finish.gd").low_closed(painter,center,not horizontal,"brine")\n'+s[b:]
p.write_text(s)
print('Updated raised, fallback, department and BRINE default doors')
