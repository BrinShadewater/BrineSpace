extends SceneTree
const Atmosphere=preload("res://scripts/screen_atmosphere.gd")
class Station extends RefCounted:
	var GRID_SIZE:=40
	var occupied:Dictionary={}
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var game:=Station.new()
	var effect=Atmosphere.new(game)
	effect.mask_image=Image.create(40,40,false,Image.FORMAT_RGBA8)
	effect.mask_texture=ImageTexture.create_from_image(effect.mask_image)
	effect._update_mask()
	game.occupied[Vector2i(20,17)]={"id":"corridor"}
	effect._update_mask()
	check(effect.mask_image.get_pixel(20,17).r==1.0,"Room mask updates on the first call after placement")
	game.occupied.clear();game.occupied[Vector2i(21,17)]={"id":"corridor"}
	effect._update_mask()
	check(effect.mask_image.get_pixel(20,17).r==0.0 and effect.mask_image.get_pixel(21,17).r==1.0,"Same-count moved footprint invalidates mask")
	game.occupied.clear()
	effect._update_mask()
	check(effect.mask_image.get_pixel(21,17).r==0.0,"Removal updates immediately")
	var uploads=effect.get("mask_uploads")
	for i in range(32):effect._update_mask()
	if uploads!=null:check(effect.mask_uploads==uploads,"Unchanged footprint skips image uploads")
	game.occupied[Vector2i(-1,0)]={};game.occupied[Vector2i(40,40)]={}
	effect._update_mask()
	check(effect.mask_image.get_pixel(0,0).r==0.0,"Out-of-grid occupied cells remain ignored")
	effect.free()
	var result:={"checks":checks,"failures":failures}
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify(result))
	print("ATMOSPHERE MASK ",JSON.stringify(result));quit(1 if failures else 0)
