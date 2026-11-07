extends "res://character/bill-floor-case-north-v1/finish_actor.gd"
## Fixture-only planted exit; normal needs/oxygen/hazards still run before move().
var transition_grid
var transition_game
var support_holds:Array=[]
func move(delta:float)->void:
 if transition_grid!=null and transition_game!=null:
  var plan:Dictionary=transition_grid.bridge
  var now:float=transition_game.get_visual_time_seconds()
  var gear:String="diving-helmet" if helmet_equipped else ""
  if not plan.is_empty() and plan.target_state=="walk" and now>=float(plan.started)+.06 and now<float(plan.started)+.5-0.0000001 and active and not dead and movement_medium=="dry" and direction=="west" and gear==plan.gear and stage.is_empty() and goal!="fire-retreat" and not path.is_empty() and foot==plan.last_foot and segment_clear(foot,foot) and swim_segment_clear(foot,foot,"west","west",false,plan.extent):
   support_holds.append({"clock":now,"foot":foot,"path":path.duplicate(),"needs":needs.duplicate(true),"gear":gear})
   state="walk"
   return
 super.move(delta)
