extends "res://tests/test_branforth_crew.gd"
func _init()->void:
	var path:="res://character/james-west-carry-walk-keys-v1/arrival-controller-v322/crew_regression.gd.uid"
	if not FileAccess.file_exists(path):var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	super()
