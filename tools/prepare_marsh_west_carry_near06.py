"""Freeze own near half against corrected complete far-support cargo."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_east_carry_near06.py').read_text().replace('east','west').replace('East','West').replace('EAST','WEST')
s=s.replace('RIGHT','TEMP_DIRECTION').replace('LEFT','RIGHT').replace('TEMP_DIRECTION','LEFT').replace('right-edge','left-edge')
s=s.replace('visible temple implant','bare visible temple with implant hidden on far side').replace('Keep its exact restrained inset side panel/single visible ivory left-edge latch','Keep its exact restrained plain inset side panel/single visible block ivory left-edge latch')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
