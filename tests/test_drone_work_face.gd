extends SceneTree
const Visibility=preload("res://scripts/underwater_visibility.gd")
class Host extends RefCounted:
	var occupied: Dictionary={}
	var wrecks: Dictionary={}
var failures:=0
func check(ok: bool,label: String):
	if not ok:failures+=1;push_error(label)
func _init():
	var game=Host.new()
	var drone={"position":Vector2(22,20),"target":Vector2(22,20),"home":Vector2i(21,20),"phase":"working","job":"clear"}
	game.occupied[Vector2i(21,20)]=true
	var point:=Visibility.drone_position(game,drone)
	check(not game.occupied.has(Vector2i(point.floor())),"Work face avoids occupied bay when exposed water exists")
	var saved: Dictionary=drone.duplicate(true)
	Visibility.drone_position(game,drone)
	check(drone==saved,"Visual work selection does not mutate simulation")
	for phase in ["outbound","returning"]:
		drone.phase=phase
		check(Visibility.drone_position(game,drone).is_equal_approx(point),phase+" matches working endpoint")
		drone.position=Vector2(21.9999,20)
		check(Visibility.drone_position(game,drone).distance_to(point)<.001,phase+" is continuous near target")
		drone.position=Vector2(21.5,20)
		check(Visibility.drone_position(game,drone).is_equal_approx(Vector2(22,20.5)),phase+" preserves distant route")
		drone.position=drone.target
	drone.phase="working"
	for delta in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN]:game.wrecks[Vector2i(22,20)+delta]={"kind":"basalt","cleared":false}
	check(Visibility.drone_position(game,drone).is_equal_approx(Vector2(21.98,20.5)),"Covered clear side remains fallback")
	game.wrecks[Vector2i(21,20)]={"kind":"basalt","cleared":false}
	check(Visibility.drone_position(game,drone).is_equal_approx(Vector2(22.5,20.5)),"Enclosed target has no invented free side")
	game.wrecks.clear();game.occupied.clear()
	drone.target=Vector2.ZERO;drone.position=Vector2.ZERO;drone.home=Vector2i(-1,0)
	point=Visibility.drone_position(game,drone)
	check(point.x>=0 and point.y>=0,"Map edge work stays in bounds")
	print("DRONE WORK FACE: %d failures"%failures)
	quit(failures)
