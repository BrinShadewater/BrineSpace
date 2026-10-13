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
			expect(style.content_margin_left==12 and style.content_margin_right==12 and style.content_margin_top==10 and style.content_margin_bottom==10,"Content margins retained")
	var parent:=Control.new();root.add_child(parent)
	Art.add_mark(parent,"Operations",Vector2(5,2),Vector2(16,16),Color.WHITE,"TestEmblem")
	Art.add_mark(parent,"common",Vector2(-15,2),Vector2(12,12),Color.WHITE,"TestRarity")
	expect(parent.get_node("TestEmblem").size==Vector2(16,16),"Emblem uses 16px, not source minimum size")
	expect(parent.get_node("TestRarity").size==Vector2(12,12),"Rarity uses 12px, not source minimum size")
	var translucent:=Art.frame_style(Color(.03,.07,.08,.78),Color("#46d3e6"))
	var red_frame:=Art.frame_style(fill,Color("#d9534f")).texture.get_image()
	var blue_frame:=Art.frame_style(fill,Color("#4f8fe6")).texture.get_image()
	expect(red_frame.get_pixel(3,142)==blue_frame.get_pixel(3,142),"Outer metal stays neutral across departments")
	expect(red_frame.get_pixel(7,142)!=blue_frame.get_pixel(7,142),"Department backing shows through the gap inside the metal")
	expect(red_frame.get_pixel(4,142)==blue_frame.get_pixel(4,142),"Opaque authored metal covers colored backing")
	var source := Art.texture("frame").get_image()
	var opaque_corners := 0
	for y in range(16):
		for x in range(16):
			if source.get_pixel(x,y).a == 1.0 and red_frame.get_pixel(x,y).a > .99:
				if red_frame.get_pixel(x,y) != blue_frame.get_pixel(x,y): push_error("Metal corner overwritten by department border"); failures += 1
				opaque_corners += 1
	expect(opaque_corners > 0,"Corner plates tested above department backing")
	expect(translucent.texture.get_image().get_pixel(3,142).a>.99,"Frame trim stays opaque over translucent stock")
	expect(absf(translucent.texture.get_image().get_pixel(100,142).a-.78)<.004,"Inner stock retains its state opacity")
	var saved:=Art.textures.duplicate();Art.textures["frame"]=null
	expect(Art.frame_style(fill,Color.WHITE)==null,"Unavailable frame selects existing flat fallback")
	Art.textures=saved;Art.enabled=false
	expect(Art.texture("back")==null,"Reference back uses existing procedural renderer")
	Art.enabled=true
	parent.queue_free();await process_frame
	print("CARD ART: checks=",checks," failures=",failures)
	quit(1 if failures else 0)
