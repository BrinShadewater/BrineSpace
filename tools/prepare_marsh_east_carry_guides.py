"""Prepare own implant-visible side cargo guides; never mirror West sources."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/prepare_marsh_south_carry_guides.py').read_text().replace('south','east').replace('South','East').replace("record('walk-east',2)","record('walk-east',3)")
exec(compile(source,str(ROOT/'tools/prepare_marsh_east_carry_guides.py'),'exec'),{'__file__':str(ROOT/'tools/prepare_marsh_east_carry_guides.py'),'__name__':'__main__'})
