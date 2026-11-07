extends SceneTree
const View = preload("res://rooms/whole-room/nursery_lighting_pilot.gd")
var view
var failures := 0
const OUT := "res://output/whole-room-pilot-01/lighting-pilot-v2"
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func frame(name: String) -> Image:
	view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(OUT.path_join(name+".png"))
	return img
func run() -> void:
	if DirAccess.dir_exists_absolute(OUT):
		push_error("Preserve prior captures: use a new output path")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1100,1000)
	root.content_scale_size = Vector2i(1100,1000)
	view = View.new()
	root.add_child(view)
	view.set_process(false)
	view.set_process_unhandled_key_input(false)
	for q in range(4):
		view.quarter = q
		view.rebuild()
		for edge in view.edges: edge.open = false
		for prop in view.props:
			if prop.id=="filter":
				check(view.prop_visual_bounds(prop).encloses(Rect2(view.fan_center(prop)-Vector2.ONE*7,Vector2.ONE*14)),"Fan envelope fits host")
		for state in range(3):
			view.set_power_state(state!=2,state==0,true)
			view.machine_clock = 0.2
			view.actor_clock = 0
			var before := await frame("q%d-state%d-a"%[q,state])
			var clock_before: float = view.machine_clock
			view.advance(0.35)
			# Freeze crew for pixel comparison; independent walking checked below.
			view.actor_clock = 0
			var after := await frame("q%d-state%d-b"%[q,state])
			check((view.machine_clock!=clock_before)==(state==0),"Machine clock follows operation")
			check((before.get_data()!=after.get_data())==(state==0),"Operating moves; idle and unpowered pixels remain still")
		view.set_power_state(true,true,true)
		view.set_power_state(false,true)
		view.advance(0.325)
		check(is_equal_approx(view.light_level,0.5),"Power transition midpoint")
		await frame("q%d-fade-midpoint"%q)
		view.paused = true
		var old_clock: float = view.machine_clock
		var old_actor: float = view.actor_clock
		var paused_before := await frame("q%d-paused-a"%q)
		view.advance(1,Vector2.RIGHT)
		var paused_after := await frame("q%d-paused-b"%q)
		check(paused_before.get_data()==paused_after.get_data() and view.light_level==0.5 and view.machine_clock==old_clock and view.actor_clock==old_actor,"Pause freezes all clocks and fade")
		view.paused = false
		view.advance(1,Vector2.RIGHT)
		check(view.light_level==0 and view.actor_clock>old_actor and view.actor.x>0,"Offline crew moves; fade completes")
	print("LIGHTING PILOT: failures=",failures,"; 4 rotations, 3 states, fan envelopes, fade midpoint, paused pixels and offline crew")
	quit(1 if failures else 0)
