extends SceneTree
const NPC=preload("res://scripts/bill_npc.gd")
class Errors extends Logger:
	var messages=[]
	func _log_error(_fn:String,_file:String,_line:int,code:String,rationale:String,_notify:bool,kind:int,_traces:Array[ScriptBacktrace])->void:
		if kind!=Logger.ERROR_TYPE_WARNING:messages.append(code+" "+rationale)
class FakeGrid extends RefCounted:
	var slow=true
	func bill_room_geometry(_room:Dictionary,_sides:Array)->Dictionary:
		if slow:OS.delay_usec(6000)
		return {"blockers":[],"open":[]}
class Station extends Node:
	var occupied={Vector2i(20,20):{"id":"storage_bay"}}
	var architect_run={}
	var wrecks={}
	var grid_view=FakeGrid.new()
	func _connected_neighbor_cells(_cell:Vector2i)->Array:return []
	func get_room_doors(_room:Dictionary)->Array:return []
var finished=false
func staged(actor,station)->void:
	await actor.rebuild(station,true)
	finished=true
func _init()->void:call_deferred("run")
func run()->void:
	var errors=Errors.new()
	OS.add_logger(errors)
	var station=Station.new()
	root.add_child(station)
	var actor=NPC.new()
	staged(actor,station)
	var yielded=not finished
	station.grid_view.slow=false
	station.occupied[Vector2i(21,20)]={"id":"life_support"}
	actor.rebuild(station)
	var signature=actor.signature
	var expected=actor.geometry.duplicate(true)
	var graph_points=actor.graph.get_point_ids()
	var graph_links={}
	for point in graph_points:graph_links[point]=actor.graph.get_point_connections(point)
	var deadline=Time.get_ticks_msec()+5000
	while not finished and Time.get_ticks_msec()<deadline:await process_frame
	var ok=yielded and finished and errors.messages.is_empty() and actor.signature==signature and actor.geometry==expected and not actor.fire_building_navigation and graph_points.size()>0 and actor.graph.get_point_ids()==graph_points
	for point in graph_points:ok=ok and actor.graph.get_point_connections(point)==graph_links[point]
	for restored_dead in [false,true]:
		actor=NPC.new()
		NPC.room_cache.clear() # Each case must exercise a cold, yielded warm-up.
		var dormant=actor.snapshot()
		dormant.dead=restored_dead
		station.grid_view.slow=true
		finished=false
		staged(actor,station)
		var dormant_yielded=not finished
		await actor.restore_snapshot(station,dormant)
		deadline=Time.get_ticks_msec()+5000
		while not finished and Time.get_ticks_msec()<deadline:await process_frame
		var dormant_ok=dormant_yielded and finished and not actor.active and actor.dead==restored_dead and actor.signature.is_empty() and actor.graph.get_point_count()==0 and actor.geometry.is_empty() and not actor.fire_building_navigation
		print("RESTORE SUPERSEDES WARMUP: dead=%s pass=%s yielded=%s points=%d geometry=%d signature=%s building=%s"%[restored_dead,dormant_ok,dormant_yielded,actor.graph.get_point_count(),actor.geometry.size(),actor.signature,actor.fire_building_navigation])
		ok=ok and dormant_ok
	ok=ok and errors.messages.is_empty()
	OS.remove_logger(errors)
	print("STAGED REBUILD REPLACEMENT: pass=%s yielded=%s finished=%s errors=%s"%[ok,yielded,finished,errors.messages])
	station.free()
	quit(0 if ok else 1)
