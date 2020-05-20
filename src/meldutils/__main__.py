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
    p.add_argument("-exe", help="program to compare with")
    p.add_argument("-n", "--dryrun", help="just report files that are different", action="store_true")
    p = p.parse_args()

    level = logging.INFO if p.dryrun else None
    logging.basicConfig(format="%(message)s", level=level)

    ref = Path(p.ref).expanduser().resolve()

    for file in mu.files_to_diff(p.root, ref):
        if p.dryrun:
            print(file, "!=", ref)
        else:
            mu.diff_gui(p.ref, file, p.exe)


if __name__ == "__main__":
    main()
