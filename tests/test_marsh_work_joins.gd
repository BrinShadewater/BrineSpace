extends SceneTree
## Current catalog handoffs, including the padded south torch endpoints.
const Player = preload("res://scripts/crew_sprite_player.gd")
var checks := 0
var failures := 0

func registered(texture: Texture2D) -> PackedByteArray:
	var canvas = Image.create(640,640,false,Image.FORMAT_RGBA8)
	var source = texture.get_image()
	canvas.blit_rect(source,Rect2i(Vector2i.ZERO,source.get_size()),Vector2i(Vector2(320,320)-texture.get_meta("crew_pivot")))
	return canvas.get_data()

func check(a:Texture2D,b:Texture2D,label:String):
	checks+=1
	if registered(a)!=registered(b):failures+=1;push_error(label)

func _init():call_deferred("run")
func run():
	var player=Player.new()
	var path="res://character/marsh-v2/catalog.json"
	var catalog=JSON.parse_string(FileAccess.get_file_as_string(path))
	for relative in catalog.body:player.load_manifest(path.get_base_dir().path_join(str(relative)),true)
	for direction in ["east","west","north","south"]:
		var idle:Texture2D=player.frames["idle-"+direction][0]
		for boundary in [["pickup",0],["unload",-1],["cargo-unload",-1],["torch-draw",0],["torch-stow",-1]]:
			var key:String=str(boundary[0])+"-"+direction
			check(player.frames[key][boundary[1]],idle,"current idle endpoint "+key)
		check(player.frames["torch-draw-"+direction][-1],player.frames["weld-"+direction][0],"draw into welding")
		check(player.frames["weld-"+direction][-1],player.frames["torch-stow-"+direction][0],"welding into stow")
		for slot in range(6):check(player.frames["torch-draw-"+direction][slot],player.frames["torch-stow-"+direction][5-slot],"whole torch reverse "+direction)
	print("MARSH WORK JOINS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
