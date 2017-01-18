# jupyter-singular
Jupyter kernel for Singular 

This is a beta version of a jupyter kernel for Singular.

## Requirements

Jupyter Singular kernel can work with pexpect or SingularPython, a Python2/3
module accessing the Singular interpreter via libSingular.

In order to work with this jupyter kernel, you need a recent version of Singular installed (>=4.1.0)
and have the Singular executable in your path.

To get a stable interface, it is highly recommended to use SingularPython, which also
provides further functionality than the pexpect fallback solution.

