"""Uniform whole-source packing preserving six selected torch timings."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/build_bill_east_run_master_v1.py').read_text(encoding='utf-8')
s=s.replace('bill-east-run-master-v1','bill-east-torch-master-v1').replace('run-east','weld-east')
s=s.replace("strideDistanceCells={'weld-east':m['strideDistanceCells']['weld-east']}","strideDistanceCells={},textureFilter='linear'")
s=s.replace('Selected run','Selected torch').replace('master run repair','master torch repair').replace('run master repair','torch master repair').replace('master-matched running','master-matched torch work')
s=s.replace('All six running poses','All six torch poses').replace('540ms loop and stride setting','960ms loop').replace('Selected running','Selected torch work')
s=s.replace('../bill-run-head-locked-v1/frames/weld-east/000.png','../bill-torch-actions-v1/frames/weld-east/000.png').replace('Running naturally leans and changes height','Torch work retains its original grip and flame direction')
s=s.replace('Selected torchning','Selected torch work')
exec(compile(s,str(__file__),'exec'))
