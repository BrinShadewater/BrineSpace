extends SceneTree
var cell_clicks:=0
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://conversation-%d.loop"%OS.get_process_id()
	game.meta.save_path="user://conversation-%d.meta"%OS.get_process_id()
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	var comms=game.crew_comms; comms.set_process(false)
	assert(comms.opening_enabled)
	comms.observe_game()
	assert(comms.pending.size()==3 and comms.pending[1].speaker==game.meta.selected_architect)
	assert("First objective:" in comms.pending[2].text)
	comms.observe_game(); assert(comms.pending.size()==3,"No repeated introduction")
	comms.show_next(); comms.advance(); comms.advance()
	assert(comms.current.speaker==game.meta.selected_architect)
	comms.advance(); comms.advance(); assert("First objective:" in comms.current.text)
	comms.dismiss()
	# Continue keeps the short greeting, without replaying the new-loop tutorial.
	comms.opening_enabled=false; comms.greeting_sent=false; comms.seen.clear(); comms.last_ambient=-60
	comms.observe_game(); assert(comms.pending.size()==1)
	comms.dismiss()
	game.selected_card_id=""
	var room_replies: Array=[]
	var resource_replies: Array=[]
	game.grid_view.cell_clicked.connect(func(_cell): cell_clicks+=1)
	for id in ["bill","veld","branforth"]:
		var actor=preload("res://scripts/architects.gd").actor_for(game,id)
		actor.active=true; actor.dead=false
		actor.foot=(Vector2(20,20)+Vector2(0.3+0.2*["bill","veld","branforth"].find(id),0.7))*384.0
		var point: Vector2=actor.foot/384.0*game.get_cell_size()-Vector2(0,game.get_cell_size()*0.09)
		assert(comms.crew_at(point,game.get_cell_size())==id)
		var event:=InputEventMouseButton.new(); event.button_index=MOUSE_BUTTON_LEFT; event.pressed=true; event.position=point
		game.grid_view._gui_input(event)
		assert(comms.current.speaker==id and cell_clicks==0,"Crew click consumed before room selection")
		assert(not comms.replies.visible,"Replies wait for the text")
		comms.advance(); assert(comms.replies.visible)
		comms.answer("This room?"); assert("BRINE" in comms.current.text or "Brine" in comms.current.text)
		assert(not room_replies.has(comms.current.text)); room_replies.append(comms.current.text)
		comms.answer("Needs attention?"); assert(not comms.current.text.is_empty())
		assert(not resource_replies.has(comms.current.text)); resource_replies.append(comms.current.text)
		actor.dead=true; assert(not comms.open_crew(id)); actor.dead=false
	# Construction input continues to reach the room handler.
	game.selected_card_id="reactor"
	var event:=InputEventMouseButton.new(); event.button_index=MOUSE_BUTTON_LEFT; event.pressed=true
	event.position=game.bill_npc.foot/384.0*game.get_cell_size()-Vector2(0,game.get_cell_size()*0.09)
	game.grid_view._gui_input(event); assert(cell_clicks==1)
	game.selected_card_id=""
	comms.transmit("brine","Queued station report.")
	comms.open_crew("bill"); comms.answer("Needs attention?")
	assert(comms.pending.size()==1,"Player questions preserve queued reports")
	comms.dismiss(); comms.transmit("brine","Oxygen reserves are critically low.","priority-test",true); comms.show_next()
	assert("PRIORITY" in comms.heading.text)
	comms.dismiss()
	game.veld_npc.active=false; game.branforth_npc.dead=true
	comms.refresh_contacts(); assert(comms.contact_picker.item_count==3,"Only BRINE and living active Bill listed")
	comms.select_contact(2); assert(comms.current.speaker=="bill")
	comms.transmit("bill","Routine report.")
	comms.transmit("brine","Urgent one.","urgent-one",true)
	comms.transmit("brine","Urgent two.","urgent-two",true)
	assert(comms.current.speaker=="bill","Urgency does not interrupt reading")
	assert(comms.pending[0].text=="Urgent one." and comms.pending[1].text=="Urgent two." and comms.pending[2].text=="Routine report.")
	comms.select_contact(1); assert(comms.current.speaker=="brine" and comms.pending.size()==3,"BRINE contact preserves reports")
	game.veld_npc.active=true; game.branforth_npc.dead=false
	comms.refresh_contacts(); assert(comms.contact_picker.item_count==5)
	comms.minimize(); var paused_characters: int=comms.body.visible_characters
	comms._process(0.3)
	assert(not comms.panel.visible and comms.minimized and comms.pending.size()==3)
	assert(comms.body.visible_characters==paused_characters,"Closing preserves reading position")
	assert("3" in game.comms_button.text)
	comms.reopen(); assert(comms.panel.visible and not comms.inbox_button.visible and comms.pending.size()==3)
	comms.dismiss(); comms.open_crew("branforth"); comms.answer("This room?"); comms.advance()
	assert("Observed:" in comms.room_status.text and "Next cycle:" in comms.room_status.text)
	assert(comms.health_button.text=="Locate room")
	var discussed:=Vector2i(20,20)
	game.occupied[discussed].suspended=true
	comms.answer("This room?"); assert("SUSPENDED" in comms.room_status.text,"Forecast reflects suspension")
	game.occupied[discussed].suspended=false
	comms.open_station_health(); assert(game.selected_room_cell==discussed and comms.minimized,"Locate uses the discussed room")
	comms.reopen()
	comms.current.room_id="removed-room"
	comms.open_station_health(); comms.update_replies()
	assert(comms.health_button.disabled and comms.health_button.text=="Room unavailable","Stale context cannot locate a replacement")
	comms.answer("Needs attention?"); comms.advance()
	assert(comms.health_button.visible)
	var was_paused: bool=game.paused
	comms.open_station_health(); assert(game._journal_is_open() and game.journal_tabs.current_tab==1)
	comms._process(0.1); assert(not comms.panel.visible)
	game._toggle_journal(); comms._process(0.1)
	assert(comms.panel.visible and game.paused==was_paused,"Health navigation restores reading and pause state")
	comms.answer("This room?"); comms.advance()
	DirAccess.make_dir_recursive_absolute("res://output/crew-conversation")
	for width in [1600,960]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		for i in range(5): await process_frame
		comms.place_panel()
		await process_frame
		assert(game.grid_scroll.get_global_rect().encloses(comms.panel.get_global_rect()),"Expanded panel stays within station view")
		assert(not comms.replies.is_visible_in_tree(),"Context controls are absent from the compact popup")
		comms.minimize()
		assert(game.hardware_panel.controls.comms.button.is_visible_in_tree(),"Dedicated side-panel access")
		game.menu_open=true; comms._process(0.1); assert(not comms.inbox_button.visible)
		game.menu_open=false; comms._process(0.1); assert(comms.minimized and not comms.panel.visible)
		comms.reopen()
		if DisplayServer.get_name()!="headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/crew-conversation/talk-%d.png"%width)
	game.menu_open=true; comms._process(0.1); assert(not comms.panel.visible)
	game.menu_open=false; comms._process(0.1); assert(comms.panel.visible)
	game._start_reboot_cycle()
	assert(comms.opening_enabled and not comms.greeting_sent and comms.seen.is_empty(),"In-scene restart resets conversation events")
	print("COMMS CONVERSATION PASS: opening, Continue gating, three crew hit targets, build input, replies, queued reports, priority cue and panel bounds")
	quit()
