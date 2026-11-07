extends SceneTree
const Visibility=preload("res://scripts/underwater_visibility.gd")
class FleetMock extends RefCounted:
	const Sites=preload("res://scripts/harvest_sites.gd")
	var sites: Dictionary={}
class Host extends RefCounted:
	var occupied: Dictionary={}
	var wrecks: Dictionary={}
	var drone_fleet:=FleetMock.new()
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
	# Harvesting works from a deposit's edge too (owner playtest, Sept 29), on a side that is open water.
	game.wrecks.clear();game.occupied.clear()
	var harvest: Dictionary={"position":Vector2(22,20),"target":Vector2(22,20),"home":Vector2i(21,20),"phase":"working","job":"harvest"}
	game.drone_fleet.sites[Vector2i(22,20)]=game.drone_fleet.Sites.make_site("mining")
	var edge:=Visibility.drone_position(game,harvest)
	check(absf(edge.distance_to(Vector2(22.5,20.5))-.52)<.001,"A harvesting drone stands just outside the deposit's edge, not its middle")
	var chosen_side:=Vector2i((edge-Vector2(22.5,20.5)).sign())
	game.drone_fleet.sites[Vector2i(22,20)+chosen_side]=game.drone_fleet.Sites.make_site("mining")
	var other:=Visibility.drone_position(game,harvest)
	check(other.distance_to(edge)>.5,"It picks another side when a second deposit fills the first")
	# A mining drone's drill meets the deposit (owner playtest, Sept 30): it stands closer than other jobs.
	harvest.kind="mining"
	check(absf(Visibility.drone_position(game,harvest).distance_to(Vector2(22.5,20.5))-Visibility.MINING_REACH)<.001,"A mining drone stands close enough for its drill to touch the deposit")
	harvest.erase("kind")
	harvest.phase="docking"
	check(Visibility.drone_position(game,harvest).is_equal_approx(Vector2(22.5,20.5)),"Only outbound, working and returning drones move to the edge")
	game.drone_fleet.sites.clear()
	game.wrecks.clear();game.occupied.clear()
	drone.target=Vector2.ZERO;drone.position=Vector2.ZERO;drone.home=Vector2i(-1,0)
	point=Visibility.drone_position(game,drone)
	check(point.x>=0 and point.y>=0,"Map edge work stays in bounds")
	print("DRONE WORK FACE: %d failures"%failures)
	quit(failures)
