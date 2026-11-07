extends SceneTree
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var game=load("res://scenes/main.tscn").instantiate();game.set_meta("tablet_controls",true);game.meta.save_path="user://fixture.meta";game.run_save_path="user://fixture.loop"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game._set_paused(true,false)
 var grid=game.grid_view
 var initial:int=grid.crew_storage_diagnostics().source_compressed_bytes
 var playback:Dictionary=grid.crew_playback_snapshot()
 game._set_paused(false,false)
 for frame in range(3):await process_frame
 game._set_paused(true,false)
 check(grid.crew_storage_diagnostics().source_compressed_bytes==initial,"Inactive crew updates must not force animation loading")
 var checkpoint:Dictionary=preload("res://scripts/run_save.gd").capture(game)
 check(not checkpoint.is_empty() and grid.crew_storage_diagnostics().source_compressed_bytes==initial,"Ordinary checkpoint capture must not load absent crew")
 check(grid.crew_storage_diagnostics().source_compressed_bytes==initial,"Snapshots must not prepare absent crew")
 playback.veld.phase=0.25;playback.veld.last_time=2.0;playback.veld.last_position=Vector2(1,2)
 grid.restore_crew_playback(playback)
 check(grid.crew_playback_snapshot().veld.phase==0.25,"Unloaded empty playback retains phase")
 check(grid.crew_storage_diagnostics().source_compressed_bytes==initial,"Restoring empty absent playback must not prepare crew")
 var veld=grid.veld_player
 var after_veld:int=grid.crew_storage_diagnostics().source_compressed_bytes
 check(after_veld>initial,"First Veld use must prepare previously absent animation sources")
 check(veld.snapshot().phase==0.25,"First Veld load applies pending playback")
 check(veld.frames.has("idle-east"),"First Veld use supplies actual idle artwork")
 var same=grid.veld_player
 check(is_same(same,veld) and grid.crew_storage_diagnostics().source_compressed_bytes==after_veld,"Repeated Veld use shares loaded sources")
 var routing=grid.Router.active
 playback.marsh.key="idle-east";playback.marsh.phase=0.35
 grid.restore_crew_playback(playback)
 var marsh=grid.marsh_player
 check(marsh.snapshot().key=="idle-east" and marsh.snapshot().phase==0.35 and grid.Router.active==routing,"Nonempty restore loads absent actor into the existing Router and retains playback")
 var after_marsh:int=grid.crew_storage_diagnostics().source_compressed_bytes
 check(after_marsh>after_veld,"First Marsh use prepares only that remaining crew")
 check(not marsh.frames.is_empty(),"First Marsh use supplies artwork")
 check(grid.branforth_player.has_method("floor_texture"),"James cargo checkpoint player remains available")
 var data:Dictionary=veld.snapshot();data.phase=0.25;data.last_time=2.0;data.last_position=Vector2(1,2)
 playback.veld=data;grid.restore_crew_playback(playback)
 check(grid.crew_playback_snapshot().veld.phase==0.25,"Deferred playback retains phase after restoration")
 print("CREW_LOADING bytes initial=",initial," veld=",after_veld," marsh=",after_marsh," failures=",failures)
 game.queue_free();await process_frame
 root.set_meta("tablet_controls",false)
 var desktop=load("res://scenes/main.tscn").instantiate();desktop.meta.save_path="user://desktop.meta";desktop.run_save_path="user://desktop.loop"
 root.add_child(desktop);current_scene=desktop
 while not desktop.startup_complete:await process_frame
 desktop._set_paused(true,false)
 check(not desktop.grid_view.deferred_replacement_crew,"Desktop eager policy remains enabled")
 var desktop_bytes:int=desktop.grid_view.crew_storage_diagnostics().source_compressed_bytes
 var desktop_veld=desktop.grid_view.veld_player;var desktop_marsh=desktop.grid_view.marsh_player
 check(not desktop_veld.frames.is_empty() and not desktop_marsh.frames.is_empty() and desktop.grid_view.crew_storage_diagnostics().source_compressed_bytes==desktop_bytes,"Desktop actors are already loaded before first access")
 desktop.queue_free();await process_frame;quit(1 if failures else 0)
