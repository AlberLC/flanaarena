import shutil
import time
from collections.abc import Iterable
from pathlib import Path

import psutil


def delete_recently_active_directory(path: str | Path, timeout: float = 10.0, retry_delay: float = 0.1) -> None:
    deadline = time.perf_counter() + timeout

    while True:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            break
        except PermissionError:
            if time.perf_counter() >= deadline:
                raise

            time.sleep(retry_delay)
        else:
            break


def read_savable_files(paths: Iterable[str | Path]) -> list[tuple[Path, bytes]]:
    savable_data = []

    for path in paths:
        if not (path := Path(path)).is_file():
            continue

        savable_data.append((path, path.read_bytes()))

    return savable_data


def search_processes(name: str) -> list[psutil.Process]:
    return [process for process in psutil.process_iter(['pid', 'name', 'cmdline']) if process.info['name'] == name]


def write_savable_files(savable_data: Iterable[tuple[Path, bytes]]) -> None:
    for path, bytes_ in savable_data:
        path.write_bytes(bytes_)
