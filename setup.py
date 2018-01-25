#!/usr/bin/env python

from glob import glob
from distutils.core import setup

import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

from os.path import dirname,abspath

from shutil import copy as file_copy

kernelpath = os.path.join("share", "jupyter", "kernels", "singular")
nbextpath = os.path.join("share", "jupyter", "nbextensions", "singular-mode")
nbconfpath = os.path.join("etc", "jupyter", "nbconfig", "notebook.d")

setup( name="jupyter_kernel_singular"
     , version="0.9.8"
     , description="A Jupyter kernel for singular"
     , author="Sebastian Gutsche"
     , author_email="sebastian.gutsche@gmail.com"
     , url="https://github.com/sebasguts/jupyter-singular"
     , packages=["jupyter_kernel_singular"]
     , package_dir={"jupyter_kernel_singular": "jupyter_kernel_singular"}
     , data_files=[(kernelpath, glob("jupyter_kernel_singular/resources/*")),
                   (kernelpath, glob("jupyter_kernel_singular/kernel.json")),
                   (nbextpath, glob("jupyter_kernel_singular/singular-mode/*")),
                   (nbconfpath, glob("jupyter_kernel_singular/singular-mode.json"))]
     )
