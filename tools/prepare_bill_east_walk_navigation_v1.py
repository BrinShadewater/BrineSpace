"""Create a real actor-update/distance-clock room traversal probe."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/review_bill_east_walk_world_v2.gd').read_text(encoding='utf-8')
source=source[:source.index(' var camera_foot=actor.foot')].replace('bill-east-walk-world-v2','bill-east-walk-navigation-v1')
source+=''' var left=Vector2.ZERO;var right=Vector2.ZERO;var longest=0.0
 for a in actor.room_nodes.get(CELL,[]):
  var pa:Vector2=actor.graph.get_point_position(a)
  if not actor.can_stand(pa):continue
  for b in actor.room_nodes.get(CELL,[]):
   var pb:Vector2=actor.graph.get_point_position(b)
   if absf(pa.y-pb.y)>.01 or pb.x-pa.x<=longest:continue
   if actor.can_stand(pb) and actor.segment_clear(pa,pb):left=pa;right=pb;longest=pb.x-pa.x
 check(longest>138.0,"actual furnished room permits two complete East gait cycles")
 if longest<=138.0:quit(1);return
 var traversals=[]
 for variant in ["candidate","selected"]:
  for key in ["idle-east","walk-east"]:
   var state=key.get_slice("-",0)
   grid.human_animations[state]["east"]=player.frames[key].duplicate() if variant=="candidate" else normal[key].duplicate()
  actor.foot=left;actor.path.clear();actor.direction="east";actor.state="idle";actor.stage="";actor.goal="";actor.timer=20;actor.movement_heading.clear();actor.avoidance_positions=PackedVector2Array();actor.avoidance_position=Vector2.INF
  grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100.0;game.paused=false
  var visited={};var walk_steps=0;var total_distance=0.0;var elapsed=0.0
  for i in range(16):
   game.visual_time_seconds+=.02;actor.update(game,.02);var shown=grid._get_human_frame_source(actor.state,actor.direction)
   if i%4==0:await capture("idle before",shown,"idle-east",i,variant)
  actor.path=PackedVector2Array([right]);actor.goal="construction";actor.goal_cell=CELL;actor.state="walk";actor.timer=0
  grid._get_human_frame_source("walk","east")
  while not actor.path.is_empty() and walk_steps<600:
   var previous=actor.foot;var old_phase=grid.human_animation_phase
   game.visual_time_seconds+=.02;actor.update(game,.02);elapsed+=.02;walk_steps+=1
   check(actor.can_stand(actor.foot),"real actor update keeps legal floor contact")
   check(actor.direction=="east","real actor move retains East facing")
   var distance=previous.distance_to(actor.foot);total_distance+=distance
   check(distance<=actor.movement_rate()*.02+.01,"actual movement bounded by actor speed")
   var shown:Texture2D=grid._get_human_frame_source(actor.state,actor.direction)
   var slot=-1
   for n in range(grid.human_animations[actor.state][actor.direction].size()):
    if same(shown,grid.human_animations[actor.state][actor.direction][n]):slot=n;break
   check(slot>=0,"real source belongs to current state bank")
   if actor.state=="walk":
    visited[slot]=true
    var increment=distance/384.0/float(grid.human_stride_distance.get("walk-east",grid.human_stride_distance["walk"]))*2.0
    check(absf(grid.human_animation_phase-old_phase-increment)<.0001,"renderer gait advances from actual traveled distance")
   samples.append({"variant":variant,"step":walk_steps,"elapsed":elapsed,"state":actor.state,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"phase":grid.human_animation_phase,"distance":distance})
   if walk_steps%4==0 or actor.path.is_empty():await capture("walking route",shown,actor.state+"-east",slot,variant)
  check(actor.path.is_empty() and actor.foot.distance_to(right)<.01,"actual actor move reaches legal destination")
  check(actor.state=="idle","actual arrival selects idle")
  check(visited.size()>=46,"distance-driven route visits almost every gait phase")
  for i in range(16):
   game.visual_time_seconds+=.02;var shown=grid._get_human_frame_source(actor.state,actor.direction)
   if i%4==0:await capture("idle after",shown,"idle-east",i,variant)
  traversals.append({"variant":variant,"steps":walk_steps,"distance":total_distance,"duration":elapsed,"visitedSlots":visited.keys(),"arrived":actor.path.is_empty()})
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"traversals":traversals,"route":{"left":[left.x,left.y],"right":[right.x,right.y],"length":longest},"scope":"Actual Bill.update/move/arrive and distance-driven retained bare renderer in default furnished ColdStore. Candidate/selected same legal route. Explicit route and source binding, simulation stepped .02s with main/tick timer disabled; not autonomous goal choice, normal admission, gear/water or save/TitleContinue."},"\\t"));file.close();print("BILL WALK NAVIGATION: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_walk_navigation_v1.gd').write_text(source,encoding='utf-8')
uids=(R/'tools/ensure_bill_east_walk_world_v2_uids.gd').read_text(encoding='utf-8').replace('walk_world_v2','walk_navigation_v1')
(R/'tools/ensure_bill_east_walk_navigation_v1_uids.gd').write_text(uids,encoding='utf-8')
runner=(R/'tools/run_bill_east_walk_world_v2.py').read_text(encoding='utf-8').replace('walk_world_v2','walk_navigation_v1').replace('walk-world-v2','walk-navigation-v1')
runner=runner.replace("len(report.get('captures',[]))==40","len(report.get('traversals',[]))==2 and all(t['arrived'] for t in report.get('traversals',[]))")
runner=runner.replace("'sourceSoleDepthAccepted':True","'sourceSoleDepthAccepted':False,'naturalActorMovementTested':True,'autonomousGoalChoiceTested':False")
(R/'tools/run_bill_east_walk_navigation_v1.py').write_text(runner,encoding='utf-8')
print('Prepared actual actor navigation/update and distance-clock comparison.')
