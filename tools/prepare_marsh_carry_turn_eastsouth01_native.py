"""Stage actual East-to-South path-corner turn with normal actor/player."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_east_carry03_actor.gd').read_text();s=s[:s.index('\tvar route_start :=')]
s=s.replace('east-carry-actor-03','carry-turn-east-south-01').replace('res://character/marsh-east-carry-material-v1/candidate-03/manifest.json','res://character/marsh-carry-turn-material-v1/east-south-01-unselected/manifest.json')
s+='''\tvar route_start:=Vector2.INF
\tvar route_probes:Array=[]
\tfor dy in range(-130,131,20):
\t\tfor dx in range(-120,121,20):
\t\t\tvar candidate:Vector2=desired+Vector2(dx,dy)
\t\t\tvar corner:=candidate+Vector2(64,0)
\t\t\tvar clear:bool=actor.segment_clear(candidate,corner) and actor.segment_clear(corner,corner+Vector2(0,96))
\t\t\tvar blocked:=0
\t\t\tfor leg in range(2):
\t\t\t\tfor travel in range(0,65 if leg==0 else 97,4):
\t\t\t\t\tvar point:Vector2=candidate+Vector2(travel,0) if leg==0 else corner+Vector2(0,travel)
\t\t\t\t\tfor offset in [Vector2.ZERO,Vector2(-25,-45),Vector2(25,-45)]:
\t\t\t\t\t\tif not actor.can_stand(point+offset):clear=false;blocked+=1
\t\t\troute_probes.append({"candidate":[candidate.x,candidate.y],"blockedSamples":blocked,"clear":clear})
\t\t\tif clear:route_start=candidate;break
\t\tif route_start.is_finite():break
\tvar probe_file=FileAccess.open(OUTPUT+"route-probes.json",FileAccess.WRITE);probe_file.store_string(JSON.stringify(route_probes,"\\t"));probe_file.close()
\tcheck(route_start.is_finite(),"actual clear East64/South96 corner with body envelope")
\tif not route_start.is_finite():quit(1);return
\tactor.foot=route_start;actor.state="idle";actor.direction="east";actor.goal="";actor.stage="";actor.path=PackedVector2Array()
\tvar player=game.grid_view.marsh_player
\tplayer.load_manifest("res://character/marsh-east-carry-material-v1/candidate-03/manifest.json",true)
\tplayer.load_manifest("res://character/marsh-south-carry-material-v1/candidate-01/manifest.json",true)
\tplayer.load_manifest(MANIFEST,true)
\tcheck(is_equal_approx(player.cycle_seconds("carry-turn-east-south"),.4),"selected400ms quarter timing retained")
\tcheck(player.frames["carry-turn-east-south"][0].get_image().get_data()==player.frames["carry-east"][0].get_image().get_data(),"exact staged East endpoint loaded")
\tcheck(player.frames["carry-turn-east-south"][4].get_image().get_data()==player.frames["carry-south"][0].get_image().get_data(),"exact staged South endpoint loaded")
\tfor slot in range(5):check(player.frames["carry-turn-east-south"][slot].get_image().get_data()==player.frames["carry-turn-south-east"][4-slot].get_image().get_data(),"reverse whole frame sequence exact")
\tgame.visual_time_seconds=100.0;player.current_key="";player.motion={}
\tawait capture("selected East idle before cargo turn",-1);captures.back()["expectedKey"]="idle-east"
\tactor.state="walk";actor.goal="curiosity";actor.stage="workshop_carry";actor.activity="carrying recovered parts"
\tactor.path=PackedVector2Array([route_start+Vector2(64,0),route_start+Vector2(64,96)])
\tgame.paused=false
\tvar turn_seen:Dictionary={};var south_seen:Dictionary={};var east_seen:=false;var returned:=false;var restores:=0;var last_key:="";var last_slot:=-1
\tfor step in range(140):
\t\tvar before:Vector2=actor.foot;actor.move(.02);game.visual_time_seconds=100.02+step*.02
\t\tvar texture:Texture2D=game.grid_view._get_marsh_frame(game)
\t\tvar key:String=player.motion.get("clip","")
\t\tif key.is_empty():key="carry-"+actor.direction
\t\tvar slot:int=player.frames[key].find(texture)
\t\tcheck(actor.animation_state()=="carry" and not actor.run_motion_active(),"actual workshop path movement remains cargo and excludes running")
\t\tcheck(actor.direction in ["east","south"] and actor.foot.distance_to(before)>0 and actor.foot.distance_to(before)<=46.0*.02+.001,"actual normal carry progresses through path corner within rate46")
\t\tcheck(slot>=0,"normal renderer selects staged carry/turn source")
\t\tif actor.direction=="east" and not east_seen:
\t\t\teast_seen=true;check(key=="carry-east" and slot==0,"initial real East cargo starts frame0")
\t\t\tawait capture("actual East cargo before corner",slot);captures.back()["expectedKey"]=key
\t\tif key=="carry-turn-east-south" and not turn_seen.has(slot):
\t\t\tcheck(slot==turn_seen.size(),"actual400ms turn phases advance0to4")
\t\t\tturn_seen[slot]=true;await capture("actual East-to-South turn pose%d"%slot,slot);captures.back()["expectedKey"]=key
\t\t\tvar saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
\t\t\tcheck(Normal.valid_marsh_snapshot(saved),"actual moving turn actor snapshot valid")
\t\t\tvar restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"turn actor/player restore preserves root and exact intermediate")
\t\t\tgame.paused=true;restored.update(game,.5)
\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause freezes restored moving turn root/source")
\t\t\tgame.paused=false;actor=restored;restores+=1
\t\tif key=="carry-south" and not south_seen.has(slot):
\t\t\tif not returned:
\t\t\t\treturned=true;check(turn_seen.size()==5 and slot==0,"turn completes into exact destination carry frame0")
\t\t\tsouth_seen[slot]=true;await capture("actual destination South cargo pose%d"%slot,slot);captures.back()["expectedKey"]=key
\t\tlast_key=key;last_slot=slot;samples.append({"elapsed":(step+1)*.02,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"playerPhase":player.phase,"animationState":actor.animation_state(),"running":actor.run_motion_active()})
\t\tgame.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
\tcheck(east_seen and returned and turn_seen.size()==5 and south_seen.size()==4 and restores==5,"all real turn/intermediate/destination phases and5restores covered")
\tgame.paused=true;var held:Dictionary=actor.snapshot();var held_texture:Texture2D=game.grid_view._get_marsh_frame(game);actor.update(game,.5)
\tcheck(actor.snapshot()==held and game.grid_view._get_marsh_frame(game).get_image().get_data()==held_texture.get_image().get_data(),"final cargo pause preserves root/source")
\tawait capture("paused South cargo after actual path turn",last_slot);captures.back()["expectedKey"]=last_key
\tvar file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"actorRestores":restores,"turnSlots":turn_seen.keys(),"destinationSlots":south_seen.keys(),"scope":"Actual normal Marsh.move workshop_carry on clear East64/South96 path corner,normal factory/main/grid/player with staged carries/quarter turn;140controlled20ms samples,five moving turn actor/player restores+pause holds,exact destination frame0 return,all4 destination phases. No full RunSave/visible TitleContinue,reverse path-turn,complete pickup/unload or continuous contact acceptance."},"\\t"));file.close()
\tprint("MARSH EAST SOUTH CARGO TURN: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
'''
p=ROOT/'tools/review_marsh_carry_turn_eastsouth01_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://de2ehstrn1v98\n')
print('Prepared actual normal East64/South96 path-turn fixture and paired UID; staged only.')

