"""Freeze own West cargo figures, primary body and complete opposite stances."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_east_carry01.py').read_text().replace('east','west').replace('East','West').replace('EAST','WEST')
s=s.replace('RIGHT','TEMP_DIRECTION').replace('LEFT','RIGHT').replace('TEMP_DIRECTION','LEFT')
s=s.replace('visible LEFT-temple metal implant','bare visible temple; implant on far hidden side').replace('Preserve own asymmetric temple implant and authentic ankle hardware','Preserve own bare visible temple/far-side implant identity and authentic ankle hardware')
s=s.replace('Plain restrained recessed front panel/two small original ivory latches','Plain restrained recessed side panel/SINGLE small ivory latch on LEFT edge, consistently matching the first own West crate projection')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
