extends RefCounted
## Staged cosmetic latest James case per workshop; no inventory/collision changes.
const FIELD="james_floor_case"
const SOURCE="james-west-case3"
const RELEASE_INDEX=4
const CUE_HASHES={"":"8f817de0728a0bf26ca19ba525937e96e20beb4928c5076956cc5f2c7bc135c1","diving-helmet":"f489a16ef76034aa74909fb756d7981c7db820472ff3d27d8311d4f7b8c989d8"}
static var checked_cues:Dictionary={}
static func valid_payload(data:Variant)->bool:
	if not data is Dictionary or data.size()!=3 or data.get("version")!=1 or not data.get("version") is int or data.get("source")!=SOURCE:return false
	var anchor:Variant=data.get("anchor")
	return anchor is Vector2 and anchor.is_finite() and absf(anchor.x)<=192 and absf(anchor.y)<=192
static func valid_rooms(rooms:Variant)->bool:
	if not rooms is Array:return false
	for room in rooms:
		if not room is Dictionary:return false
		if room.has(FIELD) and (room.get("id")!="salvage_workshop" or not valid_payload(room[FIELD])):return false
	return true
static func payload(room:Dictionary)->Dictionary:
	return room[FIELD] if room.get("id")=="salvage_workshop" and valid_payload(room.get(FIELD)) else {}
static func cue_available(player,gear:String)->bool:
	var bank:Dictionary=player.bank_for(gear)
	if not CUE_HASHES.has(gear) or bank.get("unload-west",[]).size()!=7:return false
	var cue:Texture2D=bank["unload-west"][RELEASE_INDEX]
	if cue==null:return false
	var id:int=cue.get_instance_id()
	if not checked_cues.has(id):checked_cues[id]=cue.get_image().get_data().hex_encode().sha256_text()==CUE_HASHES[gear]
	return checked_cues[id]
static func release_time(player)->float:
	var plan:Dictionary=player.return_plan
	if plan.get("facing")!="west" or not plan.get("started") is float or not is_finite(plan.started):return INF
	if not cue_available(player,str(plan.get("gear",""))):return INF
	var bank:Dictionary=player.bank_for(plan.gear)
	var clocks:Dictionary=player.timing if plan.gear=="" else player.equipment_timing.get(plan.gear,{})
	var time:float=plan.started
	var cue_time:=INF;var index:=0
	for row in plan.get("rows",[]):
		if not row is Dictionary or not row.get("index") is int or not bank.has(row.get("key")) or not clocks.has(row.get("key")):return INF
		if row.index<0 or row.index>=bank[row.key].size() or not row.get("seconds") is float or not is_finite(row.seconds) or row.seconds<=0:return INF
		var duration:float=.08 if index==0 else float(clocks[row.key].durations[row.index])/1000.0
		if absf(row.seconds-duration)>.000001:return INF
		if row.key=="unload-west" and row.index==RELEASE_INDEX:cue_time=time
		time+=row.seconds;index+=1
	if not plan.get("until") is float or not is_finite(plan.until) or absf(plan.until-time)>.0001:return INF
	return cue_time
static func observe_plan(game,actor,player,time:float)->bool:
	var plan:Dictionary=player.return_plan
	if plan.is_empty() or not is_finite(time) or time<release_time(player):return false
	if not actor.active or actor.dead or actor.movement_medium!="dry" or actor.goal!="" or actor.stage!="" or actor.state!="idle" or not actor.can_stand(actor.foot):return false
	if ("diving-helmet" if actor.helmet_equipped else "")!=plan.get("gear"):return false
	if not plan.get("floorCell") is Vector2i or not plan.get("floorFoot") is Vector2 or actor.foot!=plan.floorFoot:return false
	if not game.occupied.has(plan.floorCell):return false
	var room:Dictionary=game.occupied[plan.floorCell]
	if room.get("id")!="salvage_workshop":return false
	var anchor:Vector2=plan.floorFoot-(Vector2(plan.floorCell)+Vector2.ONE*.5)*384
	var data:Dictionary={"version":1,"source":SOURCE,"anchor":anchor}
	if not valid_payload(data) or room.has(FIELD) and not valid_payload(room[FIELD]):return false
	if payload(room)==data:return false
	room[FIELD]=data;return true
