extends "res://character/brine-smooth-v8-2026-09-26/preview_room.gd"

func draw_nameplate(prop: Dictionary) -> void:
	# Ink follows the existing curved collar; retain its material and shading.
	var font:=preload("res://scripts/ui_fonts.gd").interface_medium()
	var text:="BRINE"
	var font_size:=8
	var spacing:=0.45
	var width:=font.get_string_size(text,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size).x+spacing*4.0
	var cursor:=-width*0.5
	var source_scale: float=prop.rect.size.x/prop.registration.width
	for letter in text:
		var advance:=font.get_string_size(letter,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size).x
		var center:=cursor+advance*0.5
		var source_x:=center/source_scale
		var baseline:=life_point(prop,Vector2(570.0+source_x,537.0+0.22*source_x-0.0025*source_x*source_x))
		painter.draw_set_transform(baseline,atan(0.22-0.005*source_x),Vector2.ONE)
		painter.draw_string(font,Vector2(-advance*0.5,0),letter,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size,Color("364b4a"))
		cursor+=advance+spacing
		painter.draw_set_transform(Vector2.ZERO)
