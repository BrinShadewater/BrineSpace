extends SceneTree
const Bill=preload("res://scripts/bill_npc.gd")
var game
var failures:=0
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;print("FAIL: ",message)
func _initialize()->void:run.call_deferred()
func run()->void:
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://return-timing.meta";game.run_save_path="user://return-timing.loop"
	game.meta.unlocked_architect_ids.marsh=true;game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop()
	while not game.startup_complete:await process_frame
	game.paused=false;game.Architects.advance_core(game,10)
	# Navigation fixture: a long connected station, no free-building gameplay mode.
	for y in range(4,20):
		game.wrecks.erase(Vector2i(20,y));game._place_room("corridor",Vector2i(20,y),true)
	var actor=game.marsh_npc
	actor.rebuild(game)
	actor.foot=actor.graph.get_point_position(actor.nearest_in_room(Vector2(7872,1728),Vector2i(20,4),false))
	actor.path.clear();actor.goal="";actor.stage="";actor.state="idle";actor.battery=70
	game.resources.power=20;game.powered_room_cells[Vector2i(20,20)]=true
	var approach:Dictionary=actor.charging_approach(game)
	check(not approach.is_empty(),"Far room has a real connected path to the original pod")
	var distance:=0.0;var origin:Vector2=actor.foot
	for point in approach.get("route",PackedVector2Array()):distance+=origin.distance_to(point);origin=point
	print("INITIAL RETURN route=",distance," speed=",actor.flood_speed," battery=",actor.battery)
	var reserve:float=actor.recharge_reserve(game,0)
	var searches:int=Bill.route_searches
	for step in range(20):actor.recharge_reserve(game,.1)
	check(Bill.route_searches==searches,"Stable route budget does not search every movement frame")
	actor.flood_speed=.55
	check(actor.recharge_reserve(game,0)>reserve,"Flood slowdown immediately increases the return reserve")
	actor.flood_speed=1.0
	actor.update(game,.1)
	check(actor.returning_to_pod,"Long trip starts before the fixed 35% reserve becomes too late")
	if actor.returning_to_pod:
		var minimum:float=actor.battery
		var docked:=false
		for step in range(4000):
			var from:Vector2=actor.foot
			actor.drain_battery(.1);actor.update(game,.1)
			minimum=minf(minimum,actor.battery)
			check(from.distance_to(actor.foot)<=6.91,"Return keeps physical movement speed")
			check(actor.can_stand(actor.foot),"Return keeps floor clearance")
			docked=docked or actor.recharge_docked
			if actor.battery>=99.999 and not actor.returning_to_pod:break
		check(docked and minimum>0,"Long return docks without emergency crawl")
		check(actor.battery>=99.999 and not actor.returning_to_pod,"Recharge completes and releases Marsh to duty")
		check(game.resources.power<20,"Recharge still spends station Power")
		print("LONG RETURN minimum battery=",minimum," power spent=",20-game.resources.power)
	game.free()
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.set_process(false);music.stop_audio()
	await create_timer(.2).timeout
	print("MARSH RETURN TIMING failures=",failures)
	quit(1 if failures else 0)
