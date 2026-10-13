"""Prepare independent East normal checkpoint/admission tools from proven lane."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    pairs=[('tests/test_marsh_north_damage_production.gd','tests/test_marsh_east_damage_production.gd'),('tools/publish_marsh_north_damage_normal.py','tools/publish_marsh_east_damage_normal.py'),('tools/install_marsh_north_damage_material.py','tools/install_marsh_east_damage_material.py'),('tools/fingerprint_marsh_north_damage_normal.py','tools/fingerprint_marsh_east_damage_normal.py')]
    assert not any((ROOT/target).exists() for _,target in pairs)
    for source,target in pairs:
        text=(ROOT/source).read_text().replace('north','east').replace('North','East').replace('NORTH','EAST').replace('candidate-02','candidate-01')
        text=text.replace("['east','west','east','south']","['east','west','north','south']")
        text=text.replace('rear dark soles retained','ivory boot uppers and matte dark soles retained')
        (ROOT/target).write_text(text)
    (ROOT/'tests/test_marsh_east_damage_production.gd.uid').write_text('uid://ci8ehdamn4v76\n')
    print('Prepared East normal selection, full-checkpoint fixture/UID and scoped publisher/freeze.')
if __name__=='__main__':main()
