from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_flood_route_v1.gd').read_text()
s=s.replace('bill-floor-case-flood-route-v1','bill-floor-case-flood-navigation-v1')
start=s.index('  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;')
end=s.index('  var label:String=',start)
s=s[:start]+'''  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].water_level=0.0
  var actor=game.bill_npc;actor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.breath_oxygen=15;actor.tank_oxygen=60;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  for other in [game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
  await actor.rebuild(game)
  var pair:Array=[];var best:=0.0
  for a in actor.room_nodes[CELL]:
   var from:Vector2=actor.graph.get_point_position(a)
   for b in actor.room_nodes[CELL]:
    var to:Vector2=actor.graph.get_point_position(b);var length:float=from.distance_to(to)
    if absf(from.y-to.y)>.01 or length<best or length<100:continue
    if actor.segment_clear(from,to) and actor.swim_segment_clear(from,to,"east") and actor.swim_segment_clear(to,from,"west"):
     pair=[from,to] if from.x<to.x else [to,from];best=length
  check(pair.size()==2,"Actual room graph supplies collision-clear dry/swim navigation segment")
  if pair.is_empty():quit(1);return
  actor.foot=pair[0];actor.direction="east";actor.goal="flood-retreat";actor.goal_cell=CELL;actor.state="walk";actor.path=PackedVector2Array([pair[1],pair[0],pair[1],pair[0]]);actor.activity="prescribed collision-clear route"
  var shown:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
'''+s[end:]
# The per-tick local actor would shadow setup actor. Use its existing reference.
s=s.replace('var actor=game.bill_npc;distance+=','distance+=')
s=s.replace(' game.bill_npc.observe_finish(game,shown)',' if game.bill_npc.has_method("observe_finish"):game.bill_npc.observe_finish(game,shown)')
s=s.replace('No natural hydrology, whole station loop or normal production admission.','Initial graph-validated path prescribed; subsequent movement and safety use actual controller. No natural job dispatch/hydrology, whole station loop or normal production admission.')
s=s.replace('BILL FLOOR CASE FLOOD ROUTE V1:','BILL FLOOR CASE FLOOD NAVIGATION V1:')
(R/'tests/test_bill_floor_case_flood_navigation_v1.gd').write_text(s)
(R/'tests/test_bill_floor_case_flood_navigation_v1.gd.uid').write_text('uid://d6n4r6s8t2v5w\n')
runner=(R/'tools/run_bill_floor_case_flood_route_v1_validation.py').read_text().replace('bill-floor-case-flood-route-v1','bill-floor-case-flood-navigation-v1').replace('test_bill_floor_case_flood_route_v1','test_bill_floor_case_flood_navigation_v1').replace('BILL FLOOR CASE FLOOD ROUTE V1:','BILL FLOOR CASE FLOOD NAVIGATION V1:')
(R/'tools/run_bill_floor_case_flood_navigation_v1_validation.py').write_text(runner)
print('Separate moving-route fixture uses actual clear graph segment; failed unload-boundary evidence retained.')
