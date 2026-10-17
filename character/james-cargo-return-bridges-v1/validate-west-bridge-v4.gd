extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest(OUT+"bare-manifest-v4.json",true)
	if not player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest-v4.json"):quit(2);return
	var checks:=0
	for mode in ["bare","helmet"]:
		var gear:String="" if mode=="bare" else "diving-helmet"
		for i in range(3):
			var texture:Texture2D=player.frame_at_elapsed("carry-settle-west",.08*i+.001,gear)
			var source:=Image.new();source.load(OUT+"frames-v4/"+mode+"/%03d.png"%i);source.convert(Image.FORMAT_RGBA8)
			if texture==null or texture.get_image().get_data()!=source.get_data():push_error("Source-clock binding mismatch");quit(2);return
			checks+=1
			if texture.get_meta("crew_pivot")!=Vector2(128,224) or texture.get_meta("crew_standing_height")!=148:push_error("Source registration mismatch");quit(2);return
			checks+=1
			var bare:=Image.new();var helmet:=Image.new();bare.load(OUT+"frames-v4/bare/%03d.png"%i);helmet.load(OUT+"frames-v4/helmet/%03d.png"%i)
			if bare.get_region(Rect2i(80,110,84,69)).get_data()!=helmet.get_region(Rect2i(80,110,84,69)).get_data():push_error("Paired torso differs");quit(2);return
			checks+=1
	if not FileAccess.file_exists(OUT+"validate-west-bridge-v4.gd.uid"):
		var uid:=FileAccess.open(OUT+"validate-west-bridge-v4.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"native-v4-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":0,"selected":false,"scope":"Staged native player binding of all6paired sources, declared pivot/ruler and rectangular torso equivalence. No world motion, full semantic body/head protection or final join acceptance."},"  "))
	print("JAMES BRIDGE V4 PLAYER: ",checks,"checks; 0failures; unselected")
	quit(0)
