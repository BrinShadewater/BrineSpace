extends SceneTree
const Content = preload("res://scripts/room_content_canvas.gd")
const Settings = preload("res://scripts/title_settings.gd")
const VIEWS = [preload("res://rooms/full-wall-v1/life_support_view.gd"),preload("res://rooms/full-wall-v1/hydroponics_bay_view.gd"),preload("res://rooms/full-wall-v1/crew_hab_view.gd")]
var checks := 0
var failures := 0
var avoided := 0
var measurements := []
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	checks += 1
	if not ok: failures += 1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func compare(capture,canvas,view,label: String):
	var retained: Image=capture.get_texture().get_image()
	canvas.retain_frozen_effects=false
	canvas.submit(view,view._sorted_content_queue([]));await frame()
	check(retained.get_data()==capture.get_texture().get_image().get_data(),"Exact reference pixels: "+label)
	canvas.retain_frozen_effects=true
	canvas.submit(view,view._sorted_content_queue([]));await frame()
func run():
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected.replace("\\","/").simplify_path():
		push_error("Frozen-effects test requires isolated BRINESPACE_TEST_USER_DIR");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var original_motion: bool=Settings.reduced_motion
	var capture := SubViewport.new()
	capture.size=Vector2i(768,768);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	for script in VIEWS:
		var view = script.new();root.add_child(view);view.hide();view.set_process(false)
		for quarter in range(4):
			Settings.reduced_motion=false
			view.configure_embedded(quarter,[],true,1.23)
			var canvas = Content.new();capture.add_child(canvas);canvas.draw_origin=Vector2(384,384)
			canvas.draw_scale=0.7;canvas.profile_enabled=true;view.retained_content_host=canvas
			canvas.submit(view,view._sorted_content_queue([]));await frame()
			var effect_count := 0
			for slot in canvas.slots:
				if slot.item.kind=="library_live" and slot.live:effect_count+=1
			check(effect_count>0,"Selected room has live ordinary effects")
			check(not capture.get_texture().get_image().is_invisible(),"Visible selected props")
			for action in ["motion_on","held_advance","held_submit","wet","draining","move","zoom","hidden","visible","power_off","power_on","dry","motion_off","animated","freeze_again","motion_off_submit","freeze_submit"]:
				var before: int=canvas.live_redraws
				var advance := false
				match action:
					"motion_on","freeze_again":Settings.reduced_motion=true;advance=true
					"held_advance","animated":advance=true
					"wet":view.flood_water=0.4
					"draining":advance=true
					"move":
						preload("res://scripts/room_layout_store.gd").move_prop(view.props[0],view.props[0].rect.position+Vector2(19,9))
						var serials: Dictionary=view.get_meta("layout_apply_serials",{}).duplicate()
						serials[quarter]=int(serials.get(quarter,0))+1;view.set_meta("layout_apply_serials",serials)
					"zoom":canvas.draw_scale=0.83;canvas.draw_origin+=Vector2(7,-13)
					"hidden":canvas.clip_region=Rect2(9999,9999,1,1)
					"visible":canvas.clip_region=Rect2(-1000,-1000,2000,2000)
					"power_off":view.operating=false
					"power_on":view.operating=true
					"dry":view.flood_water=0.0
					"motion_off":Settings.reduced_motion=false;advance=true
					"motion_off_submit":Settings.reduced_motion=false
					"freeze_submit":Settings.reduced_motion=true
				view.machine_clock+=0.37;view.flood_clock=view.machine_clock
				if action=="draining":view.flood_water=0.2
				if advance:canvas.advance_live(view.machine_clock,view.flood_water)
				else:canvas.submit(view,view._sorted_content_queue([]))
				await frame()
				if action in ["held_advance","held_submit","draining"]:
					check(canvas.live_redraws==before,"Frozen commands retained: "+action);avoided+=effect_count
				if action in ["motion_on","motion_off","animated","freeze_again","motion_off_submit","freeze_submit"]:
					check(canvas.live_redraws>before,"Setting/clock updates actual effects: "+action)
				await compare(capture,canvas,view,"%s q%d %s"%[script.resource_path,quarter,action])
				if quarter==0 and action in ["wet","motion_off"]:capture.get_texture().get_image().save_png("user://%s-%s.png"%[script.resource_path.get_file().get_basename(),action])
			if quarter==0:
				for pair in range(3):
					for motion in [false,true]:
						Settings.reduced_motion=motion
						for retained in ([false,true] if pair%2==0 else [true,false]):
							canvas.retain_frozen_effects=retained;canvas.submit(view,view._sorted_content_queue([]));await frame()
							var samples := []
							var before: int=canvas.live_redraws
							for step in range(60):
								canvas.advance_live(10+step/60.0);await frame();samples.append(canvas.draw_usec)
							var redraws: int=canvas.live_redraws-before
							check(redraws==(0 if motion and retained else 60*effect_count),"Measured expected draw count")
							measurements.append({"view":script.resource_path,"pair":pair,"motion":motion,"retained":retained,"draw_usec":samples,"redraws":redraws})
			canvas.queue_free();await process_frame
		view.queue_free();await process_frame
	Settings.reduced_motion=original_motion
	capture.queue_free();await process_frame
	check(avoided>0,"Real selected live effects retained")
	FileAccess.open("user://frozen-effects.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"avoided":avoided,"measurements":measurements}))
	print("FROZEN PROP EFFECTS: %d checks; %d failures; %d command rebuilds avoided"%[checks,failures,avoided])
	quit(1 if failures else 0)
