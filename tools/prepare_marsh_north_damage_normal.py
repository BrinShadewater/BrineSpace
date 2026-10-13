"""Prepare standalone normal North checkpoint test and scoped publisher."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    fixture=ROOT/'tests/test_marsh_north_damage_production.gd'
    publisher=ROOT/'tools/publish_marsh_north_damage_normal.py'
    assert not fixture.exists() and not publisher.exists(),'already prepared; preserve independent files'
    text=(ROOT/'tests/test_marsh_south_damage_production.gd').read_text()
    text=text.replace('south','north').replace('South','North').replace('SOUTH','NORTH')
    fixture.write_text(text);fixture.with_suffix('.gd.uid').write_text('uid://cf5nhdamn1v73\n')
    text=(ROOT/'tools/publish_marsh_south_damage_normal.py').read_text()
    text=text.replace('south','north').replace('South','North').replace('SOUTH','NORTH')
    text=text.replace('../marsh-north-collapse-material-v1/candidate-01/manifest.json','../marsh-north-collapse-material-v1/candidate-02/manifest.json')
    text=text.replace("['east','west','north','north']","['east','west','north','south']")
    text=text.replace('Other-facing old boots/grade','Other-facing master/material joins')
    publisher.write_text(text)
    print('Prepared normal North full-save/Continue fixture, pairedUID and publisher.')
if __name__=='__main__':main()
