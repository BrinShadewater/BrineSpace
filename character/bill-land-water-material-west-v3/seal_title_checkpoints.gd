extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const GATE=preload("res://character/bill-land-water-material-west-v3/title_bridge_envelope.gd")
const INPUT="res://character/bill-land-water-material-west-v3/fresh-checkpoint-review/"
const OUTPUT="res://character/bill-land-water-material-west-v3/title-checkpoint-review/"
func _init():
 DirAccess.make_dir_recursive_absolute(OUTPUT)
 for name in ["bare-81","bare-432","helmet-81","helmet-432"]:
  var data:Dictionary=SAVE.read(INPUT+"bill-water-"+name+".loop")
  var file=FileAccess.open(INPUT+name+"-bridge.bin",FileAccess.READ)
  if data.is_empty() or file==null:quit(1);return
  data.erase("_path");data.staged_bill_water_bridge=file.get_var(false);file.close()
  if not GATE.valid(data) or not SAVE.problem(data).is_empty():quit(1);return
  var bytes:PackedByteArray=var_to_bytes(data)
  file=FileAccess.open(OUTPUT+name+".loop",FileAccess.WRITE)
  file.store_string(bytes.hex_encode().sha256_text()+"\n");file.store_buffer(bytes);file.close()
 print("BILL TITLE CHECKPOINT SEAL: 4 normal-compatible checksummed staged envelopes")
 quit(0)
