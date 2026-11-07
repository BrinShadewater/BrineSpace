"""Prepare independent West corrected-source actual actor fixture and publisher."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    mappings=[('tools/review_marsh_east_collapse_actor.gd','tools/review_marsh_west_collapse_actor.gd'),('tools/publish_marsh_east_collapse_actor.py','tools/publish_marsh_west_collapse_actor.py'),('tools/fingerprint_marsh_east_collapse.py','tools/fingerprint_marsh_west_collapse.py')]
    assert not any((ROOT/b).exists() for _,b in mappings)
    for a,b in mappings:
        text=(ROOT/a).read_text().replace('east','west').replace('East','West').replace('EAST','WEST')
        if 'review_' in b or 'publish_' in b:
            text=text.replace('candidate-01','candidate-02').replace('west-collapse-actor-01','west-collapse-actor-02')
        if 'fingerprint_' in b:
            text=text.replace("['sources','candidate-01']","['sources','candidate-01','candidate-02']")
            text=text.replace("'tools/prepare_marsh_west_damage_guides.py'","'tools/prepare_marsh_west_damage_guides.py','tools/prepare_marsh_west_damage_guides_helper.py'")
            text=text.replace("'tools/prepare_marsh_west_collapse_fixture.py'","'tools/prepare_marsh_west_collapse_native.py','tools/prepare_marsh_west_collapse_soften.py','tools/retain_prepare_marsh_west_soften.py','tools/build_marsh_west_collapse_soften.py'")
        (ROOT/b).write_text(text)
    (ROOT/'tools/review_marsh_west_collapse_actor.gd.uid').write_text('uid://cj9whclpm5v77\n')
    print('Prepared corrected West actual actor study, publisher and bounded freeze.')
if __name__=='__main__':main()
