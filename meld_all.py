#!/usr/bin/env python
"""
useful for updating templates.

e.g.

meld_all .appveyor.yml

meld_all .appveyor.yml -l Fortran
"""
from pathlib import Path
from argparse import ArgumentParser
from typing import Iterator
import filecmp
import logging
import subprocess
import shutil
try:
    import ghlinguist as ghl
except (ImportError, FileNotFoundError):
    ghl = None


def files_to_meld(root: Path, ref: Path,
                  language: str = None,
                  strict: bool = False) -> Iterator[Path]:

    si = 1 if strict else 2

    ref = Path(ref).expanduser()
    if not ref.is_file():
        raise FileNotFoundError(f'specify a reference file, not a directory {ref}')

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(root)

    for new in root.rglob(ref.name):
        if new.samefile(ref):
            continue

        if filecmp.cmp(new, ref, shallow=False):  # type: ignore   # mypy .pyi needs updating
            logging.info(f'SAME: {new.parent}')
            continue

        if language and ghl is not None:
            langlist = ghl.linguist(new.parent)
            if langlist is None:
                logging.info(f'SKIP: {new.parent}')
                continue

            thislangs = [l[0] for l in langlist[:si]]
            if language not in thislangs:
                logging.info(f'SKIP: {new.parent} {thislangs}')
                continue

        yield new


def meld_files(ref: Path, new: Path, rexe: str):
    """
    run file comparison program (often meld) on file pair
    """

    exe = shutil.which(rexe)
    if not exe:
        logging.critical('File comparison program not found. Try -n option to just see which files differ.')
        raise FileNotFoundError(rexe)
    # Not using check_call due to spurious errors
    new = Path(new).expanduser()
    ref = Path(ref).expanduser()
    subprocess.run([exe, str(ref), str(new)])


def main():
    p = ArgumentParser()
    p.add_argument('ref', help='filename to compare against')
    p.add_argument('root', help='top-level directory to search under')
    p.add_argument('-l', '--language', help='language to template')
    p.add_argument('-exe', help='program to compare with', default='meld')
    p.add_argument('-s', '--strict', help='compare only with first language match', action='store_true')
    p.add_argument('-n', '--dryrun', help='just report files that are different', action='store_true')
    p = p.parse_args()

    if p.dryrun:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format='%(message)s', level=level)

    root = Path(p.root).expanduser()

    files = files_to_meld(root, p.ref, p.language, strict=p.strict)

    for file in files:
        if p.dryrun:
            print(f'{file}  !=  {p.ref}')
        else:
            meld_files(p.ref, file, p.exe)


if __name__ == '__main__':
    main()
