extends SceneTree
const Effects=preload("res://scripts/station_effects.gd")
const Player=preload("res://scripts/crew_sprite_player.gd")
class Grid:
	var marsh_player
	var selected:Texture2D
	func _get_marsh_frame(_game):return selected
class Fleet:
	var orders:Array=[]
class Game:
	var marsh_npc
	var bill_npc
	var branforth_npc
	var grid_view=Grid.new()
	var drone_fleet=Fleet.new()
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var game=Game.new();game.marsh_npc=preload("res://scripts/marsh_npc.gd").new()
	var player=Player.new();game.grid_view.marsh_player=player
	var path="res://character/marsh-v2/catalog.json"
	for rel in JSON.parse_string(FileAccess.get_file_as_string(path)).body:player.load_manifest(path.get_base_dir().path_join(str(rel)),true)
	for direction in ["east","west","north","south"]:
		game.marsh_npc.direction=direction
		# Select poses out of order: attachment follows the submitted texture.
		for slot in [3,0,5,2,4,1]:
			var texture:Texture2D=player.frames["weld-"+direction][slot];game.grid_view.selected=texture
			var offset:Vector2=Effects.torch_tip_offset(game,game.marsh_npc)
			var pixel:Vector2=offset*float(texture.get_meta("crew_standing_height"))/65.28+Vector2(texture.get_meta("crew_pivot"))
			var image:Image=texture.get_image();var found:=false
			for y in range(maxi(0,int(pixel.y)-2),mini(image.get_height(),int(pixel.y)+3)):
				for x in range(maxi(0,int(pixel.x)-2),mini(image.get_width(),int(pixel.x)+3)):
					var c:Color=image.get_pixel(x,y)
					if Vector2(x+.5,y+.5).distance_to(pixel)<=1.6 and c.a>.8 and c.r>.7 and c.r>c.g*1.1 and c.b<.67:found=true
			check(found,"spark stays at submitted flame "+direction+"/"+str(slot))
	game.marsh_npc.goal="hull-repair"
	check(not Effects.construction_door(game,game.marsh_npc).is_finite(),"repairs retain pose-relative flame contact")
	game.marsh_npc.goal="construction"
	game.drone_fleet.orders=[{"builder":"marsh","work_cell":Vector2i(20,20),"pos":Vector2i(20,21)}]
	check(Effects.construction_door(game,game.marsh_npc)==Vector2(20.5,21)*384.0-Vector2(0,34),"construction keeps owner's doorway contact")
	print("MARSH TORCH ATTACHMENT: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
