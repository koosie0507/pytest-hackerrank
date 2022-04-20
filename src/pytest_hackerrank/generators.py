from os.path import abspath, join
from typing import Callable, Dict, Iterable, TextIO, Tuple

from testutil import list_file_paths


IN_DIR_NAME = "input"
EXPECTED_DIR_NAME = "expected"


def read_files(dir_path: str, visitor: Callable[[TextIO], Iterable]) -> Iterable:
    for file_path in list_file_paths(dir_path):
        with open(file_path, "r") as f:
            for item in visitor(f):
                yield item



def generate_tests_from_dir(
    metafunc,
    test_case_dir: str,
    **kwargs: Dict[str, Tuple[str, Callable[[TextIO], Iterable]]]
):
    for key in kwargs:
        if key not in metafunc.fixturenames:
            print(f"'{key}' not an argument of '{metafunc.name}'. Will not parametrise.")
            return
    test_case_dir = abspath(test_case_dir)
    results = []
    for key in kwargs:
        dir_path = join(test_case_dir, kwargs[key][0])
        results.append(read_files(dir_path, kwargs[key][1]))
    metafunc.parametrise(", ".join(kwargs.keys), zip(*results))