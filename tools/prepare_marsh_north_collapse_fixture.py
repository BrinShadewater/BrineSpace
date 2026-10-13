"""Create standalone North native actor study without modifying South proof."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    target=ROOT/'tools/review_marsh_north_collapse_actor.gd';assert not target.exists()
    source=(ROOT/'tools/review_marsh_south_collapse_actor.gd').read_text()
    source=source.replace('south-collapse-actor-01-2026-10-02','north-collapse-actor-02-2026-10-02').replace('character/marsh-south-collapse-material-v1/candidate-01/manifest.json','character/marsh-north-collapse-material-v1/candidate-02/manifest.json').replace('south','north').replace('South','North').replace('SOUTH','NORTH')
    # Original fixture checked South offsets; the North first term is now correct.
    # Keep all locomotion offsets inactive for this pure dry shutdown site.
    source=source.replace('actor.north_draw_offset() == Vector2.ZERO','actor.south_draw_offset() == Vector2.ZERO')
    target.write_text(source)
    print('Standalone North actual actor fixture created from established dry study setup.')
if __name__=='__main__':main()
