from pathlib import Path
import sys
import os
import tempfile


def get_test_file(file_path: str) -> Path:
    for sys_path in sys.path:
        target_file = Path(sys_path, file_path)
        if target_file.exists():
            return target_file
    raise FileNotFoundError()


class _PathWrapper:
    def __init__(self, origin:Path, delete_when_gc):
        self.__origin = origin
        self.__delete_when_gc = delete_when_gc

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.__origin, name)(*args, **kwargs)
        return func

    def __repr__(self):
        return repr(self.__origin)

    def __bytes__(self):
        return bytes(self.__origin)

    def __str__(self):
        return str(self.__origin)

    def __format__(self, form_spec):
        return format(self.__origin, form_spec)

    def __del__(self):
        if self.__delete_when_gc:
            self.__origin.unlink(missing_ok=True)


def get_temp_file(delete_when_gc: bool = True) -> Path:
    tmp_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    path = Path(tmp_name)
    if path.exists():
        return get_temp_file()
    else:
        path.touch()
        return _PathWrapper(path, delete_when_gc)
