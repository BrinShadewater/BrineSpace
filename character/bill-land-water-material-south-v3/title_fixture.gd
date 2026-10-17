extends "res://character/bill-land-water-material-south-v3/title_fixture_base.gd"
const WET_GATE=preload("res://character/bill-land-water-material-south-v3/title_bridge_envelope.gd")
func _continue_loop()->void:
 var checkpoint:Dictionary=RunSave.read(run_save_path)
 if not WET_GATE.valid(checkpoint):
  error_label.text="STAGED BILL TRANSITION DOES NOT MATCH THE CHECKPOINT."
  return
 super._continue_loop()
