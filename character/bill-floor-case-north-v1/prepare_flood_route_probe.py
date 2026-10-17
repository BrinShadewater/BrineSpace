from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/bill-floor-case-flood-route-v1';archive=O/'first-stationary-interval';archive.mkdir(exist_ok=True)
for f in O.iterdir():
 if f.is_file() and (f.suffix=='.png' or f.name in ['native.log','validation.json','profile-before.json','profile-after.json']):
  if not (archive/f.name).exists():shutil.copy2(f,archive/f.name)
shutil.copy2(R/'tests/test_bill_floor_case_flood_route_v1.gd',archive/'test_bill_floor_case_flood_route_v1.gd')
s=(R/'tests/test_bill_floor_case_flood_route_v1.gd').read_text();s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-flood-route-v1','bill-floor-case-flood-route-probe-v1')
s+='''func run():
 var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
 game.running=false;game.paused=true;await prepare(game,false)
 var shown:Texture2D
 for tick in 1600:
  shown=step(game)
  if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.39:break
 game.occupied[CELL].suspended=true;shown=step(game)
 game.running=true;game.paused=false
 for tick in 600:
  var seconds:float=float(tick)/60
  game.occupied[CELL].water_level=clampf(seconds/2,0,1) if seconds<6 else clampf(1-(seconds-6)/2,0,1)
  shown=step(game)
  if tick in [0,66,120,240,360,414,599]:
   var actor=game.bill_npc
   var escape:Dictionary=preload("res://scripts/flood_safety.gd").escape_route(game,actor)
   records.append({"tick":tick,"water":game.occupied[CELL].water_level,"foot":[actor.foot.x,actor.foot.y],"medium":actor.movement_medium,"state":actor.animation_state(),"goal":actor.goal,"activity":actor.activity,"stage":actor.stage,"path":str(actor.path),"canStand":actor.can_stand(actor.foot),"swimClear":actor.swim_segment_clear(actor.foot,actor.foot,actor.direction),"escape":str(escape),"air":actor.breath_oxygen,"squeeze":str(actor.squeeze_point)})
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "))
 print("BILL FLOOR CASE FLOOD ROUTE PROBE V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_flood_route_probe_v1.gd').write_text(s)
(R/'tests/test_bill_floor_case_flood_route_probe_v1.gd.uid').write_text('uid://c6n4r6s8t2v5w\n')
runner=(R/'tools/run_bill_floor_case_flood_route_v1_validation.py').read_text().replace('bill-floor-case-flood-route-v1','bill-floor-case-flood-route-probe-v1').replace('test_bill_floor_case_flood_route_v1','test_bill_floor_case_flood_route_probe_v1').replace('BILL FLOOR CASE FLOOD ROUTE V1:','BILL FLOOR CASE FLOOD ROUTE PROBE V1:')
runner=runner.replace("'--resolution','1280x900'","'--headless'")
runner=runner.replace('fresh_photo=photo.exists() and photo.stat().st_mtime>=start_epoch','fresh_photo=True').replace('capture_passed=passed and fresh_photo','capture_passed=passed')
runner=runner.replace("'capturePassed':capture_passed,", "'mode':'headless-controller-probe',").replace("'nativeScreenshot':fresh_photo", "'nativeScreenshot':False")
(R/'tools/run_bill_floor_case_flood_route_probe_v1_validation.py').write_text(runner)
print('Failed stationary native interval retained; diagnostic controller probe prepared.')
