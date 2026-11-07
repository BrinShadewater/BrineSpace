extends SceneTree
const OUT = "res://assets/room-risers-expansion-v1/review"
const Shell = preload("res://rooms/whole-room/painted_shell.gd")
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
	var wall_only := false
	var survey_time := 0.0
	var show_outlet := false
	func _draw() -> void:
		if room == null: return
		var anchor := Vector2(256,290)
		if show_outlet:anchor=Vector2(320,355)
		room.configure_embedded(q,[],false,0)
		room.set_meta("raised_north_visible",true)
		if id=="survey_probe_bay":room.survey_clock=survey_time
		if wall_only:
			draw_set_transform(Vector2(256,390))
			Shell.context(null,id).north(self)
			return
		room.render_into(self,anchor,1.0,true)
		room.shell_pass=1
		room.render_into(self,anchor,1.0,false,false)
		draw_set_transform(anchor)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,id,Vector2i.ZERO,false,false,room)
		room.shell_pass=2
		room.render_into(self,anchor,1.0,false,false)
		room.shell_pass=0
		if show_outlet:
			draw_set_transform(anchor)
			preload("res://scripts/survey_probe_art.gd").outlet(self,Vector2.ZERO,1.0,q,true)

func _init() -> void: call_deferred("run")
func run() -> void:
	if OS.get_environment("BRINE_RISER_EXPANSION_TEST")!="isolated" or DisplayServer.get_name()=="headless":
		quit(2);return
	check(OS.get_user_data_dir().replace("\\","/").contains("room-risers-expansion-v1/scratch-appdata/"),"Scratch profile required")
	if failures: quit(2);return
	print("RISER_EXPANSION_PROFILE ",OS.get_user_data_dir())
	Store.loaded=true;Store.data={}
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	var records:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-expansion-v1/registrations.json"))
	check(records.size()==28,"Exactly 28 bespoke registrations")
	var special:bool="--special" in OS.get_cmdline_user_args()
	if special:
		records=JSON.parse_string(FileAccess.get_file_as_string("res://assets/special-north-walls-v1/registrations.json"))
		check(records.size()==2,"Exactly two special north walls")
	var selected:PackedStringArray=[]
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--rooms="):selected=arg.trim_prefix("--rooms=").split(",")
	for id in records:
		var registered:Dictionary=Shell.catalog()[id]
		if special:
			registered={"base":registered.north_special}
			records[id]={"base":records[id].registration}
		check(registered.base.source==records[id].base.source,"Bespoke binding: "+id)
		var tex=Shell.png(registered.base.source)
		check(tex!=null,"Wall loads: "+id)
		for part in ["face","cap"]:
			var r:Array=registered.base[part]
			check(Rect2(Vector2.ZERO,tex.get_size()).encloses(Rect2(r[0],r[1],r[2],r[3])),"Measured "+part+": "+id)
	var preview:=Preview.new();preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	var capture_outlet:bool="--outlet" in OS.get_cmdline_user_args()
	if capture_outlet:
		preview.show_outlet=true
		root.size=Vector2i(640,640);root.content_scale_size=root.size
		DirAccess.make_dir_recursive_absolute("res://assets/probe-outlet-stub-v3/review")
	var entries:Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	var count:=0
	for entry in entries:
		if not records.has(entry.room) or (not selected.is_empty() and entry.room not in selected):continue
		var room=load(entry.view).new();room.embedded=true;room.hide();root.add_child(room)
		preview.id=entry.room;preview.room=room;preview.wall_only=false
		for q in range(4):
			if special:
				room.configure_embedded(q,[],false,0)
				var context=Shell.context(room,entry.room)
				check(context.north_special.is_empty()==(q!=0),"Special north wall follows equipment orientation: "+entry.room)
			preview.q=q;preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var output:String="res://assets/probe-outlet-stub-v3/review" if capture_outlet else OUT
			var error:=root.get_texture().get_image().save_png(output+"/%s-q%d.png"%[entry.room,q])
			check(error==OK,"Save native view")
			count+=1
		if "--mechanics" in OS.get_cmdline_user_args() and entry.room=="survey_probe_bay":
			var mech=load("res://scripts/probe_launcher_mechanics.gd")
			check(mech.motion(0).is_equal_approx(mech.motion(32)),"Cradle cycle closes without seam")
			check(mech.motion(3.4).y==1.0,"Jaws release before launch")
			check(mech.motion(6).x==mech.TRAVEL,"Cradle reaches throat")
			check(mech.BASE_RECT.position==Vector2(-24,-178),"Platform shifted left with two-unit riser overlap")
			check(mech.BASE_RECT.size.y==68,"Short platform length")
			check(mech.probe_pose(0).position.x==mech.BASE_RECT.get_center().x,"Probe centred on launcher")
			check(is_equal_approx(mech.probe_pose(6).position.x,-4.0),"Probe remains centred through tunnel")
			check(mech.motion(30).x==0.0,"Cradle recovers to dock")
			DirAccess.make_dir_recursive_absolute("res://assets/probe-launcher-v2/review")
			preview.q=0
			for frame in range(265):
				preview.survey_time=frame/24.0 if frame<=144 else 27+(frame-145)/24.0
				preview.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png("res://assets/probe-launcher-v2/review/frame-%03d.png"%frame)
			preview.survey_time=0
			print("LAUNCHER_MECHANICS 265 native frames at 24 fps; launch and recovery; deterministic clock")
		preview.wall_only=true;preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var error:=root.get_texture().get_image().save_png(OUT+"/%s-wall.png"%entry.room)
		check(error==OK,"Save bare wall")
		room.queue_free();await process_frame
	print("RISER_EXPANSION ",count," native room orientations; ",failures," failures")
	quit(0 if failures==0 else 1)
