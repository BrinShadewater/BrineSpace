extends RefCounted
const IDS := ["river","josh","margot"]
const NAMES := {"river":"River","josh":"Josh","margot":"Margot"}
const ROLES := {"river":"Small utility droid","josh":"Tracked companion","margot":"Cat in a frog hat"}
const ROOMS := {"river":"salvage_workshop","josh":"storage_bay","margot":"cryo_chamber"}
const TITLES := {"river":"Garbage Disposal Room","josh":"Derelict Storage Room","margot":"Derelict Pet Cryo Ward"}
const OBJECTS := {"river":"trash container","josh":"shipping crate","margot":"pet cryopod"}
const CELLS := {"river":Vector2i(20,18),"josh":Vector2i(22,20),"margot":Vector2i(20,22)}
const REPAIR_METAL := 8
const BOOT_SECONDS := 8.0
const NPC = preload("res://scripts/companion_npc.gd")
static var portraits := {}
static var container_textures := {}
const CONTAINER_FOOT := Vector2(90,60)
const CONTAINER_RECT := Rect2(44,8,94,64)

static func container_texture(id: String, opened: bool) -> Texture2D:
	var key := id+ ("-open" if opened else "-closed")
	if not container_textures.has(key):
		var img := Image.new()
		if img.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/companions/encounters/"+key+".png"))!=OK:return null
		var texture := ImageTexture.create_from_image(img)
		texture.set_meta("crew_frame_92",true);texture.set_meta("crew_pivot",Vector2(80,144))
		container_textures[key]=texture
	return container_textures[key]

static func room_props(props: Array, id := "") -> Array:
	if id=="margot":return [] # This found ward contains exactly its three authored pods.
	# Found compartments clear a loading area around their one recovery object.
	return props.filter(func(prop):return not prop.get("layout_hidden",false) and not prop.rect.intersects(CONTAINER_RECT.grow(16)))

static func recovery_props(id: String, recovered := false) -> Array:
	if id!="margot":return [{"id":"companion_container","rect":CONTAINER_RECT,"position":CONTAINER_FOOT}]
	return [
		{"id":"margot-human-a","rect":Rect2(-134,-127,68,116),"position":Vector2(-100,-15)},
		{"id":"margot-human-b","rect":Rect2(61,-127,68,116),"position":Vector2(95,-15)},
		{"id":"margot-open" if recovered else "margot-closed","rect":Rect2(56,65,38,64),"position":Vector2(75,125)}]

static func prop_texture(key: String) -> Texture2D:
	if not container_textures.has(key):
		var img := Image.new()
		if img.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/companions/encounters/"+key+".png"))!=OK:return null
		var texture := ImageTexture.create_from_image(img)
		texture.set_meta("crew_frame_92",true);texture.set_meta("crew_pivot",Vector2(80,144))
		container_textures[key]=texture
	return container_textures[key]

static func portrait(id: String) -> Texture2D:
	if not IDS.has(id):return null
	if not portraits.has(id):
		var img := Image.new()
		if img.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/companions/%s-portrait.png"%id))!=OK:return null
		portraits[id]=ImageTexture.create_from_image(img)
	return portraits[id]

static func begin(game) -> void:
	game.companion_actors.clear();game.companion_roster.clear()
	for id in IDS:
		game.companion_actors[id]=NPC.new(id)
		var selected: bool=game.meta.selected_companion_ids.has(id) and game.meta.unlocked_companion_ids.has(id)
		if selected:game.companion_roster[id]=Vector2i(20,20)
		else:game.wrecks[CELLS[id]]={"kind":id,"progress":0.0,"active":false,"cleared":false,"paid":false,"boot":0.0,"opened":false,"recovered":false}

static func is_site(game, cell: Vector2i) -> bool:
	return IDS.has(game.wrecks.get(cell,{}).get("kind",""))

static func accessible(game, cell: Vector2i) -> bool:
	var id: String=game.wrecks[cell].kind
	for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		if game.occupied.has(cell+offset) and game._doors_connect(ROOMS[id],0,offset,game.occupied[cell+offset]):return true
	return false

static func toggle(game, cell: Vector2i) -> void:
	if not game.running or not is_site(game,cell):return
	var site: Dictionary=game.wrecks[cell]
	if site.cleared:
		if not site.recovered:
			site.opened=true
			game._log("Two human pods failed. The smaller one is still keeping a promise." if site.kind=="margot" else "%s opened. A machine inside is still answering."%OBJECTS[site.kind],false)
	else:
		if site.active:site.active=false
		elif accessible(game,cell) and not preload("res://scripts/wreck_field.gd").busy(game.wrecks,cell):
			if not site.paid:
				if game.resources.metal<REPAIR_METAL:return
				game.resources.metal-=REPAIR_METAL;site.paid=true
			site.active=true
	game._refresh_all()

static func connect_room(game, cell: Vector2i) -> void:
	var id: String=game.wrecks[cell].kind
	var previous: int=game.selected_rotation
	game.selected_rotation=0
	game._place_room(ROOMS[id],cell,true)
	game.selected_rotation=previous
	game.occupied[cell].display_name=TITLES[id]
	game._log("%s connected. Inspect its %s."%[TITLES[id],OBJECTS[id]],false)

static func boot_status(game, cell: Vector2i) -> String:
	var site: Dictionary=game.wrecks[cell]
	if site.recovered:return "COMPANION ABOARD"
	if not site.cleared:return "REPAIRING HULL" if site.active else "SEALED DERELICT"
	if not site.opened:return "SEALED %s"%OBJECTS[site.kind].to_upper()
	if not game.occupied.has(cell) or game.occupied[cell].get("suspended",false):return "ROOM SUSPENDED"
	if not game.hardware.power or not game.powered_room_cells.has(cell):return "WAITING FOR POWER"
	return "THAWING" if site.kind=="margot" else "RESTARTING"

static func spawn(game, id: String, cell: Vector2i) -> bool:
	var actor = game.companion_actors[id]
	actor.room_cache=game.bill_npc.room_cache
	actor.rebuild(game)
	actor.avoidance_positions.clear()
	for peer in all_actors(game):
		if peer!=actor and peer.active:actor.avoidance_positions.append(peer.foot)
	var nodes: Array=actor.room_nodes.get(cell,[]).duplicate()
	var emergence := (Vector2(cell)+Vector2.ONE*0.5)*384.0+CONTAINER_FOOT+Vector2(0,40)
	nodes.sort_custom(func(a,b):return actor.graph.get_point_position(a).distance_squared_to(emergence)<actor.graph.get_point_position(b).distance_squared_to(emergence))
	for node in nodes:
		var point: Vector2=actor.graph.get_point_position(node)
		if actor.spawn_clear(point):
			actor.foot=point;actor.active=true;actor.arrive()
			if id=="river":actor.start_behavior("boot")
			return true
	return false

static func all_actors(game) -> Array:
	return [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]+game.companion_actors.values()

static func advance(game, delta: float) -> void:
	if not game.running or game.paused or delta<=0:return
	for cell in game.wrecks:
		if not is_site(game,cell) or boot_status(game,cell) not in ["RESTARTING","THAWING"]:continue
		var site: Dictionary=game.wrecks[cell]
		site.boot=minf(BOOT_SECONDS,site.boot+delta)
		if site.boot>=BOOT_SECONDS:
			if not game.meta.unlocked_companion_ids.has(site.kind):
				if not game.meta.unlock_companion(site.kind):continue
				game.run_discovered_character_ids.append(site.kind)
		if site.boot>=BOOT_SECONDS and spawn(game,site.kind,cell):
			site.recovered=true;game.companion_roster[site.kind]=cell
			game._log("COMPANION RECOVERED // %s. Available in future expedition selection."%NAMES[site.kind],false)
			game._refresh_all()
	for id in game.companion_roster:
		var actor = game.companion_actors[id]
		if not actor.active:
			if game.architect_run.get("core",{}).get("recovered",false):spawn(game,id,game.companion_roster[id])
			continue
		actor.avoidance_positions.clear()
		for peer in all_actors(game):
			if peer!=actor and peer.active:actor.avoidance_positions.append(peer.foot)
		actor.hardware_doors_locked=game.hardware.doors
		actor.update(game,delta)

static func inspect(game, cell: Vector2i) -> void:
	var site: Dictionary=game.wrecks[cell]
	var id: String=site.kind
	game.preview_name_label.text=TITLES[id]
	game.preview_tags_label.text="COMPANION RECOVERY // "+OBJECTS[id].to_upper()
	game.preview_texture.texture=portrait(id) if site.opened else null
	game.inspector_focus_button.set_meta("cell",cell);game.inspector_focus_button.disabled=false
	game.inspector_label.text="%s\n\n%s\n\n%s\n\nCompanions keep company with the crew. They do not occupy architect berths or perform construction."%[boot_status(game,cell),"Reconnect matching doors and repair the hull: 8 Metal, 18 seconds. Repair payment and progress persist." if not site.cleared else "Open the %s, then supply room power for an eight-second restart. Progress survives power loss and Save/Continue."%OBJECTS[id],"%s // %d%% restarted"%[NAMES[id],roundi(site.boot/BOOT_SECONDS*100)] if site.opened else "Something was left inside."]
	if id=="margot":
		game.inspector_label.text=game.inspector_label.text.replace("Open the pet cryopod, then supply room power for an eight-second restart.","Start the pet cryopod thaw, then supply room power for eight seconds.").replace("restarted","thawed").replace("Something was left inside.","Two broken human cryopods hold skeletons. A smaller pet pod still has a heartbeat.")
	var button: Button=game.room_operation_button
	button.set_meta("cell",cell)
	button.text="COMPANION ABOARD" if site.recovered else "RESTARTING // %d%%"%roundi(site.boot/BOOT_SECONDS*100) if site.opened else "OPEN "+OBJECTS[id].to_upper() if site.cleared else "PAUSE REPAIR" if site.active else "RESUME REPAIR" if site.paid else "REPAIR & CONNECT // 8 METAL"
	if id=="margot":button.text=button.text.replace("RESTARTING","THAWING").replace("OPEN PET CRYOPOD","THAW PET CRYOPOD")
	button.disabled=not game.running or site.recovered or site.opened or (not site.cleared and not site.active and (not accessible(game,cell) or preload("res://scripts/wreck_field.gd").busy(game.wrecks,cell) or (not site.paid and game.resources.metal<REPAIR_METAL)))
	if site.recovered:
		button.text="RESUME ROOM" if game.occupied[cell].get("suspended",false) else "SUSPEND ROOM"
		button.disabled=not game.running
		game.inspector_label.text+="\n\nRestored room inputs / cycle: %s. Outputs / cycle: %s."%[game._format_cost(game.occupied[cell].consumption),game._format_cost(game.occupied[cell].production)]

static func snapshot(game) -> Dictionary:
	var actors := {}
	for id in game.companion_actors:
		var actor = game.companion_actors[id]
		actors[id]={"npc":actor.snapshot(),"playback":actor.player.snapshot(),"personality":actor.personality_snapshot()}
	return {"version":2,"roster":game.companion_roster.duplicate(),"actors":actors}

static func can_pet(game, from_journal := false) -> bool:
	if not game.running or not game.companion_roster.has("margot"):return false
	if game.paused and not (from_journal and game._journal_is_open() and not game.pause_before_journal):return false
	var actor = game.companion_actors.margot
	return actor.active and actor.water.mode=="dry" and actor.pet_cooldown<=0 and actor.can_stand(actor.foot)

static func pet_margot(game) -> bool:
	if not can_pet(game) or not game.companion_actors.margot.pet():return false
	var cell: Vector2i=game.companion_actors.margot.cell_at(game.companion_actors.margot.foot)
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
	game._log("Margot permits a brief interruption. The purring appears intentional.",false)
	game._refresh_all()
	return true

static func valid_site(site: Dictionary) -> bool:
	for key in ["paid","opened","recovered","active","cleared"]:
		if not site.get(key) is bool:return false
	if not site.get("progress") is float or not is_finite(site.progress) or site.progress<0 or site.progress>18:return false
	if not (site.get("boot") is float) or not is_finite(site.boot) or site.boot<0 or site.boot>BOOT_SECONDS:return false
	if (site.active or site.cleared or site.progress>0) and not site.paid:return false
	if site.opened and not site.cleared:return false
	if site.boot>0 and not site.opened:return false
	return not site.recovered or site.boot==BOOT_SECONDS

static func valid(data: Variant, wrecks: Variant, rooms: Variant) -> bool:
	if not wrecks is Dictionary or not rooms is Array:return false
	for site in wrecks.values():
		if not site is Dictionary or not site.get("kind") is String:return false
	for room in rooms:
		if not room is Dictionary or not room.get("pos") is Vector2i or not room.get("id") is String:return false
	if data==null:
		for site in wrecks.values():
			if IDS.has(site.kind):return false
		return true
	if not data is Dictionary or data.get("version") not in [1,2] or not data.get("roster") is Dictionary or not data.get("actors") is Dictionary:return false
	var expected: Array=["river","josh"] if data.version==1 else IDS
	if data.actors.size()!=expected.size():return false
	var occupied := {}
	for room in rooms:occupied[room.pos]=room.id
	var sites := {}
	for cell in wrecks:
		var site: Dictionary=wrecks[cell]
		if not IDS.has(site.kind):continue
		if not expected.has(site.kind):return false
		if sites.has(site.kind) or not valid_site(site):return false
		sites[site.kind]=cell
		if site.cleared and occupied.get(cell)!=ROOMS[site.kind]:return false
		if site.recovered and data.roster.get(site.kind)!=cell:return false
	for id in data.roster:
		if not expected.has(id) or not data.roster[id] is Vector2i or not occupied.has(data.roster[id]):return false
		if sites.has(id) and not wrecks[sites[id]].recovered:return false
		if not sites.has(id) and data.roster[id]!=Vector2i(20,20):return false
	for id in expected:
		if not data.actors.get(id) is Dictionary:return false
		var record: Dictionary=data.actors[id]
		if not NPC.valid_snapshot(record.get("npc"),false) or not preload("res://scripts/crew_sprite_player.gd").valid_snapshot(record.get("playback")):return false
		if not NPC.valid_personality(record.get("personality"),id):return false
		if record.get("personality") is Dictionary and record.personality.action!="":
			if not record.npc.active or record.npc.state!="idle" or not record.npc.path.is_empty():return false
		if record.npc.active and not data.roster.has(id):return false
		if record.npc.active and not occupied.has(Vector2i(floori(record.npc.foot.x/384.0),floori(record.npc.foot.y/384.0))):return false
		if record.npc.state not in ["idle","walk"] or record.npc.goal not in ["","curiosity"] or record.npc.dead or record.npc.helmet_equipped or not record.npc.expedition.is_empty():return false
	return true

static func restore(game, data: Variant) -> void:
	game.companion_actors.clear();game.companion_roster.clear()
	if data==null:
		for id in IDS:game.companion_actors[id]=NPC.new(id)
		return
	game.companion_roster=data.roster.duplicate()
	for id in IDS:
		var actor = NPC.new(id)
		game.companion_actors[id]=actor
		if not data.actors.has(id):continue # Older robot-only loops do not gain a new rescue site.
		actor.restore_snapshot(game,data.actors[id].npc)
		actor.player.restore_snapshot(data.actors[id].playback)
		actor.restore_personality(data.actors[id].get("personality"))
