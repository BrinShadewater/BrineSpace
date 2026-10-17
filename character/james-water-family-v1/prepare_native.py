from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-staged.gd').read_text()
s=s.replace('player.load_manifest(MANIFEST)','player.load_manifest(MANIFEST)\n\tplayer.load_equipment_manifest("diving-helmet", "res://character/james-water-family-v1/helmet-manifest.json")')
start=s.index('\tvar manifest:');end=s.index('\tprint("JAMES WATER STAGED:')
block=s[start:end].replace('JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))','JSON.parse_string(FileAccess.get_file_as_string(path))').replace('MANIFEST.get_base_dir()','path.get_base_dir()').replace('player.frames','rows').replace('player.timing','clocks').replace('player.current_equipment=""','player.current_equipment=gear').replace(',"",true)',',gear,true)').replace('/2000.0)==tex','/2000.0,gear)==tex').replace('player.cycle_seconds(key)','player.cycle_seconds(key,gear)')
prefix='\tfor gear in ["", "diving-helmet"]:\n\t\tvar path: String=MANIFEST if gear.is_empty() else "res://character/james-water-family-v1/helmet-manifest.json"\n\t\tvar rows: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]\n\t\tvar clocks: Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]\n'
s=s[:start]+prefix+''.join('\t'+line+'\n' for line in block.splitlines())+s[end:]
s=s.replace('JAMES WATER STAGED:', 'JAMES WATER PAIRED STAGED:')
end=s.index('\tprint("JAMES WATER PAIRED STAGED:')
capture='''
	if DisplayServer.get_name()!="headless":
		for direction in ["east","south","west","north"]:
			var viewport:=SubViewport.new();viewport.size=Vector2i(1080,1280);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
			var bg:=ColorRect.new();bg.size=Vector2(1080,1280);bg.color=Color("303b40");viewport.add_child(bg)
			for row_index in range(8):
				var action: String=["tread","swim-start","swim","swim-stop"][row_index%4]
				var gear: String="" if row_index<4 else "diving-helmet"
				var rows: Array=player.frames[action+"-"+direction] if gear.is_empty() else player.equipment_frames[gear][action+"-"+direction]
				var title:=Label.new();title.text=direction+" "+action+" "+("bare" if gear.is_empty() else "helmet")+" / station82px";title.position=Vector2(8,row_index*160);viewport.add_child(title)
				for column in range(6):
					var tex: Texture2D=rows[column];var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=tex;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(90+column*180,row_index*160+75)-tex.get_meta("crew_pivot")*82.0/148.0;viewport.add_child(sprite)
			await RenderingServer.frame_post_draw
			check(viewport.get_texture().get_image().save_png("res://character/james-water-family-v1/native-"+direction+"-contact.png")==OK,"Native staged contact "+direction)
			viewport.queue_free()
'''
s=s[:end]+capture+s[end:]
(P/'native-paired.gd').write_text(s)
print('Prepared paired staged fixture and 82px native contacts')
