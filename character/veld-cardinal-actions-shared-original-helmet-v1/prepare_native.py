from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_south_shared_original_helmet_v2.gd').read_text()
s=s.replace('character/veld-south-shared-original-helmet-v1/','character/veld-cardinal-actions-shared-original-helmet-v1/')
s=s.replace('character/veld-idle-south-original-master-v1/bare-manifest.json','character/veld-cardinal-actions-shared-original-helmet-v1/baseline-bare-manifest.json').replace('character/veld-idle-south-original-master-v1/helmet-manifest.json','character/veld-cardinal-actions-shared-original-helmet-v1/baseline-helmet-manifest.json')
s=s.replace('output/veld-south-shared-original-helmet-v2/','output/veld-cardinal-actions-shared-original-helmet-v1/').replace('veld-south-helmet-scratch','veld-cardinal-helmet-scratch').replace('VELD SOUTH SHARED ORIGINAL HELMET','VELD CARDINAL ACTIONS SHARED ORIGINAL HELMET')
a=s.index('\t\tfor join in ');b=s.index('\n\tvar file :=',a)
s=s[:a]+'''\t\tfor direction in ["north","east","west"]:
\t\t\tfor join in [["unload",-1,"pickup",0],["pickup",-1,"carry-start",0],["carry-start",-1,"carry",0],["carry-stop",-1,"pickup",-1]]:
\t\t\t\tvar from_key: String=join[0]+"-"+direction
\t\t\t\tvar to_key: String=join[2]+"-"+direction
\t\t\t\tvar from_time: float=player.cycle_seconds(from_key,equipment) if join[1]==-1 else 0.0
\t\t\t\tvar to_time: float=player.cycle_seconds(to_key,equipment) if join[3]==-1 else 0.0
\t\t\t\tcheck(player.frame_at_elapsed(from_key,from_time,equipment).get_image().get_data()==player.frame_at_elapsed(to_key,to_time,equipment).get_image().get_data(),"Exact lifecycle source join")
\t\tvar turns=load("res://scripts/crew_sprite_player.gd").new()
\t\tturns.load_manifest("res://character/veld-helmet-original-turntable-west-v1/bare-manifest.json")
\t\tcheck(turns.load_equipment_manifest("diving-helmet","res://character/veld-helmet-original-turntable-west-v1/helmet-manifest.json"),"Quarter equipment loaded")
\t\tfor pair in [["north","north-east"],["east","east-south"],["west","west-north"]]:
\t\t\tcheck(player.frame_at_elapsed("pickup-"+pair[0],player.cycle_seconds("pickup-"+pair[0],equipment),equipment).get_image().get_data()==turns.frame_at_elapsed("carry-turn-"+pair[1],0,equipment).get_image().get_data(),"Exact cardinal held/turn equipment and body")
'''+s[b:]
(R/'tests/test_veld_cardinal_actions_shared_original_helmet_v1.gd').write_text(s)
(R/'tests/test_veld_cardinal_actions_shared_original_helmet_v1.gd.uid').write_text('uid://cvldcardinalshorig1\n')
s=(R/'tools/run_veld_south_shared_original_helmet_v2.py').read_text().replace('output/veld-south-shared-original-helmet-v2','output/veld-cardinal-actions-shared-original-helmet-v1').replace('character/veld-south-shared-original-helmet-v1','character/veld-cardinal-actions-shared-original-helmet-v1').replace('test_veld_south_shared_original_helmet_v2.gd','test_veld_cardinal_actions_shared_original_helmet_v1.gd').replace('veld-south-helmet-scratch','veld-cardinal-helmet-scratch').replace('character/veld-idle-south-original-master-v1','character/veld-helmet-original-turntable-west-v1').replace('South original-master body/shared helmet six states/both gears, actual elapsed source clocks and exact lifecycle source joins.','N/E/W shared original helmet15actions/both gears; prescribed explicit-modulo elapsed source clocks and exact lifecycle/cardinal turn joins.')
(R/'tools/run_veld_cardinal_actions_shared_original_helmet_v1.py').write_text(s)
