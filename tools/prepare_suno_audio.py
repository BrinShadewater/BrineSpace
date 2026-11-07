"""Prepare the owner's September 8 Suno WAVs; originals remain in Downloads.

Usage: python tools/prepare_suno_audio.py
Requires numpy and imageio_ffmpeg. Outputs runtime assets and a provenance manifest.
"""
import hashlib
import json
from pathlib import Path
import subprocess

import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path.home() / "Downloads"
DEST = ROOT / "assets/audio/suno-v1"
GROUPS = {
    "moonlit_canyon": ("Moonlit Canyon", "music"),
    "moonlit_test_run": ("Moonlit Test Run", "music"),
    "interior": ("Interior Ambience Of An Aging", "loop"),
    "ocean": ("Deep Underwater Ambience", "loop"),
    "placement": ("Compact Mechanical Confirmation", "effect"),
    "power_on": ("Old Industrial Equipment", "effect"),
    "door": ("A Heavy Sliding Pressure Door", "effect"),
    "airlock": ("Water Filling A Small Steel", "loop"),
    "drone": ("Small Underwater Utility", "loop"),
    "cargo": ("A Small Robotic Cargo", "effect"),
    "terminal": ("An Aging Artificial Intelligence", "effect"),
    "discovery": ("Short Discovery Sound", "effect"),
    "warning": ("An Old Industrial Station Warning", "effect"),
}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    records = []
    bank = ['extends RefCounted', '## Explicit dependencies keep audio in selected-resource exports.', 'const CLIPS := {']
    for name, (prefix, kind) in GROUPS.items():
        paths = sorted(SOURCE.glob(prefix + "*.wav"), key=lambda p: (" (" in p.name, p.name))
        if not paths:
            raise FileNotFoundError(prefix)
        assets = []
        for index, path in enumerate(paths, 1):
            raw = subprocess.run([ffmpeg, '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', '48000', '-ac', '2', '-'], check=True, capture_output=True).stdout
            data = np.frombuffer(raw, dtype='<f4').reshape(-1, 2).copy()
            source_seconds = len(data) / 48000
            # Remove only silence at effect boundaries, retaining all internal timing.
            if kind == 'effect':
                active = np.flatnonzero(np.max(np.abs(data), axis=1) > 0.003)
                if len(active):
                    data = data[max(0, active[0]-240):min(len(data), active[-1]+4801)]
            # Overlap the last 250ms with the first; the new boundary follows adjacent samples.
            if kind == 'loop':
                n = min(12000, len(data)//4)
                ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
                seam = data[-n:] * (1-ramp) + data[:n] * ramp
                data = np.concatenate([seam, data[n:-n]])
            else:
                n = min(480 if kind == 'effect' else 48000, len(data)//4)
                data[:n] *= np.linspace(0, 1, n)[:, None]
                data[-n:] *= np.linspace(1, 0, n)[:, None]
            # Peak ceiling only; never amplify quiet source noise.
            peak = float(np.max(np.abs(data)))
            gain = min(1.0, 0.70795 / max(peak, 1e-9))
            data *= gain
            extension = 'wav' if kind == 'effect' else 'ogg'
            output = DEST / f'{name}_{index:02d}.{extension}'
            codec = ['-c:a', 'pcm_s16le'] if kind == 'effect' else ['-c:a', 'libvorbis', '-q:a', '5']
            subprocess.run([ffmpeg, '-v', 'error', '-y', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', *codec, str(output)], input=data.astype('<f4').tobytes(), check=True, capture_output=True)
            resource = 'res://' + output.relative_to(ROOT).as_posix()
            assets.append(f'preload("{resource}")')
            records.append(dict(source=path.name, source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_seconds=round(source_seconds, 3), asset=resource, kind=kind, seconds=round(len(data)/48000, 3), gain_db=round(20*np.log10(gain), 2), bytes=output.stat().st_size))
        bank.append(f'\t"{name}": [{", ".join(assets)}],')
    bank.append('}\n')
    (ROOT / 'scripts/suno_audio_bank.gd').write_text('\n'.join(bank), encoding='utf-8')
    (DEST / 'manifest.json').write_text(json.dumps({'origin': 'Owner-supplied Suno exports, 2026-09-08', 'processing': '48kHz stereo; silence-edge trim for effects; 250ms overlap for loops; edge fades for effects/music; peak attenuation only; Vorbis quality 5 or PCM16 WAV.', 'files': records}, indent=2)+'\n', encoding='utf-8')
    print(f'Prepared {len(records)} assets, {sum(r["bytes"] for r in records)/1048576:.1f} MiB')


if __name__ == '__main__':
    main()
