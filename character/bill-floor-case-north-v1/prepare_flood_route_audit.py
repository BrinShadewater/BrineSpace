from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_flood_visibility_v1.gd').read_text()
s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-flood-visibility-v1','bill-floor-case-flood-route-v1').replace('flood_diagnostic_view.gd','flood_readability_v2.gd')
s=s.replace('''  if game.grid_view.content_canvases.has(CELL):
   for slot in game.grid_view.content_canvases[CELL].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[CELL].renderer.external_actor_texture==texture:submitted=true''','''  for cell in game.grid_view.content_canvases:
   for slot in game.grid_view.content_canvases[cell].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[cell].renderer.external_actor_texture==texture:submitted=true''')
s+='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 for helmet in [false,true]:
  var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].water_level=0.0
  await prepare(game,helmet)
  var shown:Texture2D;var ready:=false
  for tick in 1600:
   shown=step(game)
   if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.39:ready=true;break
  check(ready,"Actual cargo route reaches released exit entrance")
  game.occupied[CELL].suspended=true;shown=step(game);check(not player.finish_exit.is_empty(),"Actual ordinary exit begins")
  var label:String="helmet" if helmet else "bare";var first:Vector2=game.bill_npc.foot;var distance:=0.0;var previous:Vector2=first;var saw_water:=false;var saw_dry_after:=false;var states:Dictionary={}
  game.running=true;game.paused=false
  for tick in 600:
   # Prescribed room water history isolates animation/material joins; actual
   # medium selection, oxygen, safety, actor navigation and source clock advance.
   var seconds:float=float(tick)/60.0
   var water:float=clampf(seconds/2.0,0,1) if seconds<6 else clampf(1-(seconds-6)/2.0,0,1)
   game.occupied[CELL].water_level=water
   shown=step(game)
   var actor=game.bill_npc;distance+=previous.distance_to(actor.foot);previous=actor.foot
   saw_water=saw_water or actor.movement_medium=="flooded";saw_dry_after=saw_dry_after or (saw_water and actor.movement_medium=="dry")
   states[actor.animation_state()]=true
   check(not actor.dead,"Real oxygen/failure rules keep ten-second route alive")
   if tick%2==0:
    game.paused=true;view.readable_water=true
    var name:String=label+"-"+str(tick).pad_zeros(3)
    await record_capture(game,view,name+"-candidate",shown)
    records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    if tick%20==0 or tick in [64,66,68,400,402,404]:
     view.readable_water=false;await record_capture(game,view,name+"-normal",shown)
     records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    game.paused=false
   if failures:quit(1);return
  check(distance>20,"Actual controller advances physical route")
  check(saw_water and saw_dry_after,"Actual room medium crosses dry/water/dry")
  check(states.has("swim") or states.has("tread"),"Actual source selection enters water family")
  records.append({"name":label+"-summary","distance":distance,"states":states.keys(),"sawWater":saw_water,"sawDryAfter":saw_dry_after})
  game.queue_free();await process_frame
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Actual actor/world-medium/oxygen/safety/navigation and source clock at60Hz; native capture every2ticks/30Hz. Prescribed ten-second room-water rise/hold/drain, fixture-selected actor/player/workshop treatment. No natural hydrology, whole station loop or normal production admission."},"  "))
 print("BILL FLOOR CASE FLOOD ROUTE V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_flood_route_v1.gd').write_text(s)
(R/'tests/test_bill_floor_case_flood_route_v1.gd.uid').write_text('uid://b6n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_flood_motion_v2_validation.py').read_text().replace('bill-floor-case-flood-motion-v2','bill-floor-case-flood-route-v1').replace('test_bill_floor_case_flood_motion_v2','test_bill_floor_case_flood_route_v1').replace('BILL FLOOR CASE FLOOD MOTION V2:','BILL FLOOR CASE FLOOD ROUTE V1:').replace('helmet-depth-13-candidate-room.png','helmet-598-candidate-room.png')
(R/'tools/run_bill_floor_case_flood_route_v1_validation.py').write_text(s)
print('Prepared real controller/medium route capture at60Hz, native30Hz, both gears.')
