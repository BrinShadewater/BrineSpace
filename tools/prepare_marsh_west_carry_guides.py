"""Freeze own West identity and gait; never mirror implant-visible East."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_south_carry_guides.py').read_text().replace('south','west').replace('South','West').replace("record('walk-west',2)","record('walk-west',3)")
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
