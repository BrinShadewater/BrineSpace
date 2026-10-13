extends SceneTree
const Main=preload("res://scripts/main.gd")
const Cards=preload("res://scripts/draft_card.gd")
const Settings=preload("res://scripts/title_settings.gd")
var capture_dir:=""
var failures:=0
var checks:=0
class Fixture extends Main:
	func _ready() -> void: pass
	func _refresh_inspector() -> void: pass
	func _gameplay_input_blocked() -> bool: return false
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):capture_dir=arg.trim_prefix("--capture-dir=")
	call_deferred("run")
func check(ok:bool,message:String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func cards(node:Node) -> Array:
	var found:=[]
	for child in node.get_children():
		if child.has_meta("card_id"):found.append(child)
		else:found.append_array(cards(child))
	found.sort_custom(func(a,b):return int(a.get_meta("hand_index"))<int(b.get_meta("hand_index")))
	return found
func geometry(node:Node) -> Array:
	var result:=[]
	if node is Control:
		result.append([node.get_instance_id(),node.position,node.size,node.rotation,node.scale,node.get_combined_minimum_size()])
	for child in node.get_children():result.append_array(geometry(child))
	return result
func settle() -> void:
	var previous:=[]
	for i in range(90):
		await process_frame
		var current:=geometry(root)
		if not current.is_empty() and current==previous:return
		previous=current
	check(false,"Card geometry did not settle within 90 frames")
func run() -> void:
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/")!=expected:
		push_error("Hand reuse test requires scratch profile");quit(2);return
	root.size=Vector2i(1100,540)
	root.gui_disable_input=true # Pixel fixture uses explicit hover calls, not physical pointer position.
	if DisplayServer.get_name()!="headless":
		root.mode=Window.MODE_WINDOWED;root.always_on_top=true;root.grab_focus()
	var game:=Fixture.new()
	game.meta.save_path="user://hand_reuse.meta"
	root.add_child(game);game.set_process(false)
	game.hand_box=HBoxContainer.new();game.add_child(game.hand_box)
	game.hand_box.position=Vector2(100,100);game.hand_box.size=Vector2(900,350)
	game.hand_count_label=Label.new();game.add_child(game.hand_count_label)
	game.reroll_button=Button.new();game.add_child(game.reroll_button)
	game.hand_layout_button=Button.new();game.add_child(game.hand_layout_button)
	game.reroll_button.position=Vector2(30,20);game.hand_layout_button.position=Vector2(250,20)
	game.hand=["reactor","storage_bay","reactor"]
	for key in game.resources:game.resources[key]=1000
	game.card_drag=preload("res://scripts/card_drag.gd").new()
	game.card_drag.game=game;game.add_child(game.card_drag)
	var original_textures:Dictionary={}
	for id in ["reactor","storage_bay"]:
		game.card_textures[id]=game._load_card_thumbnail(preload("res://scripts/room_card_art.gd").PATHS[id])
		original_textures[id]=game.card_textures[id]
		check(game.card_textures[id]!=null,"Real room thumbnail loads: "+id)
	game.running=true
	var pixel_pairs:=0
	var timings:=[]
	for layout in ["row","fan"]:
		Settings.hand_layout=layout
		game._refresh_cards();await settle()
		var initial:=cards(game.hand_box)
		check(initial.size()==3,"Three cards, including duplicate IDs")
		var stamp:=Time.get_ticks_usec()
		for i in range(100):game._refresh_cards()
		timings.append({"layout":layout,"hundred_refresh_us":Time.get_ticks_usec()-stamp})
		check(cards(game.hand_box)==initial,"Unchanged cards retain identity in "+layout)
		check(initial[0].get_meta("hand_index")==0 and initial[2].get_meta("hand_index")==2,"Duplicate cards retain distinct input indices")
		check(initial[2].gui_input.get_connections().size()==1,"One input binding per retained card")
		game.rerolls_remaining=1;game.reroll_recovery_progress=1;game._refresh_cards()
		check(cards(game.hand_box)==initial and game.reroll_button.text.contains("REROLL HAND · 1"),"Reroll controls update without card rebuild")
		Settings.reduced_motion=true
		game._on_card_hovered("reactor",initial[0]);var pose:Vector2=initial[0].position
		game._refresh_cards()
		check(cards(game.hand_box)==initial and initial[0].position==pose,"Hover survives unchanged refresh")
		game._on_card_unhovered("reactor",initial[0]);await settle()
		for scenario in ["selected","short","shorter","prototype","art","restored"]:
			var prior:=cards(game.hand_box)
			match scenario:
				"selected":game.selected_card_id="reactor"
				"short":game.resources.metal=0
				"shorter":game.resources.metal=1
				"prototype":game.prototype_card_seen_cycle["reactor"]=0
				"art":
					var replacement:=GradientTexture2D.new()
					replacement.gradient=Gradient.new()
					game.card_textures["reactor"]=replacement
				"restored":
					game.resources.metal=1000;game.prototype_card_seen_cycle.clear();game.selected_card_id=""
					game.card_textures=original_textures.duplicate()
			game._refresh_cards();await settle()
			var changed:=cards(game.hand_box)
			check(changed!=prior,"Presentation invalidates for "+scenario)
			check(changed[0].tooltip_text==game._blueprint_decision(game.RoomDatabaseScript.get_room("reactor")),"Tooltip current for "+scenario)
			game._refresh_cards();check(cards(game.hand_box)==changed,"New presentation is retained for "+scenario)
			if DisplayServer.get_name()!="headless":
				if root.mode==Window.MODE_MINIMIZED:push_error("Native test minimized");quit(2);return
				await settle();RenderingServer.force_draw(false)
				var rendered:=root.get_texture().get_image()
				var retained:=rendered.get_data()
				if not capture_dir.is_empty():
					DirAccess.make_dir_recursive_absolute(capture_dir)
					rendered.save_png(capture_dir.path_join(layout+"-"+scenario+".png"))
				game.hand_box.remove_meta("card_presentation")
				game._refresh_cards();await settle();RenderingServer.force_draw(false)
				check(retained==root.get_texture().get_image().get_data(),"Native retained/fresh pixels match "+layout+"/"+scenario)
				pixel_pairs+=1
		# Emit the real bound input signal, including the duplicate card's index.
		var click:=InputEventMouseButton.new()
		click.button_index=MOUSE_BUTTON_LEFT;click.pressed=true;click.global_position=Vector2(10,10)
		cards(game.hand_box)[2].gui_input.emit(click)
		check(game.selected_card_id=="reactor" and game.card_drag.pressing and game.card_drag.hand_index==2,"Bound click selects and begins drag for duplicate index 2")
		var source:Control=cards(game.hand_box)[2]
		game.card_drag.ghost=game.card_drag._build_ghost();game.card_drag.add_child(game.card_drag.ghost)
		game.card_drag.dragging=true;game.card_drag._set_source_faded(true)
		check(is_equal_approx(source.modulate.a,.3) and is_equal_approx(cards(game.hand_box)[0].modulate.a,1.0),"Only the dragged duplicate is faded")
		game._refresh_cards()
		check(cards(game.hand_box)[2]==source and is_equal_approx(source.modulate.a,.3),"Unchanged refresh preserves drag source fade")
		game.card_drag._finish();game._refresh_cards()
		check(not game.card_drag.pressing and not game.card_drag.dragging and game.card_drag.ghost==null and cards(game.hand_box)[2]==source and is_equal_approx(source.modulate.a,1.0),"Cancellation restores the retained source and removes its ghost")
		game.selected_card_id="";game.running=false
		cards(game.hand_box)[2].gui_input.emit(click)
		check(game.selected_card_id.is_empty() and not game.card_drag.pressing,"Stopped game blocks card input")
		game.running=true
		game.hand=["storage_bay","reactor"]
		game._refresh_cards();await settle()
		check(cards(game.hand_box).size()==2 and cards(game.hand_box)[0].get_meta("card_id")=="storage_bay","Hand removal/order invalidates")
		game.hand=["reactor","storage_bay","reactor"]
		game._refresh_cards();await settle()
	game.queue_free();await process_frame
	print("HAND REUSE checks=",checks," failures=",failures," native_pairs=",pixel_pairs," timings=",JSON.stringify(timings))
	quit(1 if failures else 0)
