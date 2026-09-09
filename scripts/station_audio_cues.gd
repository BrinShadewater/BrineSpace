extends RefCounted
## Small original procedural cues; no external generator or new credits required.
static var cache := {}
const EXPANDED_DURATIONS := {"swim":0.65,"suit":0.35,"bubbles":0.85,"mining_work":1.5,"salvage_work":1.2,"galley_work":0.65,"medical_work":0.9,"lab_work":1.0,"cultivation_work":1.4,"warning_oxygen":1.2,"warning_power":0.8,"warning_hull":1.4}
static func get_stream(kind: String) -> AudioStreamWAV:
	if cache.has(kind): return cache[kind]
	var duration := float({"ui_select":0.075,"ui_reject":0.16,"ui_comms":0.45,"ui_saved":0.3,"power_off":1.1,"hull":2.5,"build_complete":0.65,"build_blocked":0.5,"launch":0.8,"footstep":0.12,"tools":0.35,"ui_end":2.0,"ui_failure":2.0}.get(kind,4.0))
	const RATE := 22050
	if kind=="companion_chirp":duration=0.42
	if kind in ["helmet_lock","helmet_release","site_empty"]: duration = {"helmet_lock":0.35,"helmet_release":0.45,"site_empty":0.75}[kind]
	if EXPANDED_DURATIONS.has(kind): duration = EXPANDED_DURATIONS[kind]
	if kind == "repair": duration = 0.6
	if kind in ["all_clear","crew_dispatch","crew_awake"]: duration = {"all_clear":0.7,"crew_dispatch":0.4,"crew_awake":1.2}[kind]
	if kind in ["airlock_pressure","airlock_release","airlock_ready","ui_recall","crew_return"]: duration = {"airlock_pressure":1.5,"airlock_release":0.45,"airlock_ready":0.4,"ui_recall":0.45,"crew_return":0.6}[kind]
	var frames := int(duration*RATE)
	var data := PackedByteArray()
	data.resize(frames*2)
	var rng := RandomNumberGenerator.new()
	rng.seed = 1923
	var noise := 0.0
	for i in frames:
		var t := float(i)/RATE
		var u := t/duration
		var raw_noise := rng.randf_range(-1.0,1.0)
		noise = lerpf(noise,raw_noise,0.035)
		var sample := 0.0
		match kind:
			"companion_chirp":
				var note := t if t<0.20 else t-0.23
				if note>=0:sample=sin(TAU*(720.0 if t<0.20 else 960.0)*note)*sin(PI*clampf(note/0.19,0,1))*0.18
			"ui_select": sample = sin(TAU*640*t)*exp(-t*65.0)*0.25
			"ui_reject": sample = sin(TAU*280*t)*exp(-t*22.0)*0.20
			"ui_comms":
				var pulse := fmod(t,0.22)
				sample = (sin(TAU*520*t)*0.16+noise*0.12)*exp(-pulse*35.0)*minf(1.0,pulse/0.006)
			"ui_saved":
				var second := maxf(0.0,t-0.12)
				sample = sin(TAU*480*t)*exp(-t*35.0)*0.17
				if t >= 0.12: sample += sin(TAU*720*second)*exp(-second*30.0)*minf(1.0,second/0.006)*0.14
			"power_off": sample = (sin(TAU*(100*t-25*t*t))+noise)*pow(1.0-u,2.0)*0.16
			"hull": sample = (sin(TAU*43*t+sin(TAU*0.4*t))*noise*3.0+sin(TAU*68*t)*0.12)*sin(PI*u)*0.24
			"core": sample = (sin(TAU*64*t)+sin(TAU*129*t)*0.3)*0.12
			"refrigeration": sample = (sin(TAU*57*t)*0.13+sin(TAU*114*t)*0.035+noise*0.3)
			"workshop": sample = (sin(TAU*88*t)*0.06+noise*0.35)*(0.65+0.35*sin(TAU*0.5*t))
			"build_complete": sample = (sin(TAU*360*t)*exp(-t*9.0)+sin(TAU*540*t)*sin(PI*u))*0.15
			"build_blocked": sample = sin(TAU*210*t)*exp(-fmod(t,0.25)*22.0)*sin(PI*u)*0.18
			"launch": sample = (sin(TAU*(90*t+35*t*t))*0.12+noise*0.2)*sin(PI*u)
			"footstep": sample = (noise*2.0+sin(TAU*95*t)*0.3)*exp(-t*38.0)*0.35
			"tools": sample = (sin(TAU*840*t)*0.16+noise*0.5)*exp(-t*20.0)
			"repair": sample = (sin(TAU*125*t)*0.15+noise*0.55)*sin(PI*u)*(0.5+0.5*sin(TAU*12*t))
			"all_clear": sample = (sin(TAU*330*t)+sin(TAU*495*t)*0.3)*sin(PI*u)*0.13
			"crew_dispatch": sample = (sin(TAU*410*t)*exp(-t*16.0)+noise*0.25)*sin(PI*u)*0.18
			"crew_awake": sample = (sin(TAU*(240*t+22*t*t))*0.13+noise*0.15)*sin(PI*u)
			"airlock_pressure": sample = (noise*0.85+sin(TAU*75*t)*0.03)*sin(PI*u)
			"airlock_release": sample = (noise*0.8+sin(TAU*170*t)*0.18)*exp(-t*12.0)
			"airlock_ready": sample = sin(TAU*470*t)*sin(PI*u)*0.13
			"ui_recall": sample = (sin(TAU*420*t)+sin(TAU*280*t)*0.4)*sin(PI*u)*0.12
			"crew_return": sample = (sin(TAU*350*t)+sin(TAU*525*t)*0.35)*sin(PI*u)*0.13
			"ui_end": sample = (sin(TAU*220*t)+sin(TAU*330*t)*0.5+sin(TAU*440*t)*0.25)*sin(PI*u)*0.12
			"ui_failure": sample = (sin(TAU*(180*t-18*t*t))+sin(TAU*91*t)*0.4)*sin(PI*u)*0.12
			"swim": sample = (noise*1.2+sin(TAU*65*t)*0.025)*pow(sin(PI*u),2.0)
			"suit": sample = (noise*0.7+raw_noise*0.025)*sin(PI*u)*0.7
			"bubbles": sample = sin(TAU*(220*t+180*t*t))*exp(-fmod(t,0.21)*28.0)*sin(PI*u)*0.12
			"mining_work": sample = (sin(TAU*110*t)*0.10+noise*0.6+raw_noise*0.025)*sin(PI*u)*(0.7+0.3*sin(TAU*17*t))
			"salvage_work": sample = (noise*0.75+sin(TAU*390*t)*0.07+raw_noise*0.02)*sin(PI*u)*(0.65+0.35*sin(TAU*7*t))
			"galley_work": sample = (sin(TAU*740*t)*0.11+noise*0.4)*exp(-fmod(t,0.3)*22.0)*sin(PI*u)
			"medical_work": sample = (sin(TAU*580*t)*exp(-t*14.0)*0.09+noise*0.12)*sin(PI*u)
			"lab_work": sample = (sin(TAU*310*t)*0.05+sin(TAU*930*t)*exp(-fmod(t,0.45)*25.0)*0.05+noise*0.15)*sin(PI*u)
			"cultivation_work": sample = (noise*0.65+sin(TAU*(160*t+40*t*t))*0.025)*sin(PI*u)
			"warning_oxygen": sample = sin(TAU*660*t)*exp(-fmod(t,0.4)*18.0)*sin(PI*u)*0.28
			"warning_power": sample = sin(TAU*240*t)*exp(-fmod(t,0.4)*16.0)*sin(PI*u)*0.28
			"warning_hull": sample = (sin(TAU*95*t)+sin(TAU*190*t)*0.3)*exp(-fmod(t,0.7)*10.0)*sin(PI*u)*0.24
			"helmet_lock": sample = (sin(TAU*190*t)*0.16+noise*0.6)*exp(-t*18.0)
			"helmet_release": sample = (noise*0.65+raw_noise*0.025+sin(TAU*135*t)*0.06)*sin(PI*u)
			"site_empty": sample = (sin(TAU*(300*t-55*t*t))*0.15+noise*0.1)*sin(PI*u)
		var edge := minf(1.0,minf(t,duration-t)/0.006)
		data.encode_s16(i*2,int(clampf(sample*edge,-1.0,1.0)*32767.0))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = RATE
	stream.data = data
	if kind in ["core","refrigeration","workshop"]:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_end = frames
	cache[kind] = stream
	return stream
