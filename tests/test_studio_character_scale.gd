extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const OUT="res://output/gameplay-studio-20260912/"
var failures:=0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures+=1; push_error(message)
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	Store.path=OUT+"layouts-%d.json"%OS.get_process_id(); Store.loaded=true; Store.data={}
	Store.defaults_path=OUT+"defaults.json"
	root.size=Vector2i(1600,900)
	var editor=Editor.open(root)
	await process_frame
	editor.set_process(false)
	editor.autosave_enabled=false
	check(editor.character_mode.item_count==3,"Studio offers hidden, standing and walking")
	var sample_count:=0
	for id in ["brine_core","med_bay","crew_hab","corner"]:
		for i in range(editor.entries.size()):
			if str(editor.entries[i].room)==id: editor.switch_room(i); break
		for q in range(4):
			editor.switch_rotation(q)
			var before: Dictionary=editor.draft.duplicate(true)
			editor.character_mode.select(1); editor.character_mode.item_selected.emit(1)
			editor._process(0.0)
			check(editor.scale_actor.visible,"Standing space in %s q%d"%[id,q])
			check(editor.scale_actor.can_stand(editor.scale_actor.foot),"Preview starts on clear floor")
			var members: Array=editor.scale_actor.members()
			check(members.size()==1 and float(members[0].texture.get_meta("crew_standing_height"))==148.0,"Current Bill uses gameplay standing-height registration")
			if q==0:
				await process_frame; await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(OUT+id+"-standing.png")
			editor.character_mode.select(2); editor.character_mode.item_selected.emit(2)
			var start: Vector2=editor.scale_actor.foot
			var travelled:=0.0
			for step in range(160):
				var prior: Vector2=editor.scale_actor.foot
				editor._process(0.1)
				check(editor.scale_actor.segment_clear(prior,editor.scale_actor.foot),"Walking clearance %s q%d step%d: %s -> %s"%[id,q,step,prior,editor.scale_actor.foot])
				travelled+=prior.distance_to(editor.scale_actor.foot)
				sample_count+=1
			check(travelled>40,"Walking covers clear floor in %s q%d"%[id,q])
			check(editor.draft==before and not editor.dirty,"Preview never changes furnishing data")
			if q==0:
				await process_frame; await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(OUT+id+"-walking.png")
	# Place is a preview action, not an authoring transaction.
	editor.character_place.pressed.emit()
	var before: Dictionary=editor.draft.duplicate(true)
	var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true
	press.position=editor.canvas.origin()+editor.scale_actor.foot*editor.canvas.factor()
	editor.canvas_input(press)
	check(not editor.placing_character and editor.draft==before,"Place character leaves draft untouched")
	editor.character_mode.select(0); editor.character_mode.item_selected.emit(0)
	check(editor.scale_actor.members().is_empty(),"Hidden removes the preview")
	root.size=Vector2i(960,720)
	await process_frame; await process_frame; await RenderingServer.frame_post_draw
	check(editor.character_place.get_global_rect().end.x<=editor.size.x,"Scale controls fit compact viewport")
	root.get_texture().get_image().save_png(OUT+"controls-960.png")
	editor.dirty=false; editor.rotation_drafts.clear(); editor.close_editor()
	await process_frame
	print("STUDIO CHARACTER SCALE: %s / %d clear walking samples"%["PASS" if failures==0 else str(failures)+" failures",sample_count])
	quit(0 if failures==0 else 1)
