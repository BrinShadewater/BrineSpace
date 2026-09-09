extends SceneTree
const Details=preload("res://rooms/floor-profiles-v1/details.gd")
const Floor=preload("res://rooms/whole-room/room_floor.gd")
class FloorPanel extends Node2D:
	var view
	func _draw() -> void:
		if view!=null: view.render_into(self,Vector2(256,256),1.16)
func _init() -> void: call_deferred("run")
func capture(panel: Node2D, enabled: bool) -> Image:
	Details.enabled=enabled
	panel.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var panel:=FloorPanel.new()
	panel.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(panel)
	var records: Array=[]
	var failures:=0
	for entry in preload("res://scripts/room_database.gd").all_rooms().values():
		if grid._is_narrow_corridor(entry): continue
		panel.view=grid._bill_room_view(entry)
		var profile:=Floor.profile_for(panel.view)
		for q in range(4):
			panel.view.configure_embedded(q,[],false,0.0)
			var resolved:=Details.resolve(panel.view,profile)
			failures+=resolved.missing.size()
			for item in resolved.missing: print("MISSING DETAIL: ",entry.id," q",q," ",item)
			var before: Image=await capture(panel,false)
			var after: Image=await capture(panel,true)
			for piece in resolved.pieces:
				var region:=Rect2i(Vector2i((Vector2(256,256)+piece.rect.position*1.16).floor()),Vector2i((piece.rect.size*1.16).ceil())).grow(2)
				var pixels:=0
				for y in range(region.position.y,region.end.y):
					for x in range(region.position.x,region.end.x):
						var a:=before.get_pixel(x,y)
						var b:=after.get_pixel(x,y)
						if absf(a.r-b.r)+absf(a.g-b.g)+absf(a.b-b.b)>0.025: pixels+=1
				if pixels<5:
					failures+=1
					print("HIDDEN DETAIL: ",entry.id," q",q," ",piece.asset," host=",piece.host," pixels=",pixels)
				records.append({"id":entry.id,"q":q,"asset":piece.asset,"host":piece.host,"visible_changed_pixels":pixels})
	Details.enabled=true
	var file:=FileAccess.open("res://output/floor-coverage/visibility.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"	"))
	print("FLOOR VISIBILITY: ",records.size()," placed details checked; ",failures," hidden or below contrast threshold")
	quit(1 if failures else 0)
