from pathlib import Path
P=Path(__file__).resolve().parent
base=P.parent/'james-cup-pickup-north-v1/native-journey.gd'
source=base.read_text().split('func checkpoint(')[0].replace('res://character/james-cup-pickup-north-v1/','res://character/james-meal-interrupt-north-v1/')
header=base.read_text().split('func run()->void:\n',1)[1].split('\tfor q in [0]:',1)[0]
header=header.replace('res://character/james-cup-pickup-north-v1/','res://character/james-meal-interrupt-north-v1/')
source+='func run()->void:\n'+header+'''\tvar phases:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
\tfor issue in ["power-loss","food-empty","complete"]:
\t\tfor phase in (phases if issue!="complete" else ["cup-deposit"]):
\t\t\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\t\t\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\t\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\t\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\t\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\t\t\tnpc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.helmet_returning=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
\t\t\tnpc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2.DOWN*384,cell+Vector2i.DOWN));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry"
\t\t\tnpc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.visits.clear();player.motion.clear();player.current_key="";player.last_time=-1;game.resources.food=1000;game.visual_time_seconds=100
\t\t\tnpc.decision_rng.seed=1;npc.choose_goal(game)
\t\t\tcheck(npc.goal=="hunger" and npc.goal_cell==cell and not npc.path.is_empty(),"Actual normal hunger chooser enters galley")
\t\t\tvar ticks:=0;var reached:=false
\t\t\twhile ticks<3000 and not reached:
\t\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\t\tif npc.animation_state()==phase:
\t\t\t\t\tvar slot:int=player.frames[phase+"-north"].find(texture)
\t\t\t\t\tif slot==3:reached=true
\t\t\tcheck(reached,"Actual normal meal reaches requested interruption pose")
\t\t\tvar before:Dictionary=npc.snapshot();var before_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
\t\t\tvar pictures:Array=[await capture(issue+"-"+phase+"-before",npc)]
\t\t\tif issue=="power-loss":game.powered_room_cells.erase(cell)
\t\t\tif issue=="food-empty":game.resources.food=0
\t\t\tvar credited:=0.0;var left:=false;var after_ticks:=0
\t\t\twhile after_ticks<1600 and not left:
\t\t\t\tvar hunger:float=npc.needs.hunger;var old_stage:String=npc.stage
\t\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;after_ticks+=1
\t\t\t\tvar relief:float=hunger-float(npc.needs.hunger)
\t\t\t\tif relief>1:credited+=relief+.12*preload("res://scripts/research_tree.gd").needs_rate(game.meta)/120
\t\t\t\tif after_ticks==1:
\t\t\t\t\tvar after_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
\t\t\t\t\tpictures.append(await capture(issue+"-"+phase+"-after",npc))
\t\t\t\t\tresults.append({"issue":issue,"phase":phase,"before":before,"after":npc.snapshot(),"samePixels":after_pixels==before_pixels,"captures":pictures})
\t\t\t\tleft=npc.stage not in ["life_eat","life_drink"]
\t\t\tcheck(left,"Meal completes or is genuinely cancelled")
\t\t\tcheck(absf(credited-(45.0 if issue=="complete" else 0.0))<.001,"Exactly one normal meal relief; no cancelled/empty-food relief")
\t\t\tresults[-1]["credited"]=credited;results[-1]["afterTicks"]=after_ticks
\tvar file:=FileAccess.open(OUT+"native-audit-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Thirteen actual default North galley journeys from normal hunger chooser: six power losses, six depleted-food continuations, one normal completion. Audit immediate pose continuity and hunger credit; no abort choreography or Continue proof claimed."},"  "));file.close()
\tprint("JAMES MEAL INTERRUPTION AUDIT: ",checks," checks; ",failures," failures; ",results.size()," actual journeys")
\tquit(1 if failures else 0)
'''
(P/'native-audit.gd').write_text(source)
print('Created thirteen actual meal interruption/credit audit journeys')
