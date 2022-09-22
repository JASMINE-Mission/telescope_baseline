from pathlib import Path
import sys


def get_test_file(file_path: str) -> Path:
    for sys_path in sys.path:
        target_file = Path(sys_path, file_path)
        if target_file.exists():
            return target_file
    raise FileNotFoundError()
