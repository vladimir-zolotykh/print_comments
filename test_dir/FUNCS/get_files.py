#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# file: get_files dir: test_dir

def get_files(paths):
    for path in paths:
        with path.open('rt', encoding='latin-1') as file:
            yield file
