extends SceneTree
const Main=preload("res://scripts/main.gd")
const Rooms=preload("res://scripts/room_database.gd")
const Shop=preload("res://scripts/meta_shop.gd")
var failures:=0
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;print("FAIL: ",message)
func _initialize()->void:
	var game=Main.new()
	game.meta.save_path="user://stabilization-timing.meta"
	game.toast_playing=true # Hold notifications for inspection without scene UI.
	game.meta.discovered_synergy_ids.clear();game.meta.stabilized_synergy_ids.clear()
	for entry in [["reactor",Vector2i(10,11)],["hydroponics_bay",Vector2i(10,10)],["life_support",Vector2i(11,10)]]:
		var room:Dictionary=Rooms.get_room(entry[0]).duplicate(true)
		room.pos=entry[1];room.rotation=0;game.placed_rooms.append(room);game.occupied[room.pos]=room
	game._check_synergies()
	var before:int=game._simulate_room_economy(false,1).delta.oxygen
	var cost_before:int=Shop.room_cost(game.meta,"biodome")
	for cycle in range(3):
		game._apply_room_economy();game._advance_synergy_discovery_cycle()
	check(game.meta.stabilized_synergy_ids.has("closed_air_loop"),"Three functioning cycles stabilize the pattern")
	check(game.run_stabilized_synergy_ids.has("closed_air_loop"),"New stabilization belongs to this loop")
	check(game.meta.total_research_points>0,"Archived Data pays immediately")
	check(Shop.room_cost(game.meta,"biodome")<cost_before,"Related blueprint discount applies immediately")
	var after:int=game._simulate_room_economy(false,4).delta.oxygen
	check(after==before,"Newly stabilized bonus keeps its base rate in this loop")
	var recipe:Dictionary=game.SynergyManagerScript.get_synergy("closed_air_loop")
	check(game._synergy_reward_text(recipe).contains("NEXT LOOP"),"Inspector states when the doubled bonus begins")
	check(game.toast_messages.any(func(item):return str(item).to_upper().contains("NEXT LOOP")),"Stabilization toast explains later-loop timing")
	# Starting a later loop clears this existing per-loop list; the profile stays.
	game.run_stabilized_synergy_ids.clear()
	game.inherited_stabilized_synergy_ids=game.meta.stabilized_synergy_ids.duplicate()
	check(int(game._simulate_room_economy(false,5).delta.oxygen)==before+int(recipe.bonus.oxygen),"Inherited pattern doubles in the next loop")
	check(game._synergy_reward_text(recipe).contains("DOUBLED"),"Inherited reward text confirms the active double")
	game.free()
	print("STABILIZATION LOOP TIMING failures=",failures)
	quit(1 if failures else 0)
