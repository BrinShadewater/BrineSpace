extends SceneTree
const NPC=preload("res://scripts/companion_npc.gd")
const Companions=preload("res://scripts/companions.gd")
class Fixture extends RefCounted:
	var companion_actors: Dictionary={}
	var companion_roster: Array=[]
var failures:=0
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func _init():
	var fixture:=Fixture.new()
	for id in Companions.IDS:fixture.companion_actors[id]=NPC.new(id)
	var previous:=fixture.companion_actors.duplicate()
	for actor in previous.values():
		actor.player.phase=123.0;actor.player.current_key="old-playback"
		actor.behavior="old-behavior";actor.path=[Vector2(12,34)]
	Companions.restore(fixture,null)
	var textures:=0
	for id in Companions.IDS:
		var old=previous[id];var fresh=fixture.companion_actors[id]
		check(old!=fresh,"Fresh actor: "+id)
		check(old.player!=fresh.player and old.poses!=fresh.poses,"Independent players: "+id)
		check(fresh.player.phase==0.0 and fresh.player.current_key.is_empty(),"Fresh clock: "+id)
		check(fresh.behavior.is_empty() and fresh.path.is_empty(),"Fresh behavior: "+id)
		for pair in [[old.player,fresh.player],[old.poses,fresh.poses]]:
			check(pair[0].frames.keys()==pair[1].frames.keys(),"Clip coverage: "+id)
			check(pair[0].timing==pair[1].timing and pair[0].strides==pair[1].strides,"Timing: "+id)
			for key in pair[0].frames:
				for i in range(pair[0].frames[key].size()):
					check(pair[0].frames[key][i]==pair[1].frames[key][i],"Reuse texture: "+id+key)
					textures+=1
			var key=pair[1].frames.keys()[0]
			var count:int=pair[0].frames[key].size()
			pair[1].frames[key].clear()
			check(pair[0].frames[key].size()==count,"Independent rows: "+id)
			var duration=pair[0].timing[key].durations[0]
			pair[1].timing[key].durations[0]=99999
			check(pair[0].timing[key].durations[0]==duration,"Independent durations: "+id)
		fresh.swim_clearance.clear()
		if id!="josh":check(not old.swim_clearance.is_empty(),"Independent clearance: "+id)
	var mismatched=NPC.new("josh",previous.river)
	check(mismatched.identity=="josh" and mismatched.player.frames.has("walk-east"),"Wrong identity loads own art")
	check(mismatched.player.frames["walk-east"][0]!=previous.river.player.frames["walk-east"][0],"No cross-identity reuse")
	print("COMPANION ART REUSE: ",textures," texture references, ",failures," failures")
	quit(failures)
