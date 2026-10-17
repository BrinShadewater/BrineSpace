from pathlib import Path
P=Path(__file__).resolve().parent
verify=(P.parent/'james-air-family-v1/verify.py').read_text().replace('james-air-','james-death-')
verify=verify.replace("P/'endpoint-sources.json'", "P.parent/'james-air-family-v1/endpoint-sources.json'")
start=verify.index("  if action=='swim-distress':")
end=verify.index("for d,record in records.items():",start)
verify=verify[:start]+"  check(np.array_equal(pixels(P/s['frameFiles'][0]),pixels(P.parent/'james-air-family-v1/endpoints'/mode/(('swim' if action=='death-water' else 'idle')+'-'+d+'.png'))),'Exact selected entry '+mode+key)\n"+verify[end:]
verify=verify.replace("if i==5 or (action=='swim-distress' and i==0):continue", "if i==0:continue")
(P/'verify.py').write_text(verify,encoding='utf-8')
derive=(P.parent/'james-air-family-v1/derive_clearance.py').read_text()
derive=derive.replace("s['id'].startswith('swim-distress-')", "False")
derive=derive.replace('Staged distress life envelopes only; dry recovery sampled envelopes recorded; conservative baseline preserved','Death pose envelopes for fixture placement only; all selected clearance remains unchanged')
derive=derive.replace('Derived staged distress envelopes; runtime unchanged','Derived death envelopes for fixture placement; runtime clearance unchanged')
(P/'derive_clearance.py').write_text(derive,encoding='utf-8')
fixture=(P.parent/'james-air-family-v1/native-behaviour.gd').read_text().replace('james-air-family-v1','james-death-family-v1').replace('james-air-behaviour','james-death-behaviour')
prefix=fixture[:fixture.index('\tvar clearance:Dictionary=')]
body='''
\tvar evidence:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance-evidence.json"))
\tvar player=game.grid_view.branforth_player
\tplayer.load_manifest(OUT+"bare-manifest.json",true)
\tcheck(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Candidate shared helmets")
\tgame.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
\tawait process_frame;game._center_grid_on_station_now();await process_frame
\tDirAccess.make_dir_recursive_absolute(OUT+"route-captures")
\tgame.resources.oxygen=100;game.resources.food=100
\tcheck(not preload("res://scripts/research_tree.gd").second_chance(game.meta),"Fresh scratch fixture has no Second Chance keystone")
\tfor mode in ["bare","helmet"]:
\t\tvar gear:String="" if mode=="bare" else "diving-helmet"
\t\tvar frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
\t\tfor d in ["east","south","west","north"]:
\t\t\tfor medium in ["dry","flooded"]:
\t\t\t\tvar action:String="death-ground" if medium=="dry" else "death-water"
\t\t\t\tvar key:String=action+"-"+d
\t\t\t\tnpc.helmet_equipped=mode=="helmet";npc.dead=false;npc.active=true;npc.state="idle";npc.stage="";npc.direction=d;npc.expedition.clear();npc.path.clear();npc.air_recovery=0;npc.air_was_low=false;npc.movement_medium=medium
\t\t\t\tgame.recovered_crew[0].alive=true;game.crew_count=4
\t\t\t\tfor room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
\t\t\t\tvar point:=Vector2.INF
\t\t\t\tfor node in npc.graph.get_point_ids():
\t\t\t\t\tvar at:Vector2=npc.graph.get_point_position(node)
\t\t\t\t\tif game.occupied.has(npc.cell_at(at)) and npc.swim_segment_clear(at,at,d,d,false,evidence.bounds[mode][key]):point=at;break
\t\t\t\tcheck(point.is_finite(),"Death envelope clear at actual room node "+mode+key)
\t\t\t\tif not point.is_finite():continue
\t\t\t\tnpc.foot=point;npc.path=PackedVector2Array([point+Vector2(10,0)]);npc.goal="fixture";npc.stage="fixture"
\t\t\t\tpreload("res://scripts/room_flooding.gd").kill(game,npc,"branforth","oxygen exhausted")
\t\t\t\tcheck(npc.dead and npc.state==action and npc.animation_state()==action,"Actual mortality selects "+mode+key)
\t\t\t\tcheck(npc.path.is_empty() and npc.goal=="" and npc.stage=="" and npc.expedition.is_empty(),"Death clears actions "+mode+key)
\t\t\t\tcheck(game.crew_count==3 and not game.recovered_crew[0].alive,"Actual mortality accounting "+mode+key)
\t\t\t\tcheck(npc.action_elapsed()<0,"Death uses finite cosmetic playback "+mode+key)
\t\t\t\tcheck(npc.valid_snapshot(npc.snapshot()),"Dead snapshot remains valid "+mode+key)
\t\t\t\tplayer.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100.0
\t\t\t\tcheck(game.grid_view._get_branforth_frame(game)==frames[key][0],"Exact death entry selected "+mode+key)
\t\t\t\tvar timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
\t\t\t\tvar elapsed:=0.0
\t\t\t\tfor i in range(6):
\t\t\t\t\tgame.visual_time_seconds=100.0+elapsed+float(timing[key].durations[i])/2000.0
\t\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame(game)
\t\t\t\t\tcheck(texture==frames[key][i],"Normal grid actual death slot "+mode+key+str(i))
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame(game)==texture,"Paused death clock "+mode+key+str(i))
\t\t\t\t\tawait capture(mode+"-"+action.trim_prefix("death-")+"-"+d+"-"+str(i).pad_zeros(3),npc)
\t\t\t\t\telapsed+=float(timing[key].durations[i])/1000.0
\t\t\t\tgame.visual_time_seconds=100.0+elapsed+30.0
\t\t\t\tcheck(game.grid_view._get_branforth_frame(game)==frames[key].back(),"Death terminal holds without reset "+mode+key)
\t\t\t\tpreload("res://scripts/room_flooding.gd").kill(game,npc,"branforth","oxygen exhausted")
\t\t\t\tcheck(npc.dead and npc.state==action,"Already dead actor keeps pose family "+mode+key)
\t\t\t\tresults.append({"mode":mode,"direction":d,"action":action,"actualDeath":true,"slots":6,"point":str(point)})
\tvar file:=FileAccess.open(OUT+"behaviour-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Controlled direct RoomFlooding.kill actual accounting/chooser/finite playback,16 clear room-node cases,96 normal grid candidate captures. No actual oxygen journey or disk-restored terminal-phase proof."},"  "));file.close()
\tprint("JAMES DEATH BEHAVIOUR: ",checks," checks; ",failures," failures; controlled mortality fixture")
\tquit(1 if failures else 0)
'''
# Do not invoke kill twice: kill's caller normally guards dead actors; die alone is idempotent.
body=body.replace('preload("res://scripts/room_flooding.gd").kill(game,npc,"branforth","oxygen exhausted")\n\t\t\t\tcheck(npc.dead and npc.state==action,"Already dead actor keeps pose family', 'npc.die()\n\t\t\t\tcheck(npc.dead and npc.state==action,"Already dead actor keeps pose family')
(P/'native-behaviour.gd').write_text(prefix+body,encoding='utf-8')
review=(P.parent/'james-air-family-v1/review_behaviour.py').read_text().replace("['distress','recovery']","['ground','water']")
(P/'review_behaviour.py').write_text(review,encoding='utf-8')
print('Prepared death package and actual mortality candidate fixture')

