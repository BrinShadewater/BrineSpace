from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
for src,dest in [(R/'character/krusher-station-lifecycle-v3/native/west.gd',H/'native/west.gd'),(R/'character/krusher-station-lifecycle-v3/run_west.py',H/'run_west.py')]:
 text=src.read_text().replace('krusher-station-lifecycle-v3','krusher-head-fit-v7').replace('krusher-animation-package-v4','krusher-animation-package-v8');dest.write_text(text)
print('Final West cue review staged.')
