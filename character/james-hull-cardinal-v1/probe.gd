extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-hull-cardinal-v1/"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-hull-cardinal-probe.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;var initial:Vector2=actor.foot;var core:=Vector2i(20,20);var base:Dictionary=game.occupied[core].duplicate(true);var target:=Vector2i(21,20);var rows:Array=[]
	for id in ["life_support","cold_store","maintenance_bay","reactor","battery_array","pressure_control","salvage_workshop","crew_lounge","crew_hab","observation_room","ore_refinery","listening_post","galley","research_lab"]:
		if game.RoomDatabaseScript.get_room(id).is_empty():continue
		for rotation in range(4):
			game.placed_rooms.assign([base.duplicate(true)]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0]
			game.wrecks.erase(target);game.drone_fleet.sites.erase(target)
			game._place_room(id,target,true)
			if not game.occupied.has(target):continue
			game.occupied[target].rotation=rotation
			actor.signature="";actor.rebuild(game);actor.foot=initial
			var found:Dictionary=Hull.approach(actor,target)
			if found.is_empty():rows.append({"id":id,"rotation":rotation,"reachable":false});continue
			var local:Vector2=found.point-(Vector2(target)+Vector2.ONE*.5)*384
			var facing:String=("west" if local.x<0 else "east") if absf(local.x)>absf(local.y) else ("north" if local.y<0 else "south")
			rows.append({"id":id,"rotation":rotation,"reachable":true,"facing":facing,"point":[found.point.x,found.point.y],"local":[local.x,local.y],"routePoints":found.route.size()})
	var file:=FileAccess.open(RESULT+"probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"rows":rows,"scope":"Dedicated fixture room placement plus real authored navigation/normal Hull.approach; geometry discovery, not paid work or visual acceptance."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"probe.gd.uid"):
		var uid:=FileAccess.open(RESULT+"probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES CARDINAL GEOMETRY PROBE: ",rows.size()," rows")
	game.queue_free();quit(0)
