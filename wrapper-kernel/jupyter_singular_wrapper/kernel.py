from ipykernel.kernelbase import Kernel

from subprocess import check_output
from os import unlink, path

import base64
import imghdr
import re
import signal
import urllib

try:
    from SingularPython import RunSingularCommand,GetSingularCompletion
except ImportError:
    import pexpect
    from pexpect import replwrap, EOF, which
    singular_run_command = pexpect.which( "Singular" )
    singularwrapper = pexpect.spawnu( singular_run_command + " -q" )
    singularwrapper.expect( "> " )
    
    def RunSingularCommand( code ):
        code_stripped = code.rstrip()
        singularwrapper.sendline( code_stripped + "//singular_jupyter_scan_comment" )
        singularwrapper.expect( [ "//singular_jupyter_scan_comment\r\n" ] )
        singularwrapper.expect( "> " )
        output = singularwrapper.before
        return ( False, output )
    
    def GetSingularCompletion( code, start, end ):
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

    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = "Singular Jupyter kernel"
        return self._banner

    language_info = {'name': 'Singular',
                     'codemirror_mode': 'singular', # note that this does not exist yet
                     'mimetype': 'text/x-singular',
                     'file_extension': '.singular'}
    
    help_links = [ { 'text': "Singular manual", 'url': "http://www.singular.uni-kl.de/Manual/latest/index.htm" },
                   { 'text': "Singular examples", 'url': "http://www.singular.uni-kl.de/Manual/latest/sing_842.htm" },
                   { 'text': "Singular library", 'url': "http://www.singular.uni-kl.de/Manual/latest/sing_926.htm" },
                   { 'text': "Singular index", 'url': "http://www.singular.uni-kl.de/Manual/latest/sing_2336.htm" } ]

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_singular()

    def _start_singular(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, sig)
    
    def _check_for_plot( self, code ):
        return "plot_jupyter" in code
    
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        
        code_stripped = code.rstrip()
        output = RunSingularCommand( code_stripped )
        
        output_error = output[ 0 ]
        output_string = output[ 1 ]
        
        if not output_error:
            if not silent:
                if self._check_for_plot( code_stripped ):
                    
                    with open( "/tmp/surf.jpg", "rb" ) as imageFile:
                        image_string = base64.b64encode( imageFile.read() ).decode()
                    
                    stream_content = { 'source' : 'singular',
                                      'data': { 'image/jpeg': image_string },
                                      'metadata': { 'image/jpeg' : { 'width': 400, 'height': 400 } } }
                    self.send_response(self.iopub_socket, 'display_data', stream_content)
                elif output_string.strip() != "":
                    stream_content = {'execution_count': self.execution_count, 'data': { 'text/plain': output_string } }
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
        

