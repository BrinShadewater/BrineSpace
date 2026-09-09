"""Measure current audio loudness and onset; saves full evidence under output/."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/audio-polish'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def measure(row):
    path = ROOT / row['asset'].removeprefix('res://')
    report = subprocess.run([FFMPEG, '-v', 'info', '-i', str(path), '-af', 'loudnorm=I=-23:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, check=True).stderr.decode()
    loud = json.loads(report[report.rfind('{'):report.rfind('}')+1])
    raw = subprocess.run([FFMPEG,'-v','error','-i',str(path),'-f','f32le','-ar','24000','-ac','1','-'],capture_output=True,check=True).stdout
    samples = np.frombuffer(raw,dtype='<f4')
    frames = samples[:len(samples)//480*480].reshape(-1,480)
    rms = np.sqrt(np.mean(frames**2,axis=1))
    active = np.flatnonzero(rms > max(float(rms.max())*0.12, 0.0005))
    return dict(asset=row['asset'],kind=row['kind'],seconds=row['seconds'],lufs=float(loud['input_i']),true_peak_db=float(loud['input_tp']),lra=float(loud['input_lra']),onset=round(float(active[0])*.02,3),last_body=round(float(active[-1]+1)*.02,3),loudest=round(float(np.argmax(rms))*.02,3),first_two_energy=round(float(np.sum(samples[:48000]**2)/np.sum(samples**2)),3))

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT/'assets/audio/suno-v1/manifest.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(measure,manifest['files']))
    (OUT/'measurements.json').write_text(json.dumps(records,indent=2)+'\n')
    for r in records:
        print(Path(r['asset']).stem, 'LUFS',r['lufs'],'onset',r['onset'],'peak at',r['loudest'],'first 2s energy',r['first_two_energy'])
