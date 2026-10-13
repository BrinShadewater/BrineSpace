"""Prepare independent East complete-body effect builder and impact harness."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    builder=ROOT/'tools/build_marsh_east_injury_material.py';fixture=ROOT/'tools/review_marsh_east_injury_actor.gd';publisher=ROOT/'tools/publish_marsh_east_injury_material.py'
    assert not any(p.exists() for p in [builder,fixture,publisher])
    text=(ROOT/'tools/build_marsh_north_injury_material.py').read_text().replace('north','east').replace('North','East').replace('candidate-02','candidate-01')
    text=text.replace('puddle_center=(135,172);anchors={1:(114,141),2:(120,142)}','puddle_center=(122,172);anchors={1:(98,114),2:(106,134)}')
    builder.write_text(text)
    text=(ROOT/'tools/review_marsh_north_injury_actor.gd').read_text().replace('north','east').replace('North','East').replace('NORTH','EAST')
    fixture.write_text(text);fixture.with_suffix('.gd.uid').write_text('uid://ch7ehinjm3v75\n')
    text=(ROOT/'tools/publish_marsh_north_injury_material.py').read_text().replace('north','east').replace('North','East').replace('candidate-02','candidate-01').replace('107 bounded inputs stable','Bounded inputs stable')
    publisher.write_text(text)
    print('Prepared East effect placement and independent impact fixture/publisher.')
if __name__=='__main__':main()
