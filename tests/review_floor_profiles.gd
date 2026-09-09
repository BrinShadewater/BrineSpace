extends SceneTree
const G = preload("res://tools/modular_room_geometry.gd")
const CG = preload("res://rooms/underwater/corridor_geometry.gd")
const CA = preload("res://rooms/underwater/corridor_surfaces.gd")
const Decor = preload("res://rooms/whole-room/decoration_props.gd")
class Card extends Node2D:
	var room
	var id := ""
	var q := 0
	var variant := 0
	var sources: Array
	var suspended := false
	var powered := true
	func _draw() -> void:
		if suspended: return
		if room!=null:
			room.render_into(self,Vector2(256,256),1.16)
		else:
			draw_set_transform(Vector2(256,256),0,Vector2.ONE*1.16)
			var corner := id=="corner"
			var tee := id=="tee_corridor"
			CA.draw_hull(self,CG.hull_for(corner,tee),CG.floor_for(corner,tee),Vector2.ZERO,CG.rotation({"id":id,"rotation":q}),sources,corner,powered,1.0 if powered else 0.0,tee,variant)
			draw_set_transform(Vector2.ZERO)
var output_dir := "res://output/floor-details-v3"
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output-dir="): output_dir=arg.trim_prefix("--output-dir=").trim_suffix("/")
	assert(output_dir.begins_with("res://output/"))
	call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	var rows: Array=[]
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	for entry in preload("res://scripts/room_database.gd").all_rooms().values():
		rows.append({"id":entry.id,"view":"corridor" if grid._is_narrow_corridor(entry) else grid._bill_room_view(entry).get_script().resource_path})
	var database: Dictionary=preload("res://scripts/room_database.gd").all_rooms()
	assert(rows.size()==database.size(),"Room coverage must match current database")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var card:=Card.new()
	card.sources=CA.load_sources()
	card.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(card)
	var report: Array=[]
	for row in rows:
		assert(database.has(row.id),"Unknown room "+row.id)
		card.id=row.id
		if row.view!="corridor":
			card.room=load(row.view).new()
			card.room.embedded=true
			root.add_child(card.room)
			card.room.hide()
		var samples:=0
		for q in range(4):
			card.q=q
			for live in [false,true]:
				card.powered=live
				if card.room!=null:
					card.room.configure_embedded(q,[0,1,2,3],live,1.25)
					# Every wall mount stays in a real solid wall segment, away from ports.
					for edge in card.room.edges:
						for rect in G.wall_rects(edge):
							if edge.horizontal and rect.position.y<-180 and rect.size.x>=90:
								assert(rect.size.y>=10)
				card.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var capture:=root.get_texture().get_image()
				if q==0 and not live: assert(capture.save_png((output_dir+"/%s-offline.png")%row.id)==OK)
				if live: assert(capture.save_png((output_dir+"/%s-q%d.png")%[row.id,q])==OK)
				samples+=1
		if card.room!=null:
			# Shared shell ownership must not resurrect a missing wall or change props.
			card.room.configure_embedded(0,[0,1,2,3],true,1.25,[0,1])
			card.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			assert(root.get_texture().get_image().save_png((output_dir+"/%s-shared.png")%row.id)==OK)
			card.suspended=true
			card.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			card.room.free()
			card.suspended=false
			card.room=null
		else:
			for variant in range(3):
				card.q=0
				card.variant=variant
				card.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				assert(root.get_texture().get_image().save_png((output_dir+"/%s-variant%d.png")%[row.id,variant])==OK)
			card.variant=0
		report.append({"id":row.id,"render_samples":samples,"view":row.view})
		print("DECORATION ROOM: ",row.id," rotations/state pass")
	var file:=FileAccess.open(output_dir+"/review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"rooms":report,"count":rows.size(),"render_samples":rows.size()*8},"\t"))
	print("FLOOR INTEGRATION PASS: ",rows.size()," rooms; ",rows.size()*8," rotation/state renders")
	quit()
