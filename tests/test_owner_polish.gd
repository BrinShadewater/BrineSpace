extends SceneTree
## Native review and behavioural regressions for the October 4 owner polish pass.
## Run with scratch APPDATA; --capture saves the reviewed screens.
const OUT := "res://output/polish-2026-10-04/"
const Store = preload("res://scripts/room_layout_store.gd")
const Large = preload("res://rooms/large-rooms/studio_view.gd")
const Moon = preload("res://rooms/large-rooms/moonbay.gd")
const Portrait = preload("res://scripts/crew_portrait_panel.gd")
var checks := 0
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool,label: String) -> void:
	checks+=1
	if not ok: failures+=1; push_error(label)
func settle() -> void:
	for i in range(8): await process_frame
func capture(label: String) -> void:
	if DisplayServer.get_name()=="headless" or not OS.get_cmdline_user_args().has("--capture"): return
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+label+".png")
func cards_in(game) -> Array:
	var cards: Array=[]
	for holder in game.hand_box.get_children():
		for child in holder.get_children():
			if child.has_meta("card_id"): cards.append(child)
	return cards
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	root.gui_disable_input=true
	var studio=load("res://scripts/room_layout_editor.gd").new()
	root.add_child(studio)
	await settle()
	studio.autosave_enabled=false
	studio.set_process(false)
	for id in Large.VIEWS:
		for i in range(studio.entries.size()):
			if studio.entries[i].room==id: studio.switch_room(i); break
		for q in range(4):
			studio.switch_rotation(q)
			studio.set_cast_modes({0:studio.scale_actor.Actor.WALKING})
			studio.scale_actor.rebuild(studio.room,id,q)
			check(studio.show_character.visible,id+": character controls visible")
			check(studio.scale_actor.members().size()==1,id+": actor visible q%d"%q)
			var actor=studio.scale_actor.actors[0]
			var travelled:=0.0
			for tick in range(40):
				var before: Vector2=actor.foot
				studio.scale_actor.advance(0.1)
				check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),id+": clear walking path q%d"%q)
				travelled+=before.distance_to(actor.foot)
			check(travelled>40,id+": walks around the central equipment q%d"%q)
			if q!=0: continue
			# Drag an actual default piece through the editor's pointer path, then save/reload.
			var prop: Dictionary=studio.room.props[0]
			var prop_id: String=prop.id
			var old: Vector2=prop.rect.position
			var point: Vector2=studio.entity_bounds(prop).get_center()
			var start: Vector2=studio.canvas.origin()+point*studio.canvas.factor()
			var press:=InputEventMouseButton.new()
			press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true; press.position=start
			studio.canvas_input(press)
			check(studio.selected==prop_id and studio.dragging,id+": default prop can be picked up")
			var motion:=InputEventMouseMotion.new()
			motion.position=start+Vector2(12,12)*studio.canvas.factor()
			motion.relative=motion.position-start
			studio.canvas_input(motion)
			press.pressed=false; press.position=motion.position; studio.canvas_input(press)
			var moved: Vector2=studio.selected_prop().rect.position
			check(moved.distance_to(old)>5,id+": dragging moves default prop")
			studio.save_layout()
			var live: Array=Large.live_props(id,q).filter(func(p):return p.id==prop_id)
			check(live.size()==1 and live[0].rect.position.distance_to(moved)<0.01,id+": edited prop reaches live room")
			if id=="moonbay":
				var prior: Rect2=Moon.locker_bounds({"rotation":0})
				var layout: Dictionary=Store.positions("room-moonbay",0)
				layout["library/sp-airlock-4"]=[prior.position.x-40,prior.position.y+30]
				Store.save_layout("room-moonbay",0,layout)
				check(Moon.locker_bounds({"rotation":0}).position.distance_to(prior.position+Vector2(-40,30))<0.01,"Moonbay locker follows saved position")
				check(Moon.locker_point({"rotation":0}).distance_to(Vector2(prior.position.x-66,prior.end.y+18))<0.01,"Locker interaction moves with its prop")
				layout["library/sp-airlock-4"]=null; Store.save_layout("room-moonbay",0,layout)
				check(not Moon.locker_bounds({"rotation":0}).has_area(),"Deleted Moonbay locker disappears from service")
				layout["library/sp-airlock-4"]=[prior.position.x,prior.position.y]; Store.save_layout("room-moonbay",0,layout)
			if id=="tidal_power_plant":
				studio.effects.start("tidal_fill"); studio.effects.advance(6.5)
			studio.canvas.queue_redraw()
			await settle()
			await capture("studio-"+id)
	studio.queue_free()
	await settle()
	var workshop=load("res://scripts/james_cargo_workshop.gd").new()
	root.add_child(workshop); workshop.hide()
	workshop.configure_embedded(0,[],true,0.0)
	check(Store.asset_for(workshop)=="room-salvage_workshop","Cargo workshop resolves the real layout key")
	Store.apply(workshop,Store.asset_for(workshop))
	preload("res://scripts/room_asset_library.gd").strip_retired(workshop)
	check(workshop.props.size()==4,"Live cargo workshop receives four current props")
	check(workshop.props.all(func(p):return str(p.id).begins_with("library/sp-salvage_workshop-")),"Live workshop excludes old bench and tote")
	workshop.queue_free()
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://polish.meta"
	game.run_save_path="user://polish.loop"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game._set_paused(true,false); game.tick_timer.stop(); game.set_process(false)
	game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	game.recovered_crew.clear()
	for id in game.Architects.IDS: game.recovered_crew.append({"architect_id":id,"alive":true})
	var panel=game.find_child("CrewPortraitPanel",true,false)
	game.bill_npc.needs.hunger=72.0; game.bill_npc.needs.fatigue=43.0
	game.bill_npc.starvation=22.5; game.bill_npc.breath_oxygen=7.5
	panel.selected="bill"; panel.refresh()
	check(panel.health_meter.value==75 and panel.oxygen.value==50,"Detailed health and breath meters reflect live values")
	check(panel.hunger.value==72 and panel.fatigue.value==43,"Detailed needs reflect live values")
	check(panel.compact_meters.bill.HEALTH.value==75 and panel.compact_meters.bill.OXYGEN.value==50,"Compact meters match detail values")
	game.bill_npc.helmet_equipped=true; game.bill_npc.tank_oxygen=15.0; panel.refresh()
	check(panel.oxygen.value==25,"Helmet oxygen uses tank capacity")
	game.bill_npc.dead=true; panel.refresh()
	check(panel.health_meter.value==0 and panel.oxygen.value==0,"Death clears health and oxygen")
	game.bill_npc.dead=false; game.bill_npc.helmet_equipped=false; panel.refresh()
	game.hand=["hydroponics_bay","corridor","tidal_power_plant"]
	for layout in ["fan","row"]:
		game.Preferences.hand_layout=layout; game._refresh_cards()
		await settle()
		var cards:=cards_in(game)
		check(cards.size()==3,"Three cards in "+layout)
		for card in cards:
			check(card.size.is_equal_approx(cards[0].size),layout+": equal card size "+card.name)
			check(card.size.x+0.1>=card.get_combined_minimum_size().x and card.size.y+0.1>=card.get_combined_minimum_size().y,layout+": all content fits "+card.name)
		await capture("ui-expanded-"+layout)
	panel.selected=""; panel.refresh(); await settle()
	check(not panel.details.visible and panel.compact_meters.size()==4,"Collapsed panel retains all crew meters")
	await capture("ui-compact")
	root.size=Vector2i(960,540); await settle()
	check(root.get_visible_rect().encloses(panel.get_global_rect()),"Compact portrait strip fits smallest supported viewport")
	await capture("ui-small-window")
	print("OWNER POLISH: %d checks, %d failures"%[checks,failures])
	quit(1 if failures else 0)
