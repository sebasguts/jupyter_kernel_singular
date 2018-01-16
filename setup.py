#!/usr/bin/env python

from glob import glob
from distutils.core import setup
from setuptools.command.install import install as _install

import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

from os.path import dirname,abspath

from shutil import copy as file_copy

kernelpath = os.path.join("share", "jupyter", "kernels", "singular")
nbextpath = os.path.join("share", "jupyter", "nbextensions", "singular-mode")

kernel_json = {"argv":[sys.executable,"-m","jupyter_kernel_singular", "-f", "{connection_file}"],
 "display_name":"Singular",
 "language":"singular",
 "codemirror_mode":"singular",
 "env":{"PS1": "$"}
}

class install(_install):
    def run(self):
        from notebook.nbextensions import enable_nbextension, install_nbextension
        # run from distutils install
        _install.run(self)

        #install kernel specs
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            path_of_file = dirname( abspath(__file__) ) + "/jupyter_kernel_singular/resources/"
            file_copy(path_of_file + "logo-32x32.png", td )
            file_copy(path_of_file + "logo-64x64.png", td )
            print('Installing IPython kernel spec')
            install_kernel_spec(td, 'Singular', user=self.user, replace=True)

        #install codemirror notebook extension
        install_nbextension('jupyter_kernel_singular/singular-mode', overwrite=True, user=self.user)
        enable_nbextension('notebook', 'singular-mode/main')

setup( name="jupyter_kernel_singular"
     , version="0.9.6"
     , description="A Jupyter kernel for singular"
     , author="Sebastian Gutsche"
     , author_email="sebastian.gutsche@gmail.com"
     , url="https://github.com/sebasguts/jupyter-singular"
     , packages=["jupyter_kernel_singular"]
     , package_dir={"jupyter_kernel_singular": "jupyter_kernel_singular"}
     , data_files=[(kernelpath, glob("resources/*")), (nbextpath, glob("singular-mode/*"))]
     , cmdclass={'install':install}
     )
