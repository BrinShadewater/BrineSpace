extends SceneTree
const South=preload("res://character/marsh-south-start-v1/start_controller.gd")
class Probe extends South:
	var clear:=true
	func can_stand(_p: Vector2) -> bool:return clear
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func detour_around_crew() -> bool:return false
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func probe():
	var a=Probe.new();a.active=true;a.battery=100;a.foot=Vector2(100,200);a.direction="south";a.state="idle"
	a.path=PackedVector2Array([Vector2(100,300)]);return a
func run():
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	check(player.frames.has("walk-start-south"),"normal catalog admits South start")
	player.load_manifest("res://character/marsh-south-start-v1/candidate-04/manifest.json" if OS.get_cmdline_user_args().has("--repair") else "res://character/marsh-south-start-v1/candidate-02/manifest.json",true)
	if OS.get_cmdline_user_args().has("--material"):
		player.load_manifest("res://character/marsh-south-walk-material-v1/candidate-02/manifest.json",true)
		player.load_manifest("res://character/marsh-south-walk-material-v1/candidate-02/south-start/manifest.json",true)
	check(is_equal_approx(player.strides["walk-south"],.128),"selected South gait stride remains the authored .128 cells")
	check(player.timing["walk-south"].durations==[150.0,150.0,150.0,150.0,150.0,150.0],"selected South gait uses authored150ms holds")
	for dt in [.01,.02,.08,.1,.4,.5]:
		var actor=probe();check(actor.begin_south_start(),"clear South route arms")
		var t:=0.0
		while actor.south_active() and t<1:
			actor.move(dt);t+=dt
			if actor.south_active():
				check(actor.foot.distance_to(Vector2(100,200+actor.south_progress(t)))<.001,"all dt partitions preserve bounded physical curve")
				check(actor.south_slot()==player.frames["walk-start-south"].find(player.frame_at_elapsed("walk-start-south",actor.action_elapsed())),"contact uses exact selected elapsed pose")
		check(actor.south_pending and not actor.path.is_empty() and actor.state=="walk","finite start retains ongoing normal route and pending gait")
		actor.prepare_south_gait(player,5,actor.foot/384)
		check(not actor.south_pending and player.current_key=="walk-south" and is_equal_approx(player.phase,.68+maxf(0,t-.4)*46/(.128*384)*player.cycle_seconds("walk-south")),"gait joins held endpoint at remaining phase, including extra dt")
	var actor=probe();actor.state="walk";check(not actor.begin_south_start(),"ongoing gait cannot restart idle-entry source")
	check(actor.begin_south_start(true),"fresh assignment hook can arm walk state")
	actor.move(.26);var foot: Vector2=actor.foot;actor.clear=false;actor.move(.02)
	check(actor.foot==foot and not actor.south_active() and actor.south_draw_offset()==Vector2.ZERO,"new blocking releases source without teleport")
	actor=probe();actor.flood_speed=.65;check(not actor.begin_south_start(),"water slowdown retains ordinary floor motion")
	print("MARSH SOUTH START CONTROLLER: %d checks,%d failures"%[checks,failures]);grid.free();quit(1 if failures else 0)
