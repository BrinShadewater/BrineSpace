"""Prepare independently registered West coolant with exact complete body poses."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    mappings=[('tools/build_marsh_north_injury_material.py','tools/build_marsh_west_injury_material.py'),('tools/review_marsh_north_injury_actor.gd','tools/review_marsh_west_injury_actor.gd'),('tools/publish_marsh_north_injury_material.py','tools/publish_marsh_west_injury_material.py'),('tools/fingerprint_marsh_east_injury_actor.py','tools/fingerprint_marsh_west_injury_actor.py')]
    assert not any((ROOT/b).exists() for _,b in mappings)
    for a,b in mappings:
        text=(ROOT/a).read_text().replace('north','west').replace('North','West').replace('NORTH','WEST') if 'east_' not in a else (ROOT/a).read_text().replace('east','west').replace('East','West')
        if 'build_' in b:text=text.replace('puddle_center=(135,172);anchors={1:(114,141),2:(120,142)}','puddle_center=(72,172);anchors={1:(78,124),2:(82,142)}')
        if 'publish_' in b:text=text.replace('107 bounded inputs stable','Bounded inputs stable')
        if 'fingerprint_' in b:text=text.replace('tools/prepare_marsh_west_injury_helpers.py','tools/prepare_marsh_west_injury_guides.py')
        (ROOT/b).write_text(text)
    (ROOT/'tools/review_marsh_west_injury_actor.gd.uid').write_text('uid://ck1whinjm6v78\n')
    print('Prepared West body/effect builder, actual impact fixture, publisher and input freeze.')
if __name__=='__main__':main()
