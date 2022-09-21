from pathlib import Path


def get_test_file(file_path:str, test_root_dir:str = 'tests') -> Path:
    project_root = Path.cwd()
    return Path(project_root, test_root_dir, file_path)
