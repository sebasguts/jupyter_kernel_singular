import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {"argv":[sys.executable,"-m","jupyter_singular_wrapper", "-f", "{connection_file}"],
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
        print('Installing IPython kernel spec')
        install_kernel_spec(td, 'Singular', user=user, replace=True)

def main(argv=None):
    install_my_kernel_spec()

if __name__ == '__main__':
    main()
