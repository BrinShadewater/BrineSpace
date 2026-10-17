from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-north-rest-polish-v1/native-installed.gd').read_text().replace('james-north-rest-polish-v1','james-water-north-polish-v1').replace('JAMES NORTH REST INSTALLED','JAMES NORTH WATER POLISH INSTALLED')
s=s.replace('check(frame.get_meta("crew_depth_offset")==float(state.depthOffsets[i]),"Furniture depth")','check(frame.get_meta("crew_water_pose")==true,"Water pose")')
s=s.replace('Vector2(128,224)','Vector2(128,128)').replace('"Foot pivot"','"Water pivot"')
(P/'native-installed.gd').write_text(s)
print('Prepared actual normal-grid36-slot installed proof')
