#!/usr/bin/env python

import sys
from distutils.core import setup

import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

from os.path import dirname,abspath

from shutil import copy as file_copy


kernel_json = {"argv":[sys.executable,"-m","jupyter_kernel_singular", "-f", "{connection_file}"],
 "display_name":"Singular",
 "language":"singular",
 "codemirror_mode":"singular", # note that this does not exist yet
 "env":{"PS1": "$"}
}

def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        path_of_file = dirname( abspath(__file__) ) + "/jupyter_kernel_singular/resources/"
        file_copy(path_of_file + "logo-32x32.png", td )
        file_copy(path_of_file + "logo-64x64.png", td )
        print('Installing IPython kernel spec')
        install_kernel_spec(td, 'Singular', user=user, replace=True)

def main(argv=None):
    install_my_kernel_spec()

if __name__ == '__main__':
    main()


setup( name="jupyter_kernel_singular"
     , version="0.9.4"
     , description="A Jupyter kernel for singular"
     , author="Sebastian Gutsche"
     , author_email="sebastian.gutsche@gmail.com"
     , url="https://github.com/sebasguts/jupyter-singular"
     , packages=["jupyter_kernel_singular"]
     , package_dir={"jupyter_kernel_singular": "jupyter_kernel_singular"}
     , package_data={"jupyter_kernel_singular": ["resources/logo-32x32.png","resources/logo-64x64.png"]}
     )
