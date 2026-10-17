from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['retained-berth','retained-berth-helmet']:
 path=P/(name+'.gd');s=path.read_text();marker='\t\t\troot.get_texture().get_image().save_png(out+"%s-%02d.png"%[action,slot])'
 proof='''
			# An opaque furniture layer can hide the body while loader checks pass.
			var visible:=root.get_texture().get_image().get_region(Rect2i(330,123,270,177))
			npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var background:=root.get_texture().get_image().get_region(Rect2i(330,123,270,177))
			npc.active=true
			check(visible.get_data()!=background.get_data(),"Actor visible in retained berth "+action+str(slot))
'''
 if 'Actor visible in retained berth' not in s:path.write_text(s.replace(marker,marker+proof,1))
