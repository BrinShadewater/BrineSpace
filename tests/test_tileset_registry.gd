extends SceneTree
## The tileset registry against its contract, on the sheets themselves. Headless:
## it reads PNG bytes and JSON, draws nothing. This is the check that caught a sweep
## cutting into five props the owner had kept; here it runs in the default lane.
## The contract is written up in
## skills/brinespace-room-pipeline/references/tileset-library.md.
const LIB:="res://rooms/tileset-library/"
const OPAQUE:=24.0/255.0
const CATEGORIES:=["Seating & tables","Storage","Screens & computers","Lab & science","Plants & growing",
	"Power & reactor","Industrial & workshop","Water & marine","Medical","Food & kitchen","Mining",
	"Military & security","Ship interior","Offworld surface","Shelter & survival","Derelict & damaged"]

func _init() -> void: call_deferred("run")

func fail(problems: Array) -> void:
	for line in problems.slice(0,20): push_error("TILESET REGISTRY: "+str(line))
	push_error("TILESET REGISTRY FAIL: %d problem(s)" % problems.size()); quit(1)

func edge_has_art(image: Image, x0: int, y0: int, x1: int, y1: int) -> bool:
	for y in range(y0,y1):
		for x in range(x0,x1):
			if image.get_pixel(x,y).a>=OPAQUE: return true
	return false

func run() -> void:
	var props: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+"props.json"))
	if not props is Array or props.is_empty(): return fail(["props.json is missing or empty"])
	var problems: Array=[]
	var sheets: Dictionary={}
	var ids: Dictionary={}
	var labels: Dictionary={}
	for e in props:
		var who:="%s (%s)" % [e.get("id","?"),e.get("label","?")]
		if ids.has(e.id): problems.append(who+": duplicate id")
		ids[e.id]=true
		if labels.has(e.label): problems.append(who+": label already used by "+str(labels[e.label]))
		labels[e.label]=e.id
		var bits: PackedStringArray=str(e.label).rsplit(" ",true,1)
		if bits.size()!=2 or not bits[1].is_valid_int(): problems.append(who+": label is not '<Kind> NNN'")
		if not str(e.get("category","")) in CATEGORIES: problems.append(who+": unknown category "+str(e.get("category")))
		if str(e.get("tileset","")).is_empty(): problems.append(who+": no set name")
		if e.has("title") and str(e.title).strip_edges().is_empty(): problems.append(who+": empty title")
		var source: String=str(e.source)
		if not sheets.has(source):
			var image:=Image.new()
			sheets[source]=image if FileAccess.file_exists(source) and image.load_png_from_buffer(FileAccess.get_file_as_bytes(source))==OK else null
		var sheet: Image=sheets[source]
		if sheet==null: problems.append(who+": sheet missing or unreadable: "+source); continue
		var x:=int(e.region[0]); var y:=int(e.region[1]); var w:=int(e.region[2]); var h:=int(e.region[3])
		if w<=0 or h<=0 or x<0 or y<0 or x+w>sheet.get_width() or y+h>sheet.get_height():
			problems.append(who+": region outside its sheet"); continue
		# trimmed to its art: each edge of the box touches an opaque pixel
		if not (edge_has_art(sheet,x,y,x+w,y+1) and edge_has_art(sheet,x,y+h-1,x+w,y+h) and edge_has_art(sheet,x,y,x+1,y+h) and edge_has_art(sheet,x+w-1,y,x+w,y+h)):
			problems.append(who+": region is not trimmed to its opaque art (or the art was cut into)")
		# absolute sheet coordinates: the drawer subtracts a pivot of region centre-bottom
		var want: Array=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
		var got: Array=[]
		for point in e.pieces[0]: got.append([int(point[0]),int(point[1])])
		if e.pieces.size()!=1 or got!=want: problems.append(who+": pieces are not the absolute sheet rectangle of the region")
		if absf(float(e.display_width)-float(w))>0.001: problems.append(who+": display_width is not the region width")
		var f: Variant=e.get("footprint")
		if not f is Array or f.size()!=4: problems.append(who+": no floor footprint")
		elif float(f[0])<0 or float(f[1])<0 or float(f[2])<=0 or float(f[3])<=0 or float(f[0])+float(f[2])>1.0001 or float(f[1])+float(f[3])>1.0001:
			problems.append(who+": footprint leaves the rect: "+str(f))
	# the owner's marks and the alias map must point at props that exist
	for name in ["favourites","retired"]:
		var marks: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+name+".json"))
		if marks is Array:
			for key in marks:
				if not ids.has(str(key).trim_prefix("library/tileset-")): problems.append(name+".json names a prop that is not registered: "+str(key))
	for name in ["names","categories"]:
		var marks: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+name+".json"))
		if marks is Dictionary:
			for key in marks:
				if not ids.has(str(key).trim_prefix("library/tileset-")): problems.append(name+".json names a prop that is not registered: "+str(key))
				if name=="categories" and not str(marks[key]) in CATEGORIES: problems.append("categories.json moves %s to an unknown category %s" % [key,marks[key]])
	var removed: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+"removed.json"))
	if removed is Dictionary:
		for key in removed:
			if ids.has(key): problems.append("removed.json lists a prop that is still registered: "+str(key))
	var variants: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+"variants.json"))
	if variants is Dictionary:
		var seen_in_family: Dictionary={}
		for family in variants.get("groups",[]):
			if family.size()<2: problems.append("variants.json has a family of one: "+str(family))
			for member in family:
				if not ids.has(str(member)): problems.append("variants.json names a prop that is not registered: "+str(member))
				if seen_in_family.has(member): problems.append("variants.json lists a prop in two families: "+str(member))
				seen_in_family[member]=true
	var floors: Variant=JSON.parse_string(FileAccess.get_file_as_string(LIB+"floors.json"))
	if floors is Dictionary:
		for caption in floors:
			if not FileAccess.file_exists(str(floors[caption])): problems.append("floors.json: missing texture for "+str(caption))
	if not problems.is_empty(): return fail(problems)
	print("TILESET REGISTRY PASS: %d props on %d sheets meet the registration contract; marks, removals and floors resolve" % [props.size(),sheets.size()])
	quit()
