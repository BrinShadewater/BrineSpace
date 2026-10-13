extends SceneTree
func _init():
 assert(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"))
 for path in ["res://character/bill-land-water-material-west-v6/fixture_main.gd","res://character/bill-land-water-material-west-v6/grid.gd","res://character/bill-land-water-material-west-v6/view.gd","res://character/bill-land-water-material-west-v6/support_actor.gd","res://tests/test_bill_land_water_material_west_v6.gd","res://tools/ensure_bill_water_v6_uids.gd"]:
  if not FileAccess.file_exists(path+".uid"):
   var file=FileAccess.open(path+".uid",FileAccess.WRITE)
   file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
   file.close()
 print("BILL WEST V6: newly created scripts have native resource UID pairs")
 quit()
