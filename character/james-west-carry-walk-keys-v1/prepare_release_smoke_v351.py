from pathlib import Path
r=Path.cwd();o=r/'character/james-west-carry-walk-keys-v1/release-build-review-v351';o.mkdir(exist_ok=True)
s=(r/'tests/release_new_game_smoke.gd').read_text()
s=s.replace('\tOS.add_logger(release_errors)','\tif not "brine-james-release-" in OS.get_environment("APPDATA"):\n\t\tpush_error("Scratch APPDATA required");get_tree().quit(2);return\n\tOS.add_logger(release_errors)')
s=s.replace('\tOS.add_logger(release_errors)','\tvar uid_path:String=get_script().resource_path+".uid"\n\tif not FileAccess.file_exists(uid_path):FileAccess.open(uid_path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tOS.add_logger(release_errors)')
s=s.replace('\ttitle.start_button.pressed.emit()','\ttitle.meta_state.unlocked_architect_ids["branforth"]=true\n\ttitle.meta_state.selected_architect="branforth"\n\ttitle.start_button.pressed.emit()')
s=s.replace('\tfor child in get_tree().root.get_children():\n\t\tif child.has_method("finish_after_scene_change"):', '\tcheck(game.meta.selected_architect=="branforth", "Normal New Game selects James in scratch-owned fixture")\n\tcheck(game.grid_view.branforth_player.get_script().resource_path=="res://scripts/james_water_player.gd", "Packaged selected James water player loaded")\n\tfor child in get_tree().root.get_children():\n\t\tif child.has_method("finish_after_scene_change"):',1)
needle='\tOS.remove_logger(release_errors)'
s=s.replace('\tfor i in range(10): await get_tree().process_frame\n\tvar title = get_tree().current_scene','''\tvar title
\tvar title_deadline:=Time.get_ticks_msec()+60000
\twhile Time.get_ticks_msec()<title_deadline:
\t\tawait get_tree().process_frame
\t\ttitle=get_tree().current_scene
\t\tif title!=null and title.has_method("_start_game"):break
\t\tif title!=null and title.has_method("_film_ended"):
\t\t\tvar skip:=InputEventKey.new();skip.keycode=KEY_SPACE;skip.pressed=true;title._unhandled_input(skip)''')
s=s.replace(needle,'''\tgame._set_paused(true,false)
\tvar checkpoint_path:String=game.run_save_path
\tcheck(preload("res://scripts/run_save.gd").write(game,checkpoint_path)==OK,"Write actual release scratch checkpoint")
\tvar saved_foot:Vector2=game.branforth_npc.foot
\tvar saved_stage:String=game.branforth_npc.stage
\tcheck(get_tree().change_scene_to_file("res://scenes/title_screen.tscn")==OK,"Return to packaged title for Continue")
\tvar deadline:=Time.get_ticks_msec()+30000
\twhile Time.get_ticks_msec()<deadline:
\t\tawait get_tree().process_frame
\t\ttitle=get_tree().current_scene
\t\tif title!=null and title.has_method("_continue_loop") and title.continue_button.visible:break
\tcheck(title!=null and title.has_method("_continue_loop") and title.continue_button.visible,"Normal title offers saved-loop Continue")
\tif title==null or not title.has_method("_continue_loop") or not title.continue_button.visible:get_tree().quit(1);return
\ttitle.continue_button.pressed.emit()
\tdeadline=Time.get_ticks_msec()+180000
\twhile Time.get_ticks_msec()<deadline:
\t\tawait get_tree().process_frame
\t\tvar loading_present:=false
\t\tfor child in get_tree().root.get_children():
\t\t\tif child.has_method("type_transmission"):
\t\t\t\tloading_present=true
\t\t\t\tif child.typing:
\t\t\t\t\tvar accept:=InputEventAction.new();accept.action="ui_accept";accept.pressed=true;child._input(accept)
\t\t\t\telif child.has_method("finish_after_scene_change") and not child.continue_button.disabled:child.continue_button.pressed.emit()
\t\tgame=get_tree().current_scene
\t\tif game!=null and game.get("startup_complete")==true and not loading_present and game.process_mode!=Node.PROCESS_MODE_DISABLED:break
\tcheck(game!=null and game.get("startup_complete")==true,"Normal saved-loop Continue completes")
\tif game==null or game.get("startup_complete")!=true:get_tree().quit(1);return
\tcheck(game.paused and game.branforth_npc.foot==saved_foot and game.branforth_npc.stage==saved_stage,"Continue preserves paused James contact/stage")
\tcheck(game.meta.selected_architect=="branforth" and game.grid_view.branforth_player.get_script().resource_path=="res://scripts/james_water_player.gd","Continue keeps packaged James selection")
\tgame.crew_comms.minimize();game._toggle_pause()
\tbefore=game.visual_time_seconds
\tfor i in range(120):await get_tree().process_frame
\tcheck(game.visual_time_seconds>before and game.grid_view.visible_draw_rooms.size()>0,"Continued release simulation advances and renders")
\tcheck(preload("res://scripts/safe_image.gd").failures.is_empty(),"Continued release has no missing-art placeholders")
\tawait RenderingServer.frame_post_draw
\tget_viewport().get_texture().get_image().save_png("user://release-continue.png")
'''+needle)
s=s.replace('ACTUAL RELEASE NEW GAME + F8:', 'JAMES ACTUAL RELEASE NEW GAME + SAVED CONTINUE + F8:')
(o/'release_smoke.gd').write_text(s)
print('Prepared guarded James release New Game, saved-loop Continue and F8 fixture')
