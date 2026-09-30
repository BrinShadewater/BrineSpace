extends SceneTree
const Art=preload("res://scripts/card_art.gd")
var failures:=0
var checks:=0
func expect(value: bool,label: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(label)
func _initialize() -> void:call_deferred("run")
func run() -> void:
	for key in Art.PATHS:expect(Art.texture(key)!=null,"Load "+key)
	var fill:=Color("#101a20")
	for color in [Color("#d9534f"),Color("#e6c84f"),Color("#46d3e6")]:
		var style:=Art.frame_style(fill,color)
		expect(style!=null,"Frame style loads")
		if style!=null:
			var centre:=style.texture.get_image().get_pixel(100,142)
			expect(absf(centre.r-fill.r)<.004 and absf(centre.g-fill.g)<.004 and absf(centre.b-fill.b)<.004,"Inner stock stays neutral across departments")
			expect(style.content_margin_left==8 and style.content_margin_right==8 and style.content_margin_top==8 and style.content_margin_bottom==7,"Content margins retained")
	var parent:=Control.new();root.add_child(parent)
	Art.add_mark(parent,"Operations",Vector2(5,2),Vector2(16,16),Color.WHITE,"TestEmblem")
	Art.add_mark(parent,"common",Vector2(-15,2),Vector2(12,12),Color.WHITE,"TestRarity")
	expect(parent.get_node("TestEmblem").size==Vector2(16,16),"Emblem uses 16px, not source minimum size")
	expect(parent.get_node("TestRarity").size==Vector2(12,12),"Rarity uses 12px, not source minimum size")
	var saved:=Art.textures.duplicate();Art.textures["frame"]=null
	expect(Art.frame_style(fill,Color.WHITE)==null,"Unavailable frame selects existing flat fallback")
	Art.textures=saved;Art.enabled=false
	expect(Art.texture("back")==null,"Reference back uses existing procedural renderer")
	Art.enabled=true
	parent.queue_free();await process_frame
	print("CARD ART: checks=",checks," failures=",failures)
	quit(1 if failures else 0)
