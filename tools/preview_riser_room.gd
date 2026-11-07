extends SceneTree
## Read-only native art study. Launch with tools/preview_riser_room.ps1.
const Library = preload("res://scripts/room_asset_library.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Actor = preload("res://scripts/room_scale_preview.gd")
const NewDoor = preload("res://tools/preview_door_art.gd")
const Finish = preload("res://rooms/doors/door_finish.gd")
const OldRiser = preload("res://rooms/whole-room/north_wall.gd")
const PROP_SOURCES = {
	"res://assets/station-props-v2/sp-reactor-1.png":"res://assets/riser-wall-study-2026-09-26/props/sp-reactor-1.png",
	"res://assets/station-props-v2/sp-reactor-2.png":"res://assets/riser-wall-study-2026-09-26/props/sp-reactor-2.png",
	"res://assets/station-props-v2/sp-reactor-3.png":"res://assets/riser-wall-study-2026-09-26/props/sp-reactor-3.png",
	"res://assets/station-props-v2/sp-current_turbine-2.png":"res://assets/riser-wall-study-2026-09-26/props/sp-current_turbine-2.png",
}
const OUT = "res://output/riser-room-preview/"
var room
var actor = Actor.new()
var wall: ImageTexture
var canvas: Study
var revised := true
var height := 66.0
var running := true
var door_target := 0.0
var door_amount := 0.0
var elapsed := 0.0
var distance_walked := 0.0
var clearance_failures := 0
var status: Label
var room_id := "reactor"
var segment_only := false
var guides := false
var title_label: Label
var note_label: Label
var control_box: VBoxContainer
var top_margin := 150.0
var center_fraction := 0.57
var preview_ports: Array = [0,1,2,3]

class Study extends Control:
	var host
	func zoom() -> float: return minf(size.x/650.0,(size.y-host.top_margin)/520.0)
	func origin() -> Vector2: return Vector2(size.x*0.5,size.y*host.center_fraction)
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("101a20"))
		if host.room == null: return
		var at := origin()
		var factor := zoom()
		Finish.preview_art=NewDoor if host.revised else null
		NewDoor.progress=host.door_amount
		NewDoor.select_room(host.room_id)
		if host.segment_only:
			host.draw_corridor_study(self,at,factor)
			draw_set_transform(Vector2.ZERO)
			return
		host.room.render_into(self,at,factor,true)
		var separate_caps: bool=host.revised and host.has_method("draw_wall_tops")
		var saved_shell_pass: int=host.room.shell_pass
		# Revised caps own the complete shell; never draw legacy corners beneath them.
		draw_set_transform(at,0,Vector2.ONE*factor)
		if host.revised: host.draw_riser(self)
		else: OldRiser.draw_into(self,host.room_id,Vector2i.ZERO,false,false,host.room,false)
		if separate_caps: host.draw_wall_tops(self)
		if host.preview_ports.has(0): host.draw_north_door(self)
		if host.guides: host.draw_guides(self)
		host.room.external_actors = host.actor.members()
		if separate_caps: host.room.shell_pass=2
		host.room.render_into(self,at,factor,false,false)
		host.room.shell_pass=saved_shell_pass
		host.room.external_actors.clear()
		draw_set_transform(at,0,Vector2.ONE*factor)
		for side in [1,2,3]:
			if not host.preview_ports.has(side): continue
			var door_at: Vector2 = [Vector2.ZERO,Vector2(192,0),Vector2(0,192),Vector2(-192,0)][side]+Vector2(0,-3)
			draw_set_transform(at+door_at*factor,side*PI/2,Vector2.ONE*factor)
			for left in [true,false]:
				var width: float = 36.0*(1.0-host.door_amount)
				if width>0: Finish.low_leaf(self,Rect2(-36 if left else 36-width,-6,width,12),left,false,host.door_variant())
		draw_set_transform(Vector2.ZERO)

func _init() -> void: call_deferred("run")

func png(path: String) -> ImageTexture:
	var image := Image.new()
	var error := image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	assert(error==OK,"Preview artwork missing: "+path)
	return ImageTexture.create_from_image(image)

func draw_riser(target: CanvasItem) -> void:
	var top := -192.0-height
	# Only the painted upright face is sampled. The cap uses the actual room
	# wall renderer, so all four walls share the same top surface and bevel.
	target.draw_texture_rect_region(wall,Rect2(-200,top,400,height+16),Rect2(51,209,2050,398))
	var saved = room.painter
	room.painter = target
	for x in [-200,184]: room.draw_wall(Rect2(x,top,16,height+16),false)
	room.draw_wall(Rect2(-192,top-10,384,16),true)
	for x in [-200,184]: room.draw_cap(Rect2(x,top-10,16,16))
	room.painter = saved

func draw_north_door(target: CanvasItem) -> void:
	if not revised:
		Finish.raised(target,door_amount,door_variant())
		return
	NewDoor.raised_at(target,door_amount,0.0,-263.0,height)

func door_variant() -> String:
	return preload("res://rooms/doors/department_door.gd").department({"id":room_id})

func draw_guides(target: CanvasItem) -> void:
	target.draw_rect(Rect2(-46,-258,92,82),Color("e7ba69"),false,1.0)
	for x in [-152,72]: target.draw_rect(Rect2(x,-249,80,32),Color("5cb8d8"),false,1.0)

func button(parent: Node, caption: String, action: Callable) -> void:
	var control := Button.new()
	control.text = caption
	control.custom_minimum_size = Vector2(0,38)
	control.pressed.connect(action)
	parent.add_child(control)

func run() -> void:
	if OS.get_environment("BRINE_RISER_PREVIEW")!="isolated" or DisplayServer.get_name()=="headless":
		push_error("Use the isolated native preview launcher.")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280,960)
	root.content_scale_size = root.size
	root.title = "BrineSpace — riser wall room study"
	for source in PROP_SOURCES: Library.source_textures[source] = png(PROP_SOURCES[source])
	wall = png("res://assets/riser-wall-study-2026-09-26/engineering-v2.png")
	room = preload("res://rooms/whole-room/reactor_view.gd").new()
	room.embedded = true
	root.add_child(room)
	room.hide()
	room.configure_embedded(0,[0,1,2,3],true,0.0)
	Store.apply(room,Store.asset_for(room))
	Library.strip_retired(room)
	# Freeze this read-only layout snapshot; no Studio editor or save writer runs.
	room.set_meta("layout_editor_preview",true)
	room.set_meta("layout_draft",Store.positions(Store.asset_for(room),0))
	room.set_meta("raised_north_visible",true)
	actor.mode = 2
	actor.load_art()
	actor.rebuild(room,"reactor",0)
	assert(actor.visible and room.props.size()>0,"Room must have current props and walkable floor")
	canvas = Study.new()
	canvas.host = self
	root.add_child(canvas)
	canvas.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var controls := VBoxContainer.new()
	control_box = controls
	controls.position = Vector2(26,18)
	canvas.add_child(controls)
	var title := Label.new()
	title_label = title
	title.text = "REACTOR  /  RISER WALL STUDY"
	title.add_theme_font_size_override("font_size",24)
	controls.add_child(title)
	var toolbar := HBoxContainer.new()
	toolbar.add_theme_constant_override("separation",10)
	controls.add_child(toolbar)
	button(toolbar,"Old / new wall [Tab]",toggle_wall)
	button(toolbar,"Open / close doors [D]",toggle_doors)
	button(toolbar,"Pause / walk [Space]",toggle_motion)
	button(toolbar,"Save screenshot [S]",capture_manual)
	var cast := OptionButton.new()
	for member in Actor.CAST: cast.add_item(member.name)
	cast.item_selected.connect(func(index): actor.set_cast(index); actor.rebuild(room,room_id,0))
	toolbar.add_child(cast)
	status = Label.new()
	controls.add_child(status)
	var note := Label.new()
	note_label = note
	note.text = "Current room layout + accepted prop exports. Door demonstration; walking stays inside the room."
	note.position = Vector2(26,root.size.y-38)
	canvas.add_child(note)
	process_frame.connect(advance)
	print("RISER PREVIEW READY: props=%d, navigation_nodes=%d, user_dir=%s"%[room.props.size(),actor.graph.get_point_count(),OS.get_user_data_dir()])
	if OS.get_cmdline_user_args().has("--verify"): await verify()

func advance() -> void:
	var delta := minf(root.get_process_delta_time(),0.05)
	if running:
		elapsed+=delta
		room.machine_clock=elapsed
		var before: Vector2 = actor.foot
		actor.advance(delta)
		distance_walked+=before.distance_to(actor.foot)
		if not actor.segment_clear(before,actor.foot): clearance_failures+=1
	door_amount=move_toward(door_amount,door_target,delta*(1.0/1.05 if door_target>door_amount else 1.0/0.85))
	status.text = "%s  ·  %d-unit face  ·  %s  ·  %s"%["Revised wall" if revised else "Original wall",int(height) if revised else 60,"Walking" if running else "Paused","Doors closed" if door_amount<=0.0 else ("Doors open" if door_amount>=1.0 else "Doors moving")]
	canvas.queue_redraw()

func toggle_wall() -> void: revised = not revised
func toggle_doors() -> void: door_target = 1.0-door_target
func toggle_motion() -> void: running = not running
func capture_manual() -> void:
	await capture("manual-%d"%Time.get_ticks_msec())
func _unhandled_key_input(event: InputEvent) -> void:
	if not event.is_pressed() or event.is_echo(): return
	if event.keycode==KEY_TAB: toggle_wall()
	elif event.keycode==KEY_D: toggle_doors()
	elif event.keycode==KEY_SPACE: toggle_motion()
	elif event.keycode==KEY_S: capture_manual()
	elif event.keycode==KEY_ESCAPE: quit()

func capture(label: String) -> void:
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var result := root.get_texture().get_image().save_png(OUT+label+".png")
	assert(result==OK)

func verify() -> void:
	await capture("revised-closed")
	revised=false
	await capture("original-closed")
	revised=true
	door_target=1.0
	while door_amount<1.0: await process_frame
	await capture("revised-open")
	while distance_walked<160.0 and elapsed<15.0: await process_frame
	await capture("walking")
	assert(distance_walked>=160 and clearance_failures==0,"Walking must travel around actual prop collision")
	toggle_motion()
	var stopped: Vector2 = actor.foot
	for i in range(12): await process_frame
	assert(actor.foot==stopped,"Pause holds character")
	print("RISER PREVIEW PASS: walked=%.1f, clearance_failures=%d, closed/open and old/new native captures; pause verified"%[distance_walked,clearance_failures])
	quit()
