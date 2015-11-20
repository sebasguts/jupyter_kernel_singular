#!/usr/bin/env python

import sys
from distutils.core import setup

setup( name="jupyter_singular_wrapper"
     , version="0.1"
     , description="A Jupyter wrapper kernel for singular"
     , author="Sebastian Gutsche"
     , url="https://github.com/sebasguts/jupyter-singular"
     , packages=["jupyter_singular_wrapper"]
     , package_dir={"jupyter_singular_wrapper": "jupyter_singular_wrapper"}
     , package_data={"jupyter_singular_wrapper": ["resources/logo-32x32.png","resources/logo-64x64.png"]}
     )
