#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# file: get_lines; dir: test_dir

def get_lines(files):
    for file in files:
        yield from file
