"""Run a graphical standalone wall review and require a clean Godot log."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PASS = 'WALL ASSET PASS:'
ERROR = re.compile(r'^(?:SCRIPT ERROR|ERROR|USER ERROR):', re.MULTILINE)


def review_errors(returncode, log):
    errors=[]
    if returncode != 0:
        errors.append(f'Godot exited with code {returncode}')
    if ERROR.search(log):
        errors.extend(line for line in log.splitlines() if ERROR.match(line))
    if PASS not in log:
        errors.append('Missing wall-review completion marker')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot',type=Path,required=True)
    for name in ('registration','export','review'):
        parser.add_argument('--'+name,required=True,help='Godot res:// path')
    parser.add_argument('--reference-view')
    parser.add_argument('--width',type=float,default=320)
    parser.add_argument('--log',type=Path,required=True)
    parser.add_argument('--timeout',type=float,default=60)
    args=parser.parse_args()
    log=args.log.resolve()
    if log.exists():
        parser.error('Choose a new log path; prior evidence is preserved')
    if not args.godot.is_file():
        parser.error('Godot executable not found')
    if not 0 < args.timeout <= 60:
        parser.error('Timeout must be in (0,60] seconds')
    for name in ('registration','export','review','reference_view'):
        value=getattr(args,name)
        if value and not value.startswith('res://'):
            parser.error(name+' must be a res:// path')
    log.parent.mkdir(parents=True,exist_ok=True)
    command=[str(args.godot.resolve()),'--path',str(ROOT),'--script',
             'res://tools/review_registered_wall_asset.gd','--log-file',str(log),'--',
             '--registration='+args.registration,'--export='+args.export,
             '--review='+args.review,'--width='+str(args.width)]
    if args.reference_view:
        command.append('--reference-view='+args.reference_view)
    # Keep full diagnostics in files; only bounded errors reach the console.
    capture=log.with_suffix(log.suffix+'.process.txt')
    if capture.exists():
        parser.error('Process capture already exists; choose a new log path')
    with capture.open('x',encoding='utf-8') as output:
        try:
            result=subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,
                                  timeout=args.timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        except subprocess.TimeoutExpired:
            print(f'REVIEW FAILED: timed out; inspect {log} and {capture}',file=sys.stderr)
            return 1
    evidence=log.read_text(encoding='utf-8',errors='replace') if log.exists() else ''
    evidence+='\n'+capture.read_text(encoding='utf-8',errors='replace')
    errors=review_errors(result.returncode,evidence)
    if errors:
        for error in list(dict.fromkeys(errors))[:8]:
            print('REVIEW FAILED: '+error,file=sys.stderr)
        print('Full evidence: '+str(log),file=sys.stderr)
        return 1
    print(f'Clean native export review: {log}; visual inspection still required')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
