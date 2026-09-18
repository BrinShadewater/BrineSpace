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
var meta_state
var selected := ""
var buttons := {}
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
			node.mouse_entered.connect(queue_redraw)
			node.mouse_exited.connect(queue_redraw)
			node.focus_entered.connect(select.bind(id))
			add_child(node)
			buttons[id] = node
	resized.connect(_place)
	_place()
	set_process(not preload("res://scripts/title_settings.gd").reduced_motion)

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
const RING_SPREAD := 1.75
func ring_step() -> float:
	return maxf(24.0, (minf(size.x, size.y) * 0.5 - LABEL_MARGIN - CORE_RADIUS - KEYSTONE_RADIUS) / (DEEPEST * RING_SPREAD + 0.7))

func first_ring() -> float:
	return CORE_RADIUS + ring_step() * 1.3

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
	# Depth now tops out at three, so each step can take more of the radius than a tier did.
	var ring := first_ring() + ring_step() * RING_SPREAD * float(depth)
	var row := depth_row(str(perk.branch), depth)
	var slot := maxi(row.find(id), 0)
	var angle := branch_angle(index) + node_lean(id) * (0.24 + float(depth) * 0.06)
	var spoke := Vector2.from_angle(angle)
	# Siblings sit a fixed distance apart across the spoke rather than a fixed angle, so a split
	# reads the same width close to the core as it does out at the keystone.
	var across := (float(slot) - float(row.size() - 1) * 0.5) * ring_step() * 1.5
	return center() + spoke * ring + spoke.rotated(PI * 0.5) * across

func _place() -> void:
	for id in buttons:
		var node: Button = buttons[id]
		node.position = node_position(id) - node.size * 0.5
	queue_redraw()

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
	return across if node_depth(id) % 2 == 0 else -across

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
	draw_string(font, anchor + Vector2(-width if at_left else 0.0, 4.0), text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, tint)

func size_x_limit() -> float:
	return size.x - 4.0

func _draw() -> void:
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
		var hot: bool = id == selected or buttons[id].is_hovered()
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
		# Sealed ones stay unnamed: thirty-three labels at once buried the shape of the graph.
		if state in ["owned", "ready"] or hot:
			_draw_node_name(font, at, radius, id, state, color)
