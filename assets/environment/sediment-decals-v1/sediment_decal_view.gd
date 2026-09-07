extends RefCounted
## Static displacement mark, registered beneath mooring debris.
const Mooring := preload("res://assets/environment/mooring-debris-v1/mooring_debris_view.gd")
const ROOT := "res://assets/environment/sediment-decals-v1/"
const SOURCES := {
    "silt-scour": "silt-scour-v2.png"
}
const CENTER := Mooring.CENTER
var textures: Dictionary = {}
func prepare() -> void:
	if not textures.is_empty(): return
	var source := Image.new()
	if source.load(ROOT+SOURCES["silt-scour"])==OK:
		textures["silt-scour"]=ImageTexture.create_from_image(source)
func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	if textures.is_empty(): return
	# Native trial: 90px half-cell prop, 140px decal, (-90,10) from prop top-left.
	var origin := (Mooring.CENTER-Vector2.ONE*0.25+Vector2(-0.5,1.0/18.0))*cell_size
	var size := Vector2.ONE*(7.0/9.0)*cell_size
	canvas.draw_texture_rect(textures["silt-scour"],Rect2(origin,size),false,Color(.49,.58,.57,.30))
