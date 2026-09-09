extends SceneTree
func _init() -> void:
	var db=preload("res://scripts/room_database.gd").all_rooms()
	var cards=preload("res://scripts/room_card_art.gd").PATHS
	var grid=preload("res://scripts/grid_canvas.gd").new()
	assert(cards.size()==db.size())
	for id in db:
		assert(cards.has(id))
		assert(grid.room_texture_paths[id]==cards[id],"Card/grid mismatch: "+id)
		if grid.room_texture_variant_paths.has(id):
			assert(grid.room_texture_variant_paths[id][0]==cards[id],"Variant mismatch: "+id)
		var image=Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(cards[id]))==OK)
		assert(not image.is_empty())
	grid.free()
	print("ROOM CARD CONSISTENCY PASS: ",db.size()," identities, primary/grid/variant agreement and decoded PNGs")
	quit()
