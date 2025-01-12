#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from pathlib import Path
from _io import TextIOWrapper
import re
from collections import namedtuple
from typing import Optional, Any, Generator, cast
from pydantic import BaseModel
# Data = namedtuple('Data', 'path file line line_no match')

LazyType = Generator[TextIOWrapper, None, None]

class Data(BaseModel):
    path: Path
    file: object = None
    line: str = ''
    line_no: int = 0
    match: str = ''


def get_paths(topdir, pattern):
    for path in Path(topdir).rglob(pattern):
        if path.exists():
            yield Data(path=path)


# def lazy_open(
#         path: Path, mode: str, encoding: str
# ) -> Generator[Any, None, None]:
def lazy_open(
        path: Path, mode: str, encoding: str
) -> LazyType:
    yield cast(TextIOWrapper, path.open(mode, encoding=encoding))


def get_files(paths):
    for path in paths:
        yield Data(path=path.path,
                   file=lazy_open(path.path, 'rt', encoding='latin-1'))


def get_lines(files: list[Data]) -> Generator[Data, None, None]:
    for file in files:
        line_no: int = 1
        for line in next(cast(LazyType,file.file)):
            yield Data(path=file.path, line=line, line_no=line_no)
            line_no += 1


def get_comments(lines):
    for line in lines:
        m = re.match('.*(#.*)$', line.line)
        if m:
            mm = m.group(1)
            yield Data(path=line.path, line=line.line,
                       line_no=line.line_no, match=m.group(1))


def print_matching(lines, substring):
    for line in lines:
        if substring in line.line:
            print("{:40s}:{:d} {:s}".format(
                str(line.path), line.line_no, line.match))


if __name__ == '__main__':
    paths = get_paths('.', '*.py')
    files = get_files(paths)
    lines = get_lines(files)
    comments = get_comments(lines)
    print_matching(comments, 'test_dir')
