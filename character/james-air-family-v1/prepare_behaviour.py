from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-water-turn-family-v1/native-routes.gd').read_text();prefix=source[:source.index('\tvar clearance: Dictionary=')].replace('james-water-turn-family-v1','james-air-family-v1').replace('james-water-turn-routes','james-air-behaviour')
body='''
\tvar clearance:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
\tvar evidence:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance-evidence.json"))
\tpreload("res://scripts/crew_life.gd").clearance["branforth"]=clearance.life
\tvar player=game.grid_view.branforth_player
\tplayer.load_manifest(OUT+"bare-manifest.json",true)
\tcheck(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Candidate shared helmets")
\tgame.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
\tawait process_frame;game._center_grid_on_station_now();await process_frame
\tDirAccess.make_dir_recursive_absolute(OUT+"route-captures")
\tgame.resources.oxygen=100;game.resources.food=100
\tvar flood=preload("res://scripts/room_flooding.gd")
\tfor mode in ["bare","helmet"]:
\t\tvar gear:String="" if mode=="bare" else "diving-helmet"
\t\tvar frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
\t\tfor d in ["east","south","west","north"]:
\t\t\tnpc.helmet_equipped=mode=="helmet";npc.dead=false;npc.state="idle";npc.stage="";npc.direction=d;npc.expedition.clear();npc.path.clear();npc.air_recovery=0;npc.air_was_low=false;npc.tank_oxygen=10;npc.breath_oxygen=4;npc.starvation=0;npc.movement_medium="flooded"
\t\t\tvar point:=Vector2.INF
\t\t\tfor node in npc.graph.get_point_ids():
\t\t\t\tvar at:Vector2=npc.graph.get_point_position(node)
\t\t\t\tif not game.occupied.has(npc.cell_at(at)):continue
\t\t\t\tif not npc.swim_segment_clear(at,at,d,d,false,clearance.life[mode]["swim-distress-"+d]):continue
\t\t\t\tif not npc.swim_segment_clear(at,at,d,d,false,evidence.bounds[mode]["recover-air-"+d]):continue
\t\t\t\tpoint=at;break
\t\t\tcheck(point.is_finite(),"Both action envelopes clear at actual room node "+mode+d)
\t\t\tif not point.is_finite():continue
\t\t\tnpc.foot=point
\t\t\tfor room in game.placed_rooms:room.water_level=.95
\t\t\tflood.step_crew(game,npc,"branforth",.01)
\t\t\tcheck(npc.air_was_low and npc.movement_medium=="flooded" and not npc.dead,"Actual unsafe-air low flag "+mode+d)
\t\t\tcheck(npc.animation_state()=="swim-distress" and npc.action_elapsed()<0,"Actual low-air distress chooser "+mode+d)
\t\t\tplayer.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100.0
\t\t\tgame.grid_view._get_branforth_frame(game)
\t\t\tfor i in range(6):
\t\t\t\tgame.visual_time_seconds=100.0+i*.16+.08
\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame(game)
\t\t\t\tcheck(texture==frames["swim-distress-"+d][i],"Normal grid distress slot "+mode+d+str(i))
\t\t\t\tcheck(game.grid_view._get_branforth_frame(game)==texture,"Paused distress cosmetic clock "+mode+d+str(i))
\t\t\t\tawait capture(mode+"-distress-"+d+"-"+str(i).pad_zeros(3),npc)
\t\t\tfor room in game.placed_rooms:room.water_level=0.0
\t\t\tflood.step_crew(game,npc,"branforth",.01)
\t\t\tcheck(npc.air_recovery==3.0 and not npc.air_was_low and npc.movement_medium=="dry","Safe air starts actual3sec recovery "+mode+d)
\t\t\tcheck(npc.animation_state()=="recover-air" and npc.action_elapsed()==0.0,"Recovery simulation sampler "+mode+d)
\t\t\tfor i in range(6):
\t\t\t\tvar sample:float=i*.5+.25
\t\t\t\tflood.step_crew(game,npc,"branforth",sample-(3.0-npc.air_recovery))
\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame(game)
\t\t\t\tcheck(texture==frames["recover-air-"+d][i],"Actual simulation recovery slot "+mode+d+str(i))
\t\t\t\tvar remaining:float=npc.air_recovery;game.visual_time_seconds+=1.0
\t\t\t\tcheck(game.grid_view._get_branforth_frame(game)==texture and npc.air_recovery==remaining,"Cosmetic time cannot advance recovery "+mode+d+str(i))
\t\t\t\tawait capture(mode+"-recovery-"+d+"-"+str(i).pad_zeros(3),npc)
\t\t\tflood.step_crew(game,npc,"branforth",npc.air_recovery+.000001)
\t\t\tcheck(npc.air_recovery==0.0 and npc.animation_state()=="idle","Actual recovery completion returns idle "+mode+d)
\t\t\tvar idle_texture:Texture2D=game.grid_view._get_branforth_frame(game)
\t\t\tvar idle_image:=Image.create(256,360,false,Image.FORMAT_RGBA8)
\t\t\tvar idle_pivot:Vector2=idle_texture.get_meta("crew_pivot")
\t\t\tidle_image.blit_rect(idle_texture.get_image(),Rect2i(Vector2i.ZERO,idle_texture.get_size()),Vector2i(Vector2(128,224)-idle_pivot))
\t\t\tcheck(idle_image.get_data()==frames["recover-air-"+d].back().get_image().get_data(),"Actual idle handoff preserves world-registered pixels "+mode+d)
\t\t\tvar before:Dictionary=npc.snapshot()
\t\t\tnpc.direction=d;npc.air_recovery=1.5;npc.state="walk"
\t\t\tcheck(npc.animation_state()!="recover-air" and npc.action_elapsed()<0,"Movement interrupts idle-only recovery art "+mode+d)
\t\t\tnpc.state="idle";npc.air_recovery=0.0
\t\t\tresults.append({"mode":mode,"direction":d,"distressSlots":6,"recoverySlots":6,"actualLowAir":true,"actualRecovery":true,"point":str(point)})
\tvar file:=FileAccess.open(OUT+"behaviour-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Controlled actual RoomFlooding.step_crew low-air and safe-room recovery at eight collision-checked room nodes, both modes/four directions, normal grid candidate overrides; pause/completion/idle-only interruption. Room water changed by fixture, not actual dewatering or travel proof."},"  "));file.close()
\tprint("JAMES AIR BEHAVIOUR: ",checks," checks; ",failures," failures; controlled low-air/safe-room fixture")
\tquit(1 if failures else 0)
'''
(P/'native-behaviour.gd').write_text(prefix+body)
print('Prepared actual low-air/safe-room/recovery controlled native fixture')
