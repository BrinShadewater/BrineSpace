extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Actor=preload("res://scripts/room_scale_preview.gd")
const OUT="res://character/brine-scale-v10-2026-09-26/room-preview.png"
var room
var canvas: CoreStudy
var actor=Actor.new()
var time:=0.0
var capturing:=false
class CoreStudy extends Control:
	var host
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("121b21"))
		if host.room==null: return
		host.room.external_actors=host.actor.members()
		var at:=Vector2(size.x/2,size.y*0.59)
		host.room.render_into(self,at,1.65,true)
		draw_set_transform(at,0,Vector2.ONE*1.65)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"brine_core",Vector2i.ZERO,false,false,host.room,false)
		preload("res://rooms/doors/door_finish.gd").raised(self,0.0,"brine")
		host.room.render_into(self,at,1.65,false,false)
		host.room.external_actors.clear()
func _init() -> void: call_deferred("run")
func run() -> void:
	assert(OS.get_environment("BRINE_RISER_PREVIEW")=="isolated")
	root.size=Vector2i(1100,1000)
	root.content_scale_size=root.size
	root.title="BRINE Core - corrected corner preview"
	room=preload("res://character/brine-scale-v10-2026-09-26/preview_room.gd").new()
	room.embedded=true
	root.add_child(room)
	room.hide()
	# Preview-only texture override. Preserve the original chamber registration,
	# occupant, foreground glass, bubbles and front-occlusion draw passes.
	if not OS.get_cmdline_user_args().has("--old-tube"):
		var tube_image:=Image.new()
		assert(tube_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/brine-scale-v10-2026-09-26/source-atlas.png"))==OK)
		assert(tube_image.get_size()==Vector2i(1254,1254),"Chamber atlas coordinates must remain stable")
		room.life_texture=ImageTexture.create_from_image(tube_image)
	room.configure_embedded(0,[0,1,2,3],true,0.0)
	Store.apply(room,Store.asset_for(room))
	var draft: Dictionary=Store.positions(Store.asset_for(room),0).duplicate(true)
	room.set_meta("layout_editor_preview",true)
	room.set_meta("layout_draft",draft)
	room.set_meta("raised_north_visible",true)
	room.props=room.props.filter(func(p): return str(p.id) not in ["library/brine-corner-service-nw","library/brine-corner-analysis-ne"])
	var entries=JSON.parse_string(FileAccess.get_file_as_string("res://assets/brine-core-corners-corrected-2026-09-26/manifest.json"))
	for e in entries:
		var path: String="res://assets/brine-core-corners-corrected-2026-09-26/game-size/brine-corner-service-nw.png" if str(e.id).ends_with("nw") else "res://assets/brine-core-corners-corrected-2026-09-26/game-size/brine-corner-analysis-ne.png"
		var im:=Image.new()
		assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK)
		var tex:=ImageTexture.create_from_image(im)
		var sz:=Vector2(im.get_size())
		var at:=Vector2(e.proposed_content_origin[0],e.proposed_content_origin[1])-Vector2.ONE*1.36
		var rect:=Rect2(at,sz*0.34)
		var west: bool=str(e.id).ends_with("nw")
		var cut:=floorf(sz.y*0.29)
		for part in [0,1]:
			var lo:=0.0 if part==0 else cut
			var hi:=cut if part==0 else sz.y
			var poly:=PackedVector2Array([Vector2(0,lo),Vector2(sz.x,lo),Vector2(sz.x,hi),Vector2(0,hi)])
			var boxes: Array=[[0,0,1,0.29]] if part==0 else [[0 if west else 0.75,0.29,0.25,0.71]]
			room.props.append({"id":"library/sp-preview-"+str(e.id)+str(part),"library_asset":true,"rect":rect,"center":rect.get_center(),"sort_y":at.y+hi*0.34,"collision_boxes":boxes,"library_texture":tex,"registration":{"pieces":[poly],"pivot":Vector2(sz.x/2,sz.y),"width":sz.x,"height":sz.y}})
	actor.mode=1
	actor.load_art()
	actor.rebuild(room,"brine_core",0)
	actor.place(Vector2(0,95))
	canvas=CoreStudy.new()
	canvas.host=self
	canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(canvas)
	canvas.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var label:=Label.new()
	label.text="BRINE / SUSPENDED FLOAT STUDY\nSmooth body sampling - original face and colors preserved\n8-second loop - saved room unchanged - Esc to close"
	label.position=Vector2(24,20)
	label.add_theme_font_size_override("font_size",20)
	root.add_child(label)
	process_frame.connect(advance)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(OUT)==OK)
	print("BRINE CORNER PREVIEW CAPTURED props=",room.props.size())
	if OS.get_cmdline_user_args().has("--capture-only"):
		capturing=true
		for uv in [Vector2.ZERO,Vector2.ONE,Vector2(0.2,0.5),Vector2(0.8,0.5)]:
			assert(room.drift(uv,0).distance_to(room.drift(uv,8))<0.0001,"Float loop must close")
		for sample in range(200):
			var t:=sample*0.04
			assert(room.drift(Vector2(0.35,0.08),t).distance_to(room.drift(Vector2(0.65,0.12),t))<0.0001,"Face must remain rigid")
		for uv in [Vector2(0.5,0.1),Vector2(0.2,0.5),Vector2(0.8,0.5),Vector2(0.5,0.95)]:
			var before: Vector2=(room.drift(uv,8.0)-room.drift(uv,7.999))/0.001
			var after: Vector2=(room.drift(uv,0.001)-room.drift(uv,0.0))/0.001
			assert(before.distance_to(after)<0.02,"Loop velocity must not snap")
		DirAccess.make_dir_recursive_absolute("res://character/brine-scale-v10-2026-09-26/captures")
		for frame in range(200):
			room.machine_clock=frame*0.04
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var image:=root.get_texture().get_image().get_region(Rect2i(430,315,240,335))
			assert(image.save_png("res://character/brine-scale-v10-2026-09-26/captures/frame-%03d.png"%frame)==OK)
		print("BRINE FLOAT PASS: 200 native samples; 8-second rig loop closes")
		quit()
func advance() -> void:
	if not capturing:
		time+=minf(root.get_process_delta_time(),0.05)
		room.machine_clock=time
	canvas.queue_redraw()
func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode==KEY_ESCAPE: quit()








