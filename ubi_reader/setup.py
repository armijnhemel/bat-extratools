#!/usr/bin/env python

from distutils.core import setup
import glob
import os.path

setup(name='ubi_reader',
      version='0.1-372e5da53a9b52295af98b4e9852d12f393df6ae',
      description='ubi_reader',
      author='Jason Pruitt',
      author_email='jrspruitt@gmail.com',
      url='https://github.com/jrspruitt/ubi_reader',
      packages=['modules', 'modules/debug', 'modules/ubi', 'modules/ubi/block', 'modules/ubi/volume', 'modules/ubi/image', 'modules/ubi/headers', 'modules/ubifs', 'modules/ubifs/nodes', 'modules/ubi_io'],
      license="GPL 3",
      scripts=['ubi_display_info.py', 'ubi_extract_files.py', 'ubi_extract_images.py','ubi_utils_info.py'],
     long_description="""ubi_reader is a collection of scripts
"""
     )
