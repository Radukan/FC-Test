#!/usr/bin/env python3
"""Build deterministic installable archives, with metadata for exactly one game branch."""
from pathlib import Path
import argparse, hashlib, json, zipfile
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "second-nature"
# Explicit package allowlist: never leak test saves, binaries, Git metadata or local config.
TOP_LEVEL={'info.json','settings.lua','data.lua','data-updates.lua','data-final-fixes.lua','control.lua','changelog.txt','thumbnail.png','LICENSE','README.md'}
FOLDERS={'shared','prototypes','scripts','locale','graphics','migrations'}

def build(target='2.0',output=None):
    if target != '2.0':raise ValueError('Second Nature 0.2+ supports stable Factorio 2.0 only')
    info=json.loads((MOD/'info.json').read_text())
    info['factorio_version']=target
    minimum='2.0.77'
    info['dependencies']=[f'{name} >= {minimum}' for name in ('base','space-age','quality','elevated-rails')]
    folder=f"{info['name']}_{info['version']}"
    output=Path(output) if output else ROOT/'artifacts'/f'factorio-{target}'
    output.mkdir(parents=True,exist_ok=True)
    path=output/(folder+'.zip')
    files=sorted(p for p in MOD.rglob('*') if p.is_file() and (p.relative_to(MOD).parts[0] in FOLDERS or str(p.relative_to(MOD)) in TOP_LEVEL))
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for source in files:
            relative=source.relative_to(MOD)
            data=(json.dumps(info,indent=2,ensure_ascii=False)+'\n').encode() if str(relative)=='info.json' else source.read_bytes()
            entry=zipfile.ZipInfo(folder+'/'+relative.as_posix(),date_time=(2026,9,6,0,0,0))
            entry.create_system=3;entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o100644<<16
            archive.writestr(entry,data,compresslevel=9)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_suffix('.zip.sha256').write_text(f'{digest}  {path.name}\n')
    print(f'Factorio {target}: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path} ({path.stat().st_size:,} bytes; {len(files)} files)')
    return path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',choices=['2.0'],default='2.0')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    build(args.target,args.output)
if __name__=='__main__':main()
