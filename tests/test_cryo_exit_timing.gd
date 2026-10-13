extends SceneTree
const Art = preload("res://scripts/architect_cryo_art.gd")
var failures := 0
func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)
func _init() -> void:
	for duration in [7.0, 10.0, 12.0]:
		var opening: float=duration-Art.EXIT_SECONDS
		check(is_zero_approx(Art.exit_step(opening+Art.OPEN_SECONDS,duration)),"Step waits for open chamber")
		check(Art.exit_step(duration,duration)==1.0,"Eased step reaches live release point")
		check(Art.vapour_strength(opening-0.1,duration)==0.0,"No vapour while chamber is closed")
		check(Art.vapour_strength(opening+0.2,duration)>0.0,"Icy puff when chamber opens")
		check(Art.vapour_strength(opening+1.0,duration)>0.95,"Opening whoosh holds its density")
		check(Art.vapour_strength(opening+3.0,duration)>0.25,"Blue fog lingers during recovery")
		check(Art.vapour_strength(duration,duration)==0.0,"Opening puff dissipates before release")
		check(Art.thaw_color(0.0,duration)==Color(0.66,0.82,1.0),"Occupant begins mildly blue in the shared pod grade")
		check(Art.thaw_color(opening+Art.GROUND_START,duration)==Art.COLD_COLOR,"Blue until floor contact")
		var midpoint:=Art.thaw_color(opening+(Art.GROUND_START+Art.IDLE_START)*0.5,duration)
		check(midpoint.r>Art.COLD_COLOR.r and midpoint.r<1.0,"Colour returns during grounded recovery")
		check(Art.thaw_color(duration,duration)==Color.WHITE,"Natural colour before live handoff")
		check(Art.unfreeze_progress(0.0,duration)==0.0 and Art.unfreeze_progress(opening,duration)==1.0,"Frost clears before opening")
		check(Art.wake_frame_index(0.0, duration) == 0, "Closed at start")
		check(Art.wake_frame_index(duration - 1.3, duration) == 0, "Closed during thaw")
		var seen := {}
		var previous := 0
		for sample in range(121):
			var wake: float = duration - 1.2 + sample * 0.01
			var index := Art.wake_frame_index(wake, duration)
			seen[index] = true
			check(index >= previous, "Exit progresses without reversing")
			check(index == Art.wake_frame_index(wake, duration), "Paused/restored wake selects identical pose")
			previous = index
		for index in range(1, 6): check(seen.has(index), "Every exit pose is shown")
		check(Art.wake_frame_index(duration, duration) == 5, "Standing pose at release")
	for actor in ["bill","veld","branforth"]:
		var player=Art.recovery_player(actor)
		check(Art.recovery_frame(actor,Art.FALL_START-0.01)==null,"No fall before exit completes")
		check(Art.recovery_frame(actor,Art.GROUND_START+0.1)==player.frames["cryo-fall"].back(),"Grounded pause holds fallen pose")
		check(Art.recovery_frame(actor,Art.RISE_START+0.5)!=null,"Recovery has authored push-up pose")
		check(Art.recovery_frame(actor,Art.IDLE_START)==null,"Returns to selected idle before release")
		var occupied: Image=Art.frame(actor,5).get_image()
		var empty: Image=Art.empty_frame(actor).get_image()
		check(empty.get_size()==occupied.get_size(),actor+" empty pod retains exit canvas")
		check(empty.get_region(Rect2i(0,0,418,140)).get_data()==occupied.get_region(Rect2i(0,0,418,140)).get_data(),actor+" upper shell remains exact through material calibration")
		check(empty.get_region(Rect2i(0,0,108,627)).get_data()==occupied.get_region(Rect2i(0,0,108,627)).get_data(),actor+" open lid remains exact")
		check(empty.get_pixel(205,580).a==0.0,actor+" former boot space is empty")
		check(Art.empty_frame(actor)==Art.empty_frame(actor),actor+" pause/restore reuse stable empty texture")
	check(Art.closed_frame().get_size()==Vector2(418,627),"Layered closed chamber retains registration")
	print("CRYO EXIT TIMING: failures=", failures)
	quit(0 if failures == 0 else 1)
