"""Version the current-source furnished-room fixture without changing runtime."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['review_bill_east_master_world','ensure_bill_east_master_world_v4_uids','run_bill_east_master_world']:
 old=R/'tools'/(name+'_v4.gd' if name=='review_bill_east_master_world' else name+'.gd' if name.startswith('ensure') else name+'_v4.py')
 new=R/'tools'/(name+'_v5.gd' if name=='review_bill_east_master_world' else name.replace('v4','v5')+'.gd' if name.startswith('ensure') else name+'_v5.py')
 assert not new.exists(),new
 source=old.read_text(encoding='utf-8').replace('master_world_v4','master_world_v5').replace('master-world-v4','master-world-v5').replace('bill-east-reach-adjacent-motion-v1','bill-east-reach-adjacent-motion-v2')
 if name=='review_bill_east_master_world':
  source=source.replace('func capture(label:String', '''func occupied_height(texture:Texture2D)->int:
 var im=texture.get_image();var top=im.get_height();var bottom=-1
 for y in range(im.get_height()):
  for x in range(im.get_width()):
   if im.get_pixel(x,y).a>.5:top=mini(top,y);bottom=maxi(bottom,y)
 return bottom-top+1
func capture(label:String''')
  anchor=' var camera_foot=actor.foot'
  source=source.replace(anchor,''' var expected_heights=[148,148,149,149,149,148]
 for slot in range(6):check(occupied_height(player.frames["interact-east"][slot])==expected_heights[slot],"submitted current reach occupied height equals inspected source")
'''+anchor)
  source=source.replace('"selectedContact":[old.x,old.y]','"selectedContact":[old.x,old.y],"occupiedHeight":occupied_height(shown)')
 elif name=='run_bill_east_master_world':
  source=source.replace("else 'v4';assert version in ['v4']","else 'v5';assert version in ['v5']")
  source=source.replace("paths.add(ROOT/'tools/review_bill_east_reach_pilot_v3.py')","paths.add(ROOT/'tools/review_bill_east_reach_pilot_v3.py');paths.add(ROOT/'tools/build_bill_east_reach_adjacent_motion_v4.py');paths.add(ROOT/'tools/verify_bill_reach_stature_v2.py')")
  source=source.replace('read_text()','read_text(encoding="utf-8")')
 new.write_text(source,encoding='utf-8')
print('Created V5 current-bank native fixture, runner and scratch UID helper; six actual-source height assertions added.')
