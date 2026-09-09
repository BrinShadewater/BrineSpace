"""Build short event edits and measured mix gains from the untouched v1 exports.

Run tools/audit_suno_mix.py first, then this script. Masters and v1 clips are kept.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets/audio/suno-polish-v1'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
# Explicit source-relative edits, chosen from onset / transient measurements.
EDITS = {
    'placement_01': (0, 1.15), 'placement_02': (0, 1.3),
    'placement_03': (2.55, .48), 'placement_04': (0, 1.35),
    'door_01': (7.42, 1.65), 'door_02': (.32, 1.6),
    'power_on_01': (0, 3.8), 'power_on_02': (5.4, 3.6),
    'cargo_01': (0, 1.95), 'cargo_02': (0, 1.95),
    'terminal_01': (2.55, 1.65), 'terminal_02': (1.3, 1.6),
    'discovery_01': (.32, 4.5), 'discovery_02': (0, 4.5),
    'warning_01': (5.3, 2.1),
}

def loudness(path):
    report = subprocess.run([FFMPEG,'-v','info','-i',str(path),'-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,check=True).stderr.decode()
    result = json.loads(report[report.rfind('{'):report.rfind('}')+1])
    return float(result['input_i']), float(result['input_tp'])

def main():
    DEST.mkdir(parents=True,exist_ok=True)
    measurements = json.loads((ROOT/'output/audio-polish/measurements.json').read_text())
    gains = {}
    rows = []
    for row in measurements:
        source = ROOT / row['asset'].removeprefix('res://')
        name = source.stem
        group = name.rsplit('_',1)[0]
        if name in EDITS:
            start, duration = EDITS[name]
            raw = subprocess.run([FFMPEG,'-v','error','-i',str(source),'-ss',str(start),'-t',str(duration),'-f','f32le','-ar','48000','-ac','2','-'],capture_output=True,check=True).stdout
            data = np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
            # Remove DC and taper the edit boundaries without dulling the attack.
            data -= np.mean(data,axis=0)
            attack = min(240,len(data)//4)
            tail = min(7200,len(data)//4)
            data[:attack] *= np.linspace(0,1,attack)[:,None]
            data[-tail:] *= np.linspace(1,0,tail)[:,None]**1.5
            output = DEST / (name+'.wav')
            subprocess.run([FFMPEG,'-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s16le',str(output)],input=data.astype('<f4').tobytes(),capture_output=True,check=True)
            measured, peak = loudness(output)
            # A constant runtime gain preserves dynamics. Cap boost and peak headroom.
            gain = round(min(6.0,-23.0-measured,-3.0-peak),2)
            asset = 'res://'+output.relative_to(ROOT).as_posix()
            rows.append(dict(asset=asset,source=row['asset'],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),start=start,seconds=round(len(data)/48000,3),lufs=measured,true_peak_db=peak,gain_db=gain))
        else:
            target = {'interior':-19.0,'ocean':-20.0,'airlock':-27.0,'drone':-18.0}.get(group,-17.5)
            gain = round(min(0.0,target-row['lufs']),2)
            asset = row['asset']
            rows.append(dict(asset=asset,lufs=row['lufs'],gain_db=gain))
        gains[asset] = gain
    bank = ROOT/'scripts/suno_audio_bank.gd'
    content = bank.read_text()
    for name in EDITS:
        content = re.sub(r'res://assets/audio/(?:suno-v1|suno-polish-v1)/'+name+r'\.wav','res://assets/audio/suno-polish-v1/'+name+'.wav',content)
    bank.write_text(content,encoding='utf-8')
    profile = ['extends RefCounted','## Measured constant gains; rebuild with tools/polish_suno_audio.py.','const GAIN_DB := {']
    profile += ['\t'+json.dumps(k)+': '+str(v)+',' for k,v in gains.items()]
    profile += ['}', '', 'static func gain(stream: AudioStream) -> float:', '\treturn float(GAIN_DB.get(stream.resource_path, 0.0))','']
    (ROOT/'scripts/station_audio_mix.gd').write_text('\n'.join(profile),encoding='utf-8')
    (DEST/'manifest.json').write_text(json.dumps({'processing':'Explicit transient edits, DC removal, 5ms attack, <=150ms shaped tail, PCM16. Constant runtime LUFS matching with bounded gain and peak headroom; original v1 audio untouched.','files':rows},indent=2)+'\n')
    print('Prepared 15 event edits and 27 measured gain entries.')

if __name__ == '__main__': main()
