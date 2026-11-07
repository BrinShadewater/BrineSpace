@tool
extends RefCounted
## Canvas commands retain RIDs, not Texture2D references. Keep every skin used
## in the latest draw of each canvas, then release it on redraw or scene exit.
var textures:Dictionary={}
var epochs:Dictionary={}
func keep(rid:RID,texture:Texture2D)->void:
 if not textures.has(rid):
  var tree:=Engine.get_main_loop() as SceneTree
  var owner:CanvasItem=_find_canvas(tree.root,rid) if tree!=null else null
  if owner!=null:
   var weak:WeakRef=weakref(self)
   owner.tree_exited.connect(func():
    var lease=weak.get_ref()
    if lease!=null:lease.release_canvas(rid),CONNECT_ONE_SHOT)
 # Several differently sized tabs can share one canvas in the same draw.
 # A later render epoch can replace the previous commands and their skins.
 var epoch:=Engine.get_frames_drawn()
 if int(epochs.get(rid,-1))!=epoch:
  textures[rid]={};epochs[rid]=epoch
 var current:Dictionary=textures[rid]
 current[texture.get_instance_id()]=texture
func release_canvas(rid:RID)->void:
 textures.erase(rid);epochs.erase(rid)
static func _find_canvas(node:Node,rid:RID)->CanvasItem:
 if node is CanvasItem and node.get_canvas_item()==rid:return node
 for child in node.get_children(true):
  var found:=_find_canvas(child,rid)
  if found!=null:return found
 return null
