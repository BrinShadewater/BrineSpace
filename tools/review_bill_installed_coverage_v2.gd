extends SceneTree
const OUT="res://output/bill-installed-coverage-v2/"
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"scratch profile")
 var audit:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-installed-coverage-2026-10-04/source-audit.json"))
 var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
 check(player.carry_binding()==player.MASTER_BINDING,"actual loader default version")
 var slots=0;var summaries={}
 for gear in ["bare","helmet"]:
  var rows:Dictionary=player.frames if gear=="bare" else player.equipment_frames["diving-helmet"]
  var clock:Dictionary=player.timing if gear=="bare" else player.equipment_timing["diving-helmet"]
  check(rows.size()==audit.selected[gear].size(),"all selected keys resolved")
  summaries[gear]={"states":rows.size(),"slots":0}
  for key in rows:
   check(audit.selected[gear].has(key),"selected key mapped "+key)
   if not audit.selected[gear].has(key):continue
   var state:Dictionary=audit.selected[gear][key]
   check(rows[key].size()==state.files.size(),"complete selected row "+key)
   check(clock[key].durations==state.timing and clock[key].loop==state.loop,"exact authored clock "+key)
   for i in range(rows[key].size()):
    var expected=Image.new();check(expected.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+str(state.files[i])))==OK,"raw expected PNG decoded");expected.convert(Image.FORMAT_RGBA8)
    if state.mirrored:expected.flip_x()
    var actual:Image=rows[key][i].get_image();actual.convert(Image.FORMAT_RGBA8)
    check(actual.get_data()==expected.get_data(),"exact selected RGBA "+gear+"/"+key+"/"+str(i))
    check(rows[key][i].get_meta("crew_standing_height")==float(state.standingHeight),"source density "+key)
    slots+=1;summaries[gear].slots+=1
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"selectedSlots":slots,"summary":summaries,"scope":"Actual normal loader materialized all selected rows, exact source RGBA/timing/density. Headless source inventory only; existing native/visual evidence retained separately."},"  "))
 grid.free();print("BILL INSTALLED COVERAGE: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
