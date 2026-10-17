from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_finish_world_v1.gd').read_text();s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-finish-world-v1','bill-floor-case-finish-priority-v1')
s=s.replace(' game.visual_time_seconds+=1.0/60;game.bill_npc.update(game,1.0/60)',' game.visual_time_seconds+=1.0/60\n if game.bill_npc.active and not game.bill_npc.dead:preload("res://scripts/room_flooding.gd").step_crew(game,game.bill_npc,"bill",1.0/60)\n game.bill_npc.update(game,1.0/60)')
s+='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var old=game.grid_view.human_water_player;var player=preload("res://character/bill-floor-case-north-v1/finish_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:player.set(field,old.get(field))
 game.grid_view.human_water_player=player
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 for event in ["fire","flood","gear","death","removal"]:
  for helmet in [false,true]:
   for target in [.10,.39]:
    game.running=false;game.paused=true
    if not game.occupied.has(CELL):game._place_room("salvage_workshop",CELL,true)
    var room:Dictionary=game.occupied[CELL];room.suspended=false;room.fire=0.0;room.water_level=0.0;room.erase(FLOOR.FIELD);game.powered_room_cells[CELL]=true
    view.bind_room(room);player.finish_exit.clear();player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
    await prepare(game,helmet)
    var shown:Texture2D;var ready:=false
    for tick in 1600:
     shown=step(game)
     if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=target:ready=true;break
    check(ready,"Actual cargo route reaches priority test entrance")
    if failures:quit(1);return
    room.suspended=true;shown=step(game)
    check(not player.finish_exit.is_empty(),"Actual ordinary service loss begins candidate exit")
    var state:Dictionary=FLOOR.payload(room).duplicate(true)
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+str(roundi(target*100))
    await record_capture(game,view,name+"-before",shown)
    if event=="fire":room.fire=.5;game.running=true;game.paused=false
    elif event=="flood":room.water_level=1.0;game.running=true;game.paused=false
    elif event=="gear":check(game.bill_npc.set_helmet_equipped(not helmet),"Public gear setter accepted")
    elif event=="death":game.bill_npc.prepare_death_motion(game);game.bill_npc.die()
    else:
     game.placed_rooms.erase(room);game.occupied.erase(CELL);await game.bill_npc.rebuild(game);view.bind_room({})
    shown=step(game)
    check(player.finish_exit.is_empty(),"Priority clears finite ordinary exit on first actual update")
    check(game.bill_npc.animation_state()!="carry","Priority source family replaces stale ordinary carry exit")
    if event=="fire":check(game.bill_npc.goal=="fire-retreat","Actual fire refresh dispatches retreat")
    if event=="flood":check(game.bill_npc.movement_medium=="flooded","Actual flooded room selects flooded medium")
    if event=="gear":check(game.bill_npc.helmet_equipped!=helmet,"Actual gear state changed")
    if event=="death":check(game.bill_npc.dead,"Actual mortality flag retained")
    if event!="removal":check(FLOOR.payload(room)==state,"Priority cannot invent or move released floor case")
    else:check(not game.occupied.has(CELL) and not game.placed_rooms.has(room),"Actual room removal drops owning record")
    game.paused=true
    if event!="removal":await record_capture(game,view,name+"-after",shown)
    else:
     game.selected_room_cell=CELL;game._refresh_all();game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     check(not game.grid_view.content_canvases.has(CELL),"Removed room submits neither actor nor floor prop")
     check(shown.get_image().save_png(OUT+name+"-after-source.png")==OK,"Removed-room replacement source capture")
     check(root.get_texture().get_image().save_png(OUT+name+"-after-room.png")==OK,"Removed-room actual native capture")
     records.append({"name":name+"-after","foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"caseOwned":false,"caseEnabled":false,"embedded":false,"finishActive":false,"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction,"roomRemoved":true})
    for tick in 15:
     step(game);check(player.finish_exit.is_empty(),"Priority cannot resurrect ordinary exit")
     if event!="removal":check(FLOOR.payload(room)==state,"Future priority preserves released floor anchor")
    print("BILL FLOOR FINISH PRIORITY ",name," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"20actual priority takeovers during staged ordinary North service-loss exit: fire refresh, room flooding/medium, public gear, mortality, actual placed-room/occupied removal and topology rebuild. Both gears, before/after release;15future exit/case ticks. Removal is controlled fixture mutation, not demolition UI. No successful refuge/full fall, held-case early disposition, Continue, normal selection or continuous motion acceptance."},"  "))
 print("BILL FLOOR CASE FINISH PRIORITY V1: %d checks,%d failures;20cases"%[checks,failures]);quit(1 if failures else 0)
'''
start=s.index(' var game=await fresh();',s.index('func run():'))
end=s.index(' for event in ["fire"',start)
setup=s[start:end]
s=s[:start]+''' var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
'''+s[end:]
s=s.replace('    game.running=false;game.paused=true','''    if event=="removal":
     game.queue_free();await process_frame;fixture=await new_fixture();game=fixture[0];player=fixture[1];view=fixture[2]
    game.running=false;game.paused=true''')
s=s.replace('func run():','func new_fixture():\n'+setup+' return [game,player,view]\nfunc run():',1)
(R/'tests/test_bill_floor_case_finish_priority_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_floor_case_finish_priority_v1.gd.uid').write_text('uid://p5n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_finish_world_v1_validation.py').read_text()
s=s.replace('bill-floor-case-finish-world-v1','bill-floor-case-finish-priority-v1').replace('test_bill_floor_case_finish_world_v1','test_bill_floor_case_finish_priority_v1').replace('BILL FLOOR CASE FINISH WORLD V1:','BILL FLOOR CASE FINISH PRIORITY V1:').replace('power-helmet-55-completed-room.png','removal-helmet-39-after-room.png')
(R/'tools/run_bill_floor_case_finish_priority_v1_validation.py').write_text(s,encoding='utf-8')
print('20 actual priority takeovers during staged finite exit prepared.')
