# Graphical recursive file comparison

[![DOI](https://zenodo.org/badge/186922933.svg)](https://zenodo.org/badge/latestdoi/186922933)
[![Actions Status](https://github.com/scivision/meldutils/workflows/ci/badge.svg)](https://github.com/scivision/meldutils/actions)
[![pypi versions](https://img.shields.io/pypi/pyversions/meldutils.svg)](https://pypi.python.org/pypi/meldutils)
[![PyPi Download stats](http://pepy.tech/badge/meldutils)](http://pepy.tech/project/meldutils)

Using
[Meld](https://meldmerge.org)
or
[Visual Studio Code](https://code.visualstudio.com/)
to accomplish file differencing.
Useful for managing large numbers of repos / projects, particularly for templates.

## Scripts

```sh
meld_all project/myfile.f90 ~/code
```

graphically compares `project/myfile.f90` with every other file of the same name  recursively under `~/code`.

### Usage

Particularly on Windows, the GUI may be invoked, but you don't see any difference.
This is often because only one of the two files as a trailing `\n` or `\r\n`.
Meld won't show any difference, even with all text filters off.
Because of how Python `filecmp.cmp` works, there isn't a blazing fast simple solution to this.
A possibly slow solution would be using str.replace.

So just realize it's OK, close Meld when it shows no difference and happy comparing!

Reference: https://github.com/dsindex/blog/wiki/%5Bpython%5D-string-compare-disregarding-white-space
