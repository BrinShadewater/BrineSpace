extends RefCounted
const ORDER := ["veld","branforth","marsh","bill"]
const Architects = preload("res://scripts/architects.gd")
const Generator = preload("res://scripts/site_generator.gd")

static func reveal(game) -> Array:
	var revealed: Array=[]
	if game.site_layout.is_empty(): return revealed
	var cells: Array=[]
	var available: Array=Architects.IDS.duplicate()
	available.erase(game.architect_run.selected)
	for cell in game.wrecks:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind in ["cryo","charging"]:
			for pod in ward.pods: available.erase(pod.architect_id)
		elif ward.kind=="recovery" and game.surveyed_water.has(cell): cells.append(cell)
	if cells.is_empty(): return revealed
	# One dedicated shuffle for the expedition, reconstructed after Continue.
	# Filtering assigned occupants preserves its remainder across survey batches.
	var known_order: Array=Architects.IDS.duplicate()
	var rng:=RandomNumberGenerator.new()
	rng.seed=int(game.site_layout.seed)^0x43c6a7
	for i in range(known_order.size()-1,0,-1):
		var j:=rng.randi_range(0,i)
		var swap=known_order[i];known_order[i]=known_order[j];known_order[j]=swap
	cells.sort_custom(func(a,b):
		var da:=Generator.distance(a);var db:=Generator.distance(b)
		return da<db if da!=db else (a.x<b.x if a.x!=b.x else a.y<b.y))
	for cell in cells:
		if available.is_empty(): break
		var chosen := ""
		for id in ORDER:
			if available.has(id) and not game.meta.sighted_character_ids.has(id) and not game.meta.met_character_ids.has(id) and not game.meta.unlocked_architect_ids.has(id):
				chosen=id;break
		if chosen.is_empty():
			for id in known_order:
				if available.has(id):
					chosen=id;break
		# Persist the introduction before revealing it; a disk failure retries next survey.
		if not game.meta.record_sighting(chosen): break
		var ward: Dictionary=game.wrecks[cell]
		ward.kind="charging" if chosen=="marsh" else "cryo"
		ward["paid"]=false
		ward["pods"]=[Architects.pod(chosen,"architect_"+chosen)]
		available.erase(chosen)
		revealed.append(cell)
	return revealed
