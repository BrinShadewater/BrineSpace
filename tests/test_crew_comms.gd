extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	DirAccess.make_dir_recursive_absolute("res://output/crew-comms")
	var comms=preload("res://scripts/crew_comms.gd").new(); root.add_child(comms)
	assert(not comms.transmit("unknown","Rejected"))
	for width in [1600,960]:
		root.size=Vector2i(width,roundi(width*9.0/16.0)); root.content_scale_size=root.size
		for id in ["bill","veld","branforth"]:
			comms.dismiss()
			assert(comms.transmit(id,"The channel is clear. I can read the instruments from here. Keep the pressure steady; I would rather finish this report without seawater in it.",id+str(width)))
			assert(not comms.transmit(id,"Duplicate",id+str(width)))
			comms.show_next(); comms.advance()
			for i in range(3): await process_frame
			await RenderingServer.frame_post_draw
			assert(comms.portrait.texture.get_width()==256)
			assert(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(comms.panel.get_global_rect()),"Panel fits viewport")
			assert(comms.body.visible_characters==comms.body.get_total_character_count())
			root.get_texture().get_image().save_png("res://output/crew-comms/%s-%d.png"%[id,width])
	comms.dismiss(); comms.reopen(); assert(comms.panel.visible)
	comms.dismiss(); assert(not comms.panel.visible and comms.pending.is_empty())
	print("CREW COMMS PASS: three native portraits, two sizes, reveal, deduplication, close and replay")
	quit()
