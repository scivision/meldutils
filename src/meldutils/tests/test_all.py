#!/usr/bin/env python
import pytest
import os

import meldutils as mu


def test_find(gen_file):
    f1, f2 = gen_file

    files = list(mu.files_to_diff(f1.parents[1], f1))

    assert len(files) == 0

    # add a whitespace to one file to make the file slightly different than the other file
    with f2.open("a") as f:
        f.write(" ")

    files = list(mu.files_to_diff(f1.parents[1], f1))

    assert len(files) == 1


def test_diff(gen_file):
    """
    show output of this test with
    pytest -s
    """
    f1, f2 = gen_file
    f2.write_text("hi")

    # this needs to be FC.exe in case run from PowerShell
    diff_cli = "FC.exe" if os.name == "nt" else "diff"

    mu.diff_gui(f1, f2, diff_cli)


if __name__ == "__main__":
    pytest.main([__file__])
