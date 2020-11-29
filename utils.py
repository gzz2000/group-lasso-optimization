import contextlib
import sys
import os
import re

'''
This is for recording iteration counts and objective values in shared libraries like gurobi and mosek
'''
@contextlib.contextmanager
def capture_output():
    fd = sys.stdout.fileno()
    def _redir_stdout(to):
        sys.stdout.close()
        os.dup2(to.fileno(), fd)
        sys.stdout = os.fdopen(fd, 'w')
    ret = {}
    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open('/tmp/solver_output.txt', 'w') as f:
            _redir_stdout(f)
        try:
            yield ret
        finally:
            _redir_stdout(old_stdout)
            with open('/tmp/solver_output.txt') as f:
                ret['output'] = f.read()

re_iterc_default = re.compile(r'^ *(?P<iterc>\d{1,3})\:? +(?P<objv>[0-9\.eE\+\-]+)', re.MULTILINE)

reg_solver = {
    'GUROBI': re_iterc_default,
    'MOSEK': re.compile(r'^ *(?P<iterc>\d{1,3})\:?( +(?:[0-9\.eE\+\-]+)){4} +(?P<objv>[0-9\.eE\+\-]+)', re.MULTILINE),   # skip four columns
    'CVXOPT': re_iterc_default,
}

def parse_iters(s, solver=None):
    re_iterc = reg_solver[solver] if solver in reg_solver else re_iterc_default
    ret = []
    for match in re_iterc.finditer(s):
        ret.append((int(match.groupdict()['iterc']),
                    float(match.groupdict()['objv'])))
    return ret
