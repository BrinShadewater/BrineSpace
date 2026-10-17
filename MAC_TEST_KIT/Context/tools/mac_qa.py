#!/usr/bin/env python3
"""Portable integrity checks; native launch/probe require an explicit QA account."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,time,zipfile

ROOT=Path(__file__).resolve().parents[2]
def sha(stream):
    h=hashlib.sha256()
    for chunk in iter(lambda:stream.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2),encoding='utf-8')
def relative(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name:raise ValueError('Unsafe archive path: '+name)
    return p
def verify_files(root,manifest):
    rows=read(manifest)['files'];failures=[]
    for name,digest in rows.items():
        p=root/relative(name)
        if not p.is_file():failures.append(name+' missing');continue
        with p.open('rb') as f:
            if sha(f)!=digest:failures.append(name+' hash mismatch')
    if failures:raise RuntimeError('\n'.join(failures[:20]))
    print('VERIFIED',len(rows),'files',flush=True)
def verify_archive(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate ZIP members')
        for name in names:relative(name)
        m=json.loads(z.read('FILE_SHA256.json'));failures=[]
        for name,digest in m['files'].items():
            with z.open(name) as f:
                if sha(f)!=digest:failures.append(name)
        if failures:raise RuntimeError(str(failures))
        print('VERIFIED_ARCHIVE',len(m['files']),'files',flush=True)
def mac():
    if sys.platform!='darwin':raise RuntimeError('Native Mac operation: run on macOS; no game launched')
def account(name):
    mac();import pwd
    current=pwd.getpwuid(os.getuid())
    if os.getuid()==0 or current.pw_name!=name:
        raise RuntimeError('Refusing launch: expected disposable QA login '+name+', actual '+current.pw_name)
    return current,Path(current.pw_dir)/'Library/Application Support/Godot/app_userdata/BrineSpace'
def app():
    audit=read(ROOT/'bundle-audit.json');executable=ROOT/audit['executable']
    if not executable.is_file():raise RuntimeError('App missing: use extracted game ZIP, not source-only context')
    return executable,executable.parents[2]
def command(args,timeout=30):
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        return {'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    except (OSError,subprocess.TimeoutExpired) as e:return {'command':args,'error':str(e)}
def fingerprint(folder):
    result={}
    if folder.exists():
        for p in folder.rglob('*'):
            if p.is_file() and 'logs' not in p.relative_to(folder).parts:
                with p.open('rb') as f:result[p.relative_to(folder).as_posix()]=sha(f)
    return result
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='mode',required=True)
    v=sub.add_parser('verify');v.add_argument('--archive',type=Path)
    s=sub.add_parser('verify-source');s.add_argument('--source-dir',type=Path,required=True)
    i=sub.add_parser('info');i.add_argument('--output',type=Path,default=ROOT/'Mac-results/system.json')
    for name in ['launch','probe']:
        p=sub.add_parser(name);p.add_argument('--qa-account',default='brinespace-qa');p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.mode=='verify':
        if args.archive:verify_archive(args.archive)
        else:verify_files(ROOT,ROOT/'FILE_SHA256.json')
        return
    if args.mode=='verify-source':verify_files(args.source_dir,args.source_dir/'SOURCE_FILES_SHA256.json');return
    if args.mode=='info':
        mac();exe,bundle=app()
        rows=[command(c) for c in [['sw_vers'],['uname','-m'],['sysctl','-n','hw.model'],['sysctl','-n','hw.memsize'],['sysctl','-n','machdep.cpu.brand_string'],
            ['codesign','--verify','--deep','--strict','--verbose=2',str(bundle)],['codesign','-dv','--verbose=4',str(bundle)],
            ['spctl','--assess','--type','execute','--verbose=4',str(bundle)],['xattr','-l',str(bundle)]]]
        write(args.output,{'build':read(ROOT/'build_info.json'),'native_commands':rows,'renderer':'Record actual game F7/F8 backend; not inferred from OS','note':'Signature/trust statuses recorded without changing app or security settings.'});print(args.output);return
    user,profile=account(args.qa_account);exe,bundle=app();dest=args.output.resolve()
    if dest.exists():raise RuntimeError('Choose a fresh output folder; evidence will not be overwritten')
    dest.mkdir(parents=True);before=fingerprint(profile);write(dest/'test-profile-before.json',before)
    env=os.environ.copy();cmd=[str(exe)]
    if args.mode=='probe':
        env['BRINE_SILENT']='1';env['BRINESPACE_TEST_USER_DIR']=profile.as_posix()
        cmd+=['--headless','--script',str(ROOT/'Context/tools/userdata_probe.gd'),'--','--expected-user-dir='+profile.as_posix()]
    write(dest/'launch.json',{'command':cmd,'qa_account':user.pw_name,'uid':os.getuid(),'home':user.pw_dir,'expected_profile':str(profile),
        'build':read(ROOT/'build_info.json'),'started_unix':time.time(),'scope':'Actual disposable-account profile; no HOME redirection assumed. Direct binary launch does not replace first Finder/Gatekeeper test.'})
    proc=None
    try:
        with (dest/'game.log').open('w',encoding='utf-8') as log:
            proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            try:code=proc.wait(timeout=45 if args.mode=='probe' else 4*3600)
            except (subprocess.TimeoutExpired,KeyboardInterrupt):
                proc.terminate()
                try:proc.wait(timeout=15)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
                raise
        body=(dest/'game.log').read_text(encoding='utf-8',errors='replace')
        if code!=0 or 'SCRIPT ERROR:' in body:raise RuntimeError('Native command failed; inspect '+str(dest/'game.log'))
        if args.mode=='probe' and 'MAC_USERDATA_VERIFIED ' not in body:raise RuntimeError('No actual engine user-dir proof; do not run further probes')
        print('NATIVE_COMMAND_EXIT',code,'results',dest,flush=True)
    finally:
        if proc is not None and proc.poll() is None:proc.terminate();proc.wait(timeout=15)
        after=fingerprint(profile);write(dest/'test-profile-after.json',after)
        write(dest/'completion.json',{'exit_code':None if proc is None else proc.poll(),'test_profile':str(profile),
            'changed_test_files':[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)],'scope':'These are intentional QA-account save changes, not owner-profile modifications. Gameplay/visual acceptance must be recorded separately.'})
if __name__=='__main__':main()
