# jupyter_kernel_singular
Jupyter kernel for Singular 

# Using Singular in Jupyter

It is possible to use [Jupyter](http://www.jupyter.org) as front-end for Singular.

## Installation

These installation instructions are for Ubuntu Linux 16.04 (Xenial).

### Python and Jupyter

If you want to run the Jupyter notebook locally on your computer, you need a recent version
of Python 3 and Jupyter installed.

To install Python3 run
```
apt-get install python3-pip
```
We recommend using Python3, but you can also use Python2.

To install Jupyter using pip, run
```
pip3 install jupyter
```

### Singular

You need a recent (>= 4.1.0) version of Singular.

Installation instructions for Singular can be found [here](https://github.com/Singular/Sources/wiki/Step-by-Step-Installation-Instructions-for-Singular).

It is important to have a correctly installed Singular
and to have a `Singular` executable in your `PATH`.

Normally, running
```
make install
```
from the Singular installation directory after compiling Singular will ensure that the `Singular` executable is present in a directory that is in your `PATH`.

If you are compiling and installing
Singular with custom options, make sure both the `Singular` executable and `libSingular`
are available in your system executables and include/library paths.


### Jupyter Singular kernel

The Jupyter kernel for Singular consists of two packages. You can install them via pip using
```
pip3 install PySingular
pip3 install jupyter_kernel_singular
```
While not recommended, it is possible to use the Jupyter kernel for Singular without the `PySingular`
package. If you have problems to install it, do not worry, it will be fine.


### Images using surf

It is possible to display images created by surf in the Jupyter notebooks. For this, you need to
download, compile, and install the [latest version of surf](ftp://www.mathematik.uni-kl.de/pub/Math/Singular/misc/surf-1.0.6-gcc6.tar.gz).

Please configure and compile it via
```
./configure --disable-gui
make
make install
```
For pictures to be displayed in the Notebook, you need to load a specialized Singular library, and a specialized plot command.
You can find an example of how to use it [here](https://github.com/sebasguts/jupyter-singular/blob/master/Demo.ipynb).


## Usage and examples

After installing the kernel, you can start a Jupyter Notebook server by running
```
jupyter notebook
```
Now you can create a new notebook with Singular code.

Example notebooks can be found [here](https://github.com/sebasguts/jupyter-singular/blob/master/Demo.ipynb)
and [here](https://github.com/sebasguts/jupyter-singular/blob/master/WidgetTestSingular.ipynb).



