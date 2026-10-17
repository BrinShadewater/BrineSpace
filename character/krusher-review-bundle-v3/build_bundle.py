from pathlib import Path
import hashlib,json,shutil,zipfile
P=Path(__file__).resolve().parent;R=P.parent.parent;P.mkdir(exist_ok=True)
files={
 'images/character-sheet.png':'character/krusher-production-reference-v1/character-sheet.png',
 'images/head-sheet.png':'character/krusher-production-reference-v1/head-registration-sheet.png',
 'images/equipment-sheet.png':'character/krusher-production-reference-v1/equipment-reference-sheet.png',
 'images/terminal-sheet.png':'character/krusher-production-reference-v1/terminal-key-pose-sheet.png',
 'images/base-families.png':'character/crew-base-reference-v1/base-family-comparison.png',
 'images/blink-sheet.png':'character/krusher-blink-study-v1/blink-reference-sheet.png',
 'videos/full-motion.mp4':'character/krusher-runtime-candidate-v1/review/full-motion-preview.mp4',
 'videos/bare-blink.mp4':'character/krusher-moving-blink-test-v1/review/blink-motion-preview.mp4',
 'videos/helmet-blink.mp4':'character/krusher-helmet-blink-test-v1/review/blink-motion-preview.mp4',
 'runtime/bare-manifest.json':'character/krusher-runtime-candidate-v1/bare-manifest.json',
 'runtime/helmet-manifest.json':'character/krusher-runtime-candidate-v1/helmet-manifest.json',
 'runtime/provenance.json':'character/krusher-runtime-candidate-v1/provenance.json',
 'evidence/package-validation.json':'character/krusher-runtime-candidate-v1/validation.json',
 'evidence/consumer-report.json':'character/krusher-runtime-candidate-v1/review/native/report.json',
 'evidence/motion-validation.json':'character/krusher-runtime-candidate-v1/review/motion/validation.json',
 'evidence/reference-manifest.json':'character/krusher-production-reference-v1/reference-manifest.json',
 'evidence/base-catalog.json':'character/crew-base-reference-v1/catalog.json',
 'evidence/bare-blink-verification.json':'character/krusher-moving-blink-test-v1/verification.json',
 'evidence/helmet-blink-verification.json':'character/krusher-helmet-blink-test-v1/verification.json',
 'evidence/blink-source-provenance.json':'character/krusher-blink-study-v1/provenance.json',
 'evidence/blink-prompt.txt':'character/krusher-blink-study-v1/prompt-blink.txt',
 'fonts/BarlowSemiCondensed-Regular.ttf':'assets/fonts/BarlowSemiCondensed-Regular.ttf',
 'fonts/BarlowSemiCondensed-SemiBold.ttf':'assets/fonts/BarlowSemiCondensed-SemiBold.ttf',
 'fonts/OFL.txt':'assets/fonts/OFL.txt','NOTICE.md':'NOTICE.md'}
files.update({
 'images/james-character-sheet.png':'character/krusher-james-helmet-fit-v2/review/cardinal-comparison.png',
 'images/bill-james-comparison.png':'character/krusher-james-cyan-test-v1/review/bill-james-comparison.png',
 'images/family-fit-study.png':'character/krusher-family-fit-study-v2/family-fit-comparison.png',
 'videos/james-motion.mp4':'character/krusher-james-helmet-fit-v2/review/motion-preview.mp4',
 'runtime/james/bare/manifest.json':'character/krusher-james-cyan-test-v2/manifest.json',
 'runtime/james/helmet/manifest.json':'character/krusher-james-helmet-fit-v2/manifest.json',
 'evidence/james-bare-validation.json':'character/krusher-james-cyan-test-v2/validation.json',
 'evidence/james-helmet-validation.json':'character/krusher-james-helmet-fit-v2/validation.json',
 'evidence/james-helmet-native.json':'character/krusher-james-helmet-fit-v2/review/native/report.json',
 'evidence/james-bare-provenance.json':'character/krusher-james-cyan-test-v2/verification.json',
 'evidence/james-helmet-provenance.json':'character/krusher-james-helmet-fit-v2/verification.json',
 'evidence/james-preview.json':'character/krusher-james-helmet-fit-v2/review/preview.json',
 'evidence/bill-gait-report.json':'character/krusher-runtime-candidate-v1/review/gait-report.json',
 'reuse-guidance.md':'character/krusher-review-bundle-v3/reuse-guidance.md'
})
files.update({
 'images/four-moving-families.png':'character/krusher-marsh-cyan-test-v1/review/four-family-comparison.png',
 'images/veld-character-sheet.png':'character/krusher-veld-helmet-fit-v1/review/cardinal-comparison.png',
 'images/marsh-character-sheet.png':'character/krusher-marsh-cyan-test-v1/review/cardinal-comparison.png',
 'videos/veld-motion.mp4':'character/krusher-veld-helmet-fit-v1/review/motion-preview.mp4',
 'videos/marsh-motion.mp4':'character/krusher-marsh-cyan-test-v1/review/motion-preview.mp4'
})
for family,gear,folder in [('veld','bare','krusher-veld-cyan-test-v2'),('veld','helmet','krusher-veld-helmet-fit-v1'),('marsh','bare','krusher-marsh-cyan-test-v1')]:
    source=f'character/{folder}/manifest.json';files[f'runtime/{family}/{gear}/manifest.json']=source
    files[f'evidence/{family}-{gear}-validation.json']=f'character/{folder}/validation.json'
    files[f'evidence/{family}-{gear}-provenance.json']=f'character/{folder}/verification.json'
    files[f'evidence/{family}-{gear}-native.json']=f'character/{folder}/review/native/report.json'
    for state in json.loads((R/source).read_text())['states']:
        for frame in state['frameFiles']:files[f'runtime/{family}/{gear}/'+frame]=(Path(source).parent/Path(frame)).as_posix()
for gear in ['bare','helmet']:
    source=files[f'runtime/james/{gear}/manifest.json']
    manifest=json.loads((R/source).read_text())
    for state in manifest['states']:
        for frame in state['frameFiles']:files[f'runtime/james/{gear}/'+frame]=str(Path(source).parent/Path(frame)).replace('\\','/')
for gear in ['bare','helmet']:
    manifest=json.loads((R/files[f'runtime/{gear}-manifest.json']).read_text())
    for state in manifest['states']:
        for frame in state['frameFiles']:files['runtime/'+frame]='character/krusher-runtime-candidate-v1/'+frame
records=[]
for target,source in files.items():
    src=R/source;dst=P/target;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst) if src.resolve()!=dst.resolve() else None
    records.append({'file':target,'projectSource':source,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size})
(P/'source-map.json').write_text(json.dumps({'scope':'Owner review delivery; original source packages remain authoritative. Facial studies are excluded from runtime manifests.','files':records},indent=2)+'\n')
included=[r['file'] for r in records]+['source-map.json','index.html','README.md']
archive=P/'Krusher-Dom-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in included:z.write(P/path,path)
preview=P/'Krusher-Dom-preview.zip';preview_records=[r for r in records if not r['file'].startswith('runtime/')]
with zipfile.ZipFile(preview,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for record in preview_records:z.write(P/record['file'],record['file'])
    for path in ['index.html','README.md']:z.write(P/path,path)
    z.writestr('source-map.json',json.dumps({'scope':'Preview-only owner review delivery; runtime assets are in the full download. Facial studies remain separate from the runtime candidate.','files':preview_records},indent=2)+'\n')
print(json.dumps({'fullArchive':archive.name,'fullFiles':len(included),'fullBytes':archive.stat().st_size,'previewArchive':preview.name,'previewFiles':len(preview_records)+3,'previewBytes':preview.stat().st_size,'runtimeUniquePngs':len([p for p in files if p.startswith('runtime/') and p.endswith('.png')])}))
