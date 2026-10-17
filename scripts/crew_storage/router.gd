extends RefCounted
const Slots=preload("res://scripts/crew_storage/slots.gd")
static var active
var bank
var presenter:=Slots.new()
var canvas:Dictionary={}
var epochs:Dictionary={}
var tree:SceneTree
var tracked_owners:Dictionary={}
var resolved:=0
var missing:=0
var shown_frames:Dictionary={}
func diagnostics_snapshot()->Dictionary:
	# Fixed-size counters only: no pixel readbacks, source iteration or timing reset.
	return {"active":bank!=null,"source_reference_count":bank.sources.size() if bank!=null else 0,
		"source_decoded_bytes":bank.decoded_bytes if bank!=null else 0,
		"source_compressed_bytes":bank.compressed_bytes if bank!=null else 0,
		"generated_readbacks":bank.generated_readbacks if bank!=null else 0,
		"resolved":resolved,"missing":missing,"shown_pose_count":shown_frames.size(),
		"registered_canvases":canvas.size(),"tracked_owners":tracked_owners.size(),"draw_epochs":epochs.size(),
		"presenter":presenter.diagnostics_snapshot()}
static func start(target_tree:SceneTree,root:Node,source_bank):
	assert(active==null)
	active=new();active.bank=source_bank;active.presenter.bank=source_bank;active.tree=target_tree
	active.register_tree(target_tree.root)
	target_tree.node_added.connect(active.register)
	target_tree.node_removed.connect(active.unregister)
	RenderingServer.frame_post_draw.connect(active.presenter.finish_frame)
	root.tree_exited.connect(active.close,CONNECT_ONE_SHOT)
func register_tree(node:Node):
	register(node)
	for child in node.get_children():register_tree(child)
func register(node:Node):
	if node is CanvasItem:canvas[node.get_canvas_item().get_id()]=weakref(node)
func unregister(node:Node):
	var owner:=node as CanvasItem
	if owner==null:return
	# WeakRef is itself an Object. Retired UI/audio canvases must not leave one
	# behind for the rest of the expedition; re-entry registers the canvas again.
	canvas.erase(owner.get_canvas_item().get_id())
	var id:int=owner.get_instance_id()
	epochs.erase(id)
	if tracked_owners.has(id):
		var callback:Callable=tracked_owners[id].callback
		if owner.draw.is_connected(callback):owner.draw.disconnect(callback)
		tracked_owners.erase(id)
func track_script_draw(owner:CanvasItem):
	var id:int=owner.get_instance_id()
	if tracked_owners.has(id):return
	# Only plain script-drawn canvas classes have no native texture draw before
	# the signal. Sprite/TextureRect subclasses retain their original fallback.
	if owner.get_class() not in ["Node2D","Control"]:return
	var script=owner.get_script()
	if script==null:return
	var methods:Array=script.get_script_method_list()
	# The engine signal precedes virtual _draw, but follows notifications.
	# Native/custom-notification consumers retain the original fallback.
	if not methods.any(func(m):return m.name=="_draw") or methods.any(func(m):return m.name=="_notification"):return
	var callback:Callable=before_script_draw.bind(id)
	tracked_owners[id]={"owner":weakref(owner),"callback":callback}
	owner.draw.connect(callback)
func before_script_draw(id:int):
	if not tracked_owners.has(id):return
	var owner:CanvasItem=tracked_owners[id].owner.get_ref()
	if owner==null:return
	presenter.begin_draw(owner)
	epochs[id]=Engine.get_process_frames()
static func resolve(rid:RID,source:Texture2D)->Texture2D:
	if active==null:push_error("CPU texture draw has no private routing");return null
	var weak:WeakRef=active.canvas.get(rid.get_id())
	var owner:CanvasItem=weak.get_ref() if weak!=null else null
	if owner==null:active.missing+=1;push_error("CPU texture draw canvas is unregistered");return null
	active.track_script_draw(owner)
	var epoch:int=Engine.get_process_frames()
	if active.epochs.get(owner.get_instance_id(),-1)!=epoch:
		active.presenter.begin_draw(owner);active.epochs[owner.get_instance_id()]=epoch
	active.resolved+=1
	active.shown_frames[source.get_instance_id()]=true
	return active.presenter.acquire(owner,source)
func close():
	for record in tracked_owners.values():
		var owner:CanvasItem=record.owner.get_ref()
		if owner!=null and owner.draw.is_connected(record.callback):owner.draw.disconnect(record.callback)
	tracked_owners.clear()
	if RenderingServer.frame_post_draw.is_connected(presenter.finish_frame):RenderingServer.frame_post_draw.disconnect(presenter.finish_frame)
	if tree.node_added.is_connected(register):tree.node_added.disconnect(register)
	if tree.node_removed.is_connected(unregister):tree.node_removed.disconnect(unregister)
	for id in presenter.owners.keys():presenter.release_owner(id)
	canvas.clear();epochs.clear();shown_frames.clear();bank=null;presenter.bank=null
	if active==self:active=null
