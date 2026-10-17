from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-water-cargo-family-v1/native-staged.gd').read_text().replace('james-water-cargo-family-v1','james-air-family-v1').replace('JAMES WATER CARGO STAGED:','JAMES AIR STAGED:')
s=s.replace('Vector2(128,128)','Vector2(128,224)').replace('get_meta("crew_water_pose")==true','get_meta("crew_water_pose")==state.waterPoses[i]')
a=s.index('\t\tfor d in ["east","south","west","north"]:');b=s.index('\t\tif DisplayServer',a);s=s[:a]+s[b:]
s=s.replace('Vector2(110+i*210,75+r*150)','Vector2(110+i*210,(35 if m.states[r].waterPoses[0] else 135)+r*150)')
(P/'native-staged.gd').write_text(s)
print('Prepared standalone player + native82px distress/recovery checks')
