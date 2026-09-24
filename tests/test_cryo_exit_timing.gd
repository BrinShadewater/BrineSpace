extends SceneTree
const Art = preload("res://scripts/architect_cryo_art.gd")
var failures := 0
func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)
func _init() -> void:
	for duration in [7.0, 10.0, 12.0]:
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
		var occupied: Image=Art.frame(actor,5).get_image()
		var empty: Image=Art.empty_frame(actor).get_image()
		check(empty.get_size()==occupied.get_size(),actor+" empty pod retains exit canvas")
		check(empty.get_region(Rect2i(0,0,418,250)).get_data()==occupied.get_region(Rect2i(0,0,418,250)).get_data(),actor+" upper housing remains exact")
		check(empty.get_region(Rect2i(0,0,108,627)).get_data()==occupied.get_region(Rect2i(0,0,108,627)).get_data(),actor+" open lid remains exact")
		check(empty.get_pixel(205,580).a==0.0,actor+" former boot space is empty")
		check(Art.empty_frame(actor)==Art.empty_frame(actor),actor+" pause/restore reuse stable empty texture")
	print("CRYO EXIT TIMING: failures=", failures)
	quit(0 if failures == 0 else 1)
