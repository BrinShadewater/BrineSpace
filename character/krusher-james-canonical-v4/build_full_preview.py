from pathlib import Path
import hashlib, json, subprocess

P = Path(__file__).resolve().parent
review = P / 'review'
sources = [P.parent/'krusher-james-canonical-v3',P]
entries, chapters = [], []
elapsed = 0
for root in sources:
    report = json.loads((root / 'review/motion/report.json').read_text())
    for sample, slot in zip([s for s in report['samples'] if s['cycle'] == 0], report['schedule']):
        if root != P and sample['state'].endswith('-north'):continue
        path = root / 'review/motion' / sample['capture']
        if not chapters or chapters[-1]['state'] != sample['state']:
            chapters.append({'state': sample['state'], 'startMs': elapsed})
        entries.append({'capture': str(path), 'durationMs': slot['durationMs'], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        elapsed += slot['durationMs']
concat = review / 'motion-concat.txt'
def quote(path):
    return "'" + str(path).replace('\\', '/').replace("'", "'\\''") + "'"
concat.write_text(''.join(f"file {quote(e['capture'])}\nduration {e['durationMs']/1000:.6f}\n" for e in entries) + f"file {quote(entries[-1]['capture'])}\n")
with (review / 'media-encode.log').open('w') as log:
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning', '-f', 'concat', '-safe', '0', '-i', str(concat), '-vf', 'fps=60', '-t', str(elapsed/1000), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(review / 'full-motion-preview.mp4')], stdout=log, stderr=subprocess.STDOUT, check=True)
meta = {'method': 'Native captured poses replayed with declared source durations; 60 fps H.264 presentation quantizes boundaries to video frames.', 'durationMs': elapsed, 'chapters': chapters, 'entries': entries, 'scope': 'Compiled from prior four-direction native interval (East/South/West byte-identical) and corrected North native interval; replayed with declared holds, not unbroken screen recording. No station integration or owner acceptance.'}
(review / 'full-motion-preview.json').write_text(json.dumps(meta, indent=2)+'\n')
print(json.dumps({'frames':len(entries),'durationMs':elapsed,'bytes':(review/'full-motion-preview.mp4').stat().st_size}))
