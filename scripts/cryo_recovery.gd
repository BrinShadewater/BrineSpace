extends RefCounted
## Finite occupants belong to a discovered compartment, never a blueprint.
const REPAIR_METAL := 8
const WAKE_SECONDS := 7.0
const CHARGE_SECONDS := 12.0

static func duration(ward: Dictionary) -> float:
	return CHARGE_SECONDS if ward.kind == "charging" else WAKE_SECONDS
const NAMES := ["Rowan Hale", "Ellis Ward", "Morgan Vale"]

static func seed(wrecks: Dictionary) -> void:
	for i in range(2):
		var pods: Array = []
		for j in range(i+1):
			pods.append({"id":"cryo_%d_%d" % [i,j],"name":NAMES[i+j],"wake":0.0,"recovered":false})
		wrecks[Vector2i(19,18) if i==0 else Vector2i(22,21)] = {"kind":"cryo","progress":0.0,"active":false,"cleared":false,"paid":false,"rotation":i,"pods":pods}

static func accessible(game, cell: Vector2i) -> bool:
	var ward: Dictionary = game.wrecks[cell]
	for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		if game.occupied.has(cell+offset) and game._doors_connect("cryo_chamber",int(ward.rotation),offset,game.occupied[cell+offset]):
			return true
	return false

static func status(game, cell: Vector2i) -> String:
	var ward: Dictionary = game.wrecks[cell]
	if not ward.cleared:
		return "REPAIRING PRESSURE HULL" if ward.active else "SEALED DERELICT"
	var remaining := false
	for pod in ward.pods:
		remaining = remaining or not pod.recovered
	if not remaining: return "RECOVERY COMPLETE"
	if not game.occupied.has(cell) or game.occupied[cell].get("suspended",false): return "ROOM SUSPENDED"
	if not game.powered_room_cells.has(cell): return "WAITING FOR POWER / NEXT CYCLE"
	if ward.kind == "charging" and ward.pods[0].wake < CHARGE_SECONDS: return "PUMPING WHITE FLUID / RECHARGING"
	if game.crew_count >= game._get_crew_capacity(): return "WAITING FOR A FREE BERTH"
	if ward.kind == "charging": return "PUMPING WHITE FLUID / RECHARGING"
	if game.resources.get("oxygen",0)<=0 or game.resources.get("food",0)<=0: return "WAITING FOR FOOD AND OXYGEN"
	return "THAWING / WAKING"

static func advance(game, delta: float) -> void:
	if not game.running or game.paused: return
	for cell in game.wrecks:
		var ward: Dictionary = game.wrecks[cell]
		if ward.kind not in ["cryo","charging"] or status(game,cell) not in ["THAWING / WAKING","PUMPING WHITE FLUID / RECHARGING"]: continue
		var seconds := duration(ward)
		for pod in ward.pods:
			if pod.recovered: continue
			pod.wake = minf(seconds,float(pod.wake)+maxf(delta,0.0))
			if pod.wake >= seconds:
				if game.crew_count >= game._get_crew_capacity(): break
				if not preload("res://scripts/architects.gd").release(game,pod,cell):
					pod.wake=seconds-0.001
					break
				pod.recovered = true
				var member := {"id":pod.id,"name":pod.name,"origin":cell,"alive":true}
				if pod.has("architect_id"):
					member["architect_id"]=pod.architect_id
					if game.meta.unlock_architect(pod.architect_id):
						game.run_discovered_character_ids.append(pod.architect_id)
						game._log("ARCHITECT RECOVERED // %s is available for future loops." % pod.name,false)
				game.recovered_crew.append(member)
				game.play_station_sound("crew_awake",Vector2(cell))
				game.crew_count += 1
				game.had_crew = true
				game._log("%s added to crew roster. The pod is empty. The station is less so." % pod.name,false)
				game._refresh_all()
			break # One controlled emergence at a time in each ward; no catch-up births.

static func valid_ward(w: Dictionary) -> bool:
	if not w.get("paid") is bool or not w.get("rotation") is int or w.rotation not in [0,1,2,3]: return false
	if not w.get("pods") is Array or w.pods.size()<1 or w.pods.size()>2: return false
	if (w.progress>0 or w.active or w.cleared) and not w.paid: return false
	var ids := {}
	for p in w.pods:
		if not p is Dictionary or not p.get("id") is String or p.id.is_empty() or ids.has(p.id) or not p.get("name") is String: return false
		ids[p.id] = true
		if p.has("architect_id"):
			if not preload("res://scripts/architects.gd").IDS.has(p.architect_id) or p.name!=preload("res://scripts/architects.gd").NAMES[p.architect_id]: return false
		if not p.get("wake") is float or not is_finite(p.wake) or p.wake<0 or p.wake>duration(w) or not p.get("recovered") is bool: return false
		if p.recovered and p.wake!=duration(w): return false
		if w.kind != "charging" and p.recovered != (p.wake==duration(w)): return false
		if not w.cleared and p.wake>0: return false
		if w.kind == "charging" and (w.pods.size()!=1 or p.get("architect_id","")!="marsh"): return false
	return true

static func valid_roster(roster: Variant, wrecks: Dictionary, rooms: Array, architects: Dictionary = {}) -> bool:
	if not roster is Array: return false
	var expected := {}
	var all_ids := {}
	if not architects.is_empty() and architects.core.recovered:
		expected[architects.core.id]={"name":architects.core.name,"origin":preload("res://scripts/architects.gd").CORE_CELL,"architect_id":architects.selected}
	for cell in wrecks:
		var w: Dictionary = wrecks[cell]
		if w.kind not in ["cryo","charging"]: continue
		if w.cleared:
			var found := false
			for room in rooms:
				if room.pos==cell and room.id=="cryo_chamber" and room.get("recovered_derelict",false) and int(room.rotation)==int(w.rotation): found=true
			if not found: return false
		for p in w.pods:
			if all_ids.has(p.id): return false
			all_ids[p.id]=true
			if p.recovered: expected[p.id]={"name":p.name,"origin":cell,"architect_id":p.get("architect_id","")}
	for member in roster:
		if not member is Dictionary or not member.get("id") is String or not expected.has(member.id): return false
		if member.get("name")!=expected[member.id].name or member.get("origin")!=expected[member.id].origin or not member.get("alive") is bool: return false
		if member.get("architect_id","")!=expected[member.id].get("architect_id",""): return false
		expected.erase(member.id)
	return expected.is_empty()
