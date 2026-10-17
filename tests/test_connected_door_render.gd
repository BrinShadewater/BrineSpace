extends SceneTree
class Original extends RefCounted:
	static func frame(grid,main, cell_a: Vector2i, cell_b: Vector2i) -> int:
		if main.hardware.doors: return 0
		if main.occupied.get(cell_a, {}).get("doors_locked", false) or main.occupied.get(cell_b, {}).get("doors_locked", false): return 0
		var drone_frame: int = grid._drone_door_frame(main,cell_a,cell_b)
		if main.bill_npc.active or main.has_dr_veld() or main.has_chief_branforth() or main.has_marsh() or not main.companion_roster.is_empty():
			if not main.occupied.has(cell_a) or not main.occupied.has(cell_b): return 0
			var offset:=cell_b-cell_a
			if absi(offset.x)+absi(offset.y)!=1 or not main._placed_rooms_connected(main.occupied[cell_a],main.occupied[cell_b],offset,cell_a,cell_b): return 0
			var center: Vector2 = (Vector2(cell_a + cell_b) * 0.5 + Vector2.ONE * 0.5) * grid._cell_size()
			var distance: float = grid._nearest_crew_foot(main, center).distance_to(center) * 384.0 / grid._cell_size()
			# Fully open before either crew member reaches the threshold; close
			# only after both have left its proximity zone.
			var amount := clampf((100.0 - distance) / 45.0, 0.0, 1.0)
			return maxi(drone_frame,roundi(amount * float(GridCanvas.DOOR_OPEN_FRAMES - 1)))
		if main.test_walker_next_cell == Vector2i(-1, -1):
			return drone_frame
		var current: Vector2i = main.test_walker_cell
		var next: Vector2i = main.test_walker_next_cell
		var crossing: bool = (current == cell_a and next == cell_b) or (current == cell_b and next == cell_a)
		if not crossing:
			return drone_frame
		var progress: float = clampf(float(main.test_walker_progress), 0.0, 1.0)
		var open_amount: float = 1.0
		if progress < 0.16:
			open_amount = progress / 0.16
		elif progress > 0.84:
			open_amount = (1.0 - progress) / 0.16
		return maxi(drone_frame,clampi(int(round(open_amount * float(GridCanvas.DOOR_OPEN_FRAMES - 1))), 0, GridCanvas.DOOR_OPEN_FRAMES - 1))

	# Drones pass through doorways without opening the doors (owner playtest): they still route
	# through them, but doors, door lighting and flood flow between rooms follow crew only.

class Main extends RefCounted:
	var hardware:Dictionary={"doors":false}
	var occupied:Dictionary={}
	var bill_npc:Dictionary={"active":true}
	var companion_roster:Dictionary={}
	var foot:=Vector2.ZERO
	var connected:=true
	var connectivity_calls:=0
	var drone_frame:=0
	var test_walker_next_cell:=Vector2i(-1,-1)
	var test_walker_cell:=Vector2i.ZERO
	var test_walker_progress:=0.0
	func has_dr_veld()->bool:return false
	func has_chief_branforth()->bool:return false
	func has_marsh()->bool:return false
	func _placed_rooms_connected(_a,_b,_offset,_ca,_cb)->bool:connectivity_calls+=1;return connected
class Grid extends GridCanvas:
	func _cell_size()->float:return 384.0
	func _drone_door_frame(main,_a,_b)->int:return main.drone_frame
	func _nearest_crew_foot(main,_center)->Vector2:return main.foot
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var grid:=Grid.new();var main:=Main.new()
	for cell in [Vector2i.RIGHT,Vector2i.UP,Vector2i(2,0)]:
		main.occupied={Vector2i.ZERO:{},cell:{}}
		for locked in [false,true]:
			main.occupied[cell].doors_locked=locked
			for disabled in [false,true]:
				main.hardware.doors=disabled
				for crew in [false,true]:
					main.bill_npc.active=crew
					for connected in [false,true]:
						main.connected=connected
						for drone_frame in [0,4,12]:
							main.drone_frame=drone_frame
							for distance in [0.0,54.0,55.0,77.5,99.0,100.0,180.0]:
								main.foot=(Vector2(cell)*.5+Vector2.ONE*.5)*384+Vector2(distance,0)
								check(Original.frame(grid,main,Vector2i.ZERO,cell)==grid._compute_door_frame_for_pair(main,Vector2i.ZERO,cell),"Default path matches original")
								if connected and absi(cell.x)+absi(cell.y)==1:
									var expected:int=Original.frame(grid,main,Vector2i.ZERO,cell)
									main.connectivity_calls=0
									check(expected==grid._compute_door_frame_for_pair(main,Vector2i.ZERO,cell,true),"Established connection frame exact")
									check(main.connectivity_calls==0,"Established connection avoids repeated query")
	main.hardware.doors=false;main.bill_npc.active=true;main.connected=true;main.occupied={Vector2i.ZERO:{},Vector2i.RIGHT:{}};main.foot=Vector2(384,192)
	grid.render_door_cache_active=true;grid.render_door_cache.clear();main.connectivity_calls=0
	var cached_frame:int=grid._door_frame_for_pair(main,Vector2i.ZERO,Vector2i.RIGHT,true)
	check(cached_frame==Original.frame(grid,main,Vector2i.ZERO,Vector2i.RIGHT),"Render cache frame matches original")
	main.connectivity_calls=0
	check(grid._door_frame_for_pair(main,Vector2i.RIGHT,Vector2i.ZERO)==cached_frame,"Reverse edge reuses symmetric render cache")
	check(main.connectivity_calls==0,"Cached render frame avoids repeated topology query")
	grid.render_door_cache_active=false
	check(grid._door_frame_for_pair(main,Vector2i.ZERO,Vector2i.RIGHT)>0,"Live connected frame opens")
	main.connected=false
	check(grid._door_frame_for_pair(main,Vector2i.ZERO,Vector2i.RIGHT)==0,"Live path observes disconnect in same tick")
	main.occupied.erase(Vector2i.RIGHT)
	check(grid._compute_door_frame_for_pair(main,Vector2i.ZERO,Vector2i.RIGHT)==0,"Missing room remains closed")
	grid.free()
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("DOOR_FRAME ",checks," checks, ",failures," failures");quit(1 if failures else 0)
