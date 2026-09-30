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
	var translucent:=Art.frame_style(Color(.03,.07,.08,.78),Color("#46d3e6"))
	var red_frame:=Art.frame_style(fill,Color("#d9534f")).texture.get_image()
	var blue_frame:=Art.frame_style(fill,Color("#4f8fe6")).texture.get_image()
	expect(red_frame.get_pixel(3,142)==blue_frame.get_pixel(3,142),"Outer metal stays neutral across departments")
	expect(red_frame.get_pixel(7,142)==blue_frame.get_pixel(7,142),"Inset outline leaves a gap beside the metal")
	Art.update_inner_outline(parent,Color("#e6c84f"),true)
	var edge:=parent.get_node("CardInnerOutline")
	expect(edge.z_index==0 and edge.get_index()==parent.get_child_count()-1 and edge.outline.border_width_left==3,"Inner outline is the last child (over the content) without a raised z, so a fan neighbour cannot draw over it")
	Art.update_inner_outline(parent,Color("#46d3e6"),true)
	expect(edge.outline.border_color==Color("#46d3e6"),"Outline follows updated card state color")
	Art.update_inner_outline(parent,Color.WHITE,false)
	expect(not edge.visible,"Flat fallback hides authored inner outline")
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
