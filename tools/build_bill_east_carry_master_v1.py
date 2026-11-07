"""Reuse uniform packing while retaining all eight carry metadata entries and stride."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/build_bill_east_run_master_v1.py').read_text(encoding='utf-8')
source=source.replace('bill-east-run-master-v1','bill-east-carry-master-v1').replace('run-east','carry-east').replace('range(6)','range(8)').replace('n_frames==6','n_frames==8').replace('(1536,860)','(2048,860)').replace('frames=6','frames=8').replace('decodedMovieFrames=24','decodedMovieFrames=32').replace('frameCount=6','frameCount=8')
source=source.replace("strideDistanceCells={'carry-east':m['strideDistanceCells']['carry-east']}","strideDistanceCells={'carry':m['strideDistanceCells']['carry']},textureFilter='linear'")
source=source.replace('Selected run','Selected carry').replace('Bill East whole master run repair','Bill East whole master carry repair').replace('Bill East run master repair','Bill East carry master repair').replace('master-matched running','master-matched carrying').replace('All six running poses','All eight carrying poses').replace('Original six-frame order, 540ms loop','Original eight-frame order, 840ms loop').replace('Selected running','Selected carrying').replace('../bill-run-head-locked-v1/frames/carry-east/000.png','../bill-carry-east-gait-v3/frames/bare/carry-east/000.png').replace('Running naturally leans and changes height','Carrying naturally changes leg pose')
exec(compile(source,str(R/'tools/build_bill_east_run_master_v1.py'),'exec'))
