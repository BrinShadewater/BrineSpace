from pathlib import Path
import shutil
H=Path(__file__).resolve().parent;R=H.parents[1];OLD=R/'character/krusher-head-fit-v7';(H/'native').mkdir(exist_ok=True)
shutil.copyfile(R/'character/krusher-style-neck-bank-v1/candidate-bank-index.json',H/'candidate-bank-index.json')
for name in ['build_package','validate_package','build_preview','polish_preview','review_final','run_native_verify','run_repair','run_bunk','run_water','run_west','refresh_bunk_scope']:
 text=(OLD/(name+'.py')).read_text(encoding='utf-8').replace('krusher-head-fit-v7','krusher-style-neck-v1').replace('krusher-animation-package-v8','krusher-animation-package-v9')
 if name=='validate_package':text=text.replace("OLD=R/'character/krusher-animation-package-v3'","OLD=R/'character/krusher-animation-package-v8'")
 (H/(name+'.py')).write_text(text,encoding='utf-8')
for name in ['verify','repair','bunk','water','west']:
 text=(OLD/'native'/(name+'.gd')).read_text(encoding='utf-8').replace('krusher-head-fit-v7','krusher-style-neck-v1').replace('krusher-animation-package-v8','krusher-animation-package-v9');(H/'native'/(name+'.gd')).write_text(text,encoding='utf-8')
shutil.copyfile(OLD/'bunk-scope.json',H/'bunk-scope.json')
print('Style/neck candidate packaging and isolated native validation staged.')
