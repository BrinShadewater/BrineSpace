"""Install the room-specific overhead layout; preserve unrelated renderer methods."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'rooms/underwater/cold-store-v1/cold_store_view.gd'
s=p.read_text()
start=s.index('func rebuild()');end=s.index('func configure_embedded',start)
s=s[:start]+'''func overhead_texture(id: String) -> ImageTexture:
	var source: String="cooler" if id.begins_with("cooler") else id
	var key:=source+"-q"+str(quarter)
	if not overhead_textures.has(key):overhead_textures[key]=load_source_texture("res://assets/rooms/cold-store/pack/"+key+".png")
	return overhead_textures[key]
func overhead_bounds(prop: Dictionary) -> Rect2:
	var size:=Vector2(overhead_texture(prop.id).get_size())
	size*=minf(prop.rect.size.x/size.x,prop.rect.size.y/size.y)
	return Rect2(prop.rect.get_center()-size*.5,size)
func rebuild() -> void:
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":1}]
	edges=Geometry.edges(layout)
	for edge in edges:edge.open=edge.port
	props.clear()
	for id in ["fridge","rack","cooler-0","cooler-1"]:
		var rect:=Rect2(-184,-126,70,252) if id=="fridge" else Rect2(104,-126,80,252)
		if id.begins_with("cooler"):rect=Rect2(-44,-82 if id=="cooler-0" else 30,88,50)
		var size: Vector2=rect.size if quarter%2==0 else Vector2(rect.size.y,rect.size.x)
		rect=Rect2(Geometry.turn(rect.get_center(),quarter)-size*.5,size)
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{},"overhead_furnishing":true})
	queue_redraw()
'''+s[end:]
s=s.replace('func prop_visual_bounds(prop: Dictionary) -> Rect2:\n','func prop_visual_bounds(prop: Dictionary) -> Rect2:\n\tif prop.get("overhead_furnishing",false):return overhead_bounds(prop)\n')
s=s.replace('func draw_registered_prop(prop: Dictionary) -> void:\n','''func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("overhead_furnishing",false):
		painter.draw_texture_rect(overhead_texture(prop.id),overhead_bounds(prop),false)
		return
''')
p.write_text(s)
s=(root/'tools/update_observation_rotated_layout.py').read_text().replace('Observation','Cold Store').replace('observation_room','cold_store').replace('observation-owner-v2','cold-store-owner-v2').replace('wooden-desk','fridge').replace('chair-rear','rack')
(root/'tools/update_cold_store_rotated_layout.py').write_text(s)
