extends "res://tests/playtest_underwater_life_support.gd"
func subject_view(): return game.grid_view.brine_view
func verify_motion_and_routes() -> void:
	subject_id="brine_core"
	await super.verify_motion_and_routes()
	var cell := Vector2i(20,20)
	var regions := {"body":Rect2(594,590,65,147),"bubbles":Rect2(661,577,16,171),"light":Rect2(549,575,9,152)}
	for q in range(4):
		game.occupied[cell].rotation=q
		for working in [true,false]:
			game.powered_room_cells.clear()
			if working: game.powered_room_cells[cell]=true
			game.visual_time_seconds=0.2
			await capture("components-q%d-%s-a"%[q,working])
			var before := {}
			for name in regions: before[name]=component_pixels(cell,regions[name])
			game.visual_time_seconds=1.1
			await capture("components-q%d-%s-b"%[q,working])
			for name in regions:
				expect((before[name]!=component_pixels(cell,regions[name]))==(working and name!="light"),"BRINE independent "+name+" state q%d"%q)
	var perimeter_view=subject_view()
	for q in range(4):
		perimeter_view.configure_embedded(q,[],false,0.0)
		for step in range(360):
			var angle:=step*TAU/360.0
			expect(perimeter_view.can_stand(Vector2(cos(angle),sin(angle))*100.0),"BRINE observation perimeter stays clear")
	print("BRINE PERIMETER: 1440 positions around chamber")
	print("BRINE COMPONENTS: body, bubble and light regions independently checked, four rotations, operating/offline")

func component_pixels(cell: Vector2i,source: Rect2) -> PackedByteArray:
	var view=subject_view()
	var prop: Dictionary=view.props[0]
	var scale: float=game.get_cell_size()/384.0
	var bounds := Rect2(view.life_point(prop,source.position),source.size*(prop.rect.size.x/prop.registration.width))
	var local := Rect2(game._cell_center(cell)+bounds.position*scale,bounds.size*scale)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
	return root.get_texture().get_image().get_region(Rect2i(screen)).get_data()
