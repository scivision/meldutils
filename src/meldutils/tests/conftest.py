import pytest
from pathlib import Path


@pytest.fixture
def gen_file(tmp_path):
    f1 = tmp_path / "a/hi.txt"
    f2 = tmp_path / "b/hi.txt"

    make_file(f1)
    make_file(f2)

    return f1, f2


def make_file(path: Path):
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text("hello")
