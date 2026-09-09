extends RefCounted
static func refresh(game) -> void:
	if not is_instance_valid(game.flood_alert_button): return
	var critical := 0
	var rising := 0
	var wet := 0
	var target := Vector2i(-1,-1)
	var worst := -1.0
	var history: Dictionary=game.flood_alert_button.get_meta("levels",{})
	var present := {}
	var announced: Dictionary=game.flood_alert_button.get_meta("stages",{})
	for room in game.placed_rooms:
		var water := float(room.get("water_level",0))
		present[room.pos]=true
		if water>0.001: wet+=1
		if water>=0.85: critical+=1
		var prior: float=history.get(room.pos,water)
		if water>prior+0.0001 or float(room.get("hull_crack",0))>0: rising+=1
		var stage := 3 if water>=0.85 else 2 if water>=0.55 else 1 if water>=0.25 else 0
		var previous_stage: int=announced.get(room.pos,0)
		if game.running and not game.paused and stage>previous_stage:
			game._log("FLOOD %s at %s. %d%% water." % [["LOW","WADING","SWIMMING","CRITICAL"][stage],room.pos,roundi(water*100)],true)
			announced[room.pos]=stage
		elif previous_stage>0 and water < [0.0,0.22,0.52,0.82][previous_stage]: announced[room.pos]=stage
		history[room.pos]=water
		var score := water+ (3.0 if water>=0.85 else 1.0 if float(room.get("hull_crack",0))>0 else 0.0)
		if (water>0.001 or score>=1) and score>worst: worst=score; target=room.pos
	for cell in history.keys():
		if not present.has(cell): history.erase(cell); announced.erase(cell)
	game.flood_alert_button.set_meta("levels",history)
	game.flood_alert_button.set_meta("stages",announced)
	game.flood_alert_button.set_meta("target",target)
	game.flood_alert_button.text="FLOOD / %d CRITICAL / %d LEAKING OR RISING" % [critical,rising] if wet>0 or rising>0 else "FLOOD / CLEAR"
	game.flood_alert_button.modulate=Color("ef987c") if critical>0 else Color("8bc8c3")
	game.flood_alert_button.tooltip_text="%d rooms with water. Click to inspect the most urgent damage." % wet
