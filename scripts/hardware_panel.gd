extends PanelContainer
var game
var controls: Dictionary={}
class HardwareButton extends Button:
	var idle: Texture2D
	var engaged: Texture2D
	var amount:=0.0
	var target:=0.0
	var key: String=""
	var drag_start:=Vector2.ZERO
	var drag_active:=false
	var dragged:=false
	var host
	func _ready() -> void:
		flat=true; mouse_default_cursor_shape=Control.CURSOR_POINTING_HAND
		pressed.connect(activate)
		mouse_exited.connect(queue_redraw); focus_exited.connect(queue_redraw)
	func activate() -> void:
		if key=="power" and (drag_active or dragged): return
		host.activate(key,not bool(host.game.hardware.get(key,false)))
	func clear_drag() -> void: dragged=false
	func _gui_input(event: InputEvent) -> void:
		if key!="power": return
		if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT:
			if event.pressed: drag_start=event.position; drag_active=true; dragged=false
			elif drag_active:
				drag_active=false; dragged=true
				var movement: float=event.position.y-drag_start.y
				host.activate(key,movement>0 if absf(movement)>12 else not host.game.hardware.power)
				call_deferred("clear_drag")
	func _process(delta: float) -> void:
		var next: float=move_toward(amount,target,delta*5)
		if next!=amount or is_hovered() or has_focus() or is_pressed(): amount=next; queue_redraw()
	func _draw() -> void:
		if idle==null: return
		var art_height: float=size.y-8.0 if key in ["power","comms"] else size.y
		var fit: float=minf(size.x/idle.get_width(),art_height/idle.get_height())
		var dimensions: Vector2=idle.get_size()*fit
		var rect:=Rect2(Vector2((size.x-dimensions.x)*0.5,size.y-dimensions.y)+Vector2(0,2 if is_pressed() else 0),dimensions)
		var tint:=Color(0.45,0.46,0.40) if disabled else Color(0.91,0.98,1.0)
		draw_texture_rect(idle,rect,false,tint)
		if engaged!=null and amount>0: draw_texture_rect(engaged,rect,false,Color(tint.r,tint.g,tint.b,amount))
		if has_focus() or is_hovered(): draw_rect(Rect2(Vector2.ONE,size-Vector2.ONE*2),Color("6b9287"),false,1)
func _ready() -> void:
	custom_minimum_size=Vector2(516,210)
	var style:=StyleBoxFlat.new(); style.bg_color=Color("10272b"); style.border_color=Color("35565b")
	style.set_border_width_all(2); style.set_content_margin_all(8); add_theme_stylebox_override("panel",style)
	# Brushed green gunmetal with directional reflection and a machined bevel.
	var metal:=ColorRect.new(); metal.mouse_filter=Control.MOUSE_FILTER_IGNORE
	var shader:=Shader.new()
	shader.code="""shader_type canvas_item;
float grain(vec2 p) { return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453); }
float mottling(vec2 p) {
	vec2 cell=floor(p); vec2 f=fract(p); f=f*f*(3.0-2.0*f);
	return mix(mix(grain(cell),grain(cell+vec2(1.0,0.0)),f.x),
		mix(grain(cell+vec2(0.0,1.0)),grain(cell+vec2(1.0)),f.x),f.y);
}
void fragment() {
	vec2 p=UV*vec2(480.0,220.0);
	float fine=grain(floor(p*2.0))-0.5;
	float brush=mottling(p*vec2(0.025,3.0))-0.5;
	float patina=mottling(p*0.035)-0.5;
	float sweep=UV.x+UV.y*0.42;
	float reflection=exp(-pow((sweep-0.40)/0.24,2.0));
	float reflected_edge=exp(-pow((sweep-0.64)/0.035,2.0));
	vec3 steel=vec3(0.043,0.095,0.108)+vec3(0.035,0.055,0.061)*reflection;
	steel+=fine*0.009+brush*0.021+patina*0.007+reflected_edge*0.010;
	float upper=1.0-smoothstep(0.6,2.2,min(p.x,p.y));
	float lower=1.0-smoothstep(0.6,2.2,min(480.0-p.x,220.0-p.y));
	steel+=upper*vec3(0.075,0.115,0.125)-lower*0.046;
	float inset=min(min(p.x,480.0-p.x),min(p.y,220.0-p.y));
	steel-=exp(-pow((inset-3.1)/0.65,2.0))*0.022;
	float seam=exp(-pow((p.y-21.0)/0.55,2.0));
	steel-=seam*0.025;
	steel+=exp(-pow((p.y-22.0)/0.5,2.0))*0.017;
	COLOR=vec4(steel,1.0);
}"""
	var finish:=ShaderMaterial.new(); finish.shader=shader; metal.material=finish; add_child(metal)
	var column:=VBoxContainer.new(); add_child(column)
	var heading:=Label.new(); heading.text="STATION CONTROLS"; heading.add_theme_color_override("font_color",Color("c5d6d2")); heading.add_theme_font_size_override("font_size",13); column.add_child(heading)
	var row:=HBoxContainer.new(); row.add_theme_constant_override("separation",6); column.add_child(row)
	add_control(row,"power","POWER",Vector2(96,132),"heavy-lever-v1/raised.tres","heavy-lever-v1/lowered.tres","Drag down for power on; up for off. Click or Enter also toggles. Stored reserves remain; crew still consume food and oxygen.")
	add_control(row,"comms","COMMS",Vector2(86,132),"comms-speaker-v2/idle.tres","comms-speaker-v2/active.tres","Open the comms window")
	var grid:=GridContainer.new(); grid.columns=3; grid.add_theme_constant_override("h_separation",8); grid.add_theme_constant_override("v_separation",6); row.add_child(grid)
	for entry in [["walls","WALLS/BASE","Show or hide room shells and station foundations"],["sprinklers","SPRINKLERS","Visible spray only; fire suppression is not implemented"],["doors","DOORS","Lock/unlock internal crew doors. Drone transfers hold while locked; airlock safety cycles remain separate."],["interior","INT. LIGHTS","Turn room lighting on/off"],["exterior","EXT. LIGHTS","Turn exterior marker lights on/off"],["pumps","PUMPS","Enable powered bilge drainage and water-producing rooms"]]:
		var prefix: String={"walls":"lever","sprinklers":"lever","doors":"rocker","pumps":"push"}.get(entry[0],"slide")
		var dimensions:=Vector2(88,60 if entry[0] in ["walls","sprinklers","doors"] else 46)
		add_control(grid,entry[0],entry[1],dimensions,"industrial-switches-v1/"+prefix+"-off.tres","industrial-switches-v1/"+prefix+"-on.tres",entry[2])
	refresh()
func add_control(parent, key: String, caption: String, dimensions: Vector2, off: String, on: String, tip: String) -> void:
	var column:=VBoxContainer.new(); column.add_theme_constant_override("separation",2); parent.add_child(column)
	var button:=HardwareButton.new(); button.host=self; button.key=key; button.custom_minimum_size=dimensions
	button.idle=load("res://brineui/"+off); button.engaged=load("res://brineui/"+on); button.tooltip_text=tip
	button.disabled=false; column.add_child(button)
	var label:=Label.new(); label.text=caption; label.add_theme_color_override("font_color",Color("bdceca")); label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_constant_override("line_spacing",0); label.add_theme_font_size_override("font_size",12); column.add_child(label)
	var status:=Label.new(); status.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; status.add_theme_font_size_override("font_size",10); column.add_child(status)
	controls[key]={"button":button,"status":status}
func activate(key: String, value: bool) -> void:
	if game._gameplay_input_blocked(): return
	if key=="comms": game.crew_comms.reopen()
	else: preload("res://scripts/station_hardware.gd").set_control(game,key,value)
	refresh()
func refresh() -> void:
	for key in controls:
		var entry: Dictionary=controls[key]
		var enabled: bool=game.hardware.get(key,false)
		entry.button.target=1.0 if enabled else 0.0
		entry.status.add_theme_color_override("font_color",Color("a8b99a") if enabled else Color("879e9e"))
		if key=="doors" and enabled: entry.status.add_theme_color_override("font_color",Color("c0a56d"))
		entry.status.text=("LOCKED" if enabled else "UNLOCKED") if key=="doors" else ("ON" if enabled else "OFF")
		if key=="comms":
			var open: bool=is_instance_valid(game.crew_comms) and game.crew_comms.panel.visible
			entry.button.target=1.0 if open else 0.0
			entry.status.text="OPEN" if open else "COMMS"
func _process(_delta: float) -> void: refresh()
