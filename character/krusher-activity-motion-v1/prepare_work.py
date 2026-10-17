from pathlib import Path
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;old=R/'character/krusher-station-lifecycle-v1'
for name in ['repair','construction']:
 text=(old/'native'/(name+'.gd')).read_text().replace('res://character/krusher-complete-animation-v1/progress.json','res://character/krusher-animation-package-v11/package.json').replace('res://character/krusher-station-lifecycle-v1/native/'+name+'.gd.uid','res://character/krusher-activity-motion-v1/'+name+'.gd.uid')
 if name=='repair':
  text=text.replace('if action!=previous or tick%30==0:', 'if action!=previous or (not actual.is_empty() and str(actual.key)+":"+str(actual.index)!=str(get_meta("last_pose",""))):')
  text=text.replace('    var stage_before:String=actor.stage;', '    set_meta("last_pose",str(actual.get("key",""))+":"+str(actual.get("index",-1)))\n    var stage_before:String=actor.stage;')
 else:
  text=text.replace('if action!=previous or (step%60==0):','if action!=previous or step%6==0:')
  needle='     game.visual_time_seconds+=1.0/60.0;Construction.advance(game,actor,1.0/60.0)'
  hook='\n     var transition_texture:Texture2D=game.grid_view._get_branforth_frame_source(game)\n     var transition_pixels:PackedByteArray=pixels(transition_texture)\n     if transition_pixels!=get_meta("transition_pixels",PackedByteArray()):\n      await capture_work(actor,transition_texture,gear,"transition-"+str(step)+"-"+str(game.visual_time_seconds),camera)\n      set_meta("transition_pixels",transition_pixels)'
  text=text.replace(needle,needle+hook)
 text=text.replace('records.append({"file":name+".png",','records.append({"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"file":name+".png",')
 text=text.replace('await capture(name)','game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw')
 needle=' records.append({"screen":'
 insert=' var image:Image=root.get_texture().get_image();var crop:Rect2i=Rect2i(screen.grow(7).intersection(Rect2(Vector2.ZERO,image.get_size())))\n image.get_region(crop).save_png(capture_dir.path_join(name+".png"))\n var context_key:String="context-"+("bare" if gear.is_empty() else "helmet")+"-"+actor.direction+"-"+actor.animation_state()\n if not has_meta(context_key):image.save_png(capture_dir.path_join(name+"-full.png"));set_meta(context_key,true)\n'
 text=text.replace(needle,insert+' records.append({"crop":[crop.position.x,crop.position.y,crop.size.x,crop.size.y],"source":game.grid_view.branforth_player.last_source.duplicate(true),"screen":')
 text=text.replace(' if not has_meta(context_key):',' context_key=context_key.replace("-","_")\n if not has_meta(context_key):')
 (H/(name+'.gd')).write_text(text,encoding='utf-8')
 runner=(old/('run_'+name+'.py')).read_text().replace("review=P/'review/"+name+"'","review=P/'"+name+"'").replace('res://character/krusher-station-lifecycle-v1/native/'+name+'.gd','res://character/krusher-activity-motion-v1/'+name+'.gd').replace('timeout=240','timeout=360')
 runner=runner.replace("review=P/'"+name+"'","review=P/'"+name+("-v4'" if name=='construction' else "-v3'"))
 (H/('run_'+name+'.py')).write_text(runner)
print('Prepared current V11 native maintenance and paid construction review')
