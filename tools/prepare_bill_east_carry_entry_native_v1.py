from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_cargo_handoffs_native_v1.gd').read_text().split(' var grid=game.grid_view;var player=grid.human_water_player;var normal={}')[0]
s=s.replace('bill-east-cargo-handoffs-native-v1','bill-east-carry-entry-native-v1')
s+=''' var grid=game.grid_view;var player=grid.human_water_player
 for manifest in ["res://character/bill-east-carry-master-v1/manifest.json","res://character/bill-east-cargo-handoffs-master-v1/manifest.json","res://character/bill-east-carry-entry-master-v1/manifest.json"]:
  player.load_manifest(manifest,true)
 var row:Array=player.frames["carry-start-east"];var times:Array=player.timing["carry-start-east"].durations
 check(row.size()==6 and times.map(func(t):return int(t))==[40,50,55,65,65,45],"six entry holds retain original320ms")
 check(same(row[0],player.frames["pickup-east"][10]),"exact pickup to first-step whole seam")
 check(same(row[4],player.frames["carry-east"][0]) and same(row[5],row[4]),"exact entry to gait whole seam")
 var origin=Vector2.INF
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and actor.can_stand(point+Vector2(96,0)) and actor.segment_clear(point,point+Vector2(96,0)):origin=point;break
 check(origin.is_finite(),"legal prescribed East carrying segment in actual floor graph")
 if origin.is_finite():
  actor.foot=origin;actor.direction="east";actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+Vector2(96,0)])
  game.paused=false;game.visual_time_seconds=100;player.clear_carry()
  var seen={};var records=[];var entry_started=-1.0;var resumed=false
  for step in range(150):
   var before:Vector2=actor.foot;game.visual_time_seconds+=.005;actor.update(game,.005)
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"actual controller foot movement remains clear")
   if not player.start_motion.is_empty():
    if entry_started<0:entry_started=float(player.start_motion.started)
    var elapsed:float=game.visual_time_seconds-float(player.start_motion.started);var cursor=0.0;var slot=5
    for i in range(6):
     cursor+=float(times[i])/1000.0
     if elapsed<cursor:slot=i;break
    check(same(shown,row[slot]),"actual carry player elapsed dispatch matches entry slot")
    if not seen.has(slot):await capture("actual first-step slot "+str(slot),shown,"carry-start-east",slot,"moving");seen[slot]=true
    records.append({"time":game.visual_time_seconds,"elapsed":elapsed,"slot":slot,"foot":[actor.foot.x,actor.foot.y]})
   elif entry_started>=0 and not resumed:
    check(same(shown,player.frame_at_elapsed("carry-east",.104)),"production resume begins at retained .104 gait clock")
    await capture("actual carry gait resumes",shown,"carry-east",0,"moving");resumed=true
  check(seen.size()==6 and resumed,"actual controller displays all6 entry holds and resumes gait")
  check(actor.foot.x>origin.x+20 and actor.direction=="east","carrying actor moves physically East")
  var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
  file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"scope":"Selected production Bill actor/player with fixture-only master carry/entry/pickup rows. Legal prescribed96-unit East floor segment, actual .005s actor.update and grid submission, all6 entry holds and .104 gait resume, exact whole endpoints. Not natural workshop dispatch/turns, gear, normal admission or Continue."},"\\t"));file.close()
 print("BILL ENTRY: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
s=s.replace('bill-east-carry-entry-native-v1','bill-east-carry-entry-native-v2')
(R/'tools/review_bill_east_carry_entry_native_v2.gd').write_text(s,encoding='utf-8');(R/'tools/review_bill_east_carry_entry_native_v2.gd.uid').write_text('uid://c4billeastent2\n')
runner=(R/'tools/run_bill_east_cargo_handoffs_native_v1.py').read_text().replace('bill-east-cargo-handoffs-native-v1','bill-east-carry-entry-native-v1').replace('bill-east-cargo-handoffs-master-v1','bill-east-carry-entry-master-v1').replace('cargo_handoffs','carry_entry')
runner=runner.replace("len(report.get('captures',[]))==27 and len(report.get('slots',[]))==25","len(report.get('captures',[]))==7 and len(report.get('records',[]))>=60")
runner=runner.replace('bill-east-carry-entry-native-v1','bill-east-carry-entry-native-v2').replace('review_bill_east_carry_entry_native_v1','review_bill_east_carry_entry_native_v2').replace('run_bill_east_carry_entry_native_v1','run_bill_east_carry_entry_native_v2')
runner=runner.replace(' result=inputs()',' result=inputs()\n for folder in ["bill-east-carry-master-v1","bill-east-cargo-handoffs-master-v1"]:\n  for p in (R/"character"/folder).rglob("*"):\n   if p.is_file():result[str(p)]=sha(p)')
(R/'tools/run_bill_east_carry_entry_native_v2.py').write_text(runner,encoding='utf-8')
print('Moving carry entry fixture prepared')
