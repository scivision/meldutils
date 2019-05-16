[![Build Status](https://travis-ci.com/scivision/meldutils.svg?branch=master)](https://travis-ci.com/scivision/meldutils)

# Meld Utilities

Python scripts using [Meld](https://meldmerge.org) to accomplish tasks useful for managing large numbers of repos / projects, particularly for templates.
It works on any OS Meld works on (Linux, MacOS, Windows).


## Scripts

```sh
meld_all project/myfile.f90 ~/code
```

That terminal command invokes `meld` between `project/myfile.f90` and every other file with the same name found recursively under `~/code`.
