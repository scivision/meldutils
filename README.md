# Meld Utilities

[![DOI](https://zenodo.org/badge/186922933.svg)](https://zenodo.org/badge/latestdoi/186922933)
[![Actions Status](https://github.com/scivision/meldutils/workflows/ci/badge.svg)](https://github.com/scivision/meldutils/actions)

[![pypi versions](https://img.shields.io/pypi/pyversions/meldutils.svg)](https://pypi.python.org/pypi/meldutils)
[![PyPi Download stats](http://pepy.tech/badge/meldutils)](http://pepy.tech/project/meldutils)

Python scripts using
[Meld](https://meldmerge.org)
to accomplish tasks useful for managing large numbers of repos / projects, particularly for templates.
It works on any OS Meld works on (Linux, MacOS, Windows).

## Scripts

```sh
meld_all project/myfile.f90 ~/code
```

That terminal command invokes `meld` between `project/myfile.f90` and every other file with the same name found recursively under `~/code`.

### Usage

Particularly on Windows, you may get Meld brought up and you don't see any difference.
This is often because one file as a trailing \n and the other file does not, or the other file has \r\n.
Meld won't show any difference, even with all text filters off.
Because of how Python `filecmp.cmp` works, there isn't a blazing fast simple solution to this besides using str.replace, which I didn't want to do.

So just realize it's OK, close Meld when it shows no difference and happy comparing!

Reference: https://github.com/dsindex/blog/wiki/%5Bpython%5D-string-compare-disregarding-white-space
