extends SceneTree
const OUT = "res://assets/ocean-windows-v3/review"
const Windows = preload("res://rooms/whole-room/ocean_windows.gd")
const Store = preload("res://scripts/room_layout_store.gd")
var failures := 0
func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

class Preview extends Node2D:
	var room
	var id: String
	var q := 0
	var variant := 0
	var corridor_textures: Array = preload("res://rooms/underwater/corridor_surfaces.gd").load_sources()
	func _draw() -> void:
		if room == null: return
		var anchor := Vector2(256,290)
		room.configure_embedded(q,[],false,0)
		room.set_meta("raised_north_visible",true)
		if id in ["corridor","corner","tee_corridor"]:
			draw_set_transform(anchor)
			var g = preload("res://rooms/underwater/corridor_geometry.gd")
			var rotation: int = g.rotation({"id":id,"rotation":q})
			preload("res://rooms/underwater/corridor_surfaces.gd").draw_hull(self,g.hull_for(id=="corner",id=="tee_corridor"),g.floor_for(id=="corner",id=="tee_corridor"),Vector2.ZERO,rotation,corridor_textures,id=="corner",true,1,id=="tee_corridor",0)
			preload("res://rooms/underwater/corridor_dressing.gd").draw_risers(self,g.hull_for(id=="corner",id=="tee_corridor"),rotation,variant,1)
		else:
			room.render_into(self,anchor,1.0,true)
			room.shell_pass=1
			room.render_into(self,anchor,1.0,false,false)
			draw_set_transform(anchor)
			preload("res://rooms/whole-room/north_wall.gd").draw_into(self,id,Vector2i.ZERO,false,false,room)
			room.shell_pass=2
			room.render_into(self,anchor,1.0,false,false)
			room.shell_pass=0

func _init() -> void: call_deferred("run")
func run() -> void:
	if OS.get_environment("BRINE_WINDOW_TEST") != "isolated" or DisplayServer.get_name()=="headless":
		quit(2); return
	check(OS.get_user_data_dir().replace("\\","/").contains("ocean-windows-v3/scratch-appdata/"),"Godot user directory is the scratch profile")
	if failures: quit(2); return
	print("WINDOW_PROFILE ",OS.get_user_data_dir())
	Store.loaded=true; Store.data={}
	root.size=Vector2i(512,512); root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	for kind in Windows.SOURCES:
		var tex = Windows.texture(kind)
		check(tex != null,"Window loads: "+kind)
		var im: Image = tex.get_image()
		var source: Rect2 = Windows.source_region(kind)
		check(Rect2(Vector2.ZERO,im.get_size()).encloses(source),"Source registration: "+kind)
		check(im.get_pixel(0,0).a<.1,"Transparent exterior: "+kind)
		check(im.get_pixelv(Vector2i(source.get_center())).a>.98,"Ocean source coverage (square panes have opaque backing): "+kind)
		for mount in [Rect2(-152,-249,80,32),Rect2(72,-249,80,32),Rect2(20,-93,72,23),Windows.CENTER_MOUNT]:
			var fitted: Rect2 = Windows.fitted_rect(kind,mount)
			check(mount.grow(.001).encloses(fitted),"Frame fits reserve: "+kind)
			var logical: Rect2=Windows.SOURCES[kind][1]
			check(absf(fitted.size.aspect()-logical.size.aspect())<.001,"Original silhouette aspect preserved: "+kind)
	check(Windows.room_allowed(true,"cold_store",[]),"Sealed north permits windows")
	check(not Windows.room_allowed(true,"cold_store",[0]),"North doorway excludes windows")
	check(not Windows.room_allowed(false,"cold_store",[]),"No raised north face excludes windows")
	check(not Windows.room_allowed(true,"airlock",[],true),"Exterior hatch excludes windows")
	check(not Windows.room_allowed(true,"brine_core",[]),"Special BRINE core assembly preserved")
	check(Rect2(-46,-255,92,79).encloses(Windows.CENTER_MOUNT),"Central viewing window stays inside existing wall panel")
	for kind in ["square_steel","square_ivory","square_sage"]:
		var fitted := Windows.fitted_rect(kind,Windows.CENTER_MOUNT)
		check(fitted.size.x>=54 and fitted.size.y>=54,"Reduced square window keeps substantial viewing area")
	var preview := Preview.new()
	preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(preview)
	var entries: Array = JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	var selected := ["cold_store","galley","biomass_digester","reactor","corridor","corner","tee_corridor"]
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--rooms="): selected=Array(arg.trim_prefix("--rooms=").split(","))
	var count := 0
	var expected := 0
	for entry in entries:
		if entry.room not in selected: continue
		var room = load(entry.view).new()
		room.embedded=true; room.hide(); root.add_child(room)
		preview.id=entry.room; preview.room=room
		var variants := 3 if entry.room in ["corridor","corner","tee_corridor"] else 1
		expected+=variants*4
		for variant in range(variants):
			preview.variant=variant
			for q in range(4):
				preview.q=q; preview.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var suffix: String="" if variant==0 else "-v%d"%variant
				var result := root.get_texture().get_image().save_png(OUT+"/%s-q%d%s.png"%[entry.room,q,suffix])
				check(result==OK,"Native capture saved")
				count+=1
		preview.room=null; preview.queue_redraw()
		room.queue_free(); await process_frame
	check(count==expected and count>0,"Selected hosts, finishes and four orientations captured")
	for path in ["res://rooms/whole-room/ocean_windows.gd.uid","res://tools/review_ocean_windows.gd.uid"]:
		if not FileAccess.file_exists(path):
			var file := FileAccess.open(path,FileAccess.WRITE)
			file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	print("WINDOW_REVIEW captures=",count," failures=",failures)
	quit(1 if failures else 0)
