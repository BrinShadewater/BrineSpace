extends RefCounted
## Normal-packet James cargo extension. No RunSave dependency: callers validate
## the base station separately before mutation. Normal factory/save/title hooks use this contract.
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
const PLAYER=preload("res://character/james-floor-case-west-v1/checkpoint_floor_player_v2.gd")
const PLANNER=preload("res://character/james-east-cargo-heads-v3/return_plan.gd")
const FIELD="james_cargo_return"
const BINDING="james-west-return9-rise6-floor7"
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
static func floor_binding(player)->Dictionary:
	if player.has_method("floor_texture"):
		var texture:Texture2D=player.floor_texture()
		if texture==null:return {}
		return {"source":FLOOR.SOURCE,"png":FileAccess.get_sha256(FLOOR.ART_PATH),"rgba":texture.get_image().get_data().hex_encode().sha256_text(),"pivot":Vector2(128,224),"height":148}
	if player.preview_view==null or player.preview_view.case_texture==null:return {}
	return {"source":FLOOR.SOURCE,"png":FileAccess.get_sha256(FLOOR.ART_PATH),"rgba":player.preview_view.case_texture.get_image().get_data().hex_encode().sha256_text(),"pivot":Vector2(128,224),"height":148}
static func bank_bindings(player)->Dictionary:
	var result:Dictionary={}
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.bank_for(gear)
		var clocks:Dictionary=player.timing if gear=="" else player.equipment_timing.get(gear,{})
		var bound:Dictionary={}
		for key in ["unload-west","carry-settle-west"]:
			if not bank.has(key) or not clocks.has(key):return {}
			var rows:Array=[]
			for index in range(bank[key].size()):
				var texture:Texture2D=bank[key][index]
				rows.append({"rgba":texture.get_image().get_data().hex_encode().sha256_text(),"pivot":texture.get_meta("crew_pivot"),"height":texture.get_meta("crew_standing_height"),"seconds":float(clocks[key].durations[index])/1000.0})
			bound[key]=rows
		result[gear]=bound
	return result
static func valid_floor_binding(value:Variant)->bool:
	if not value is Dictionary or value.size()!=5:return false
	if value.get("source")!=FLOOR.SOURCE or value.get("pivot")!=Vector2(128,224) or value.get("height")!=148:return false
	for key in ["png","rgba"]:
		if not value.get(key) is String or value[key].length()!=64:return false
	return true
static func valid_bank_bindings(value:Variant)->bool:
	if not value is Dictionary or value.size()!=2:return false
	for gear in ["","diving-helmet"]:
		if not value.get(gear) is Dictionary or value[gear].size()!=2:return false
		for key in ["unload-west","carry-settle-west"]:
			var rows:Variant=value[gear].get(key)
			if not rows is Array or rows.size()!=(7 if key=="unload-west" else 6):return false
			for row in rows:
				if not row is Dictionary or row.size()!=4 or not row.get("rgba") is String or row.rgba.length()!=64:return false
				if not row.get("pivot") is Vector2 or row.pivot!=Vector2(128,224) or row.get("height")!=148:return false
				if not row.get("seconds") is float or not is_finite(row.seconds) or row.seconds<=0 or row.seconds>.5:return false
	return true
static func capture(base:Dictionary,player,actor_stage:String)->Dictionary:
	var data:Dictionary=base.duplicate(true)
	var plan:Dictionary=player.return_plan.duplicate(true)
	data.crew.branforth.stage=actor_stage
	data[FIELD]={"version":2,"binding":BINDING,"actorStage":actor_stage,"plan":plan,"sourceBindings":source_bindings(player,plan),"floorBinding":floor_binding(player),"bankBindings":bank_bindings(player)}
	return data
static func base_packet(data:Dictionary)->Dictionary:
	var copy:Dictionary=data.duplicate(true)
	copy.erase(FIELD)
	return copy
static func occupancy_for_rooms(rooms:Array)->Dictionary:
	var occupied:Dictionary={}
	for room in rooms:
		if not room is Dictionary or not room.get("pos") is Vector2i:return {}
		for cell in preload("res://scripts/room_footprint.gd").cells(room.pos,room.get("size",Vector2i.ONE)):
			occupied[cell]=room
	return occupied
static func valid_shape(data:Variant)->bool:
	if not data is Dictionary or data.has("james_return_candidate") or not data.get(FIELD) is Dictionary:return false
	var extra:Dictionary=data[FIELD]
	if extra.size()!=7 or extra.get("version")!=2 or not extra.get("version") is int or extra.get("binding")!=BINDING:return false
	if not extra.get("actorStage") is String or not extra.get("plan") is Dictionary or not extra.get("sourceBindings") is Array:return false
	if extra.actorStage==MARKER:return false
	if not data.get("crew") is Dictionary or not data.crew.get("branforth") is Dictionary or data.crew.branforth.get("stage")!=extra.actorStage:return false
	if not data.crew.get("playback") is Dictionary or not data.crew.playback.get("branforth") is Dictionary:return false
	if not data.get("state") is Dictionary or not FLOOR.valid_rooms(data.state.get("placed_rooms")):return false
	if not valid_floor_binding(extra.get("floorBinding")) or not valid_bank_bindings(extra.get("bankBindings")):return false
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
	var rooms:Dictionary=occupancy_for_rooms(data.state.placed_rooms)
	if not rooms.has(plan.floorCell) or rooms[plan.floorCell].id!="salvage_workshop":return false
	var local:Vector2=plan.floorFoot-(Vector2(plan.floorCell)+Vector2.ONE*.5)*384
	return FLOOR.valid_payload({"version":1,"source":FLOOR.SOURCE,"anchor":local})
static func admits_loaded(data:Dictionary,player)->bool:
	if player==null or not player.has_method("return_texture") or not player.has_method("bank_for"):return false
	if not valid_shape(data):return false
	if data[FIELD].floorBinding!=floor_binding(player) or data[FIELD].bankBindings!=bank_bindings(player):return false
	var plan:Dictionary=data[FIELD].plan
	if plan.is_empty():return true
	var canonical:Dictionary=PLANNER.build(player,plan.source,plan.sourceIndex,plan.gear)
	if canonical.is_empty():return false
	canonical.started=plan.started;canonical.until=plan.until;canonical.floorCell=plan.floorCell;canonical.floorFoot=plan.floorFoot
	if canonical!=plan or source_bindings(player,plan)!=data[FIELD].sourceBindings:return false
	var at=probe(player,plan);var release:float=FLOOR.release_time(at)
	if not is_finite(release):return false
	if data.state.visual_time_seconds>=release:
		var rooms:Dictionary=occupancy_for_rooms(data.state.placed_rooms)
		var owned:Dictionary=FLOOR.payload(rooms[plan.floorCell])
		var local:Vector2=plan.floorFoot-(Vector2(plan.floorCell)+Vector2.ONE*.5)*384
		if owned.is_empty() or owned.anchor!=local:return false
	return true
static func restore_player(data:Dictionary,player,clock:float)->bool:
	if not admits_loaded(data,player) or not is_finite(clock):return false
	if clock!=float(data.state.visual_time_seconds):return false
	player.return_plan=data[FIELD].plan.duplicate(true)
	player.return_clock=clock
	player.last_source.clear()
	return true
