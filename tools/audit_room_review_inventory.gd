extends SceneTree
## Current database/card/ledger reconciliation; no visual approval is inferred.
const Database=preload("res://scripts/room_database.gd")
const Cards=preload("res://scripts/room_card_art.gd")
func _init() -> void:
	var ledger: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://docs/ORGANIC_ROOM_ROLLOUT.json"))
	var covered: Dictionary={}
	for entry in ledger.rooms: covered[entry.id]=true
	var rows: Array=[]
	var errors: Array=[]
	var rooms:=Database.all_rooms()
	for id in rooms:
		var path: String=Cards.PATHS.get(id,"")
		var image:=Image.new()
		var valid:=not path.is_empty() and FileAccess.file_exists(path)
		if valid: valid=image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK
		if not valid: errors.append("Missing or undecodable selected card: "+id)
		if not covered.has(id): errors.append("Room missing from rollout ledger: "+id)
		rows.append({"id":id,"name":rooms[id].display_name,"card":path,"card_sha256":FileAccess.get_sha256(path) if valid else "","width":image.get_width(),"height":image.get_height(),"ledger_present":covered.has(id)})
	for id in covered:
		if not rooms.has(id): errors.append("Ledger room absent from database: "+id)
	print(JSON.stringify({"scope":"Current database identities and selected card bytes; not runtime composition or visual acceptance","rooms":rows,"errors":errors},"\t"))
	quit(0 if errors.is_empty() else 1)
