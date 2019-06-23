#!/usr/bin/env python
import pytest
from pathlib import Path
import os

import meld_all as mu


@pytest.fixture
def gen_file(tmp_path):
    f1 = tmp_path/'a/hi.txt'
    f2 = tmp_path/'b/hi.txt'

    make_file(f1)
    make_file(f2)

    return f1, f2


def make_file(path: Path):
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text('hello')


def test_find(gen_file):
    f1, f2 = gen_file

    files = list(mu.files_to_meld(f1.parents[1], f1))

    assert len(files) == 0

    # add a whitespace to one file to make the file slightly different than the other file
    with f2.open('a') as f:
        f.write(' ')

    files = list(mu.files_to_meld(f1.parents[1], f1))

    assert len(files) == 1


def test_diff(gen_file):
    f1, f2 = gen_file
    f2.write_text('hi')

    if os.name == 'nt':
        diff = 'FC'
    else:
        diff = 'diff'

    mu.meld_files(f1.parents[1], f1, diff)


if __name__ == '__main__':
    pytest.main([__file__])
