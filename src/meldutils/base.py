import typing
from pathlib import Path
import shutil
import subprocess
import logging
import filecmp

try:
    import ghlinguist as ghl
except (ImportError, FileNotFoundError):
    ghl = None


def files_to_meld(root: Path, ref: Path, language: str = None, strict: bool = False) -> typing.Iterator[Path]:

    si = 1 if strict else 2

    ref = Path(ref).expanduser()
    if not ref.is_file():
        raise FileNotFoundError(f"specify a reference file, not a directory {ref}")

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(f"{root} is not a directory")

    for new in root.rglob(ref.name):
        if new.samefile(ref):
            continue

        if filecmp.cmp(new, ref, shallow=False):  # type: ignore   # mypy .pyi needs updating
            logging.info(f"SAME: {new.parent}")
            continue

        if language and ghl is not None:
            langlist = ghl.linguist(new.parent)
            if langlist is None:
                logging.info(f"SKIP: {new.parent}")
                continue

            thislangs = [lang[0] for lang in langlist[:si]]
            if language not in thislangs:
                logging.info(f"SKIP: {new.parent} {thislangs}")
                continue

        yield new


def meld_files(ref: Path, new: Path, rexe: str):
    """
    run file comparison program (often meld) on file pair
    """

    exe = shutil.which(rexe)
    if not exe:
        raise FileNotFoundError(f"{rexe} not found. Try -n option to just see which files differ.")
    # Not using check_call due to spurious errors
    new = Path(new).expanduser()
    ref = Path(ref).expanduser()
    subprocess.run([exe, str(ref), str(new)])
