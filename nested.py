#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
# PYTHON_ARGCOMPLETE_OK"

import pathlib
import re


if __name__ == '__main__':
    _path: str = ''
    _line_no: int = 1
    for path in pathlib.Path('.').rglob('*.py'):
        if path.exists():
            with path.open('rt', encoding='latin-1') as file:
                _path = str(path)
                _line_no = 1
                for line in file:
                    m = re.match('.*(#.*)$', line)
                    if m:
                        comment = m.group(1)
                        if 'test_dir' in comment:
                            print(f'{_path = }, {_line_no = }, {comment = }')
                    _line_no += 1
