#!/usr/bin/env python3
"""Run an opt-in real Factorio smoke test. Requires a user-supplied headless binary.
No game download, account, server port or credentials are required by this script.
"""
import argparse,json,re,shutil,subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from package import build

def run(binary:Path):
    binary=binary.resolve()
    if not binary.is_file():raise SystemExit(f'Factorio binary not found: {binary}')
    version_output=subprocess.check_output([str(binary),'--version'],text=True)
    match=re.search(r'Version:\s*(2\.0\.\d+)',version_output)
    if not match:raise SystemExit('Expected stable Factorio 2.0 headless.\n'+version_output)
    version=match.group(1);branch='.'.join(version.split('.')[:2])
    root=ROOT/'.cache'/f'engine-{version}';mods=root/'mods';write=root/'user-data'
    mods.mkdir(parents=True,exist_ok=True);write.mkdir(parents=True,exist_ok=True)
    archive=build(branch,mods)
    version_mod=json.loads((ROOT/'second-nature/info.json').read_text())['version']
    for old in mods.glob('second-nature_*.zip'):
        if old != archive: old.unlink()
    test=mods/'second-nature-engine-tests_0.1.0';test.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'tests/engine/control.lua',test/'control.lua')
    shutil.copyfile(ROOT/'tests/engine/module_probes.lua',test/'module_probes.lua')
    for directory in ('scripts','shared'):
        shutil.copytree(ROOT/'second-nature'/directory,test/directory,dirs_exist_ok=True)
    (test/'info.json').write_text(json.dumps({'name':'second-nature-engine-tests','version':'0.1.0','title':'Second Nature engine validation','author':'Radukan','factorio_version':branch,'dependencies':['second-nature = '+version_mod]}))
    enabled=['base','space-age','quality','elevated-rails','second-nature','second-nature-engine-tests']
    (mods/'mod-list.json').write_text(json.dumps({'mods':[{'name':m,'enabled':True} for m in enabled]}))
    config=root/'config.ini'
    config.write_text('[path]\nread-data=__PATH__executable__/../../data\nwrite-data='+str(write)+'\n[general]\nenable-new-mods=false\n')
    world=root/'smoke.zip'
    base=[str(binary),'--config',str(config),'--mod-directory',str(mods)]
    outputs=[]
    for label,args in [('create',['--create',str(world)]),('benchmark',['--benchmark',str(world),'--benchmark-ticks','2100','--benchmark-runs','1'])]:
        command=base+args
        result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        print(result.stdout,end='');(root/(label+'.log')).write_text(result.stdout)
        if result.returncode:
            summary=result.stdout[-3300:].replace('%','%25').replace('\r','%0D').replace('\n','%0A')
            print('::error title=Factorio engine failure::'+summary)
            raise SystemExit(f'Factorio {label} failed ({result.returncode}); see {root/(label+".log")}')
        outputs.append(result.stdout)
    if not all(marker in '\n'.join(outputs) for marker in ('SECOND_NATURE_ENGINE_SMOKE_OK','SECOND_NATURE_ENGINE_CAMPAIGN_PROBES_OK','SECOND_NATURE_ENGINE_LOGISTICS_AUDIO_OK')):
        raise SystemExit('Engine exited without the smoke-test success marker. This is NOT a pass. Inspect '+str(root))
    print(f'ENGINE VALIDATION PASSED: Factorio {version}. Logs: {root}')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--factorio',required=True,type=Path)
    run(parser.parse_args().factorio)
