extends SceneTree
const PACK := "res://assets/environment/seabed-v1/"
class Sheet extends Control:
	var entries: Array = []
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("0b1d25"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(25,34),"BRINE / SEABED ASSET LIBRARY",HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color("85c5ba"))
		for i in range(entries.size()):
			var entry: Dictionary = entries[i]
			var at := Vector2(20+(i%5)*316,58+floori(i/5.0)*338)
			draw_rect(Rect2(at,Vector2(302,324)),Color("17313b"))
			var native: Vector2 = entry.texture.get_size()
			var display := native * minf(288.0/native.x,288.0/native.y)
			draw_texture_rect(entry.texture,Rect2(at+Vector2(7,4)+(Vector2(288,288)-display)*0.5,display),false)
			draw_string(font,at+Vector2(9,312),entry.id,HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color("d4e4e0"))

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK+"manifest.json"))
	var sheet := Sheet.new()
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,58+ceili(manifest.assets.size()/5.0)*338)
	sheet.size = root.size
	for asset in manifest.assets:
		var image := Image.new()
		assert(image.load(PACK+asset.selected_source)==OK)
		sheet.entries.append({"id":asset.id,"texture":ImageTexture.create_from_image(image)})
	root.add_child(sheet)
	for i in range(4):
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/seabed-v1/asset-sheet.png")
	print("SEABED SHEET: %d assets rendered" % sheet.entries.size())
	quit()
