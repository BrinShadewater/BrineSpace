extends RefCounted
## Staged paired disk contract. Marker prevents ordinary Continue silently dropping
## this unselected return/room renderer. Normal selection remains a separate gate.
const SAVE=preload("res://scripts/run_save.gd")
const FLOOR=preload("res://character/james-floor-case-west-v1/floor_state.gd")
const ACTOR=preload("res://character/james-floor-case-west-v1/floor_actor.gd")
const PLAYER=preload("res://character/james-floor-case-west-v1/floor_player.gd")
const PLANNER=preload("res://character/james-east-cargo-heads-v3/return_plan.gd")
const FIELD="james_return_candidate"
const BINDING="james-west-return9-floor3"
const MARKER="unadmitted_james_cargo_return"
static func probe(player,plan:Dictionary):
	var copy=PLAYER.new()
	for key in ["frames","timing","equipment_frames","equipment_timing"]:copy.set(key,player.get(key))
	copy.return_plan=plan.duplicate(true)
	return copy
static func source_bindings(player,plan:Dictionary)->Array:
	var result:Array=[]
	if plan.is_empty():return result
	var bank:Dictionary=player.bank_for(plan.gear)
	for row in plan.rows:
		var texture:Texture2D=bank[row.key][row.index]
		result.append({"rgba":texture.get_image().get_data().hex_encode().sha256_text(),"pivot":texture.get_meta("crew_pivot"),"height":texture.get_meta("crew_standing_height")})
	return result
static func capture(game)->Dictionary:
	var data:Dictionary=SAVE.capture(game)
	var player=game.grid_view.branforth_player
	var plan:Dictionary=player.return_plan.duplicate(true)
	var stage:String=str(data.crew.branforth.stage)
	if not plan.is_empty():stage=""
	data[FIELD]={"version":1,"binding":BINDING,"actorStage":stage,"plan":plan,"sourceBindings":source_bindings(player,plan)}
	data.crew.branforth.stage=MARKER
	return data
static func base_packet(data:Dictionary)->Dictionary:
	var copy:Dictionary=data.duplicate(true)
	copy.crew.branforth.stage=copy[FIELD].actorStage
	copy.erase(FIELD)
	return copy
static func valid_shape(data:Variant)->bool:
	if not data is Dictionary or not data.get(FIELD) is Dictionary:return false
	var extra:Dictionary=data[FIELD]
	if extra.size()!=5 or extra.get("version")!=1 or not extra.get("version") is int or extra.get("binding")!=BINDING:return false
	if not extra.get("actorStage") is String or not extra.get("plan") is Dictionary or not extra.get("sourceBindings") is Array:return false
	if not data.get("crew") is Dictionary or not data.crew.get("branforth") is Dictionary or data.crew.branforth.get("stage")!=MARKER:return false
	if not data.crew.get("playback") is Dictionary or not data.crew.playback.get("branforth") is Dictionary:return false
	if not data.get("state") is Dictionary or not FLOOR.valid_rooms(data.state.get("placed_rooms")):return false
	if not SAVE.problem(base_packet(data)).is_empty():return false
	var plan:Dictionary=extra.plan
	if plan.is_empty():return extra.sourceBindings.is_empty()
	var required:Array=["gear","source","sourceIndex","facing","rows","gaps","selected","started","until","floorCell","floorFoot"]
	if plan.size()!=required.size():return false
	for key in required:
		if not plan.has(key):return false
	if plan.gear not in ["","diving-helmet"] or plan.facing!="west" or not plan.source is String or not plan.sourceIndex is int or plan.sourceIndex<0:return false
	if not plan.selected is bool or plan.selected or not plan.rows is Array or plan.rows.is_empty() or plan.rows.size()>64 or not plan.gaps is Array:return false
	if not plan.floorCell is Vector2i or not plan.floorFoot is Vector2 or not plan.floorFoot.is_finite():return false
	for key in ["started","until"]:
		if not plan[key] is float or not is_finite(plan[key]) or plan[key]<0:return false
	var clock:Variant=data.state.get("visual_time_seconds")
	if not clock is float or not is_finite(clock) or clock<plan.started or clock>=plan.until:return false
	var seconds:=0.0
	for row in plan.rows:
		if not row is Dictionary or row.size()!=3 or not row.get("key") is String or not row.get("index") is int or row.index<0 or row.index>63:return false
		if not row.get("seconds") is float or not is_finite(row.seconds) or row.seconds<=0 or row.seconds>.5:return false
		seconds+=row.seconds
	if absf(plan.until-plan.started-seconds)>.000001:return false
	if plan.rows[0].key!=plan.source or plan.rows[0].index!=plan.sourceIndex:return false
	if extra.sourceBindings.size()!=plan.rows.size():return false
	for item in extra.sourceBindings:
		if not item is Dictionary or item.size()!=3 or not item.get("rgba") is String or item.rgba.length()!=64:return false
		if not item.get("pivot") is Vector2 or not item.pivot.is_finite() or item.get("height")!=148:return false
	var actor:Dictionary=data.crew.branforth
	if extra.actorStage!="" or not actor.active or actor.get("dead",false) or actor.movement_medium!="dry" or actor.state!="idle" or actor.goal!="" or not actor.path.is_empty() or actor.timer!=0.0:return false
	if actor.foot!=plan.floorFoot or actor.goal_cell!=plan.floorCell or ("diving-helmet" if actor.helmet_equipped else "")!=plan.gear:return false
	if data.crew.playback.branforth.get("equipment","")!=plan.gear:return false
	if not data.crew.playback.branforth.get("motion",{}).is_empty():return false
	var rooms:Dictionary=SAVE.occupancy_for_rooms(data.state.placed_rooms)
	if not rooms.has(plan.floorCell) or rooms[plan.floorCell].id!="salvage_workshop":return false
	var local:Vector2=plan.floorFoot-(Vector2(plan.floorCell)+Vector2.ONE*.5)*384
	return FLOOR.valid_payload({"version":1,"source":FLOOR.SOURCE,"anchor":local})
static func admits_loaded(data:Dictionary,player)->bool:
	if not valid_shape(data):return false
	var plan:Dictionary=data[FIELD].plan
	if plan.is_empty():return true
	var canonical:Dictionary=PLANNER.build(player,plan.source,plan.sourceIndex,plan.gear)
	if canonical.is_empty():return false
	canonical.started=plan.started;canonical.until=plan.until;canonical.floorCell=plan.floorCell;canonical.floorFoot=plan.floorFoot
	if canonical!=plan or source_bindings(player,plan)!=data[FIELD].sourceBindings:return false
	var at=probe(player,plan);var release:float=FLOOR.release_time(at)
	if not is_finite(release):return false
	if data.state.visual_time_seconds>=release:
		var rooms:Dictionary=SAVE.occupancy_for_rooms(data.state.placed_rooms)
		var owned:Dictionary=FLOOR.payload(rooms[plan.floorCell])
		var local:Vector2=plan.floorFoot-(Vector2(plan.floorCell)+Vector2.ONE*.5)*384
		if owned.is_empty() or owned.anchor!=local:return false
	return true
static func write(game,path:String)->Error:
	if not game.running or game.testing_free_build or game.testing_disable_failures or game.get_meta("restoring_checkpoint",false):return ERR_UNAVAILABLE
	var data:Dictionary=capture(game)
	if not admits_loaded(data,game.grid_view.branforth_player):return ERR_INVALID_DATA
	var bytes:PackedByteArray=var_to_bytes(data)
	var file:=FileAccess.open(path+".tmp",FileAccess.WRITE)
	if file==null:return FileAccess.get_open_error()
	file.store_string(bytes.hex_encode().sha256_text()+"\n");file.store_buffer(bytes);file.flush()
	var error:Error=file.get_error();file.close()
	if error!=OK:return error
	if FileAccess.file_exists(path):
		error=DirAccess.copy_absolute(path,path+".bak")
		if error!=OK:return error
		error=DirAccess.remove_absolute(path)
		if error!=OK:return error
	return DirAccess.rename_absolute(path+".tmp",path)
static func read(path:String)->Dictionary:
	var file:=FileAccess.open(path,FileAccess.READ)
	if file==null or file.get_length()>16*1024*1024:return {}
	var hash:String=file.get_line();var bytes:PackedByteArray=file.get_buffer(file.get_length()-file.get_position())
	if bytes.hex_encode().sha256_text()!=hash:return {}
	var data:Variant=bytes_to_var(bytes)
	if not valid_shape(data):return {}
	data._path=path;return data
static func restore_staged(game,data:Dictionary)->bool:
	var player=game.grid_view.branforth_player
	if not admits_loaded(data,player):return false
	if not await SAVE.restore_staged(game,base_packet(data)):return false
	var actor=ACTOR.new();actor.preview_player=player
	await actor.restore_snapshot(game,base_packet(data).crew.branforth,true)
	game.branforth_npc=actor
	player.return_plan=data[FIELD].plan.duplicate(true);player.return_clock=game.get_visual_time_seconds();player.last_source.clear()
	return true
