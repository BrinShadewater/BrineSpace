"""Prepare own rear cargo references with North's opposite walk0/walk3 guides."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/prepare_marsh_south_carry_guides.py').read_text().replace('south','north').replace('South','North').replace("record('walk-north',2)","record('walk-north',3)")
exec(compile(source,str(ROOT/'tools/prepare_marsh_north_carry_guides.py'),'exec'),{'__file__':str(ROOT/'tools/prepare_marsh_north_carry_guides.py'),'__name__':'__main__'})
