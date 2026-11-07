extends "res://tests/test_bill_carry_normal_snapshot_v1.gd"
const FINISH=preload("res://character/bill-floor-case-north-v1/finish_plan.gd")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var p=make_player()
 for gear in ["","diving-helmet"]:
  reset(p);p.clear_carry()
  p.frame("pickup","north",9,Vector2.ONE,gear);p.frame("carry","north",10,Vector2.ONE,gear)
  p.frame("carry","north",10.1,Vector2.ONE,gear)
  check(p.begin_stow(10.1,gear,"north"),"Real selected North arrival plan")
  var original:Dictionary=p.stow_plan.duplicate(true);var durations:Dictionary=p.timing if gear.is_empty() else p.equipment_timing[gear]
  var starts:=0.0
  for index in 14:
   var at:float=float(original.unload_started)+starts+.001
   var shown:Texture2D=p.frame("carry","north",at,Vector2.ONE,gear)
   var exit:Dictionary=FINISH.create(p,shown,gear,at)
   check(not exit.is_empty(),"Every authored unload interior can finish without a jump")
   if exit.is_empty():quit(1);return
   check(FINISH.valid(exit),"Authored finite exit schema admitted")
   for fault in ["binding_time","first_seconds","order","extra","nan"]:
    var bad:Dictionary=exit.duplicate(true)
    if fault=="binding_time":bad.release_at+=.001
    elif fault=="first_seconds":bad.rows[0].seconds+=.001
    elif fault=="order":bad.rows[0].index=(int(bad.rows[0].index)+1)%14
    elif fault=="extra":bad.rows[0].extra=true
    else:bad.started=NAN
    check(not FINISH.valid(bad),"Malformed finite clock/sequence rejected")
   check(FINISH.texture_at(p,exit,at)==shown,"Cancellation entrance is exact displayed texture")
   check(p.stow_plan==original,"Preparing exit leaves active arrival unchanged")
   check(absf(float(exit.until)-(float(original.unload_started)+.64))<.00001,"No restarted crouch or two-second service terminal hold")
   for tick in 40:
    var clock:float=at+tick/60.0
    if clock>=float(exit.until):break
    check(FINISH.texture_at(p,exit,clock)==p.frame("carry","north",clock,Vector2.ONE,gear),"Remaining exit sources follow original authored clock exactly")
   check(FINISH.texture_at(p,exit,exit.until)==null,"Finite exit releases playback at authored end")
   starts+=float(durations["unload-north"].durations[index])/1000.0
  var time:float=float(original.unload_started)+.32
  var shown:Texture2D=p.frame("carry","north",time,Vector2.ONE,gear)
  check(FINISH.create(p,shown,gear,float(original.unload_started)+.39).is_empty(),"Wrong source clock cannot restart stale cancellation")
  check(FINISH.create(p,shown,"diving-helmet" if gear.is_empty() else "",time).is_empty(),"Gear mismatches rejected")
  var terminal_time:float=float(original.unload_started)+.8
  check(FINISH.create(p,p.frame("carry","north",terminal_time,Vector2.ONE,gear),gear,terminal_time).is_empty(),"Extended service hold cannot invent a new authored rise")
  p.stow_plan.clear();check(FINISH.create(p,shown,gear,time).is_empty(),"Cancelled or missing plan cannot create an exit")
 print("BILL FLOOR CASE FINISH PLAN V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
