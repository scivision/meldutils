import typing as T
from pathlib import Path
import shutil
import subprocess
import logging
import filecmp
import os

__all__ = ["files_to_diff", "diff_gui"]


def files_to_diff(root: Path, ref: Path) -> T.Iterator[Path]:
    """
    Yield filenames that match criteria (same filename but different contents).
    """

    ref = Path(ref).expanduser().resolve()
    if not ref.is_file():
        raise FileNotFoundError(f"specify a reference file, not a directory {ref}")

    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"{root} is not a directory")

    for new in root.rglob(ref.name):
        if new.samefile(ref):
            continue

        if filecmp.cmp(new, ref, shallow=False):  # type: ignore   # MyPy .pyi incorrect
            logging.info(f"SAME: {new.parent}")
            continue

        yield new


def diff_gui(ref: Path, new: Path, exe: str = None) -> None:
    """
    run file comparison GUI on file pair

    Not using check_call due to spurious errors
    """

    diff_cli = "FC.exe" if os.name == "nt" else "diff"

    if not exe:
        for e in ("meld", "code", diff_cli):
            exe = shutil.which(e)
            if exe:
                break

    exe = shutil.which(exe)
    if not exe:
        raise FileNotFoundError("diff GUI not found. Try -n option to just see which files differ.")

    new = Path(new).expanduser().resolve()
    ref = Path(ref).expanduser().resolve()

    if "code" in Path(exe).name.lower():
        cmd = [exe, "--wait", "--diff", str(ref), str(new)]
    else:
        # assuming just the plain executable name without options
        # this is how "meld" works
        cmd = [exe, str(ref), str(new)]

    logging.info(cmd)
    subprocess.run(cmd)
