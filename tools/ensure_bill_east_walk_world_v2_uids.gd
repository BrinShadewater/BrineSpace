extends SceneTree
func _init():
 assert(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"))
 for path in ["res://tools/review_bill_east_walk_world_v2.gd","res://tools/ensure_bill_east_walk_world_v2_uids.gd"]:
  if not FileAccess.file_exists(path+".uid"):
   var file=FileAccess.open(path+".uid",FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");file.close()
 quit()
