extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-hull-cardinal-v1/"
class CardinalJames extends "res://scripts/branforth_npc.gd":
	var available_face:String="north"
	var work_cell:=Vector2i(21,20)
	func can_stand(point:Vector2) -> bool:
		if not super.can_stand(point):return false
		if cell_at(point)!=work_cell:return true
		var local:Vector2=point-(Vector2(work_cell)+Vector2.ONE*.5)*384
		if maxf(absf(local.x),absf(local.y))<80:return true
		var facing:String=("west" if local.x<0 else "east") if absf(local.x)>absf(local.y) else ("north" if local.y<0 else "south")
		return facing==available_face
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-hull-cardinal-access-probe.loop")
	game.branforth_npc=CardinalJames.new();game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;var core:=Vector2i(20,20);var base:Dictionary=game.occupied[core].duplicate(true);var target:=Vector2i(21,20);var rows:Array=[]
	for id in ["life_support","cold_store","maintenance_bay","crew_lounge","observation_room","galley"]:
		for facing in ["north","east","south","west"]:
			game.placed_rooms.assign([base.duplicate(true)]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0]
			game.wrecks.erase(target);game.drone_fleet.sites.erase(target);game._place_room(id,target,true)
			actor.available_face=facing;actor.signature="";actor.room_cache.clear();actor.rebuild(game)
			var starts:Array=[]
			for node in actor.room_nodes.get(target,[]):
				var point:Vector2=actor.graph.get_point_position(node);var local:Vector2=point-(Vector2(target)+Vector2.ONE*.5)*384
				if maxf(absf(local.x),absf(local.y))<80 and actor.can_stand(point):starts.append(point)
			if starts.is_empty():rows.append({"id":id,"wanted":facing,"reachable":false,"reason":"no interior fixture start"});continue
			actor.foot=starts[0];var found:Dictionary=Hull.approach(actor,target)
			if found.is_empty():rows.append({"id":id,"wanted":facing,"reachable":false,"reason":"normal approach unavailable"});continue
			var local:Vector2=found.point-(Vector2(target)+Vector2.ONE*.5)*384
			var selected:String=("west" if local.x<0 else "east") if absf(local.x)>absf(local.y) else ("north" if local.y<0 else "south")
			rows.append({"id":id,"wanted":facing,"reachable":true,"facing":selected,"start":[actor.foot.x,actor.foot.y],"point":[found.point.x,found.point.y],"local":[local.x,local.y],"routePoints":found.route.size()})
	var file:=FileAccess.open(RESULT+"access-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"rows":rows,"scope":"Dedicated free-placed room, prescribed available wall band and genuine interior graph start; inherited real floor/prop checks and normal Hull.approach. Geometry discovery only."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"access_probe.gd.uid"):
		var uid:=FileAccess.open(RESULT+"access_probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES CARDINAL ACCESS PROBE: ",rows.size()," rows");game.queue_free();quit(0)
