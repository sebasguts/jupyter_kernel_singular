from IPython.kernel.zmq.kernelbase import Kernel
import pexpect
from pexpect import replwrap, EOF, which

from subprocess import check_output
from os import unlink, path

import base64
import imghdr
import re
import signal
import urllib

__version__ = '0.3'

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

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_singular()

    def _start_singular(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            singular_run_command = pexpect.which( "Singular" )
            self.singularwrapper = pexpect.spawnu( singular_run_command + " -q" )
            self.singularwrapper.expect( "> " )
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            code_stripped = code.rstrip()
            self.singularwrapper.sendline( code_stripped + "//singular_jupyter_scan_comment" )
            self.singularwrapper.expect( [ "//singular_jupyter_scan_comment\r\n" ] )
            self.singularwrapper.expect( "> " )
            output = self.singularwrapper.before
        except KeyboardInterrupt:
            self.singularwrapper.child.sendintr()
            interrupted = True
            self.singularwrapper.expect( "> " )
            output = self.singularwrapper.before
        except EOF:
            output = self.singularwrapper.before + 'Restarting singular'
            self._start_singular()

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        try:
            exitcode = 0
        except Exception:
            exitcode = 1

        if exitcode:
            return {'status': 'error', 'execution_count': self.execution_count,
                    'ename': '', 'evalue': str(exitcode), 'traceback': []}
        else:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

    # This is a rather poor completion at the moment
    def do_complete(self, code, cursor_pos):

        return {'matches': [ ], 'cursor_start': 0,
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}


