extends RefCounted
## Authored opinions only: room operation and resource figures come from live state.
const GREETINGS={
	"marsh":"I am available. Current task: %s. What requires attention?",
	"bill":"You have my attention. Current task: %s. What needs looking at?",
	"veld":"I can spare a moment. Current task: %s. What have you noticed?",
	"branforth":"I'm listening. Current task: %s. Tell me where to start."}
const STEADY={
	"marsh":"The essential reserves are stable. I have retained the previous readings for comparison.",
	"bill":"The essential reserves are holding steady. Let's check the connections before we stretch the station any further.",
	"veld":"No essential reserve is declining in the current forecast. A stable reading is useful. A second one is more convincing.",
	"branforth":"The essential supplies are keeping up. I'd inspect the existing connections before adding another load."}
const SHORTAGES={
	"marsh":"%s is falling: %d in reserve, %.1f used per cycle. The deficit requires a correction.",
	"bill":"%s is falling: %d in reserve, %.1f used per cycle. That is the first thing I'd address.",
	"veld":"%s is falling: %d in reserve, %.1f used per cycle. The trend concerns me more than the number.",
	"branforth":"%s is falling: %d in reserve, %.1f used per cycle. Let's check supply and demand before adding another load."}
const ROOM_LINES={
	"brine_core":{
		"bill":"I prefer a command room with someone behind the controls. I'm still deciding whether this counts.",
		"veld":"BRINE remembers things we don't. I would like to distinguish damaged records from things she chooses not to say.",
		"branforth":"A lot of the station comes back to this room. I don't like single points of failure, even when they can argue."},
	"pressure_control":{
		"bill":"A gauge gives us something to act on before a door becomes difficult to open. I appreciate the warning.",
		"veld":"Pressure readings need context. One moving needle is an observation; several moving together deserve attention.",
		"branforth":"Valves, seals, gauges. Start with the connections you can inspect before blaming the instrument."},
	"listening_post":{
		"bill":"I'd like to know what's moving outside before it reaches the hull. This seems a reasonable place to listen.",
		"veld":"First record what the station itself sounds like. Otherwise every loose fitting becomes a discovery.",
		"branforth":"Pumps and bearings have their own voices. Learn those first. Then we can worry about the unfamiliar ones."},
	"crew_hab":{
		"bill":"A place to rest matters. People make worse decisions when every room feels like a shift that hasn't ended.",
		"veld":"I would like somewhere to put my notes where I don't have to move them to eat. This has possibilities.",
		"branforth":"A berth and a little quiet. If something starts rattling in here, I expect to hear about it."},
	"salvage_workshop":{
		"bill":"A place to decide what is worth keeping. I'd rather make that decision at a bench than in a corridor.",
		"veld":"Label what comes off the wreckage. A part without its history can answer entirely the wrong question.",
		"branforth":"Room to lay things out and see what fits. Keep the useful stock separate from the parts we're still suspicious of."}}
# Josh speaks; River answers in chirps with a status-lamp translation; Margot answers as a cat.
# Lines rotate per click.
const COMPANION_GREETINGS={
	"josh":[
		"Josh here. Current task: %s. My treads are clean and my optics are clear. What should we look at?",
		"Hello again. I watched the crew weld a seam today. I would like to try. I have been asked to wait.",
		"I have counted every bolt in this room. Two are missing. I did not take them. River might have."],
	"river":[
		"Two bright chirps and a whirr. River's status lamp spells it out: %s. No faults worth mentioning.",
		"A rising chirp, then a doubtful one. River has found another loose bolt and is not ready to discuss giving it back.",
		"Soft clicks. River's dome turns to the nearest hatch, then back to you. Translation: still counting the exits. All present."],
	"margot":[
		"Margot flicks an ear under her frog hat. She is %s, and will permit a short interruption.",
		"A small, questioning mrrp. Margot has inspected the station and found it badly short of sunbeams.",
		"Margot purrs, gives you one slow blink, and goes back to washing a paw. Your report has been received."]}

static func companion_greeting(id: String, activity: String, water_mode: String, count: int) -> String:
	if water_mode=="offline": return "Josh does not answer. His standby light pulses slowly while the water is this deep."
	if water_mode=="float": return "A muffled chirp from the waterline. River's lamp blinks: afloat, dry inside, would prefer the floor back."
	if water_mode=="swim": return "Margot paddles for the nearest dry ledge with enormous dignity. She would like a word about the water."
	var lines: Array=COMPANION_GREETINGS[id]
	var line: String=lines[count%lines.size()]
	return line%activity if line.contains("%s") else line

static func greeting(id: String, activity: String) -> String:
	return GREETINGS[id]%activity
static func room_comment(id: String, room_id: String) -> String:
	return ROOM_LINES.get(room_id,{}).get(id,"")
static func resource_report(id: String, resource: String, reserve: int, used: float) -> String:
	if resource.is_empty(): return STEADY[id]
	return SHORTAGES[id]%[resource.capitalize(),reserve,used]
