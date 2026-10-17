extends "res://tests/test_ward_repair.gd"
func run():
	var path:String="res://character/james-ward-lifecycle-v1/bill_compat.gd.uid"
	if not FileAccess.file_exists(path):
		var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	await super.run()
