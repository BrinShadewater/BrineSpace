extends SceneTree
const Repairs=preload("res://scripts/hull_repair.gd")
const Safety=preload("res://scripts/flood_safety.gd")
class BlockedJoin extends "res://scripts/bill_npc.gd":
 func smooth_route(_route: PackedVector2Array,_origin := Vector2.INF) -> PackedVector2Array:
  return PackedVector2Array()
class FailedEscape extends "res://scripts/bill_npc.gd":
 var attempts: Array=[]
 func route_to_any(_start: int,_targets: Dictionary,avoid_crew := false,_turn_at := Vector2.INF) -> PackedVector2Array:
  attempts.append(avoid_crew)
  return PackedVector2Array()
var failures:=0
func check(ok: bool,message: String):
 if not ok: failures+=1;push_error(message)
func _init(): call_deferred("run")
func run():
 # Long dry travel projects water at arrival without consuming underwater air.
 var flooded={"hull_crack":1.0,"water_level":0.95}
 var job={"duration":10.0,"progress":0.0}
 var nearby=Repairs.air_needed(flooded,job,0.0,0.008)
 var remote=Repairs.air_needed(flooded,job,100.0,0.008)
 check(is_equal_approx(nearby,remote),"Dry travel must not spend tank oxygen")
 check(is_equal_approx(Repairs.air_needed(flooded,job,100.0,0.008,8.0),remote+8),"Wet transit must still spend air")
 var game=load("res://scenes/main.tscn").instantiate()
 game.meta.save_path="user://owner-regressions-%d.json" % OS.get_process_id()
 game.run_save_path=game.meta.save_path+".loop"
 root.add_child(game);current_scene=game
 while not game.startup_complete: await process_frame
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
 game.running=true;game.paused=false
 game.hardware.doors=false;game.hardware.pumps=false
 game.architect_run={"selected":"bill"}
 game.recovered_crew=[{"architect_id":"bill","alive":true}]
 game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
 game.wrecks.clear();game.drone_fleet.orders.clear();game.drone_fleet.sites.clear()
 for x in range(19,23):
  var id="reactor" if x==20 else "corridor" if x==21 else "storage_bay"
  var room=game.RoomDatabaseScript.get_room(id).duplicate(true)
  room.pos=Vector2i(x,20);room.rotation=1 if id=="corridor" else 0
  room.water_level=0.0
  game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
 var actor=game.bill_npc
 actor.active=true;actor.dead=false;actor.movement_medium="dry"
 actor.rebuild(game)
 var failed_escape=FailedEscape.new()
 failed_escape.active=true;failed_escape.rebuild(game)
 failed_escape.foot=failed_escape.graph.get_point_position(failed_escape.room_nodes[Vector2i(19,20)][0])
 failed_escape.movement_medium="flooded"
 var joins=Safety.escape_starts(failed_escape).size()
 check(joins>0,"Failed escape fixture has usable starting joins")
 check(Safety.escape_route(game,failed_escape).is_empty(),"Unreachable refuge stays unreachable")
 check(failed_escape.attempts.size()==joins,"Without peers, each escape join is searched only once")
 failed_escape.attempts.clear()
 failed_escape.avoidance_position=failed_escape.foot+Vector2(20,0)
 Safety.escape_route(game,failed_escape)
 check(failed_escape.attempts.size()==joins*2,"With peers, escape retains its avoidance fallback")
 var blocked=BlockedJoin.new()
 blocked.active=true;blocked.rebuild(game)
 blocked.foot=blocked.graph.get_point_position(blocked.room_nodes[Vector2i(19,20)][0])
 blocked.service_preferences={"hunger":["storage_bay"],"fatigue":[],"curiosity":[],"maintenance":[]}
 var prior_searches: int=blocked.route_searches
 blocked.choose_goal(game)
 check(blocked.goal!="hunger","An unjoinable route cannot start a meal remotely")
 # Two food rooms, three curiosity rooms and one local pacing attempt.
 check(blocked.route_searches-prior_searches<=41,"Failed smoothed joins obey the per-destination search bound: %d" % (blocked.route_searches-prior_searches))
 var cell=Vector2i(20,20)
 var desired=(Vector2(cell)+Vector2.ONE*0.5)*384+Vector2(-70,-115)
 var start=actor.nearest_in_room((Vector2(cell)+Vector2.ONE*0.5)*384,cell,false)
 actor.foot=actor.graph.get_point_position(start)
 var approach=Repairs.approach(actor,cell)
 check(not approach.is_empty(),"Furnished Reactor has a reachable repair position")
 if not approach.is_empty():
  check(approach.point.distance_to(desired)>50,"Fixture exercises blocked original repair anchor")
  actor.path=approach.route
  for i in range(600):
   actor.move(0.1)
   if actor.path.is_empty():break
  check(actor.foot.distance_to(approach.point)<1,"Repair fallback is physically reachable")
 game.resources.metal=20
 game.occupied[cell].water_level=0.95
 game.occupied[cell].hull_crack=1.0
 actor.foot=actor.graph.get_point_position(actor.room_nodes[Vector2i(19,20)][0])
 actor.goal="";actor.path.clear();actor.helmet_equipped=false;actor.breath_oxygen=15
 check(Repairs.request(game,cell),"Unsafe repair remains a paid queued job")
 Repairs.advance(game,actor,0.1)
 check(game.occupied[cell].leak_repair.status.begins_with("Unsafe"),"Fixture needs more air and has no locker")
 var searches: int=actor.route_searches
 for i in range(20): Repairs.advance(game,actor,0.01)
 check(actor.route_searches==searches,"Unavailable air does not replan the same repair every frame")
 actor.helmet_equipped=true;actor.tank_oxygen=60
 Repairs.advance(game,actor,0.1)
 check(game.occupied[cell].leak_repair.worker=="bill","Improved air immediately bypasses the failed-repair retry delay")
 Repairs.cancel(game,cell)
 game.occupied[cell].water_level=0.0;game.occupied[cell].hull_crack=0.0
 # High water without low air must still free a swimmer wedged in a doorway.
 game.occupied[Vector2i(21,20)].water_level=0.6
 actor.goal="";actor.path.clear();actor.helmet_equipped=true
 actor.tank_oxygen=60;actor.movement_medium="flooded";actor.direction="east"
 var doorway=(Vector2(21,20)+Vector2.ONE*0.5)*384+Vector2(-190,20)
 actor.foot=doorway
 check(actor.can_stand(doorway) and not actor.swim_segment_clear(doorway,doorway,actor.direction),"Fixture catches the standing-to-swimming doorway transition")
 var destination=(Vector2(21,20)+Vector2.ONE*0.5)*384
 actor.goal="hull-repair"
 actor.path=PackedVector2Array([destination])
 check(Safety.rejoin_swim_route(actor),"Dry-planned work route can join swimming navigation at the threshold")
 check(actor.goal=="hull-repair","Joining a swim route preserves the assigned work")
 for i in range(200):
  actor.move(0.1)
  if actor.path.is_empty():break
 check(actor.foot.distance_to(destination)<1,"Compact transition physically reaches the work route")
 actor.foot=doorway;actor.direction="east";actor.goal="";actor.path.clear()
 actor.squeeze_point=Vector2.INF
 check(Safety.advance(game,actor,0.1) and actor.goal=="flood-retreat","Cramped swimmer retreats before oxygen becomes critical")
 for i in range(600):
  Safety.advance(game,actor,0.1)
  if actor.goal!="flood-retreat":break
 check(actor.cell_at(actor.foot)!=Vector2i(21,20) and not actor.dead,"Crew physically leaves flooded doorway")
 for room in game.placed_rooms: room.water_level=0.6 if room.pos==Vector2i(21,20) else 0.3
 actor.foot=doorway;actor.direction="east";actor.goal="";actor.path.clear()
 actor.squeeze_point=Vector2.INF;actor.set_meta("flood_safety_wait",0.0)
 check(Safety.advance(game,actor,0.1) and actor.goal=="flood-retreat","Wading-depth refuge remains usable when no room is completely dry")
 check(float(game.occupied.get(actor.goal_cell,{}).get("water_level",1.0))<0.55,"Refuge stays below swimming depth")
 for room in game.placed_rooms: room.water_level=0.6
 actor.foot=doorway;actor.direction="east";actor.goal="";actor.path.clear()
 actor.squeeze_point=Vector2.INF;actor.set_meta("flood_safety_wait",0.0)
 Safety.advance(game,actor,0.1)
 check(not actor.path.is_empty(),"No refuge still permits moving clear of a caught doorway pose")
 for i in range(30):
  actor.move(0.1)
  if actor.path.is_empty():break
 check(actor.foot.distance_to(doorway)>1,"No-refuge recovery moves physically without granting oxygen")
 game.resources.power=game._get_power_capacity()
 game._refresh_resources()
 check(game.resource_labels.power.text.contains("FULL"),"Full power storage is labelled in the HUD")
 print("OWNER REPORT REGRESSIONS ","PASS" if failures==0 else "FAIL")
 quit(0 if failures==0 else 1)

