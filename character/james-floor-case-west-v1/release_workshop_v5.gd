extends "res://character/james-floor-case-west-v1/release_workshop.gd"
func _ready()->void:
	super._ready()
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image,"res://character/james-floor-case-west-v1/floor-case-west-v5.png")
	case_texture=ImageTexture.create_from_image(image)
