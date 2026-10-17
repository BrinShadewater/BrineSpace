from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
s=(ROOT/'tests/test_veld_recover_air_east_candidates.gd').read_text()
s=s.replace('recover-air-east','recover-air-west').replace('actor.direction="east"','actor.direction="west"').replace('actor.animation_state()+"-east"','actor.animation_state()+"-west"')
(ROOT/'tests/test_veld_recover_air_west_candidates.gd').write_text(s)
(ROOT/'tests/test_veld_recover_air_west_candidates.gd.uid').write_text('uid://bv1h8s4g9m762\n')
s=(ROOT/'tools/run_veld_recover_air_east_candidate_validation.py').read_text().replace('recover_air_east','recover_air_west').replace('recover-air-east','recover-air-west').replace('staged east recovery','staged west recovery')
(ROOT/'tools/run_veld_recover_air_west_candidate_validation.py').write_text(s)
