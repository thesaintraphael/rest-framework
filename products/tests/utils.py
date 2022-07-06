import contextlib
import shutil


def remove_upladed_files(path: str) -> None:
    """
    Remove all files in the given path.
    """
    with contextlib.suppress(OSError):
        shutil.rmtree(path)
