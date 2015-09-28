# jupyter-singular
Jupyter kernels for Singular 

This is an alpha version of a jupyter kernel for Singular. All of this is non-finished and might not work,
depending on your OS, libs, etc.

## singular-kernel

The `singular-kernel` is a Jupyter kernel based on the [bash wrapper kernel](https://github.com/takluyver/bash_kernel),
to install

```shell
    python setup.py install
    python -m jupyter_singular_wrapper.install
```

To use it, use one of the following:

```shell
    ipython notebook
    ipython qtconsole --kernel Singular
    ipython console --kernel Singular
```

Note that this kernel assumes that `Singular` is in the `PATH`.
