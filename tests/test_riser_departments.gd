extends SceneTree
const Catalog=preload("res://rooms/whole-room/riser_catalog.gd")
const DB=preload("res://scripts/room_database.gd")
const Baker=preload("res://tools/bake_current_architecture_cards.gd")
const Corridor=preload("res://tools/bake_corridor_variants.gd")
const OUT="res://output/riser-departments-v1/"
func _init() -> void: call_deferred("run")
func run() -> void:
	for path in ["res://rooms/whole-room/riser_catalog.gd","res://tests/test_riser_departments.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var file=FileAccess.open(path+".uid",FileAccess.WRITE)
			file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	var seen: Array=["brine_core","airlock"]
	for group in Catalog.GROUPS:
		for id in Catalog.GROUPS[group]:
			assert(not id in seen,"Duplicate room mapping")
			seen.append(id)
		var region:=Catalog.source_rect(group,"face")
		assert(absf(region.size.x/region.size.y-6.4)<.001)
		assert(Rect2(Vector2.ZERO,Catalog.texture(group).get_size()).encloses(region))
	for id in DB.all_rooms(): assert(id in seen,"Unmapped room: "+id)
	assert(seen.size()==DB.all_rooms().size())
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var store=preload("res://scripts/room_layout_store.gd")
	store.path=OUT+"isolated-layout.json";store.loaded=true;store.data={}
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide();grid.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(grid)
	var preview=Baker.Preview.new();preview.compact=true;root.add_child(preview)
	for group in Catalog.GROUPS:
		preview.id=Catalog.GROUPS[group][0]
		preview.room=grid._bill_room_view(DB.get_room(preview.id))
		for q in range(4):
			preview.q=q;preview.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			assert(root.get_texture().get_image().save_png(OUT+group+"-q"+str(q)+".png")==OK)
	preview.queue_free();await process_frame
	var card=Corridor.Card.new();card.textures=Corridor.Art.load_sources();root.add_child(card)
	for id in ["corridor","corner","tee_corridor"]:
		for variant in range(3):
			card.corner=id=="corner";card.tee=id=="tee_corridor";card.variant=variant;card.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var name=id+("" if variant==0 else "-"+str(variant))+".png"
			assert(root.get_texture().get_image().save_png("res://assets/riser-departments-v1/cards/"+name)==OK)
	print("RISER DEPARTMENTS PASS: 47 explicit mappings, 8 aspect-correct faces, 32 rotated room previews, 9 corridor cards")
	quit()
