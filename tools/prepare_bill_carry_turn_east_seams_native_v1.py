from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_cargo_handoffs_native_v1.gd').read_text().split(' var grid=game.grid_view;var player=grid.human_water_player;var normal={}')[0].replace('bill-east-cargo-handoffs-native-v1','bill-carry-turn-east-seams-native-v1')
s+=''' var grid=game.grid_view;var player=grid.human_water_player
 for manifest in ["res://character/bill-east-carry-master-v1/manifest.json","res://character/bill-east-cargo-handoffs-master-v1/manifest.json","res://character/bill-east-carry-entry-master-v1/manifest.json","res://character/bill-carry-turn-east-seams-v1/manifest.json"]:player.load_manifest(manifest,true)
 var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-carry-turn-east-seams-v1/review.json"));var cases=[]
 game.paused=false;game.visual_time_seconds=100
 for contract in review.records:
  var key:String=contract.key;var from_direction:String=key.get_slice("-",2);var to_direction:String=key.get_slice("-",3)
  var delta:Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[to_direction]*96
  var origin=Vector2.INF
  for id in actor.room_nodes.get(CELL,[]):
   var point:Vector2=actor.graph.get_point_position(id)
   if actor.can_stand(point) and actor.can_stand(point+delta) and actor.segment_clear(point,point+delta):origin=point;break
  check(origin.is_finite(),"legal actual floor segment for "+key)
  if not origin.is_finite():continue
  var row:Array=player.frames[key];var durations:Array=player.timing[key].durations
  check(durations==contract.originalState.frameDurationsMs and row.size()==contract.originalState.frameFiles.size(),"complete original turn clock/poses retained")
  for index in contract.changedSlots:check(same(row[int(index)],player.frames["pickup-east"][10]),"exact repaired shared East whole turn pose")
  player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
  actor.foot=origin;actor.direction=from_direction;actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+delta]);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  var seen={};var resumed=false;var records=[];var onset=-1.0
  for step in range(450):
   var before:Vector2=actor.foot;game.visual_time_seconds+=.005;actor.update(game,.005)
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"actual turn floor contact clear")
   if str(player.motion.get("clip",""))==key:
    if onset<0:onset=float(player.motion.started)
    var elapsed:float=game.visual_time_seconds-float(player.motion.started);var cursor=0.0;var slot=row.size()-1
    for i in range(row.size()):
     cursor+=float(durations[i])/1000
     if elapsed<cursor:slot=i;break
    check(same(shown,row[slot]),"actual production turn source identity")
    check(actor.foot.distance_to(origin)<.0001,"production carry pivot remains planted")
    if not seen.has(slot):await capture(key+" / slot "+str(slot),shown,key,slot,"actual-turn");seen[slot]=true
    records.append({"time":game.visual_time_seconds,"elapsed":elapsed,"slot":slot,"foot":[actor.foot.x,actor.foot.y]})
   elif onset>=0 and actor.foot.distance_to(origin)>.01:
    resumed=true;break
  check(seen.size()==row.size() and resumed,"full actual planted turn then resumed movement: "+key)
  check(actor.direction==to_direction,"turn retains requested physical heading")
  cases.append({"key":key,"seen":seen.keys(),"records":records,"resumed":resumed})
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"cases":cases,"scope":"Seven selected-production carry turn programs with fixture-only repaired bare East endpoint/entry/gait. Actual .005s actor.update on prescribed legal96-unit floor segments: full57turn slots, planted pivots and resumed physical headings. Original800/1600ms clocks; seven exact whole East aliases,50other poses unchanged. Not natural dispatch, continuous cadence, equipment, normal admission or Continue."},"\\t"));file.close()
 print("BILL TURN SEAMS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_carry_turn_east_seams_native_v1.gd').write_text(s,encoding='utf-8');(R/'tools/review_bill_carry_turn_east_seams_native_v1.gd.uid').write_text('uid://c4billeasttrn1\n')
runner=(R/'tools/run_bill_east_carry_entry_native_v2.py').read_text().replace('bill-east-carry-entry-native-v2','bill-carry-turn-east-seams-native-v1').replace('bill-east-carry-entry-master-v1','bill-carry-turn-east-seams-v1').replace('carry_entry','carry_turn_east_seams').replace('native_v2','native_v1')
runner=runner.replace("['prepare_bill_east_carry_turn_east_seams_master_v1.py','build_bill_east_carry_turn_east_seams_master_v1.py','prepare_bill_east_carry_turn_east_seams_native_v1.py','review_bill_east_carry_turn_east_seams_native_v1.gd','review_bill_east_carry_turn_east_seams_native_v1.gd.uid','run_bill_east_carry_turn_east_seams_native_v1.py']","['build_bill_carry_turn_east_seams_v1.py','prepare_bill_carry_turn_east_seams_native_v1.py','review_bill_carry_turn_east_seams_native_v1.gd','review_bill_carry_turn_east_seams_native_v1.gd.uid','run_bill_carry_turn_east_seams_native_v1.py']")
runner=runner.replace('review_bill_east_carry_turn_east_seams_native_v1','review_bill_carry_turn_east_seams_native_v1').replace('run_bill_east_carry_turn_east_seams_native_v1','run_bill_carry_turn_east_seams_native_v1')
runner=runner.replace('["bill-east-carry-master-v1","bill-east-cargo-handoffs-master-v1"]','["bill-east-carry-master-v1","bill-east-cargo-handoffs-master-v1","bill-east-carry-entry-master-v1"]')
runner=runner.replace("len(report.get('captures',[]))==7 and len(report.get('records',[]))>=60","len(report.get('captures',[]))==57 and len(report.get('cases',[]))==7")
(R/'tools/run_bill_carry_turn_east_seams_native_v1.py').write_text(runner,encoding='utf-8')
print('Seven actual production turn cases prepared')
