from ipykernel.kernelbase import Kernel

from subprocess import check_output
from os import unlink, path

import base64
import imghdr
import re
import signal
import urllib
import pexpect
from pexpect import replwrap, EOF, which

from ipykernel.comm import Comm
from ipykernel.comm import CommManager

import sys

kernel_object_for_ipython = None

def _mock_get_ipython():
    global kernel_object_for_ipython
    return kernel_object_for_ipython

try:
    import IPython
    ipython_loaded = True
except ImportError:
    ipython_loaded = False

if ipython_loaded:
    ## Rewrite this incredibly stupid get_ipython method
    get_ipython = _mock_get_ipython
    sys.modules['IPython'].get_ipython = _mock_get_ipython
    sys.modules['IPython'].core.getipython.get_ipython = _mock_get_ipython

try:
    from ipywidgets import *
    ipywidgets_extension_loaded = True
except ImportError:
    ipywidgets_extension_loaded = False

class own_ipython:
    kernel = None
    def __init__(self, kernel = None ):
        self.kernel = kernel

class own_ipython:
    kernel = None
    def __init__(self, kernel = None ):
        self.kernel = kernel


try:
    from PySingular import InitializeSingular,RunSingularCommand,GetSingularCompletion
except ImportError:
    def InitializeSingular( path ):
        global singularwrapper
        singularwrapper = pexpect.spawnu( path + " -q" )
        singularwrapper.expect( "> " )
    
    def RunSingularCommand( code ):
        global singularwrapper
        code_stripped = code.rstrip()
        singularwrapper.sendline( code_stripped + "//singular_jupyter_scan_comment" )
        singularwrapper.expect( [ "//singular_jupyter_scan_comment\r\n" ] )
        singularwrapper.expect( "> " )
        output = singularwrapper.before
        return ( False, output )
    
    def GetSingularCompletion( code, start, end ):
        global singularwrapper
        code = code[ start : end ]
        matches = [ ]
        scan_string = "// " + code
        singularwrapper.send( scan_string )
        singularwrapper.send( "\t\t\t" )
        out_num = self.singularwrapper.expect( [ "Display", "> " ] )
        if out_num == 0:
            output_list = self.singularwrapper.before[3:]
            singularwrapper.send( "n\r\n" )
        else:
            output_list = self.singularwrapper.before
        matches.extend(output_list.split())
        singularwrapper.sendline( "" )
        singularwrapper.sendline( ";//singular_jupyter_scan_comment" )
        singularwrapper.expect( [ "//singular_jupyter_scan_comment" ] )
        singularwrapper.expect( [ "> " ] )
        matches = [m for m in matches if m.isalnum() ]
        return matches
    

__version__ = '0.4'

version_pat = re.compile(r'version (\d+(\.\d+)+)')

class SingularKernel(Kernel):
    implementation = 'jupyter_singular_wrapper'
    implementation_version = __version__
    
    def _replace_get_ipython(self):
        new_kernel = own_ipython(self)
        global kernel_object_for_ipython
        kernel_object_for_ipython = new_kernel
    
    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = "Singular Jupyter Kernel"
        return self._banner

    language_info = {'name': 'Singular',
                     'codemirror_mode': 'singular', # note that this does not exist yet
                     'mimetype': 'text/x-singular',
                     'file_extension': '.singular'}
    
    help_links = [ { 'text': "Singular manual", 'url': "http://www.singular.uni-kl.de/Manual/4-1-0/index.htm" },
                   { 'text': "Singular examples", 'url': "http://www.singular.uni-kl.de/Manual/4-1-0/sing_786.htm" },
                   { 'text': "Singular library", 'url': "http://www.singular.uni-kl.de/Manual/4-1-0/sing_870.htm" },
                   { 'text': "Singular index", 'url': "http://www.singular.uni-kl.de/Manual/4-1-0/sing_2557.htm" } ]

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._replace_get_ipython()
        #self.comm_manager = CommManager(shell=None, parent=self,
                                        #kernel=self)
        
        #self.shell_handlers['comm_open'] = self.comm_manager.comm_open
        #self.shell_handlers['comm_msg'] = self.comm_manager.comm_msg
        #self.shell_handlers['comm_close'] = self.comm_manager.comm_close
        #if ipywidgets_extension_loaded:
            #self.comm_manager.register_target('ipython.widget', Widget.handle_comm_opened)
        self._start_singular()

    def _start_singular(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, sig)
        InitializeSingular( which( "Singular" ) )
    
    def _check_for_plot( self, code ):
        return "plot_jupyter" in code
    
    def _process_python( self, code ):
        if code.find( "@python" ) == -1 and code.find( "@widget" ) == -1:
            return False
        exec(code[7:],globals(),locals())
        return True
    
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        
        default = {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
        
        if not code.strip():
            return default
        
        if self._process_python( code ):
            return default
        
        interrupted = False
        
        code_stripped = code.rstrip()
        output = RunSingularCommand( code_stripped )
        
        output_error = output[ 0 ]
        output_string = output[ 1 ]
        
        if not output_error:
            if not silent:
                if self._check_for_plot( code_stripped ):
                    
                    filename_image = output_string.rstrip() + ".jpg"
                    
                    with open( filename_image, "rb" ) as imageFile:
                        image_string = base64.b64encode( imageFile.read() ).decode()
                    
                    stream_content = { 'source' : 'singular',
                                      'data': { 'image/jpeg': image_string },
                                      'metadata': { 'image/jpeg' : { 'width': 400, 'height': 400 } } }
                    self.send_response(self.iopub_socket, 'display_data', stream_content)
                elif output_string.strip() != "":
                    stream_content = {'execution_count': self.execution_count, 'data': { 'text/plain': output_string }, 'metadata' : { } }
                    self.send_response( self.iopub_socket, 'execute_result', stream_content )
                
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
        
        else:
            
            stream_content = {'execution_count': self.execution_count, 'data': { 'text/plain': "Error:" } }
            self.send_response( self.iopub_socket, 'execute_result', stream_content )
            stream_content = {'execution_count': self.execution_count, 'data': { 'text/plain': output_string } }
            self.send_response( self.iopub_socket, 'execute_result', stream_content )
            
            
            stream_content = { 'execution_count': self.execution_count, 'ename': '', 'evalue': output_string, 'traceback': [ ] }
            self.send_response( self.iopub_socket, 'error', stream_content )
            return {'status': 'error', 'execution_count': self.execution_count,
                    'ename': '', 'evalue': output_string, 'traceback': [ ] }
        
    
    def do_complete( self, code, cursor_pos ):
        code = code[:cursor_pos]
        default = {'matches': [], 'cursor_start': 0,
                   'cursor_end': cursor_pos, 'metadata': dict(),
                   'status': 'ok'}
        
        token = code.encode( "utf-8" )
        start = cursor_pos - len(token)
        completion_list = GetSingularCompletion( code, start, cursor_pos )
        
        if not completion_list:
            return default
        
        return {'matches': sorted(completion_list), 'cursor_start': start,
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}
        
    def do_is_complete( self, code ):
        code = code.rstrip()
        if code[-1] == ";":
            return { 'status': 'complete' }
        else:
            return { 'status': 'incomplete', 'indent': '  ' }
          


