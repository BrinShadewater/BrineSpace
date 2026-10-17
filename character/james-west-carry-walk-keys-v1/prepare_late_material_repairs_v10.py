from pathlib import Path
p = Path(__file__).resolve().parent
source = (p / 'prepare_material_repairs_v10.py').read_text()
source = source.replace('((21, (20, 22)), (34, (33, 35)))', '((45, (44, 47)), (46, (44, 47)))')
source = source.replace('if j == 20 else', 'if j in (20, 44) else')
source = source.replace('files.extend((base, promptfile, Path(__file__),', "files.extend((base, promptfile, Path(__file__), p / 'prepare_material_repairs_v10.py',")
exec(compile(source, str(p / 'prepare_material_repairs_v10.py'), 'exec'))
