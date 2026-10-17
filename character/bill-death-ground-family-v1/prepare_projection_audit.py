from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[1]
source=(R/'tests/test_bill_death_ground_station_lowered_candidates.gd').read_text()
source=source.replace('bill-death-ground-station-candidate-v1','bill-death-ground-projection-audit-v1')
source=source.replace('var records:=[]','var records:=[]\n\tvar projections:=[]\n\tvar props:=[]\n\tfor prop in data.get("props",[]):\n\t\tvar bounds:=[]\n\t\tfor rect in actor.Geometry.prop_collision_rects(prop):bounds.append(rect_array(rect))\n\t\tprops.append({"id":prop.get("id",""),"sortY":prop.get("sort_y",0),"collisionRects":bounds})')
needle='\t\t\t\tvar foot:Vector2=actor.foot;'
assert needle in source
source=source.replace(needle,'''\t\t\t\tvar row:Array=player.equipment_frames["diving-helmet"]["death-ground-"+d] if gear else player.frames["death-ground-"+d]
\t\t\t\tfor slot in row.size():
\t\t\t\t\tprojections.append(projected_overlap(row[slot],contact[1],d,gear,slot,data))
'''+needle)
needle='\tvar file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);'
assert needle in source
source=source.replace(needle,'''\tvar audit:=FileAccess.open(OUT+"projection-audit.json",FileAccess.WRITE)
\taudit.store_string(JSON.stringify({"scope":"screen-space alpha against registered collision rectangles; not anatomical floor footprint certification", "actorDrawLift":384*.038,"props":props,"records":projections},"\\t"));audit.close()
\tcheck(projections.size()==96,"All six authored slots at two contacts, four directions, two gears audited")
'''+needle)
source+='''
func rect_array(rect:Rect2) -> Array:
\treturn [rect.position.x,rect.position.y,rect.size.x,rect.size.y]
func projected_overlap(texture:Texture2D,local:Vector2,direction:String,gear:bool,slot:int,data:Dictionary) -> Dictionary:
\tvar image:Image=texture.diffuse_texture.get_image() if texture is CanvasTexture else texture.get_image()
\tvar pivot:Vector2=texture.get_meta("crew_pivot")
\tvar density:float=65.28/texture.get_meta("crew_standing_height")
\tvar overlaps:=[]
\tfor prop in data.get("props",[]):
\t\tvar pixels:=0
\t\tvar bounds:Array=game.bill_npc.Geometry.prop_collision_rects(prop)
\t\tfor y in image.get_height():
\t\t\tfor x in image.get_width():
\t\t\t\tif image.get_pixel(x,y).a<.5:continue
\t\t\t\tvar projected:Vector2=local+Vector2(0,384*.038)+(Vector2(x+.5,y+.5)-pivot)*density
\t\t\t\tfor rect in bounds:
\t\t\t\t\tif rect.has_point(projected):pixels+=1;break
\t\tif pixels:overlaps.append({"prop":prop.get("id",""),"opaquePixels":pixels,"sortY":prop.get("sort_y",0),"actorDrawY":local.y+384*.038})
\treturn {"local":[local.x,local.y],"direction":direction,"gear":gear,"slot":slot,"projectedExtent":rect_array(Rect2(local+Vector2(0,384*.038)+texture.get_meta("crew_alpha_extent").position,texture.get_meta("crew_alpha_extent").size)),"overlaps":overlaps}
'''
(R/'tests/test_bill_death_ground_projection_audit.gd').write_text(source,encoding='utf-8')
(R/'tests/test_bill_death_ground_projection_audit.gd.uid').write_text('uid://a9b8w3m6p2r9v\n')
runner=(R/'tools/run_bill_death_ground_station_lowered_candidate_validation.py').read_text().replace('bill-death-ground-station-candidate-v1','bill-death-ground-projection-audit-v1').replace('test_bill_death_ground_station_lowered_candidates.gd','test_bill_death_ground_projection_audit.gd')
(R/'tools/run_bill_death_ground_projection_audit.py').write_text(runner,encoding='utf-8')
print('Prepared independent 96-pose projected overlap audit; prior captures preserved')
