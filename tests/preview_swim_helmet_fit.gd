extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
class Review extends Node2D:
	var rows: Array=[]
	func _draw():
		draw_rect(Rect2(0,0,1280,900),Color("1d252a"))
		for r in range(rows.size()):
			for i in range(rows[r].size()):
				var texture: Texture2D=rows[r][i]
				draw_texture_rect(texture,Rect2(Vector2(i*208,r*150),texture.get_size()*1.3),false)
func _init(): call_deferred("run")
func run():
	root.size=Vector2i(1280,900)
	root.content_scale_size=Vector2i(1280,900)
	var review=Review.new();root.add_child(review)
	for direction in ["east","west","south","north"]:
		review.rows=[]
		for actor in ["bill","veld","branforth"]:
			var legacy: bool=actor=="veld" and direction=="north"
			var version="v3" if actor=="branforth" and direction=="north" else "v2"
			var path="res://character/crew-underwater-v1/revisions/%s-swim-%s-%s/"%[actor,direction,version]
			var helmet_path=path+"helmet/manifest.json"
			if legacy:
				path="res://character/crew-underwater-v1/pilot/veld-swim-north/"
				helmet_path="res://character/crew-underwater-v1/equipment/fitting/veld-swim-north/manifest.json"
			var player=Player.new();player.load_manifest(path+"manifest.json")
			var previous=Player.new();previous.load_manifest(helmet_path)
			assert(player.load_equipment_manifest("diving-helmet",helmet_path))
			var runtime=Player.new()
			var grid=preload("res://scripts/grid_canvas.gd").new()
			grid._load_water_pilots(runtime,actor)
			grid.free()
			for i in range(6):
				var fitted: Texture2D=player.equipment_frames["diving-helmet"]["swim-"+direction][i]
				assert(fitted.get_image().get_data()==runtime.equipment_frames["diving-helmet"]["swim-"+direction][i].get_image().get_data())
				var filename="res://output/helmet-fit-%s-%s-%d.png"%[actor,direction,i]
				fitted.get_image().save_png(filename)
			review.rows.append(previous.frames["swim-"+direction])
			review.rows.append(player.equipment_frames["diving-helmet"]["swim-"+direction])
		review.queue_redraw()
		for i in range(3): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/swim-helmet-fit-"+direction+".png")
	print("SWIM HELMET FIT PREVIEW PASS")
	quit()
