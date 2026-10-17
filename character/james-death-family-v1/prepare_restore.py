from pathlib import Path
P=Path(__file__).resolve().parent
base=(P/'native-installed-behaviour.gd').read_text()
prefix=base[:base.index('func run() -> void:')].replace('installed-behaviour-captures','restore-captures')
body='''func run() -> void:
\tcheck("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
\tcheck(OS.get_user_data_dir().replace("\\\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\\\","/").to_lower()+"/"),"Resolved scratch profile")
\tif failures:quit(2);return
\troot.size=Vector2i(1600,900)
\tvar store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
\tgame=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
\tvar stem:String="user://james-death-restore-"+str(OS.get_process_id())
\tgame.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
\tgame.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
\troot.add_child(game);current_scene=game
\twhile not game.startup_complete:await process_frame
\tgame.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
\tgame.Architects.advance_core(game,10)
\tvar hab:=Vector2i(20,22);game.wrecks.erase(hab)
\tgame._place_room("corridor",Vector2i(20,21),true);game._place_room("maintenance_bay",hab,true);game.powered_room_cells[hab]=true
\tfor peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
\tgame.test_walker_cell=Vector2i(-1,-1);game.resources.oxygen=100;game.resources.food=100
\tgame._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9);await process_frame
\tDirAccess.make_dir_recursive_absolute(OUT+"restore-captures")
\tvar evidence:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance-evidence.json"))
\tvar save=preload("res://scripts/run_save.gd")
\tfor mode in ["bare","helmet"]:
\t\tvar gear:String="" if mode=="bare" else "diving-helmet"
\t\tfor d in ["east","south","west","north"]:
\t\t\tfor medium in ["dry","flooded"]:
\t\t\t\tvar npc=game.branforth_npc;npc.dead=false;npc.active=true;npc.state="idle";npc.stage="";npc.goal="";npc.direction=d;npc.helmet_equipped=mode=="helmet";npc.movement_medium=medium;npc.path.clear();npc.expedition.clear();npc.air_recovery=0;npc.air_was_low=false;npc.rebuild(game)
\t\t\t\tvar action:String="death-ground" if medium=="dry" else "death-water";var key:String=action+"-"+d
\t\t\t\tfor room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
\t\t\t\tvar point:=Vector2.INF
\t\t\t\tfor node in npc.room_nodes.get(hab,[]):
\t\t\t\t\tvar at:Vector2=npc.graph.get_point_position(node)
\t\t\t\t\tif npc.swim_segment_clear(at,at,d,d,false,evidence.bounds[mode][key]):point=at;break
\t\t\t\tcheck(point.is_finite(),"Restored death fixture clear node "+mode+key)
\t\t\t\tif not point.is_finite():continue
\t\t\t\tnpc.foot=point;npc.die()
\t\t\t\tvar player=game.grid_view.branforth_player;var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
\t\t\t\tplayer.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100.0
\t\t\t\tgame.grid_view._get_branforth_frame(game)
\t\t\t\tvar middle:=0.0
\t\t\t\tfor i in range(3):middle+=float(timing[key].durations[i])/1000.0
\t\t\t\tmiddle+=float(timing[key].durations[3])/2000.0
\t\t\t\tfor sample in [middle,player.cycle_seconds(key,gear)+30.0]:
\t\t\t\t\tgame.visual_time_seconds=100.0+sample
\t\t\t\t\tvar expected_index:int=3 if sample==middle else 5
\t\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame(game);var pixels:=texture.get_image().get_data()
\t\t\t\t\tcheck(texture==frames[key][expected_index],"Selected pre-save phase "+mode+key+str(expected_index))
\t\t\t\t\tvar clock:float=game.visual_time_seconds;var playback:Dictionary=player.snapshot()
\t\t\t\t\tvar reason:String=save.problem(save.capture(game));check(reason.is_empty(),"Valid actual checkpoint: "+reason)
\t\t\t\t\tif not reason.is_empty():quit(1);return
\t\t\t\t\tcheck(save.write(game,game.run_save_path)==OK,"Death checkpoint writes "+mode+key)
\t\t\t\t\tvar checkpoint:Dictionary=save.read(game.run_save_path);check(not checkpoint.is_empty(),"Death checkpoint reads "+mode+key)
\t\t\t\t\tif checkpoint.is_empty():quit(1);return
\t\t\t\t\tcheck(await save.restore_staged(game,checkpoint),"Death checkpoint restores "+mode+key+save.last_error)
\t\t\t\t\tgame.run_save_path=stem+".loop";game.tick_timer.stop();game.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
\t\t\t\t\tcheck(npc.dead and npc.animation_state()==action and npc.direction==d,"Restore preserves death identity/facing "+mode+key)
\t\t\t\t\tcheck(game.paused and game.visual_time_seconds==clock,"Restore paused visual clock "+mode+key)
\t\t\t\t\tcheck(player.snapshot()==playback,"Restore exact independent sprite phase "+mode+key)
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Restore exact pose pixels "+mode+key)
\t\t\t\t\tgame._process(.5)
\t\t\t\t\tcheck(game.visual_time_seconds==clock and game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Pause does not restart/advance dead pose "+mode+key)
\t\t\t\t\tif expected_index==5:
\t\t\t\t\t\tgame.visual_time_seconds+=10.0
\t\t\t\t\t\tcheck(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Resumed corpse remains terminal "+mode+key)
\t\t\t\t\t\tvar target:Vector2=npc.foot/384.0/float(game.GRID_SIZE)
\t\t\t\t\t\tgame._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9,true,target)
\t\t\t\t\t\tawait process_frame
\t\t\t\t\t\tfor attempt in range(30):
\t\t\t\t\t\t\tif game._grid_view_center_ratio().distance_to(target)<.004:break
\t\t\t\t\t\t\tawait process_frame
\t\t\t\t\t\tcheck(game._grid_view_center_ratio().distance_to(target)<.004,"Restored camera visibly centers corpse "+mode+key)
\t\t\t\t\t\tawait capture(mode+"-"+action.trim_prefix("death-")+"-"+d+"-terminal",npc)
\t\t\t\t\tresults.append({"mode":mode,"key":key,"index":expected_index,"actualDiskRestore":true})
\tvar file:=FileAccess.open(OUT+"restore-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"32 actual scratch RunSave writes/reads/staged restores,mid-collapse and terminal,16 selected states/gear cases; exact pixels/clock/phase/pause/resumed terminal and16 native terminal captures. Does not prove actual oxygen journey or legacy saves lacking playback."},"  "));file.close()
\tprint("JAMES DEATH DISK RESTORE: ",checks," checks; ",failures," failures;32 actual checkpoint phases")
\tquit(1 if failures else 0)
'''
(P/'native-restore.gd').write_text(prefix+body,encoding='utf-8')
print('Prepared actual32-phase death checkpoint restore fixture')
