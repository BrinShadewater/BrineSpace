extends SceneTree
## The automatic stall report must not fire while a station is loading: a Continue decodes the
## crew art inside one multi-second frame, and that used to save a report and log a diagnostics
## line into the player's station log every time. A slow frame in play must still be caught.
const Monitor=preload("res://scripts/performance_monitor.gd")
var failures:=0
var checks:=0

class Reporter extends Node:
	var saved: Array[String]=[]
	func save_report(reason: String) -> String:
		saved.append(reason)
		return "user://stall-watch-loading-fixture.zip"
class Station extends Node:
	var startup_complete:=false
	var paused:=false
	# Read by the monitor's once-a-second summary of a station scene.
	var placed_rooms: Array=[]
	var cycle:=0
	var time_speed_index:=0
	var running:=true
	var grid_view=null
	var logged: Array[String]=[]
	func capture_bug_report_snapshot() -> Dictionary: return {}
	func _log(message: String,_important:=false) -> void: logged.append(message)
class Transition extends Node:
	func finish_after_scene_change() -> void: pass

func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:
		failures+=1
		push_error(message)
func _init() -> void:
	call_deferred("run")
## One real frame of the monitor's own _process that took `ms`.
func long_frame(monitor: Node,ms: float) -> void:
	monitor.last_usec=Time.get_ticks_usec()-int(ms*1000.0)
	monitor._process(0.0)
func run() -> void:
	var reporter:=Reporter.new()
	root.add_child(reporter)
	var monitor=Monitor.new()
	reporter.add_child(monitor)
	# A script-run session never captures by itself; switch it on for this fixture only, with
	# breadcrumbs pushed far into the future so nothing is written.
	check(not monitor.auto_capture,"Script-run sessions keep automatic capture off")
	monitor.auto_capture=true
	monitor.breadcrumb_ms=1<<40
	var station:=Station.new()
	root.add_child(station)
	current_scene=station
	await process_frame
	var focused: bool=root.has_focus()

	check(not monitor.loading(null),"No scene and no transition is not loading")
	check(monitor.loading(station),"A station still starting up is loading")
	station.startup_complete=true
	check(not monitor.loading(station),"A started station is not loading")
	var transition:=Transition.new()
	root.add_child(transition)
	check(monitor.loading(station),"The loading transition on screen is loading")
	check(monitor.loading(null),"The loading transition counts before the station scene exists")
	root.remove_child(transition)
	transition.free()
	check(not monitor.loading(station),"Loading ends when the transition leaves")

	# The detector itself, as the frame loop calls it.
	station.startup_complete=false
	monitor._watch_for_stalls(3449.0,monitor.loading(station),false,100000.0)
	check(reporter.saved.is_empty() and station.logged.is_empty(),"A 3.4 s loading frame saves no report and logs nothing")
	station.startup_complete=true
	monitor._watch_for_stalls(3449.0,monitor.loading(station),false,200000.0)
	check(reporter.saved.size()==1 and reporter.saved[0].contains("one frame took 3449 ms"),"The same frame in play still saves a report")
	check(station.logged.size()==1 and station.logged[0].begins_with("DIAGNOSTICS //"),"The play stall is still logged")

	# The frame loop's wiring: the monitor's own _process with a long frame behind it.
	if focused:
		var fresh=Monitor.new()
		reporter.add_child(fresh)
		fresh.auto_capture=true
		fresh.breadcrumb_ms=1<<40
		reporter.saved.clear();station.logged.clear()
		station.startup_complete=false
		long_frame(fresh,3449.0)
		check(reporter.saved.is_empty(),"Frame loop: a long frame during start-up saves no report")
		check(fresh.slow_ms==0.0,"Frame loop: loading does not build toward the slow-seconds trigger")
		station.startup_complete=true
		var overlay:=Transition.new()
		root.add_child(overlay)
		long_frame(fresh,3449.0)
		check(reporter.saved.is_empty(),"Frame loop: a long frame under the loading transition saves no report")
		root.remove_child(overlay)
		overlay.free()
		long_frame(fresh,3449.0)
		check(reporter.saved.size()==1,"Frame loop: a long frame in play saves a report")
		station.paused=true
		fresh.last_auto_ms=-Monitor.AUTO_GAP_MS*2.0
		long_frame(fresh,3449.0)
		check(reporter.saved.size()==1,"Frame loop: a paused station is still exempt")
	print("STALL WATCH LOADING: focused=",focused," checks=",checks," failures=",failures)
	current_scene=null
	station.queue_free()
	reporter.queue_free()
	quit(0 if failures==0 else 1)
