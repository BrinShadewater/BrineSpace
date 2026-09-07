extends SceneTree
## Native static depth oracle. No gameplay scene or player save access.
var output := ""
var review_view := ""
var review_props := PackedStringArray()
class DepthPanel extends Node2D:
	var room
	var prop: Dictionary
	var mode := "normal"
	var behind := false
	func _draw() -> void:
		draw_rect(Rect2(0,0,800,800),Color("424d51"))
		draw_set_transform(Vector2(400,450)-prop.rect.get_center()*2,0,Vector2(2,2))
		room.painter = self
		if mode in ["normal", "full-room"]: room.draw_room_world(mode == "full-room")
		else:
			var actor_first: bool = behind if mode == "expected" else not behind
			if actor_first: room.draw_actor()
			room.draw_registered_prop(prop)
			if not actor_first: room.draw_actor()
		draw_set_transform(Vector2.ZERO)

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
		if arg.begins_with("--view="): review_view=arg.trim_prefix("--view=")
		if arg.begins_with("--props="): review_props=arg.trim_prefix("--props=").split(",",false)
	call_deferred("run")

func frame(panel: DepthPanel, mode: String) -> Image:
	panel.mode=mode
	panel.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()

func run() -> void:
	if not review_view.is_empty() and not ResourceLoader.exists(review_view):
		push_error("Depth review view does not exist: "+review_view)
		quit(1)
		return
	if not output.begins_with("res://output/") or output.contains("..") or DirAccess.dir_exists_absolute(output):
		push_error("Depth review requires a new directory beneath res://output/")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(800,800)
	root.content_scale_size=root.size
	var image:=Image.new()
	var actor_path := "res://character/major-bill-v2/rotations/south.png"
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(actor_path))==OK)
	var actor_texture:=ImageTexture.create_from_image(image)
	actor_texture.set_meta("major_bill_v2",true)
	var records: Array=[]
	var failures:=0
	var subjects: Array=[]
	for kind in ["mining","salvage"]: subjects.append({"path":"res://rooms/production-ten/%s_drone_bay_view.gd"%kind,"props":[kind+"_rov",kind+"_hatch"]})
	if not review_view.is_empty():
		assert(not review_props.is_empty(),"Specify exact prop IDs for a custom review")
		subjects=[{"path":review_view,"props":review_props}]
	for subject in subjects:
		var room=load(subject.path).new()
		room.embedded=true
		root.add_child(room)
		var panel:=DepthPanel.new()
		panel.room=room
		root.add_child(panel)
		for q in range(4):
			for prop_id in subject.props:
				for pose in ["behind","front","forced-overlap"]:
					var behind: bool = pose != "front"
					room.quarter=q
					room.rebuild()
					var selected: Dictionary
					for prop in room.props:
						if prop.id==prop_id: selected=prop
					assert(not selected.is_empty(),"Unknown reviewed prop: "+str(prop_id))
					room.actor=Vector2(selected.rect.get_center().x,selected.rect.position.y-14 if behind else selected.rect.end.y+14)
					if pose=="forced-overlap": room.actor.y=float(selected.sort_y)-14
					var standable: bool=room.can_stand(room.actor)
					room.external_actor_texture=actor_texture
					room.show_actor=true
					panel.prop=selected
					panel.behind=behind
					var full_room:=await frame(panel,"full-room")
					room.props.assign([selected])
					room.edges.clear()
					room.layout.clear()
					panel.prop=selected
					panel.behind=behind
					var actual:=await frame(panel,"normal")
					var expected:=await frame(panel,"expected")
					var wrong:=await frame(panel,"wrong")
					var correct:=actual.get_data()==expected.get_data()
					var sensitive:=expected.get_data()!=wrong.get_data()
					var clearance_only: bool = str(prop_id).ends_with("_hatch") and pose=="behind"
					if not correct or (review_view.is_empty() and ((sensitive==clearance_only) or (pose!="forced-overlap" and not standable))) or (pose=="forced-overlap" and not sensitive): failures+=1
					var name:="%s-q%d-%s"%[prop_id,q,pose]
					full_room.save_png(output.path_join(name+"-full-room.png"))
					actual.save_png(output.path_join(name+".png"))
					wrong.save_png(output.path_join(name+"-wrong-order.png"))
					records.append({"capture":name,"correct_order":correct,"reverse_order_changes_pixels":sensitive,"clearance_only":clearance_only,"forced_non_walkable_pose":pose=="forced-overlap","standable_in_full_room":standable})
		panel.free()
		room.free()
	var report:=FileAccess.open(output.path_join("review.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Static native prop/crew ordering plus full-room diagnostic captures at 2x; custom review reports clearance without requiring rear access; not continuous movement or typical station zoom","actor_sha256":FileAccess.get_sha256(actor_path),"failures":failures,"records":records},"\t"))
	print("DRONE CREW DEPTH: ",records.size()," static poses; ",failures," ordering/sensitivity failures")
	quit(1 if failures else 0)
