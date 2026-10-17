from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'bill-seated-loops-east-v1/build.py').read_text().replace('east','west')
source=source.replace('(x>np.median(x))','(x<np.median(x))').replace('(bx>np.median(bx))','(bx<np.median(bx))').replace('dx=19-head.width/2','dx=20-head.width/2')
start=source.index('    specs=[')
end=source.index('\n    for action,name,heads',start)
source=source[:start]+"    specs=json.loads((P/'source-rulers.json').read_text())"+source[end:]
(P/'build.py').write_text(source)
print('Prepared fixed-ruler west loop builder;requires measured source-rulers.json')
