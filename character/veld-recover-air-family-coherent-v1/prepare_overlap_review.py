from pathlib import Path
import json
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tools/review_veld_recovery_furnished_v1.gd').read_text().replace('output/veld-recovery-furnished-v1','output/veld-recovery-overlap-v1').replace('VELD RECOVERY FURNISHED','VELD RECOVERY OVERLAP')
inventory=json.loads((ROOT/'character/veld-remaining-specials-audit-v1/inventory.json').read_text())
prior={g:{k:['res://'+p for p in inventory['selected'][g][k]['files']] for k in ['recover-air-east','recover-air-west']} for g in ['bare','helmet']}
s=s.replace('var checks:=0','const PRIOR='+json.dumps(prior)+'\nvar checks:=0')
s=s.replace('for r in audit.records:\n', 'for r in audit.records:\n\t\tif r.state not in ["recover-air-east","recover-air-west"]:continue\n')
s=s.replace('if found==null and npc.cell_at(point)==origin:found=point','pass')
s=s.replace('if idle_clear:added_vs_idle+=1','if idle_clear:\n\t\t\t\t\tadded_vs_idle+=1\n\t\t\t\t\tif found==null and npc.cell_at(point)==origin:found=point')
s=s.replace('check(visual_clear(npc,npc.foot,r.candidateEnvelope),"All-pose visual envelope clear at reviewed point")','check(visual_clear(npc,npc.foot,r.selectedIdleEnvelope) and not visual_clear(npc,npc.foot,r.candidateEnvelope),"Idle-clear added-overlap point retained")')
old='check(image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,image.get_size())))).save_png(CAPTURES[r.state+"-"+r.gear])==OK,"Fresh furnished frame3 capture")'
new='''var crop:=Rect2i(screen.intersection(Rect2(Vector2.ZERO,image.get_size())))
				var candidate:=image.get_region(crop)
				var saved_recovery: float=npc.air_recovery;npc.air_recovery=0
				grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var idle_picture:=root.get_texture().get_image().get_region(crop)
				npc.air_recovery=saved_recovery
				var inventory: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-remaining-specials-audit-v1/inventory.json"))
				var old: Dictionary=inventory.selected[r.gear][r.state]
				var old_image:=Image.load_from_file(ProjectSettings.globalize_path(PRIOR[r.gear][r.state][3]))
				var old_texture:=ImageTexture.create_from_image(old_image)
				var candidate_texture=row[3]
				for name in candidate_texture.get_meta_list():old_texture.set_meta(name,candidate_texture.get_meta(name))
				old_texture.set_meta("crew_pivot",Vector2(old.pivot[0],old.pivot[1]));old_texture.set_meta("crew_standing_height",old.standingHeight)
				check(old_texture.get_meta("crew_frame_92",false),"Historical comparison retains room-renderer crew flag")
				row[3]=old_texture
				check(grid._get_veld_frame(game)==old_texture,"Actual renderer uses old comparison texture at identical elapsed pose")
				grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var old_picture:=root.get_texture().get_image().get_region(crop);row[3]=candidate_texture
				var comparison:=Image.create(crop.size.x*3,crop.size.y,false,Image.FORMAT_RGBA8)
				comparison.blit_rect(idle_picture,Rect2i(Vector2i.ZERO,crop.size),Vector2i.ZERO)
				comparison.blit_rect(old_picture,Rect2i(Vector2i.ZERO,crop.size),Vector2i(crop.size.x,0))
				comparison.blit_rect(candidate,Rect2i(Vector2i.ZERO,crop.size),Vector2i(crop.size.x*2,0))
				check(comparison.save_png(CAPTURES[r.state+"-"+r.gear])==OK,"Idle/old/new furnished comparison capture")'''
assert old in s;s=s.replace(old,new)
s=s.replace('Five authored rooms,dry selected standing geometry,candidate loaded explicitly,all48poses at8reviewed clear points.','Five authored rooms,4newly overlapping side-view points. Each comparison shows selected idle / prior frame3 / candidate frame3 at identical foot/camera;current candidates explicitly injected.')
(ROOT/'tools/review_veld_recovery_overlap_v1.gd').write_text(s)
(ROOT/'tools/review_veld_recovery_overlap_v1.gd.uid').write_text('uid://bg5r2n4m8s931\n')
s=(ROOT/'tools/run_veld_recovery_furnished_validation_v1.py').read_text().replace('output/veld-recovery-furnished-v1','output/veld-recovery-overlap-v1').replace('review_veld_recovery_furnished_v1.gd','review_veld_recovery_overlap_v1.gd')
(ROOT/'tools/run_veld_recovery_overlap_validation_v1.py').write_text(s)
print('Prepared4side-view overlap comparison cases at identical foot/camera')
