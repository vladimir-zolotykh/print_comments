#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
# PYTHON_ARGCOMPLETE_OK"

import pathlib
import re


if __name__ == '__main__':
    for path in pathlib.Path('.').rglob('*.py'):
        if path.exists():
            with path.open('rt', encoding='latin-1') as file:
                for line in file:
                    m = re.match('.*(#.*)$', line)
                    if m:
                        comment = m.group(1)
                        if 'test_dir' in comment:
                            print(comment)
