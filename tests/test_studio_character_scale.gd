extends SceneTree
## Studio's Characters & Companions preview (owner, Sept 27): one row per cast member with an
## activity picker; several members share a room at gameplay scale; never saved as furniture.
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Prefs=preload("res://scripts/room_studio_prefs.gd")
const Actor=preload("res://scripts/room_scale_preview.gd")
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
	check(editor.cast_rows.size()==Actor.CAST.size(),"One row per character and companion")
	for row in editor.cast_rows:
		check(row.item_count==5 and row.get_item_text(0)=="Hidden" and row.get_item_text(4)=="Interacting","Rows offer Hidden / Walking / Running / Swimming / Interacting")
	var bill=editor.scale_actor.actors[0]
	var sample_count:=0
	for id in ["brine_core","med_bay","crew_hab","corner"]:
		for i in range(editor.entries.size()):
			if str(editor.entries[i].room)==id: editor.switch_room(i); break
		for q in range(4):
			editor.switch_rotation(q)
			var before: Dictionary=editor.draft.duplicate(true)
			editor.set_cast_modes({0:Actor.WALKING})
			editor._process(0.0)
			check(bill.visible,"Standing space in %s q%d"%[id,q])
			check(bill.can_stand(bill.foot),"Preview starts on clear floor")
			var members: Array=editor.scale_actor.members()
			check(members.size()==1 and float(members[0].texture.get_meta("crew_standing_height"))==148.0,"Current Bill uses gameplay standing-height registration")
			var travelled:=0.0
			for step in range(160):
				var prior: Vector2=bill.foot
				editor._process(0.1)
				check(bill.segment_clear(prior,bill.foot),"Walking clearance %s q%d step%d: %s -> %s"%[id,q,step,prior,bill.foot])
				travelled+=prior.distance_to(bill.foot)
				sample_count+=1
			check(travelled>40,"Walking covers clear floor in %s q%d"%[id,q])
			check(editor.draft==before and not editor.dirty,"Preview never changes furnishing data")
			if q==0:
				await process_frame; await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(OUT+id+"-walking.png")
	# Several members at once, each doing something different; still preview only.
	var before: Dictionary=editor.draft.duplicate(true)
	editor.set_cast_modes({0:Actor.WALKING,1:Actor.RUNNING,3:Actor.SWIMMING,4:Actor.WALKING,5:Actor.INTERACTING,6:Actor.INTERACTING})
	for step in range(30): editor._process(0.1)
	check(editor.scale_actor.members().size()==6,"Six members share the room: %d"%editor.scale_actor.members().size())
	check(editor.draft==before,"The cast never changes the draft")
	await process_frame; await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"cast-mixed.png")
	editor.set_cast_modes({})
	check(editor.scale_actor.members().is_empty(),"Hidden removes the preview")
	root.size=Vector2i(960,720)
	await process_frame; await process_frame; await RenderingServer.frame_post_draw
	check(editor.cast_rows.back().get_global_rect().end.x<=editor.size.x,"Cast rows fit a compact viewport")
	root.get_texture().get_image().save_png(OUT+"controls-960.png")
	# The toolbar switch, and view options kept across rotations, rooms and reopening
	# (owner playtest). Only this fixture's own settings file is written.
	var prefs_file:=OUT+"studio-prefs-%d.cfg"%OS.get_process_id()
	Prefs.path=prefs_file
	editor.show_character.button_pressed=true
	check(editor.scale_actor.mode_of(0)==Actor.WALKING and not editor.scale_actor.members().is_empty(),"Show characters walks Bill in the room")
	editor.pref_controls.clean.button_pressed=true
	editor.pref_controls.snap.button_pressed=false
	editor.zoom_slider.value=1.3
	editor.switch_rotation(editor.quarter+1)
	editor.switch_room((editor.index+1)%editor.entries.size())
	editor._process(0.0)
	check(editor.show_character.button_pressed and editor.scale_actor.mode_of(0)==Actor.WALKING and not editor.scale_actor.members().is_empty(),"Character stays shown in the next room and rotation")
	check(editor.clean_preview and not editor.snap.button_pressed and is_equal_approx(editor.zoom,1.3),"Options survive room and rotation changes")
	editor.dirty=false; editor.rotation_drafts.clear(); editor.close_editor()
	await process_frame
	Prefs.session.clear()
	editor=Editor.open(root)
	await process_frame
	editor.set_process(false)
	editor.autosave_enabled=false
	check(editor.show_character.button_pressed and editor.scale_actor.mode_of(0)==Actor.WALKING and editor.pref_controls.clean.button_pressed and not editor.snap.button_pressed and is_equal_approx(editor.zoom_slider.value,1.3),"Options and the cast come back from the settings file when the Studio reopens")
	editor.show_character.button_pressed=false
	check(not editor.scale_actor.any_shown() and editor.scale_actor.members().is_empty(),"Unticking hides the cast")
	editor.dirty=false; editor.rotation_drafts.clear(); editor.close_editor()
	await process_frame
	Prefs.path=""; Prefs.session.clear()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(prefs_file))
	print("STUDIO CHARACTER SCALE: %s / %d clear walking samples"%["PASS" if failures==0 else str(failures)+" failures",sample_count])
	quit(0 if failures==0 else 1)
