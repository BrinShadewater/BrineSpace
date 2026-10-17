from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-meal.gd').read_text().split('\tfor q in range(4):',1)[0]
source+='''	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for offset in [Vector2i.ZERO,inside]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.goal="";npc.path.clear();npc.timer=30;npc.helmet_equipped=false;npc.movement_medium="dry";npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0}
		var geometry:Dictionary=npc.geometry[cell];var counters:Array=[]
		for prop in geometry.props:
			if preload("res://scripts/room_asset_library.gd").role_of(prop)!="galley_counter":continue
			var candidates:Array=[];var rect:Rect2=prop.rect
			for y in range(128,177,16):
				var point:=Vector2(rect.get_center().x,y);var graph_node:int=npc.nearest_in_room(center+point,cell)
				candidates.append({"point":str(point),"stand":npc.can_stand(center+point),"approachBlocked":npc.RoomActivity._approach_blocked(geometry,point),"nearestNode":str(npc.graph.get_point_position(graph_node)-center) if graph_node>=0 else "none"})
			counters.append({"id":prop.id,"rect":str(rect),"registration":prop.get("registration",{}),"collision":str(preload("res://tools/modular_room_geometry.gd").prop_collision_rects(prop)),"frontCandidates":candidates})
		var stations:Array=npc.RoomActivity.stations(geometry)
		check(not stations.is_empty(),"Current galley station")
		if not stations.is_empty():
			npc.foot=center+Vector2(stations[0].point);npc.direction=stations[0].facing;npc.state="idle"
			await capture("contact-q%d-current"%q,npc)
		results.append({"rotation":q,"counters":counters,"stations":stations})
	var file:=FileAccess.open(OUT+"native-contact-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Static actual default galley geometry and native registered idle contact study, four rotations. No pickup animation or gameplay journey claimed."},"  "));file.close()
	print("JAMES CONTACT PROBE: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
'''
(P/'native-contact-probe.gd').write_text(source)
print('Created four-rotation registered counter contact probe')
