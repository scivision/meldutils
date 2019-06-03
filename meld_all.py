#!/usr/bin/env python
"""
useful for updating templates.

e.g.

meld_all .appveyor.yml

meld_all .appveyor.yml -l Fortran
"""
from pathlib import Path
from argparse import ArgumentParser
import filecmp
import logging
import subprocess
import shutil
try:
    import ghlinguist as ghl
except (ImportError, FileNotFoundError):
    ghl = None

EXE = shutil.which('meld')
if not EXE:
    raise FileNotFoundError('meld is not found')


def meldloop(root: Path, filename: Path,
             language: str = None, exe: str = EXE,
             strict: bool = False):

    si = 1 if strict else 2

    filename = Path(filename).expanduser()
    if not filename.is_file():
        raise FileNotFoundError(filename)

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(root)

    for f in root.rglob(filename.name):
        if f.samefile(filename):
            continue

        if filecmp.cmp(f, filename, shallow=False):  # type: ignore   # mypy .pyi needs updating
            print('SAME:', f.parent)
            continue

        if language and ghl is not None:
            langlist = ghl.linguist(f.parent)
            if langlist is None:
                logging.warning('SKIP: {}'.format(f.parent))
                continue

            thislangs = [l[0] for l in langlist[:si]]
            if language not in thislangs:
                print('SKIP:', f.parent, thislangs)
                continue

        # Not using check_call due to spurious errors
        subprocess.run([exe, str(filename), str(f)])

        if not filecmp.cmp(f, filename, shallow=False):  # type: ignore   # mypy .pyi needs updating
            logging.warning('{} and {} do not match after Meld'.format(f, filename))
        else:
            print('SAME:', f.parent)


def main():
    p = ArgumentParser()
    p.add_argument('filename', help='filename to compare against')
    p.add_argument('root', help='top-level directory to search under')
    p.add_argument('-l', '--language', help='language to template')
    p.add_argument('-exe', help='program to compare with', default=EXE)
    p.add_argument('-s', '--strict', help='compare only with first language match', action='store_true')
    p = p.parse_args()

    fn = Path(p.filename).expanduser()

    root = Path(p.root).expanduser()

    meldloop(root, fn, p.language, p.exe, strict=p.strict)


if __name__ == '__main__':
    main()
