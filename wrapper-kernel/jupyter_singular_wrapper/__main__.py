from ipykernel.kernelapp import IPKernelApp
from .kernel import SingularKernel
IPKernelApp.launch_instance(kernel_class=SingularKernel)
