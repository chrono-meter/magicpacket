#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# from distutils.core import setup
from cx_Freeze import setup, Executable


if __name__ == '__main__':
    setup(
        name='magicpacket',
        version='2.0.0',
        license='MIT',
        author='chrono-meter@gmx.net',
        author_email='chrono-meter@gmx.net',
        description='WOL magic packet sender',
        options={
            # 'build_exe': {
            #     'packages': ['os'],
            #     'excludes': ['tkinter'],
            # },
        },
        executables=[Executable('magicpacket.py')],
    )
