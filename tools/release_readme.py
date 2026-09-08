"""Rewrite the bundled mod README from the repository README.

The root README uses relative `docs/...` links, which only resolve inside a
source checkout. The copy shipped inside the mod ZIP is read from the Factorio
mods folder, so every relative link is rewritten to point at the immutable
release tag for the current mod version.

    python3 tools/release_readme.py            # write second-nature/README.md
    python3 tools/release_readme.py --check    # fail if it is out of date
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / 'second-nature'
REPOSITORY = 'https://github.com/Radukan/FC-Test'


def version():
    return json.loads((MOD / 'info.json').read_text())['version']


def render():
    tag = 'v%s-factorio-2.0' % version()
    text = (ROOT / 'README.md').read_text()
    text = re.sub(r'\]\((docs/)', '](%s/blob/%s/\\1' % (REPOSITORY, tag), text)
    assert '](docs/' not in text
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    arguments = parser.parse_args()
    target = MOD / 'README.md'
    wanted = render()
    if arguments.check:
        if target.read_text() != wanted:
            print('second-nature/README.md is stale; run tools/release_readme.py')
            return 1
        print('second-nature/README.md is current')
        return 0
    target.write_text(wanted)
    print('wrote %s for %s' % (target.relative_to(ROOT), version()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
