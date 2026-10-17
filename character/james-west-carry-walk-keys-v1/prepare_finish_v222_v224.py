from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_finish_v215_v216.py').read_text(encoding='utf-8')
s=s.replace('[(35,215),(36,216)]','[(40,222),(41,223),(42,224)]')
s=s.replace('The feet are separating: the boot on the left points left, while the boot on the right retains its diagonal down-left toe and raised up-right heel.', 'This is a wider stride with separated feet. Preserve the exact original toe and heel heights and independent sole angles of each boot in Image1. Do not force them to a shared pitch or floor height.')
exec(compile(s,str(p/'prepare_finish_v222_v224.py'),'exec'))
