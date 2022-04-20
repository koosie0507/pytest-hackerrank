from os import walk
from os.path import basename, join, dirname, abspath
from re import S, compile, match
from typing import List


__NUMERIC_PREFIX_REGEX = compile("^(\d+).*", S)


def __filename_sort_key(val):
    fname = basename(val)
    dpath = dirname(val)
    m = match(__NUMERIC_PREFIX_REGEX, fname)
    if m and m.group(1):
        n = m.group(1)
        rest = val[m.endpos:]
        return join(dpath, n.zfill(10)+rest)
    return val


def list_file_paths(dir_path: str) -> List[str]:
    return sorted(
        next(walk(abspath(dir_path)), (None, None, []))[2],
        key=__filename_sort_key
    )


def read_int_array(file):
    with open(file) as f:
        n = int(f.readline().strip())
        arr = list(map(int, f.readline().strip().split()))
    if n != len(arr):
        raise ValueError('bad input file')
    return arr


def read_int(file):
    with open(file) as f:
        return int(f.readline().strip())


def read_str_list(file):
    with open(file) as f:
        return list(
            map(lambda x: x.strip(), f.readlines())
        )


def read_tuple_list(file):
    with open(file) as f:
        return [
            tuple(line.split(" "))
            for line in map(lambda x: x.strip(), f.readlines())
        ]