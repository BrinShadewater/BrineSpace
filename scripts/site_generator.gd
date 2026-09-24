extends RefCounted
## New-loop geography only. Dedicated RNG never consumes the deck/simulation stream.
const VERSION := 1
const CORE := Vector2i(20,20)
const DIRECTIONS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
const BANDS := [Vector2i(4,6),Vector2i(7,9),Vector2i(10,12)]
const COMPANIONS := [Vector2i(20,18),Vector2i(22,20),Vector2i(20,22)]

static func distance(a: Vector2i, b: Vector2i = CORE) -> int:
	return absi(a.x-b.x)+absi(a.y-b.y)

static func inside(cell: Vector2i) -> bool:
	return cell.x>=0 and cell.y>=0 and cell.x<40 and cell.y<40

static func obstacle(kind: String) -> Dictionary:
	return {"kind":kind,"progress":0.0,"active":false,"cleared":false}

static func generate(seed_value: int) -> Dictionary:
	var start := Time.get_ticks_usec()
	for attempt in range(32):
		var result := candidate(seed_value,attempt)
		if valid(result):
			result["generation_usec"]=Time.get_ticks_usec()-start
			return result
	# This fixed candidate is exercised by the seed contract, not an unbounded retry.
	var fallback := candidate(20260923,0)
	fallback.seed=seed_value
	fallback["fallback"]=true
	fallback["generation_usec"]=Time.get_ticks_usec()-start
	return fallback

static func reserve_route(reserved: Dictionary, target: Vector2i) -> void:
	var at := CORE
	while at != target:
		reserved[at]=true
		if at.x!=target.x: at.x+=signi(target.x-at.x)
		else: at.y+=signi(target.y-at.y)
	reserved[at]=true

static func candidate(seed_value: int, attempt: int) -> Dictionary:
	var rng := RandomNumberGenerator.new()
	rng.seed=seed_value+attempt*104729
	var reserved := {}
	for x in range(18,23):
		for y in range(18,23): reserved[Vector2i(x,y)]=true
	for cell in COMPANIONS:
		for direction in DIRECTIONS: reserved[cell+direction]=true
	# A cross keeps early bay launches and a turbine intake possible.
	for direction in DIRECTIONS:
		for step in range(1,5): reserved[CORE+direction*step]=true
	var wards: Array = []
	for band in BANDS:
		var choices: Array = []
		for x in range(8,33):
			for y in range(8,33):
				var cell := Vector2i(x,y)
				if distance(cell)<band.x or distance(cell)>band.y or reserved.has(cell): continue
				var separated := true
				for other in wards:
					if distance(cell,other)<5: separated=false
				if separated: choices.append(cell)
		if choices.is_empty(): return {}
		var cell: Vector2i=choices[rng.randi_range(0,choices.size()-1)]
		wards.append(cell)
		# All approaches are open; rotation zero has the canonical N/S doors.
		for direction in DIRECTIONS: reserve_route(reserved,cell+direction)
		reserved[cell]=true
	var wrecks := {}
	for cell in wards:
		wrecks[cell]=obstacle("recovery")
		wrecks[cell]["rotation"]=0
	# Irregular connected masses, never loose random blockers around the core.
	for mass in range(9):
		var at := Vector2i(rng.randi_range(5,34),rng.randi_range(5,34))
		for step in range(rng.randi_range(15,30)):
			if inside(at) and not reserved.has(at): wrecks[at]=obstacle("basalt")
			at+=DIRECTIONS[rng.randi_range(0,3)]
			at=Vector2i(clampi(at.x,2,37),clampi(at.y,2,37))
	var kinds := ["engineering","medical","habitation","hydroponics"]
	for i in range(8):
		var cell := Vector2i(rng.randi_range(8,32),rng.randi_range(8,32))
		if reserved.has(cell) or wrecks.has(cell): continue
		wrecks[cell]=obstacle(kinds[i%4])
	# A buried cache replaces an interior rock, retaining its enclosing formation.
	for cell in wrecks.keys():
		if wrecks[cell].kind!="basalt": continue
		var enclosed := true
		for d in DIRECTIONS:
			if wrecks.get(cell+d,{}).get("kind","")!="basalt": enclosed=false
		if enclosed:
			wrecks[cell]=obstacle("engineering")
			wrecks[cell]["buried"]=true
			break
	var sites := {}
	# Guaranteed accessible first deposits, away from the protected opening/intakes.
	var early := [Vector2i(17,18),Vector2i(23,22)]
	for i in range(early.size()):
		var cell: Vector2i=early[i]
		reserve_route(reserved,cell+Vector2i.LEFT)
		wrecks.erase(cell)
		sites[cell]=preload("res://scripts/harvest_sites.gd").make_site("mining" if i==0 else "salvage")
	for cell in reserved:
		if not wards.has(cell): wrecks.erase(cell)
	for i in range(60):
		if sites.size()>=16: break
		var cell := Vector2i(rng.randi_range(6,34),rng.randi_range(6,34))
		if reserved.has(cell) or wrecks.has(cell) or sites.has(cell): continue
		sites[cell]=preload("res://scripts/harvest_sites.gd").make_site("mining" if sites.size()%2==0 else "salvage")
	var scenery: Array = []
	var rock_anchors: Array=[]
	var debris_anchors: Array=[]
	for cell in wrecks:
		if wrecks[cell].kind=="basalt": rock_anchors.append(cell)
		elif wrecks[cell].kind!="recovery": debris_anchors.append(cell)
	for cell in sites:
		if sites[cell].kind=="salvage": debris_anchors.append(cell)
	var dressed := {}
	for i in range(28):
		# Low stones collect at formation edges; timber follows wreck/debris sites.
		var anchors: Array=rock_anchors if i%4<2 else debris_anchors
		if anchors.is_empty(): continue
		var anchor: Vector2i=anchors[rng.randi_range(0,anchors.size()-1)]
		var cell: Vector2i=anchor+DIRECTIONS[rng.randi_range(0,3)]
		if not inside(cell) or distance(cell)<4 or wrecks.has(cell) or sites.has(cell) or COMPANIONS.has(cell) or dressed.has(cell): continue
		dressed[cell]=true
		scenery.append({"at":Vector2(cell)+Vector2(.5,.5),"family":i%4,"size":rng.randf_range(.20,.38) if i%4<2 else rng.randf_range(.35,.55)})
	var habitats: Array=[]
	var biome_ids := ["sulfur","sponge","brine","kelp","coral","nodules","iron"]
	var phase := rng.randf()*TAU
	for i in range(biome_ids.size()):
		var angle := phase+TAU*float(i)/7.0
		var center := Vector2(CORE)+Vector2(cos(angle),sin(angle))*rng.randf_range(8.0,13.0)
		habitats.append({"biome":biome_ids[i],"center":center,"radius":Vector2(rng.randf_range(3.0,5.0),rng.randf_range(3.0,4.5))})
	return {"version":VERSION,"seed":seed_value,"attempt":attempt,"wrecks":wrecks,"sites":sites,"recovery_cells":wards,"scenery":scenery,"reserved":reserved,"habitats":habitats}

static func valid(data: Variant) -> bool:
	if not data is Dictionary or data.get("version")!=VERSION or not data.get("seed") is int: return false
	if not data.get("wrecks") is Dictionary or not data.get("sites") is Dictionary or not data.get("reserved") is Dictionary: return false
	if not data.get("recovery_cells") is Array or data.recovery_cells.size()!=3 or not data.get("scenery") is Array or data.scenery.size()>100: return false
	if not data.get("habitats") is Array or data.habitats.size()!=7: return false
	var biome_ids := ["sulfur","sponge","brine","kelp","coral","nodules","iron"]
	for region in data.habitats:
		if not region is Dictionary or not biome_ids.has(region.get("biome")): return false
		biome_ids.erase(region.biome)
		if not region.get("center") is Vector2 or not region.center.is_finite() or not inside(Vector2i(region.center)): return false
		if not region.get("radius") is Vector2 or not region.radius.is_finite() or region.radius.x<1 or region.radius.y<1 or region.radius.x>6 or region.radius.y>6: return false
	for item in data.scenery:
		if not item is Dictionary or not item.get("at") is Vector2 or not item.at.is_finite() or not inside(Vector2i(item.at)): return false
		if not item.get("family") is int or item.family<0 or item.family>3 or not item.get("size") is float or not is_finite(item.size) or item.size<.1 or item.size>2: return false
	if not preload("res://scripts/wreck_field.gd").valid(data.wrecks,{}): return false
	for cell in data.wrecks:
		if not cell is Vector2i or not inside(cell) or data.sites.has(cell): return false
	for cell in data.sites:
		if not cell is Vector2i or not inside(cell): return false
	for cell in data.reserved:
		if not cell is Vector2i or not inside(cell): return false
	for x in range(19,22):
		for y in range(19,22):
			if data.wrecks.has(Vector2i(x,y)) or data.sites.has(Vector2i(x,y)): return false
	var blocked: Dictionary=data.wrecks.duplicate()
	blocked.merge(data.sites)
	for cell in COMPANIONS: blocked[cell]=true
	var reached := {CORE:true}
	var queue: Array=[CORE]
	var index := 0
	while index<queue.size():
		var cell: Vector2i=queue[index];index+=1
		for d in DIRECTIONS:
			var next: Vector2i=cell+d
			if inside(next) and not blocked.has(next) and not reached.has(next): reached[next]=true;queue.append(next)
	for i in range(3):
		var cell=data.recovery_cells[i]
		if not cell is Vector2i or distance(cell)<BANDS[i].x or distance(cell)>BANDS[i].y: return false
		if data.wrecks.get(cell,{}).get("kind")!="recovery": return false
		if not reached.has(cell+Vector2i.UP) or not reached.has(cell+Vector2i.DOWN): return false
		for j in range(i):
			if distance(cell,data.recovery_cells[j])<5: return false
	for cell in COMPANIONS:
		if data.wrecks.has(cell) or data.sites.has(cell) or not reached.has(cell+Vector2i.UP): return false
	for cell in [Vector2i(17,18),Vector2i(23,22)]:
		if not data.sites.has(cell) or not reached.has(cell+Vector2i.LEFT): return false
	return preload("res://scripts/harvest_sites.gd").valid(data.sites)
