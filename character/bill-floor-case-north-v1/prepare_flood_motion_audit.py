from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
view=P/'flood_readability_v2.gd'
s=view.read_text()
if 'static func draw_fading_wake' not in s:
 water=(R/'scripts/flood_visuals.gd').read_text()
 wake=water[water.index('static func draw_crew_wake('):water.index('static func draw_door_currents(')]
 wake=wake.replace('draw_crew_wake','draw_fading_wake').replace('width: float) -> void:','width: float, weight: float) -> void:').replace('clock=condition_clock(clock)','clock=preload("res://scripts/flood_visuals.gd").condition_clock(clock)').replace('Color(0.62,0.76,0.72,alpha)','Color(0.62,0.76,0.72,alpha*weight)')
 view.write_text(s+'\n'+wake.replace(chr(9),' '))
s=(R/'tests/test_bill_floor_case_flood_readability_v1.gd').read_text()
s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-flood-readability-v1','bill-floor-case-flood-motion-v2').replace('finish_player.gd','flood_motion_player.gd').replace('flood_readability_view.gd','flood_readability_v2.gd')
s+='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
 game.running=false;game.paused=true
 for other in [game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
 var actor=game.bill_npc;actor.active=true;actor.dead=false;actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.movement_medium="flooded";actor.state="walk"
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(-112,128)
 for helmet in [false,true]:
  actor.helmet_equipped=helmet
  var gear:String="diving-helmet" if helmet else "";var label:String="helmet" if helmet else "bare"
  var clips:Dictionary=player.equipment_frames[gear] if helmet else player.frames
  var timings:Dictionary=player.equipment_timing[gear] if helmet else player.timing
  for kind in ["swim","tread"]:
   for direction in ["east","south","west","north"]:
    var key:String=kind+"-"+direction
    check(clips.has(key) and timings.has(key),"Complete loaded cardinal water family")
    player.study_key=key;actor.direction=direction;actor.state="walk" if kind=="swim" else "idle"
    var elapsed:=0.0;game.occupied[CELL].water_level=1.0
    for index in clips[key].size():
     player.study_elapsed=elapsed+.00001;game.visual_time_seconds=100+elapsed
     var source:Texture2D=clips[key][index]
     var name:String=label+"-"+key+"-"+str(index)
     for candidate in [false,true]:
      view.readable_water=candidate
      await record_capture(game,view,name+("-candidate" if candidate else "-normal"),source)
      check(game.grid_view._get_human_frame_source(kind,direction)==source,"Prescribed authored source submitted unchanged")
      records.back()["durationMs"]=timings[key].durations[index];records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=1.0
     elapsed+=float(timings[key].durations[index])/1000.0
  actor.direction="east";actor.state="walk";player.study_key="swim-east";player.study_elapsed=.00001;game.visual_time_seconds=100
  var depths:Array=[.55,.60,.65,.70,.75,.80,.84,.849,.85,.851,.86,.90,.95,1.0]
  for index in depths.size():
   game.occupied[CELL].water_level=depths[index]
   var source:Texture2D=clips["swim-east"][0]
   for candidate in [false,true]:
    view.readable_water=candidate
    await record_capture(game,view,label+"-depth-"+str(index)+("-candidate" if candidate else "-normal"),source)
    records.back()["water"]=depths[index];records.back()["durationMs"]=150;records.back()["clock"]=100
    check(game.bill_npc.foot==(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(-112,128),"Root remains fixed through material sweep")
 if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Prescribed loaded authored swim/tread source holds/all four directions/both gears through actual retained room drawing, paired normal/candidate. Fixed-root material sweep including .849/.85/.851. No natural route, safety, physics or full master acceptance."},"  "))
 print("BILL FLOOR CASE FLOOD MOTION V2: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_flood_motion_v2.gd').write_text(s)
for target,uid in [(view,'y5'),(P/'flood_motion_player.gd','z5'),(R/'tests/test_bill_floor_case_flood_motion_v2.gd','a6')]:target.with_suffix(target.suffix+'.uid').write_text(f'uid://{uid}n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_flood_readability_v1_validation.py').read_text().replace('bill-floor-case-flood-readability-v1','bill-floor-case-flood-motion-v2').replace('test_bill_floor_case_flood_readability_v1','test_bill_floor_case_flood_motion_v2').replace('BILL FLOOR CASE FLOOD READABILITY V1:','BILL FLOOR CASE FLOOD MOTION V2:').replace('helmet-alpha90-room.png','helmet-depth-13-candidate-room.png')
(R/'tools/run_bill_floor_case_flood_motion_v2_validation.py').write_text(s)
print('Prepared full loaded cardinal swim/tread native source holds and depth seam study.')
