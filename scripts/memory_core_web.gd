extends Control
## BRINE memory core (owner playtest, Sept 17: Meta Progression option A; note 10: it should read
## like a journal graph). Upgrades as a graph of memory nodes around BRINE's core: one cluster per
## department in the owner's palette, tiers outward on curved links, each node named, a keystone
## at the end of every cluster.
## Lines light in the department colour as nodes are bought; buying sends a pulse along the
## line. Selecting a node shows it in the detail panel, which does the buying.

signal node_selected(id: String)
const Research = preload("res://scripts/research_tree.gd")
const NODE_RADIUS := 18.0
const KEYSTONE_RADIUS := 24.0
const CORE_RADIUS := 40.0
const LABEL_MARGIN := 34.0
const ResourceIcons = preload("res://scripts/resource_icons.gd")
var meta_state
var selected := ""
var buttons := {}
var hover_card: PanelContainer
var hover_text: RichTextLabel
var hovered := ""
var pulses: Array = []
var clock := 0.0

func _ready() -> void:
	custom_minimum_size = Vector2(700, 700)
	mouse_filter = Control.MOUSE_FILTER_PASS
	for branch in Research.BRANCHES:
		for id in Research.perks_in(branch.id):
			var node := Button.new()
			node.name = id
			node.flat = true
			node.focus_mode = Control.FOCUS_ALL
			node.tooltip_text = str(Research.PERKS[id].name)
			var radius := KEYSTONE_RADIUS if Research.PERKS[id].get("keystone", false) else NODE_RADIUS
			node.size = Vector2.ONE * radius * 2.0
			node.custom_minimum_size = node.size
			for state in ["normal", "hover", "pressed", "focus", "disabled", "hover_pressed"]:
				node.add_theme_stylebox_override(state, StyleBoxEmpty.new())
			node.pressed.connect(select.bind(id))
			node.mouse_entered.connect(_hover.bind(id))
			node.mouse_exited.connect(_unhover.bind(id))
			node.focus_entered.connect(select.bind(id))
			add_child(node)
			buttons[id] = node
	# What a memory actually does, in the resource colours and icons the rest of the station uses.
	hover_card = PanelContainer.new()
	hover_card.name = "HoverCard"
	hover_card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hover_card.visible = false
	hover_card.custom_minimum_size = Vector2(300, 0)
	var frame := StyleBoxFlat.new()
	frame.bg_color = Color("0a1a22ee")
	frame.border_color = Color("2e5d66")
	frame.set_border_width_all(1)
	frame.set_corner_radius_all(10)
	frame.set_content_margin_all(12)
	hover_card.add_theme_stylebox_override("panel", frame)
	hover_text = RichTextLabel.new()
	hover_text.bbcode_enabled = true
	hover_text.fit_content = true
	hover_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hover_text.custom_minimum_size = Vector2(276, 0)
	hover_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hover_text.add_theme_font_size_override("normal_font_size", 14)
	hover_text.add_theme_font_size_override("bold_font_size", 14)
	hover_card.add_child(hover_text)
	add_child(hover_card)
	resized.connect(_place)
	_place()
	set_process(not preload("res://scripts/title_settings.gd").reduced_motion)
	queue_redraw()

func _process(delta: float) -> void:
	clock += delta
	for pulse in pulses: pulse.t += delta / 0.55
	pulses = pulses.filter(func(p): return p.t < 1.0)
	queue_redraw()

func center() -> Vector2:
	return size * 0.5

# Rings scale with the space available so the whole graph fits on screen. A department is three
# steps deep now (root, the split, the pair before the keystone, the keystone), each 1.75 steps
# apart, and the spare fraction leaves room for the department's name outside the keystone.
const DEEPEST := 3.0
const RING_SPREAD := 1.7
func ring_step() -> float:
	return maxf(24.0, (minf(size.x, size.y) * 0.5 - LABEL_MARGIN - CORE_RADIUS - KEYSTONE_RADIUS) / (DEEPEST * RING_SPREAD + 0.7))

func first_ring() -> float:
	# Eight lobes leave little arc between their roots, so the first ring sits further out.
	return CORE_RADIUS + ring_step() * 1.7

func branch_angle(index: int) -> float:
	return -PI * 0.5 + TAU * float(index) / float(Research.BRANCHES.size())

# A hand-kept graph, not a diagram: each node sits on its department's spoke but leans off it by a
# fixed amount derived from its own name, so a cluster wanders the way a journal graph does. The
# lean is deterministic, so a node never moves between sessions.
func node_lean(id: String) -> float:
	var seed := 0
	for i in id.length(): seed = (seed * 31 + id.unicode_at(i)) % 1000
	return (float(seed) / 1000.0 - 0.5) * 0.34

# Rings out from the core follow the dependency chain, not the tier number: a node sits one ring
# past the furthest node it needs. Two paths off the same root therefore share a ring and fan out
# to either side of their department's spoke.
func node_depth(id: String) -> int:
	var deepest := -1
	for needed in Research.requirements(id):
		deepest = maxi(deepest, node_depth(str(needed)))
	return deepest + 1

# Every node at the same depth in the same department, in a stable order.
func depth_row(branch: String, depth: int) -> Array:
	var row: Array = []
	for id in Research.perks_in(branch):
		if node_depth(id) == depth: row.append(id)
	return row

func node_position(id: String) -> Vector2:
	var perk: Dictionary = Research.PERKS[id]
	var index := 0
	for i in range(Research.BRANCHES.size()):
		if Research.BRANCHES[i].id == perk.branch: index = i
	var depth := node_depth(id)
	# Depth tops out at three - root, dendrite, the memory past it, then the keystone.
	# Alternate lobes sit a little further out, so neighbouring roots never share a radius and the
	# core reads as grown rather than drawn.
	var stagger := 0.38 if index % 2 == 1 else 0.0
	var ring := first_ring() + ring_step() * (RING_SPREAD * float(depth) + stagger)
	var row := depth_row(str(perk.branch), depth)
	var slot := maxi(row.find(id), 0)
	var angle := branch_angle(index) + node_lean(id) * (0.24 + float(depth) * 0.06)
	var spoke := Vector2.from_angle(angle)
	# Siblings sit a fixed distance apart across the spoke rather than a fixed angle, so a split
	# reads the same width close to the core as it does out at the keystone.
	var across := (float(slot) - float(row.size() - 1) * 0.5) * ring_step() * 1.05
	return center() + spoke * ring + spoke.rotated(PI * 0.5) * across

func _place() -> void:
	for id in buttons:
		var node: Button = buttons[id]
		node.position = node_position(id) - node.size * 0.5
	queue_redraw()

func _hover(id: String) -> void:
	hovered = id
	_show_card(id)
	queue_redraw()

func _unhover(id: String) -> void:
	if hovered != id: return
	hovered = ""
	if is_instance_valid(hover_card): hover_card.visible = false
	queue_redraw()

# The card reads like the station's own readouts: the lobe in its department colour, the effect run
# through ResourceIcons so every amount carries its icon and colour, then the price or the state.
func _show_card(id: String) -> void:
	if not is_instance_valid(hover_card) or not Research.PERKS.has(id): return
	var perk: Dictionary = Research.PERKS[id]
	var color := _branch_color(id)
	var lobe := ""
	for branch in Research.BRANCHES:
		if branch.id == perk.branch: lobe = str(branch.name)
	var state := Research.state(meta_state, id)
	var keystone: bool = perk.get("keystone", false)
	var lines: Array[String] = []
	lines.append("[color=#%s]%s%s[/color]" % [color.to_html(false), lobe, "  ·  KEYSTONE" if keystone else ""])
	lines.append("[b][color=#%s]%s[/color][/b]" % ["f1d58a" if keystone else "e6f6f3", str(perk.name).to_upper()])
	lines.append(ResourceIcons.decorate(str(perk.text), 15))
	var price := "%s %d Archived Data" % [ResourceIcons.icon("archived_data", 15), int(perk.cost)]
	match state:
		"owned": lines.append("[color=#%s]RECOVERED[/color]" % color.to_html(false))
		"ready": lines.append("[color=#a8d8c4]%s[/color]" % price)
		"short": lines.append("[color=#e0a97e]%s  ·  not banked yet[/color]" % price)
		_:
			var waiting: Array = Research.missing(meta_state, id).map(func(other): return str(Research.PERKS[other].name))
			lines.append("[color=#7f9aa3]Sealed until %s  ·  %s[/color]" % [" and ".join(waiting), price])
	hover_text.text = "\n".join(lines)
	hover_card.visible = true
	hover_card.reset_size()
	_place_card(node_position(id))

# The card sits beside its node and stays inside the panel.
func _place_card(at: Vector2) -> void:
	var card_size := hover_card.size
	var spot := at + Vector2(NODE_RADIUS + 14.0, -card_size.y * 0.5)
	if spot.x + card_size.x > size.x - 6.0: spot.x = at.x - NODE_RADIUS - 14.0 - card_size.x
	spot.x = clampf(spot.x, 6.0, maxf(6.0, size.x - card_size.x - 6.0))
	spot.y = clampf(spot.y, 6.0, maxf(6.0, size.y - card_size.y - 6.0))
	hover_card.position = spot

func select(id: String) -> void:
	if selected == id: return
	selected = id
	queue_redraw()
	node_selected.emit(id)

# Called after a purchase: a pulse runs from the previous node (or the core) to the new one.
func celebrate(id: String) -> void:
	var previous := Research.previous(id)
	pulses.append({"from": node_position(previous) if not previous.is_empty() else center(), "to": node_position(id), "t": 0.0, "color": _branch_color(id)})
	queue_redraw()

func _branch_color(id: String) -> Color:
	return Research.branch_color(str(Research.PERKS[id].branch))

# Links bow away from the core so neighbouring clusters read as separate threads rather than a
# star. Drawn as a short polyline, which antialiases where draw_line between two nodes cannot bend.
func _draw_link(from: Vector2, to: Vector2, color: Color, width: float) -> void:
	var middle := (from + to) * 0.5
	var bow := (middle - center()).normalized().rotated(PI * 0.5) * from.distance_to(to) * 0.13
	var control := middle + bow
	var points := PackedVector2Array()
	for step in range(9):
		var t := float(step) / 8.0
		points.append(from.lerp(control, t).lerp(control.lerp(to, t), t))
	draw_polyline(points, color, width, true)

# Which way a node's name leans. A node that sits off to one side of its department's spoke writes
# outward, away from its sibling; one sitting on the spoke alternates by depth so a name never
# lands on the node past it.
func label_side(id: String) -> Vector2:
	var perk: Dictionary = Research.PERKS[id]
	var index := 0
	for i in range(Research.BRANCHES.size()):
		if Research.BRANCHES[i].id == perk.branch: index = i
	var spoke := Vector2.from_angle(branch_angle(index))
	var across := spoke.rotated(PI * 0.5)
	var offset := (node_position(id) - center()).dot(across)
	if absf(offset) > 1.0: return across if offset > 0.0 else -across
	# A root sits on its spoke, and its neighbours' roots are close at eight lobes, so every root
	# writes the same way around the core instead of two of them meeting in the gap.
	return across

# A node wears its name, the way a journal graph labels every note. The name sits beside the node,
# square to its spoke, so it never lands on the next node out. Owned and available names read
# clearly; the rest stay faint so the cluster shape still comes through.
func _draw_node_name(font: Font, at: Vector2, radius: float, id: String, state: String, color: Color) -> void:
	var text := str(Research.PERKS[id].name)
	var size := 12
	var width := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
	var tint := color.lightened(0.25) if state == "owned" else (Color("d3e6ea") if state == "ready" else Color(0.72, 0.82, 0.85, 0.45))
	var side := label_side(id)
	var gap := radius + 8.0
	var anchor := at + side * gap
	if anchor.x - width < 4.0 or anchor.x + width > size_x_limit():
		side = -side
		anchor = at + side * gap
	var at_left: bool = side.x < 0.0
	# Alternate lobes drop their names a few pixels, so two neighbours' names never sit on the same
	# line where their dendrites pass close to each other.
	var lobe := 0
	for i in range(Research.BRANCHES.size()):
		if Research.BRANCHES[i].id == Research.PERKS[id].branch: lobe = i
	var lift := 11.0 if lobe % 2 == 1 else -1.0
	draw_string(font, anchor + Vector2(-width if at_left else 0.0, lift), text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, tint)

func size_x_limit() -> float:
	return size.x - 4.0

# Motes drifting up through the core, the way silt moves past a light outside the hull. Deterministic
# from the clock, so it never needs particles of its own, and it holds still under reduced motion.
const DRIFT_COUNT := 34

func _draw_drift() -> void:
	var reduced: bool = preload("res://scripts/title_settings.gd").reduced_motion
	var drift_time: float = 0.0 if reduced else clock
	var middle := center()
	for i in range(DRIFT_COUNT):
		var seed := float((i * 73) % 97) / 97.0
		var span := float((i * 31) % 53) / 53.0
		var column: float = fposmod(seed * 1.37 + 0.05, 1.0) * size.x
		var speed := 7.0 + span * 16.0
		var height: float = fposmod(size.y - (drift_time * speed + span * size.y), maxf(size.y, 1.0))
		var sway := sin(drift_time * (0.3 + span * 0.4) + seed * TAU) * (5.0 + span * 9.0)
		var at := Vector2(column + sway, height)
		# Fade toward the edges, and keep clear of the core so the graph stays legible.
		var to_core: float = at.distance_to(middle)
		var edge: float = clampf(minf(at.x, size.x - at.x) / 40.0, 0.0, 1.0)
		var alpha: float = 0.08 + 0.07 * span
		alpha *= edge * clampf((to_core - CORE_RADIUS * 1.4) / 120.0, 0.0, 1.0)
		if alpha <= 0.004: continue
		var radius := maxf(1.0, 1.0 + span * 2.4)
		draw_circle(at, radius, Color(0.45, 0.85, 0.82, alpha))
		if span > 0.72:
			draw_arc(at, radius + 2.0, 0, TAU, 10, Color(0.45, 0.85, 0.82, alpha * 0.5), 1.0, true)

func _draw() -> void:
	_draw_drift()
	var c := center()
	var outer := first_ring() + ring_step() * RING_SPREAD * DEEPEST + KEYSTONE_RADIUS + 22.0
	for ring in range(6):
		draw_arc(c, first_ring() + ring_step() * ring, 0, TAU, 96, Color(0.3, 0.55, 0.6, 0.07), 1.0, true)
	var font := get_theme_default_font()
	for i in range(Research.BRANCHES.size()):
		var branch: Dictionary = Research.BRANCHES[i]
		var department: Color = Research.branch_color(str(branch.id))
		var direction := Vector2.from_angle(branch_angle(i))
		var perks: Array = Research.perks_in(branch.id)
		for id in perks:
			var to := node_position(id)
			var state := Research.state(meta_state, id)
			var owned := state == "owned"
			var line_color: Color = department if owned else (department.darkened(0.55) if state in ["ready", "short"] else Color(0.25, 0.33, 0.36, 0.55))
			# One line per requirement, so a split shows as two lines leaving a node and the
			# keystone shows as two lines arriving at it. A root hangs off the core itself.
			var needed: Array = Research.requirements(id)
			if needed.is_empty():
				_draw_link(c + direction * CORE_RADIUS, to, line_color, 4.0 if owned else 2.0)
			for parent in needed:
				_draw_link(node_position(str(parent)), to, line_color, 4.0 if owned else 2.0)
		# Labels sit beside the keystone, rotated a little off the spoke so they never cover a node.
		var label_at := c + Vector2.from_angle(branch_angle(i) + 0.22) * outer
		var text := str(branch.name)
		var width := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15).x
		draw_string(font, label_at - Vector2(width * 0.5, -5), text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15, department)
	for pulse in pulses:
		var at: Vector2 = pulse.from.lerp(pulse.to, ease(pulse.t, 0.6))
		draw_circle(at, 9.0, Color(pulse.color, 1.0 - pulse.t * 0.5))
		draw_circle(at, 18.0, Color(pulse.color, 0.25 * (1.0 - pulse.t)))
	# The core: BRINE's memory, breathing slowly.
	var breath := 0.5 + 0.5 * sin(clock * 1.4)
	draw_circle(c, CORE_RADIUS + 16.0 + breath * 6.0, Color(0.37, 0.83, 0.77, 0.06 + breath * 0.04))
	draw_circle(c, CORE_RADIUS, Color("0e2b31"))
	draw_arc(c, CORE_RADIUS, 0, TAU, 64, Color("5fd3c4"), 3.0, true)
	draw_circle(c, CORE_RADIUS * 0.42, Color(0.37, 0.83, 0.77, 0.55 + breath * 0.3))
	var core_text := "BRINE"
	var core_width := font.get_string_size(core_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15).x
	draw_string(font, c + Vector2(-core_width * 0.5, CORE_RADIUS + 22), core_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("9ff3df"))
	for id in buttons:
		var perk: Dictionary = Research.PERKS[id]
		var at := node_position(id)
		var state := Research.state(meta_state, id)
		var color := _branch_color(id)
		var keystone: bool = perk.get("keystone", false)
		var radius := KEYSTONE_RADIUS if keystone else NODE_RADIUS
		var hot: bool = id == selected or id == hovered or buttons[id].is_hovered()
		if state == "owned":
			draw_circle(at, radius + 7.0 + breath * 2.0, Color(color, 0.16))
			draw_circle(at, radius, color.darkened(0.25))
			draw_arc(at, radius, 0, TAU, 40, color.lightened(0.35), 2.5, true)
		elif state == "ready":
			draw_circle(at, radius, Color("10262e"))
			draw_arc(at, radius, 0, TAU, 40, color, 2.5 + breath * 1.0, true)
		elif state == "short":
			draw_circle(at, radius, Color("0d1f26"))
			draw_arc(at, radius, 0, TAU, 40, color.darkened(0.4), 2.0, true)
		else:
			draw_circle(at, radius, Color("0a171c"))
			draw_arc(at, radius, 0, TAU, 40, Color(0.3, 0.38, 0.41, 0.8), 1.5, true)
		if keystone:
			var diamond := PackedVector2Array([at + Vector2(0, -radius * 0.5), at + Vector2(radius * 0.5, 0), at + Vector2(0, radius * 0.5), at + Vector2(-radius * 0.5, 0)])
			draw_colored_polygon(diamond, Color("f1d58a") if state == "owned" else Color(0.95, 0.83, 0.54, 0.35))
		else:
			var tier_text := str(int(perk.tier))
			var tier_width := font.get_string_size(tier_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15).x
			draw_string(font, at + Vector2(-tier_width * 0.5, 5.5), tier_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("0b1a20") if state == "owned" else Color(0.75, 0.85, 0.88, 0.9 if state != "locked" else 0.4))
		if hot:
			draw_arc(at, radius + 6.0, 0, TAU, 40, Color("e6f6f3"), 2.0, true)
		# Recovered and reachable memories carry their names, as does whatever the pointer is on.
		# Sealed ones stay unnamed, and so do the roots: eight of them ring the core closely enough
		# that their names ran into each other, and the lobe's own name already sits outside.
		if ((state in ["owned", "ready"]) and node_depth(id) > 0) or hot:
			_draw_node_name(font, at, radius, id, state, color)
