"""Run native audio/title/save/quit checks against the frozen Windows package.

Usage: python tools/check_audio_playtest.py OUTPUT_DIRECTORY
All tests use isolated APPDATA/LOCALAPPDATA; no player saves are touched.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

def main():
    out = Path(sys.argv[1]).resolve()
    binary = out/'build/BrineSpace.exe'
    cases = [('audio','audio',[],'SUNO AUDIO PASS'),('space','space',[],'AUDIO SPACE PASS'),('title','title',[],'TITLE SCREEN: PASS'),('systems','systems',[],'STATION SYSTEMS PASS'),('quit-title','quit',['--mode=title'],'AUDIO QUIT PASS: title'),('quit-game','quit',['--mode=game'],'AUDIO QUIT PASS: game')]
    results = {}
    for name,fixture,extra,marker in cases:
        path = out/(name+'.log')
        if path.exists(): raise RuntimeError('Existing evidence: '+str(path))
        userdata = out/('userdata-'+name)
        userdata.mkdir(exist_ok=False)
        env = os.environ.copy()
        env['APPDATA'] = str(userdata)
        env['LOCALAPPDATA'] = str(userdata)
        started = time.monotonic()
        with path.open('w',encoding='utf-8') as log:
            try:
                result = subprocess.run([str(binary),'--audio-driver','Dummy','--','--audio-check='+fixture,*extra],cwd=out/'build',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
                code = result.returncode
            except subprocess.TimeoutExpired: code = -1
        text = path.read_text(errors='replace')
        errors = re.findall(r'^.*(?:SCRIPT ERROR:|ERROR:|Assertion failed).*$',text,re.M)
        results[name] = {'exit_code':code,'errors':errors,'seconds':round(time.monotonic()-started,2),'pass':code==0 and not errors and marker in text}
        (out/'checks.json').write_text(json.dumps(results,indent=2))
        print(name, 'PASS' if results[name]['pass'] else 'FAIL',flush=True)
        if not results[name]['pass']: raise RuntimeError('Check failed: '+name)
    manifest = json.loads((out/'package.json').read_text())
    for name,record in manifest.items():
        with (out/'build'/name).open('rb') as handle:
            assert hashlib.file_digest(handle,'sha256').hexdigest() == record['sha256'], name
    print('All six packaged checks passed; package hashes unchanged.',flush=True)

if __name__ == '__main__': main()
