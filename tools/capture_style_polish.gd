extends SceneTree
## Native source export and equal-world-scale comparison; no player save access.
const OUT="res://output/room-style-polish-2026-09-08/"
const PACK="res://assets/room-style-polish-v1/"
class Art extends Node2D:
	var data: Dictionary
	var texture: Texture2D
	func setup(registration: Dictionary) -> void:
		data=registration
		var raw:=Image.new(); assert(raw.load_png_from_buffer(FileAccess.get_file_as_bytes(data.source))==OK)
		texture=ImageTexture.create_from_image(raw)
	func paint(canvas: CanvasItem,origin: Vector2,scale: float,offset: Vector2) -> void:
		for polygon in data.pieces:
			var points:=PackedVector2Array(); var uv:=PackedVector2Array()
			for point in polygon:
				var at:=Vector2(point[0],point[1]); points.append(origin+(at-offset)*scale); uv.append(at/Vector2(texture.get_size()))
			canvas.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,texture)
	func _draw() -> void: paint(self,Vector2.ZERO,1.0,Vector2.ZERO)
class Board extends Node2D:
	var before: Art
	var after: Art
	var crew: Texture2D
	var label: String
	func _draw() -> void:
		draw_rect(Rect2(0,0,880,270),Color("233438"))
		draw_string(ThemeDB.fallback_font,Vector2(16,28),label,HORIZONTAL_ALIGNMENT_LEFT,-1,20)
		for i in range(2):
			var art: Art=before if i==0 else after
			var r: Array=art.data.region
			art.paint(self,Vector2(20+i*450,62),344.0/float(r[2]),Vector2(r[0],r[1]))
			draw_string(ThemeDB.fallback_font,Vector2(20+i*450,205),"Before" if i==0 else "Polished",HORIZONTAL_ALIGNMENT_LEFT,-1,17)
		var scale:=65.28/74.0
		var pivot: Vector2=crew.get_meta("crew_pivot",Vector2(46,86))
		draw_texture_rect(crew,Rect2(Vector2(411,146)-pivot*scale,crew.get_size()*scale),false)
		draw_string(ThemeDB.fallback_font,Vector2(16,247),"344-unit banks and Bill at runtime scale. Static material/scale comparison; not route acceptance.",HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(880,270); root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	DirAccess.make_dir_recursive_absolute(OUT+"comparisons");DirAccess.make_dir_recursive_absolute(PACK+"exports")
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var grid=preload("res://scripts/grid_canvas.gd").new();grid.hide();grid.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(grid)
	var board:=Board.new();board.crew=grid.human_sprites.get("south",grid.human_sprite);assert(board.crew!=null);root.add_child(board)
	var viewport:=SubViewport.new();viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
	var rows: Array=JSON.parse_string(FileAccess.get_file_as_string(PACK+"manifest.json"))
	for row in rows:
		var filename: String="side-"+row.id+"-south.json"
		var before:=Art.new();before.setup(JSON.parse_string(FileAccess.get_file_as_string(PACK+"previous-registrations/"+filename)))
		var after:=Art.new();after.setup(JSON.parse_string(FileAccess.get_file_as_string("res://"+row.registration)))
		board.before=before;board.after=after;board.label=row.id;board.queue_redraw()
		viewport.size=Vector2i(after.texture.get_size());viewport.add_child(after)
		await process_frame;await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png(OUT+"comparisons/"+row.id+".png")==OK)
		assert(viewport.get_texture().get_image().save_png(PACK+"exports/"+row.id+".png")==OK)
		viewport.remove_child(after);after.free();before.free();board.before=null;board.after=null
	var uid_path: String=get_script().resource_path+".uid"
	if not FileAccess.file_exists(uid_path):
		var file=FileAccess.open(uid_path,FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close()
	print("POLISH CAPTURE PASS: ",rows.size()," native alpha exports and equal-scale before/after comparisons with Bill")
	quit()
