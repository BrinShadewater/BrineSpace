from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-air-family-v1/build.py').read_text()
source=source.replace("james-air-", "james-death-")
source=source.replace("P/'endpoints'/mode", "P.parent/'james-air-family-v1/endpoints'/mode")
source=source.replace("('swim-distress',range(6)),('recover-air',range(6,12))", "('death-ground',range(6)),('death-water',range(6,12))")
source=source.replace("action=='swim-distress'", "action=='death-water'")
source=source.replace("'swim' if action=='swim-distress' else 'idle'", "'swim' if action=='death-water' else 'idle'")
start=source.index("    donor_key=")
end=source.index("donor=hreg",start)
source=source[:start]+"    donor_key=str(c[action]['helmetDonors'][j]);"+source[end:]
needle="patch=Image.fromarray(pa)"
source=source.replace(needle,needle+";patch=patch.rotate(c[action].get('helmetAngles',[0]*6)[j],resample=Image.Resampling.BICUBIC,expand=True)")
start=source.index("   if action=='death-water':\n    for mode,rows")
end=source.index("   records[d]['actions']",start)
source=source[:start]+"   for mode,rows in [('bare',bare),('helmet',helmet)]:rows[0]=endpoint(mode,'swim' if action=='death-water' else 'idle',d)\n"+source[end:]
source=source.replace("Fixed anatomical scale per action row; fixed material gains per row; reused selected shared helmets; exact swim loop seam or final idle endpoint", "Fixed anatomical scale per action row; fixed material gains per row; shared helmets with recorded pitch; exact idle/swim entry, finite terminal hold")
source=source.replace("Exact swim seams/final idle", "Exact idle/swim entries")
source=source.replace("['swim-distress','recover-air']", "['death-ground','death-water']")
source=source.replace("James distress/recovery", "James ground/water death")
source=source.replace("Staged8 states/48 refs per mode, exact swim seams/final idle, retained960ms/3sec clocks", "Staged8 death states/48 refs per mode, exact entry seams, retained finite clocks")
source=source.replace("helmetScale=hscale,helmetPosition", "helmetScale=hscale,helmetAngle=c[action].get('helmetAngles',[0]*6)[j],helmetPosition")
assert "swim-distress" not in source and "recover-air" not in source
dest=P/'build.py'
if dest.exists(): raise RuntimeError('Do not overwrite reviewed death builder')
dest.write_text(source,encoding='utf-8')
print('Prepared fixed-anatomy death builder; reviewed configs required')
