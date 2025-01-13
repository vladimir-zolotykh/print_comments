#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pathlib
import _io
import re
from dataclasses import dataclass
from typing import TypeVar, Generator


@dataclass
class Path:
    path: pathlib.Path


@dataclass
class File:
    file: _io.TextIOWrapper

    @property
    def path(self):
        return self.file.name


@dataclass
class Line(Path):
    line: str = ''
    line_no: int = -1


@dataclass
class Comment(Line):
    comment: str = ''

T = TypeVar('T')
TypedGenerator = Generator[T, None, None]
Paths = TypedGenerator[Path]
Files = TypedGenerator[File]
Lines = TypedGenerator[Line]


def get_paths(topdir: str, pattern: str) -> Paths:
    for path in pathlib.Path(topdir).rglob(pattern):
        if path.exists():
            yield Path(path=path)


def get_files(paths: Paths) -> Files:
    for path in paths:
        with path.path.open('rt', encoding='latin-1') as file:
            yield File(file=file)


def get_lines(files: Files) -> Lines:
    for file in files:
        line_no: int = 1
        for line in file.file:
            yield Line(path=file.path, line=line, line_no=line_no)
            line_no += 1


def get_comments(lines: Lines) -> Generator[Comment, None, None]:
    for line in lines:
        m = re.match('.*(#.*)$', line.line)
        if m:
            mm = m.group(1)
            yield Comment(path=line.path, line=line.line,
                          line_no=line.line_no, comment=m.group(1))


def print_matching(lines, substring):
    for line in lines:
        if substring in line.line:
            print("{:40s}:{:d} {:s}".format(str(line.path),
                                            line.line_no, line.comment))


if __name__ == '__main__':
    paths = get_paths('.', '*.py')
    files = get_files(paths)
    lines = get_lines(files)
    comments = get_comments(lines)
    print_matching(comments, 'test_dir')
