#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pathlib
import _io
import re
from collections import namedtuple
from typing import Optional, Any, Generator
from pydantic import BaseModel
# Data = namedtuple('Data', 'path file line line_no match')

LazyFile = Generator[_io.TextIOWrapper, None, None]

class Data(BaseModel):
    path: pathlib.Path
    file: object = None
    # file: _io.TextIOWrapper
    line: Optional[str] = ''
    line_no: Optional[int] = 0
    match: Optional[str] = ''

    @classmethod
    def from_list(cls, *items):
        options = {k: v for k, v in zip(cls.__annotations__, items)}
        return cls(**options)


def get_paths(topdir, pattern):
    for path in pathlib.Path(topdir).rglob(pattern):
        if path.exists():
            # yield Data.from_list(path, None, None, None, None)
            yield Data(path=path)


def LazyFile(path, mode, **kwargs):
    yield path.open(mode, **kwargs)


def get_files(paths):
    for path in paths:
        # yield Data.from_list(
        #     path.path, LazyFile(path.path, 'rt', encoding='latin-1'),
        #     None, None, None)
        yield Data(path=path.path,
                   file=LazyFile(path.path, 'rt', encoding='latin-1'))
        # with path.path.open('rt', encoding='latin-1') as file:
        #     yield Data.from_list(path.path, file, None, None, None)


def get_lines(files):
    for file in files:
        line_no: int = 1
        for line in next(file.file):
            # yield Data.from_list(file.path, file.file, line, line_no, None)
            yield Data(path=file.path, line=line, line_no=line_no)
            line_no += 1
        # yield from file


def get_comments(lines):
    for line in lines:
        m = re.match('.*(#.*)$', line.line)
        if m:
            mm = m.group(1)
            # yield Data.from_list(line.path, line.file, line.line,
            #                      line.line_no, m.group(1))
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
