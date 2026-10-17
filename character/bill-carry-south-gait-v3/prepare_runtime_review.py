"""Fixture-only South source admission with selected controller/player types."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_carry_north_start_station_v2.gd').read_text(encoding='utf-8')
s=s.replace('bill-carry-north-start-station-v2','bill-carry-south-start-station-v2').replace('bill-carry-north-gait-v2','bill-carry-south-gait-v3').replace('bill-carry-start-north-v2','bill-carry-start-south-v2').replace('north','south').replace('North','South').replace('NORTH','SOUTH')
s=s.replace('actor.foot=finish;','actor.foot=begin;').replace('actor.path=PackedVector2Array([begin])','actor.path=PackedVector2Array([finish])')
s=s.replace('   game.bill_npc=original_actor\n   game.bill_npc=original_actor','   game.bill_npc=original_actor')
(R/'tests/test_bill_carry_south_start_station_v2.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_carry_south_start_station_v2.gd.uid').write_text('uid://s4n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_carry_north_start_station_v2_validation.py').read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH')
(R/'tools/run_bill_carry_south_start_station_v2_validation.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_carry_north_start_player_v2.gd').read_text(encoding='utf-8').replace('bill-carry-north-gait-v2','bill-carry-south-gait-v3').replace('bill-carry-start-north-v2','bill-carry-start-south-v2').replace('north','south').replace('North','South').replace('NORTH','SOUTH').replace('Vector2(0,-tick*.002)','Vector2(0,tick*.002)')
(R/'tests/test_bill_carry_south_start_player_v2.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_carry_south_start_player_v2.gd.uid').write_text('uid://t4n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_carry_north_start_player_v2_validation.py').read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH')
(R/'tools/run_bill_carry_south_start_player_v2_validation.py').write_text(s,encoding='utf-8')
print('South player/native review fixtures saved; selected controller types, fixture-only source overrides')
