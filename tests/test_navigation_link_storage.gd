extends SceneTree
const NPC=preload("res://scripts/bill_npc.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
 var actor=NPC.new()
 var key="storage-regression"
 var locals=[Vector2i(-16,0),Vector2i(0,0),Vector2i(16,16)]
 actor.room_cache[key]={"points":locals,"links":[[locals[0],locals[1]],[locals[1],locals[2]]],"data":{}}
 actor.room_nodes[Vector2i.ZERO]=[]
 var ids=actor.append_cached_room_points(Vector2i.ZERO,Vector2.ZERO,key)
 actor.append_cached_room_links(key,ids)
 check(not actor.room_cache[key].has("links"),"Packed admission releases nested pair arrays")
 check(actor.room_cache[key].packed_links==PackedInt32Array([0,1,1,2]),"Canonical link order unchanged")
 check(actor.graph.get_id_path(0,2)==PackedInt64Array([0,1,2]),"Original route unchanged")
 actor.append_cached_room_links(key,ids)
 check(actor.graph.get_point_connections(1)==PackedInt64Array([0,2]),"Repeated admission preserves ordered connections")
 actor.room_cache.erase(key)
 print("NAVIGATION LINK STORAGE ",checks," checks ",failures," failures");quit(1 if failures else 0)
