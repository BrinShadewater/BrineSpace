"""Use raw PNG buffers for expected images; preserve the warning-bearing V1 run."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_installed_coverage_v1.gd').read_text().replace('output/bill-installed-coverage-v1/','output/bill-installed-coverage-v2/')
s=s.replace('var expected=Image.load_from_file("res://"+str(state.files[i]));expected.convert(Image.FORMAT_RGBA8)','var expected=Image.new();check(expected.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+str(state.files[i])))==OK,"raw expected PNG decoded");expected.convert(Image.FORMAT_RGBA8)')
(R/'tools/review_bill_installed_coverage_v2.gd').write_text(s,encoding='utf-8');(R/'tools/review_bill_installed_coverage_v2.gd.uid').write_text('uid://c4billcoverage2\n')
s=(R/'tools/run_bill_installed_coverage_v1.py').read_text().replace("output/bill-installed-coverage-v1","output/bill-installed-coverage-v2").replace('review_bill_installed_coverage_v1','review_bill_installed_coverage_v2').replace('run_bill_installed_coverage_v1','run_bill_installed_coverage_v2')
(R/'tools/run_bill_installed_coverage_v2.py').write_text(s,encoding='utf-8')
