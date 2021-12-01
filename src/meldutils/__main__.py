#!/usr/bin/env python
"""
useful for updating templates.

e.g.

python -m meldutils .appveyor.yml

python -m meldutils .appveyor.yml -l Fortran
"""

from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
import meldutils as mu
import logging


def diff_if_different(ref: Path, file: Path, diff_exe: str, exclude: list[str], dryrun: bool):
    print(file)
    for e in exclude:
        for p in file.parts:
            if e in p:
                print(f"excluded {file}")
                return
    if dryrun:
        print(file, "!=", ref)
    else:
        mu.diff_gui(ref, file, diff_exe)


p = ArgumentParser(description="compare file across directory tree")
p.add_argument("ref", help="filename to compare against")
p.add_argument("root", help="top-level directory to search under")
p.add_argument("-exe", help="program to compare with", choices=["meld", "code"])
p.add_argument("-n", "--dryrun", help="just report files that are different", action="store_true")
p.add_argument(
    "--exclude",
    help="exclude folders matching this pattern",
    nargs="+",
    default=["_deps", "-prefix"],
)
P = p.parse_args()

level = logging.INFO if P.dryrun else None
logging.basicConfig(format="%(message)s", level=level)

ref = Path(P.ref).expanduser().resolve()

for file in mu.files_to_diff(P.root, ref):
    diff_if_different(ref, file, diff_exe=P.exe, exclude=P.exclude, dryrun=P.dryrun)
