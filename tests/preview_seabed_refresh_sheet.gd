extends SceneTree
class Sheet extends Node2D:
	var view=preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
	func _draw():
		draw_rect(Rect2(0,0,1100,700),Color("17292d"))
		for row in range(3):
			var id: String=["basalt-outcrop","wreck-timbers","ribbon-kelp"][row]
			draw_string(ThemeDB.fallback_font,Vector2(20,35+row*220),id, HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
			for col in range(4):
				var center:=Vector2(145+col*265,130+row*220)
				var bg: Color=[Color("8b9a91"),Color("233b41")][col%2]
				draw_rect(Rect2(center-Vector2(120,85),Vector2(240,170)),bg)
				var tint: Color=Color.WHITE if col<2 else (Color(.59,.68,.66,.85) if row==2 else Color(.65,.76,.75,.9))
				var width: float=95.0 if row<2 else 120.0
				view.draw_asset(self,id,center,width,tint)
				draw_string(ThemeDB.fallback_font,center+Vector2(-100,78),"source" if col<2 else "runtime tint",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init():call_deferred("run")
func run():
	root.content_scale_size=Vector2i(1100,700)
	root.size=Vector2i(1100,700)
	var sheet:=Sheet.new()
	sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(sheet)
	await process_frame
	RenderingServer.force_draw(false)
	sheet.view.prepare()
	for id in sheet.view.SOURCES:
		assert(sheet.view.textures[id]!=null and sheet.view.textures[id].get_width()==512)
	var habitat=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd").new()
	habitat.prepare()
	assert(habitat.textures["kelp-ribbon-kelp"].get_width()==512)
	assert(preload("res://scripts/site_scenery.gd").REPLACEMENTS["uw1-188"]=="basalt-outcrop")
	assert(preload("res://scripts/site_scenery.gd").REPLACEMENTS["mat-130"]=="wreck-timbers")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	root.get_texture().get_image().save_png("res://assets/environment/seabed-refresh-v1/review/native-density-v2.png")
	print("SEABED REFRESH: 3 textures, habitat binding and 2 scenery bindings checked; 0 failures")
	quit()
