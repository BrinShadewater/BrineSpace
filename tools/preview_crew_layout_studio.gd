extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Actor=preload("res://scripts/room_scale_preview.gd")
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	root.title="BrineSpace — Crew walk preview / copied Layout Studio profile"
	var editor=Editor.open(root)
	editor.autosave_enabled=false
	var matte: bool="matte" in OS.get_cmdline_user_args()
	if matte:
		root.title="BrineSpace — Matte + linear crew / copied Layout Studio"
		var overrides={0:"res://character/crew-matte-studio-v1/bill/manifest.json",2:"res://character/crew-matte-studio-v1/branforth/manifest.json",3:"res://character/crew-matte-studio-v1/veld/manifest.json"}
		for i in overrides:
			var actor=editor.scale_actor.actors[i]
			actor.finish_preview_manifest=overrides[i]
			actor.player.frames.clear();actor.full_art=false
	for i in range(editor.entries.size()):
		if str(editor.entries[i].room)=="research_lab":editor.switch_room(i);break
	editor.set_cast_modes({0:Actor.WALKING,2:Actor.WALKING,3:Actor.WALKING})
	var before: Dictionary=editor.draft.duplicate(true)
	var starts=[]
	for i in [0,2,3]:starts.append(editor.scale_actor.actors[i].foot)
	await create_timer(5.0).timeout
	var moving:=0
	for j in range(3):
		var i: int=[0,2,3][j]
		var actor=editor.scale_actor.actors[i]
		if actor.foot.distance_to(starts[j])>1:moving+=1
		var expected: int={0:30,2:36,3:28}[i]
		assert(actor.player.frames['walk-north'].size()==expected,"Studio must use latest accepted rear walk")
	assert(moving==3,"All three crew move on the copied layout")
	assert(editor.draft==before,"Walking must not change furniture")
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("res://output/crew-layout-studio-preview")
	root.get_texture().get_image().save_png("res://output/crew-layout-studio-preview/preview.png")
	print("CREW STUDIO READY: three moving actors; latest frames; layout unchanged")
	if matte:
		for i in [0,2,3]:
			var texture: Texture2D=editor.scale_actor.actors[i].player.frames['walk-north'][0]
			assert(texture is CanvasTexture and texture.texture_filter==CanvasItem.TEXTURE_FILTER_LINEAR)
		if "verify" in OS.get_cmdline_user_args():
			for room in ["research_lab","med_bay","crew_hab"]:
				for i in range(editor.entries.size()):
					if str(editor.entries[i].room)==room:editor.switch_room(i);break
				for scale_value in [1.25,0.83,0.42]:
					editor.zoom_slider.value=scale_value
					await process_frame;await RenderingServer.frame_post_draw
					root.get_texture().get_image().save_png("res://character/crew-matte-studio-v1/%s-%s.png"%[room,str(scale_value)])
			print("MATTE STUDIO: three rooms x three zooms; character-only linear filtering verified")
	if "verify" in OS.get_cmdline_user_args():quit()
