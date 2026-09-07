extends RefCounted
## Character identities persist as unlocks; physical presence belongs to one loop.
const IDS := ["bill", "veld", "branforth"]
const NAMES := {"bill":"Major Bill", "veld":"Dr. Veld", "branforth":"Chief Engineer Branforth"}
const ROLES := {"bill":"Station Architect", "veld":"Science Architect", "branforth":"Engineering Architect"}
const STARTING_SUPPLIES := {
	"bill": {"food":4,"oxygen":4},
	"veld": {"data":6,"biomass":2},
	"branforth": {"metal":6,"rare_minerals":1}
}
const PERKS := {
	"bill":"Emergency provisions: +4 Food and +4 Oxygen at loop start.",
	"veld":"Research cache: +6 Data and +2 Biomass at loop start.",
	"branforth":"Repair stock: +6 Metal and +1 Rare Mineral at loop start."
}
const PORTRAITS := {"bill":"major-bill-v2", "veld":"dr-veld-v1", "branforth":"chief-engineer-branforth-v1"}

static func starting_supplies(id: String) -> Dictionary:
	return STARTING_SUPPLIES.get(id, {}).duplicate()

static func portrait(id: String) -> Texture2D:
	var picture := Image.new()
	var bytes := FileAccess.get_file_as_bytes("res://character/%s/frames/idle-south/frame_000.png" % PORTRAITS[id])
	if picture.load_png_from_buffer(bytes) != OK: return null
	var atlas := AtlasTexture.new()
	atlas.atlas = ImageTexture.create_from_image(picture)
	atlas.region = Rect2(30, 9, 32, 34)
	return atlas

const CORE_CELL := Vector2i(20,20)
const CORE_POD_RECT := Rect2(-143,-147,62,90)
const DURATION := 7.0

static func pod(id: String, key: String) -> Dictionary:
	return {"id":key,"architect_id":id,"name":NAMES[id],"wake":0.0,"recovered":false}

static func begin(game) -> Dictionary:
	var selected: String = game.meta.selected_architect
	if not IDS.has(selected) or not game.meta.unlocked_architect_ids.has(selected): selected="bill"
	var others: Array = IDS.duplicate()
	others.erase(selected)
	var index := 0
	for cell in game.wrecks:
		var ward: Dictionary = game.wrecks[cell]
		if ward.kind!="cryo": continue
		ward.pods=[pod(others[index],"architect_"+others[index])]
		index+=1
	return {"version":1,"selected":selected,"core":pod(selected,"core_architect")}

static func present(game, id: String) -> bool:
	if game.architect_run.is_empty(): return true # Legacy checkpoints retain their existing crew.
	for member in game.recovered_crew:
		if member.get("architect_id","")==id and member.alive: return true
	return false

static func actor_for(game, id: String):
	match id:
		"veld": return game.veld_npc
		"branforth": return game.branforth_npc
	return game.bill_npc

static func release(game, occupant: Dictionary, cell: Vector2i) -> bool:
	var id: String = occupant.get("architect_id","")
	if id.is_empty(): return true
	var actor = actor_for(game,id)
	actor.rebuild(game)
	var room: Dictionary = game.occupied[cell]
	var geometry: Dictionary = game.grid_view.bill_room_geometry(room,[])
	var desired := (Vector2(cell)+Vector2.ONE*0.5)*384.0
	for prop in geometry.props:
		if prop.id in ["architect_pod","cryo_pod_0"]:
			desired+=Vector2(prop.rect.get_center().x,prop.rect.end.y+18)
			break
	actor.avoidance_positions.clear()
	for peer_id in IDS:
		var peer = actor_for(game,peer_id)
		if peer!=actor and peer.active: actor.avoidance_positions.append(peer.foot)
	var chosen := -1
	var distance := INF
	for point_id in actor.room_nodes.get(cell,[]):
		var point: Vector2 = actor.graph.get_point_position(point_id)
		if actor.spawn_clear(point) and point.distance_squared_to(desired)<distance:
			chosen=point_id
			distance=point.distance_squared_to(desired)
	if chosen<0: return false
	actor.foot=actor.graph.get_point_position(chosen)
	actor.active=true
	actor.direction="south"
	actor.state="idle"
	actor.activity="recovered from cryostasis"
	actor.timer=1.0
	return true

static func advance_core(game, delta: float) -> void:
	if game.architect_run.is_empty() or not game.running or game.paused: return
	var occupant: Dictionary=game.architect_run.core
	if occupant.recovered: return
	# The core pod's initial emergency wake is supplied by the reboot sequence.
	occupant.wake=minf(DURATION,float(occupant.wake)+maxf(delta,0.0))
	if occupant.wake<DURATION: return
	if not release(game,occupant,CORE_CELL):
		occupant.wake=DURATION-0.001
		return
	occupant.recovered=true
	game.recovered_crew.append({"id":occupant.id,"architect_id":occupant.architect_id,"name":occupant.name,"origin":CORE_CELL,"alive":true})
	game.crew_count+=1
	game.had_crew=true
	game._log("%s awake. Your station has been waiting longer than you have." % occupant.name,false)
	game._refresh_all()

static func valid(data: Variant, wrecks: Dictionary, roster: Variant) -> bool:
	if data==null: return false
	if data is Dictionary and data.is_empty(): return true
	if not roster is Array: return false
	if not data is Dictionary or data.get("version")!=1 or not IDS.has(data.get("selected")): return false
	var p=data.get("core")
	if not p is Dictionary or p.get("id")!="core_architect" or p.get("architect_id")!=data.selected or p.get("name")!=NAMES[data.selected]: return false
	if not p.get("wake") is float or not is_finite(p.wake) or p.wake<0 or p.wake>DURATION or not p.get("recovered") is bool or p.recovered!=(p.wake==DURATION): return false
	var seen := {data.selected:true}
	for ward in wrecks.values():
		if ward.kind!="cryo": continue
		for occupant in ward.pods:
			var id: String = occupant.get("architect_id","")
			if not IDS.has(id) or seen.has(id): return false
			seen[id]=true
	if seen.size()!=IDS.size(): return false
	for member in roster:
		if not member is Dictionary: return false
		if not IDS.has(member.get("architect_id")): return false
	return true
