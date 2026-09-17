extends RefCounted
## Local machinery heat and compartment fires. Rates are prototype tuning.
const MACHINERY := {"reactor":0.025,"biomass_digester":0.025,"galley":0.02,"salvage_workshop":0.02}
const WARNING := 0.75
const FLOOD_OUT := 0.25
const GROWTH := 0.012
const SUPPRESSION := 0.09
const WATER_SECONDS := 5.0

static func intensity(room: Dictionary) -> float:
	return float(room.get("fire",0.0))

static func burning(room: Dictionary) -> bool:
	return intensity(room)>0.0

static func fault(room: Dictionary) -> bool:
	return bool(room.get("electrical_fault",false)) or float(room.get("fire_heat",0))>=WARNING

static func cycle(game) -> void:
	if not game.running or game.paused: return
	var changed := false
	for room in game.placed_rooms:
		if not MACHINERY.has(room.id) or burning(room): continue
		var before := float(room.get("fire_heat",0))
		var operating: bool=game.hardware.power and game.powered_room_cells.has(room.pos) and not room.get("suspended",false) and float(room.get("water_level",0))<FLOOD_OUT
		if before>=WARNING: room.electrical_fault=true
		room.fire_heat=clampf(before+(float(MACHINERY[room.id]) if operating else -0.2),0,1)
		if room.fire_heat>=1.0-0.000001:
			room.fire=0.12
			room.fire_heat=0.0
			game._log("FIRE // %s at %s. Machinery shut down. Enable sprinklers; check power and water. I would prefer to keep this compartment." % [room.display_name,room.pos],true)
			changed=true
		elif not room.get("electrical_fault",false) and room.fire_heat>=WARNING:
			room.electrical_fault=true
			game._log("ELECTRICAL FAULT // %s at %s. Suspend the room. Crew can repair isolated machinery; continued operation risks ignition." % [room.display_name,room.pos],true)
	if changed: refresh_operation(game)

static func emergency_power(game) -> bool:
	if not game.hardware.power: return false
	if int(game.resources.get("power",0))>0: return true
	for room in game.placed_rooms:
		if game.powered_room_cells.has(room.pos) and not burning(room) and not room.get("suspended",false) and int(room.get("production",{}).get("power",0))>0: return true
	return false

static func spraying(game,room: Dictionary) -> bool:
	return burning(room) and game.hardware.sprinklers and emergency_power(game) and float(room.get("fire_water_seconds",0))>0

static func sprinkler_status(game,room: Dictionary) -> String:
	if not game.hardware.sprinklers: return "OFF"
	if not emergency_power(game): return "NO POWER"
	if int(game.resources.get("water",0))<=0 and float(room.get("fire_water_seconds",0))<=0: return "NO WATER"
	if spraying(game,room): return "SPRAYING"
	return "READY" if burning(room) else "ARMED"

static func refresh_operation(game) -> void:
	var forecast: Dictionary={}
	# Fire changes only the affected compartment's operation. The other rooms
	# already paid for this cycle; a forecast must not revoke their service.
	for room in game.placed_rooms:
		var cell: Vector2i=room.pos
		if burning(room):
			game.powered_room_cells.erase(cell)
			game.offline_reasons[cell]="FIRE"
		elif game.offline_reasons.get(cell,"")=="FIRE":
			# A room that stops burning during this cycle's blackout stays dark with the station.
			var blocked: bool=preload("res://scripts/rare_branch_control.gd").offline(room) or (not game.hardware.get("pumps",true) and int(room.get("production",{}).get("water",0))>0)
			if game.get("power_blackout") == true and not blocked and int(room.get("consumption",{}).get("power",0))>0:
				game.powered_room_cells.erase(cell)
				game.offline_reasons[cell]="POWER BLACKOUT"
				continue
			if forecast.is_empty(): forecast=game._simulate_room_economy(true,game.cycle+1)
			if forecast.working_cells.has(cell):
				game.powered_room_cells[cell]=true
				game.offline_reasons.erase(cell)
			else:
				game.powered_room_cells.erase(cell)
				# Only a real station blackout carries that label (a save reads it back as one).
				var reason: String=str(forecast.offline.get(cell,"OFFLINE"))
				game.offline_reasons[cell]="NEEDS POWER" if reason=="POWER BLACKOUT" else reason
	game.unpowered_room_cells=game.offline_reasons.duplicate()
	game.active_synergy_links=game.DiscoveryManagerScript.functioning_links(game.connected_synergy_links,game.powered_room_cells)
	game._refresh_all()

static func advance(game,delta: float) -> void:
	if not is_finite(delta) or delta<=0 or not game.running or game.paused: return
	# Only cycle() ignites rooms. Keep dictionary references for this update,
	# avoiding a full station scan for every 0.1-second catch-up step.
	var fires: Array=[]
	for room in game.placed_rooms:
		if burning(room): fires.append(room)
	if fires.is_empty(): return
	var changed := false
	var remaining := delta
	while remaining>0.000001:
		var dt := minf(remaining,0.1)
		var powered: bool=game.hardware.sprinklers and emergency_power(game)
		for room in fires:
			if not burning(room): continue
			if float(room.get("water_level",1.0 if room.get("flooded",false) else 0.0))>=FLOOD_OUT:
				extinguish(game,room,"floodwater")
				changed=true
				continue
			var spray_time := 0.0
			if game.hardware.sprinklers and powered:
				var charge := float(room.get("fire_water_seconds",0))
				if charge<dt and int(game.resources.get("water",0))>0:
					game.resources.water-=1
					charge+=WATER_SECONDS
					signal_water_changed(game)
					signal_water_shortage(game,room,false)
				elif charge<=0 and int(game.resources.get("water",0))<=0:
					signal_water_shortage(game,room,true)
				spray_time=minf(dt,charge)
				room.fire_water_seconds=maxf(0,charge-spray_time)
			room.fire=clampf(intensity(room)+GROWTH*dt-SUPPRESSION*spray_time,0,1)
			# Scorching compromises the hull; the existing paid weld job repairs it.
			room.hull_cause="fire damage"
			room.hull_crack=minf(1,float(room.get("hull_crack",0))+intensity(room)*0.0015*dt)
			if not burning(room):
				extinguish(game,room,"sprinklers")
				changed=true
		remaining-=dt
	if changed: refresh_operation(game)

static func signal_water_changed(game) -> void:
	game._refresh_resources()

static func signal_water_shortage(game,room: Dictionary,empty: bool) -> void:
	if empty and not room.get("fire_water_warning",false):
		game._log("FIRE // Sprinklers at %s have exhausted stored water." % room.pos,true)
	room.fire_water_warning=empty

static func extinguish(game,room: Dictionary,cause: String) -> void:
	# Sprinklers that were spraying keep visibly spraying a few seconds as the flood puts the fire
	# out, instead of cutting off the moment water reaches wading depth (owner playtest).
	if cause=="floodwater" and sprinkler_status(game,room)=="SPRAYING": room["spray_visual_until"]=game.get_visual_time_seconds()+3.0
	room.fire=0.0
	room.fire_heat=0.0
	room.electrical_fault=false
	room.electrical_repair_progress=0.0
	room.erase("fire_water_warning")
	game._log("FIRE OUT // %s at %s, suppressed by %s. Inspect the hull before calling it fortunate." % [room.display_name,room.pos,cause],true)

static func inspector(game,room: Dictionary) -> String:
	if burning(room):
		var status := sprinkler_status(game,room)
		return "[color=#ef987c]FIRE %d%% // PRODUCTION HALTED[/color]\nSprinklers: %s / 1 Water per 5s per burning room.\nFloodwater at 25%% extinguishes fire. Crew seek refuge.\n[url=fire-sprinklers]Enable station sprinklers[/url]" % [ceili(intensity(room)*100),status]
	if fault(room):
		return "[color=#a7dfff]ELECTRICAL FAULT // HEAT %d%%[/color]\n%s\nCrew repair isolated, dry machinery in 8 seconds. Repair %d%%. Resume manually after repair." % [roundi(float(room.get("fire_heat",0))*100),"ISOLATED / waiting for reachable crew" if room.get("suspended",false) else "Suspend this room to stop escalation and allow repair. Ignition at 100% heat.",roundi(float(room.get("electrical_repair_progress",0))/8.0*100)]
	if MACHINERY.has(room.id):
		return "MACHINERY HEAT %d%% // %s\nHeat rises each functioning cycle; suspension cools 20%% per cycle. Ignition at 100%%." % [roundi(float(room.get("fire_heat",0))*100),"FAULT WARNING / SUSPEND TO COOL" if float(room.get("fire_heat",0))>=WARNING else "STABLE"]
	return ""

static func valid_rooms(rooms: Array) -> bool:
	for room in rooms:
		if not room is Dictionary: return false
		for key in ["fire","fire_heat","fire_water_seconds","electrical_repair_progress"]:
			if not room.has(key): continue
			if not (room[key] is float or room[key] is int): return false
			if not is_finite(float(room[key])) or room[key]<0 or room[key]>(WATER_SECONDS if key=="fire_water_seconds" else 8.0 if key=="electrical_repair_progress" else 1.0): return false
		if room.has("electrical_fault") and not room.electrical_fault is bool: return false
		if room.has("fire_water_warning") and not room.fire_water_warning is bool: return false
	return true

static func refresh_alert(game) -> void:
	if not is_instance_valid(game.fire_alert_button): return
	var count := 0
	var warnings := 0
	var target := Vector2i(-1,-1)
	var worst := -1.0
	for room in game.placed_rooms:
		var score := intensity(room)+2 if burning(room) else float(room.get("fire_heat",0))
		if burning(room): count+=1
		elif fault(room): warnings+=1
		else: continue
		if score>worst: worst=score;target=room.pos
	game.fire_alert_button.visible=count>0 or warnings>0
	game.fire_alert_button.text="FIRE / %d BURNING / %d ELECTRICAL FAULTS" % [count,warnings]
	game.fire_alert_button.set_meta("target",target)
	game.fire_alert_button.tooltip_text="Inspect the most urgent fire or machinery heat fault."

static func draw(canvas,game,rooms: Array,size: float) -> void:
	if preload("res://scripts/fire_effects.gd").draw(canvas,game,rooms,size): return
	var time: float=game.get_visual_time_seconds()
	for room in rooms:
		if not burning(room): continue
		var heat := intensity(room)
		var origin: Vector2=(Vector2(room.pos)+Vector2(0.5,0.40))*size
		var pixel := maxf(1,size*0.0035)
		for i in range(7):
			var base := origin+Vector2((i-3)*0.036,sin(i*2.7)*0.016)*size
			base=(base/pixel).floor()*pixel
			var clock := floorf(time*8.0)
			var height := 14+roundi(heat*12)+roundi(sin(clock*.73+i*2.1)*3)
			for row in range(height):
				var rise := float(row)/height
				var bend := sin(rise*4+clock*.32+i)*rise*2.4
				var width := (1-rise)*4.4+sin(rise*PI)*1.2
				for col in range(-6,7):
					var edge := absf(col-bend)/maxf(width,.1)
					if edge>1: continue
					var color := Color("9e3d26")
					if edge<.80: color=Color("cb632e")
					if edge<.53 and rise<.72: color=Color("e99443")
					if edge<.31 and rise<.40: color=Color("f1c577")
					if edge<.18 and rise<.16: color=Color("f3dfaf")
					canvas.draw_rect(Rect2(base+Vector2(col,-row)*pixel,Vector2.ONE*pixel),color)
			var drift := fposmod(time*.28+i*.173,1)
			var smoke := base+Vector2(sin(time*.7+i)*size*.025,-height*pixel-drift*size*.12)
			smoke=(smoke/pixel).floor()*pixel
			var breadth := pixel*(3+floorf(drift*5))
			canvas.draw_rect(Rect2(smoke,Vector2(breadth*1.5,breadth)),Color(.17,.18,.18,(1-drift)*.42))
			canvas.draw_rect(Rect2(smoke+Vector2(pixel,-pixel),Vector2(breadth,breadth+pixel*2)),Color(.22,.23,.22,(1-drift)*.25))
