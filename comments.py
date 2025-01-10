#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pathlib
import _io
import re
from collections import namedtuple
from typing import Optional, Any
from pydantic import BaseModel
# Data = namedtuple('Data', 'path file line line_no match')


class Data(BaseModel):
    path: pathlib.Path
    file: object
    # file: _io.TextIOWrapper
    line: Optional[str]
    line_no: Optional[int]
    match: Optional[str]

    @classmethod
    def from_list(cls, *items):
        options = {k: v for k, v in zip(cls.__annotations__, items)}
        return cls(**options)


def get_paths(topdir, pattern):
    for path in pathlib.Path(topdir).rglob(pattern):
        if path.exists():
            yield Data.from_list(path, None, None, None, None)


def get_files(paths):
    for path in paths:
        with path.path.open('rt', encoding='latin-1') as file:
            yield Data.from_list(path.path, file, None, None, None)


def get_lines(files):
    for file in files:
        line_no: int = 1
        for line in file.file:
            yield Data.from_list(file.path, file.file, line, line_no, None)
            line_no += 1
        # yield from file


def get_comments(lines):
    for line in lines:
        m = re.match('.*(#.*)$', line.line)
        if m:
            yield Data.from_list(line.path, line.file, line.line, line.line_no,
                                 m.group(1))


def print_matching(lines, substring):
    for line in lines:
        if substring in line.line:
            print("{:40s}:{:d} {:s}".format(str(line.path), line.line_no,
                                            line.line), end='')


if __name__ == '__main__':
    paths = get_paths('.', '*.py')
    files = get_files(paths)
    lines = get_lines(files)
    comments = get_comments(lines)
    print_matching(comments, 'test_dir')
