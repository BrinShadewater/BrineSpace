"""Prepare own West normal damage checkpoint/admission tools."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    pairs=[('tests/test_marsh_north_damage_production.gd','tests/test_marsh_west_damage_production.gd'),('tools/publish_marsh_north_damage_normal.py','tools/publish_marsh_west_damage_normal.py'),('tools/install_marsh_north_damage_material.py','tools/install_marsh_west_damage_material.py'),('tools/fingerprint_marsh_north_damage_normal.py','tools/fingerprint_marsh_west_damage_normal.py')]
    assert not any((ROOT/b).exists() for _,b in pairs)
    for a,b in pairs:
        text=(ROOT/a).read_text().replace('north','west').replace('North','West').replace('NORTH','WEST')
        text=text.replace("['east','west','west','south']","['east','west','north','south']")
        text=text.replace('rear dark soles retained','ivory boot uppers and charcoal sole material retained')
        (ROOT/b).write_text(text)
    (ROOT/'tests/test_marsh_west_damage_production.gd.uid').write_text('uid://cl2whdamn7v79\n')
    print('Prepared own West normal selection/20checkpoint fixture/UID and proof helpers.')
if __name__=='__main__':main()
