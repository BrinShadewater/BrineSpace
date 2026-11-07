extends SceneTree
## Diagnostic renders only: no source modification, gameplay scene or save access.
var view_path := ""
var output := ""
class EdgePanel extends Node2D:
	var room
	var index := 0
	var light := false
	func _draw() -> void:
		draw_rect(Rect2(0,0,800,800),Color("ddd2bd") if light else Color("3a193d"))
		room.configure_embedded(0,[],false,0.0)
		var prop: Dictionary=room.props[index]
		var bounds: Rect2=room.prop_visual_bounds(prop)
		draw_set_transform(Vector2(400,420)-bounds.get_center()*4.0,0,Vector2(4,4))
		room.painter=self
		room.draw_registered_prop(prop)
		draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(20,26),str(prop.id)+" / OFFLINE / 4 pixels per world unit",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.BLACK if light else Color.WHITE)
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--view="): view_path=arg.trim_prefix("--view=")
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
	call_deferred("run")
func run() -> void:
	assert(view_path.begins_with("res://rooms/"),"Use a registered room view")
	assert(output.begins_with("res://output/") and not DirAccess.dir_exists_absolute(output),"Use a new review directory")
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(800,800)
	root.content_scale_size=root.size
	var room=load(view_path).new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var panel:=EdgePanel.new()
	panel.room=room
	root.add_child(panel)
	var records: Array=[]
	for index in range(room.props.size()):
		panel.index=index
		for light in [false,true]:
			panel.light=light
			panel.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var bounds: Rect2=room.prop_visual_bounds(room.props[index])
			var screen:=Rect2(Vector2(400,420)-bounds.size*2.0,bounds.size*4.0)
			assert(Rect2(12,40,776,748).encloses(screen.grow(8)),"Complete prop must fit native review canvas")
			var name:="%s-%s.png"%[str(room.props[index].id),"light" if light else "dark"]
			assert(root.get_texture().get_image().save_png(output.path_join(name))==OK)
			var detail:=screen.grow(8)
			var pixels:=Rect2i(Vector2i(detail.position.floor()),Vector2i(detail.end.ceil()-detail.position.floor()))
			records.append({"prop":str(room.props[index].id),"file":name,"background":"light" if light else "dark","crop":[pixels.position.x,pixels.position.y,pixels.size.x,pixels.size.y],"sha256":FileAccess.get_sha256(output.path_join(name))})
	var record:=FileAccess.open(output.path_join("edge-review.json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"view":view_path,"view_sha256":FileAccess.get_sha256(view_path),"world_scale":4,"state":"offline","scope":"Native prop-only contrast diagnostic; not alpha cleanup or acceptance","renders":records},"\t"))
	print("PROP EDGE CAPTURES: ",records.size()," unmodified registered-prop renders; manual review required")
	quit()
