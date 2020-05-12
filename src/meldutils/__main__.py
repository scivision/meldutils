#!/usr/bin/env python
"""
useful for updating templates.

e.g.

meld_all .appveyor.yml

meld_all .appveyor.yml -l Fortran
"""
from pathlib import Path
from argparse import ArgumentParser
import meldutils as mu
import logging


def main():
    p = ArgumentParser()
    p.add_argument("ref", help="filename to compare against")
    p.add_argument("root", help="top-level directory to search under")
    p.add_argument("-l", "--language", help="language to template")
    p.add_argument("-exe", help="program to compare with", default="meld")
    p.add_argument("-s", "--strict", help="compare only with first language match", action="store_true")
    p.add_argument("-n", "--dryrun", help="just report files that are different", action="store_true")
    p = p.parse_args()

    if p.dryrun:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format="%(message)s", level=level)

    root = Path(p.root).expanduser()
    if not root.is_dir():
        raise SystemExit(f"{root} is not a directory")

    files = mu.files_to_meld(root, p.ref, p.language, strict=p.strict)

    for file in files:
        if p.dryrun:
            print(f"{file}  !=  {p.ref}")
        else:
            mu.meld_files(p.ref, file, p.exe)


if __name__ == "__main__":
    main()
