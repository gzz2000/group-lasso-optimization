import numpy as np
from utils import stoprange

MAX_ITER = 999
th_converge = 1e-3

def solver_ADMM_primal_direct(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]

    def obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    def prox(y, mu):
        norm = np.linalg.norm(y, axis=1, keepdims=True)
        return y * np.maximum(0, norm - mu) / ((norm < mu * 0.1) + norm)

    iters = []
    x = x0
    y = x0
    z = np.zeros((n, l))

    t = opts.get('t', 0.1)
    inv = np.linalg.inv(t * np.eye(n) + A.T @ A)
    ATb = A.T @ b

    for it, report_convergence in stoprange(MAX_ITER, 8):
        x = inv @ (t * y + ATb - z)
        y0 = y
        y = prox(x + z / t, mu / t)
        z = z + t * (x - y)
        iters.append((it, obj(y)))

        primal_sat = np.linalg.norm(x - y)
        dual_sat = np.linalg.norm(y0 - y)
        is_conv = primal_sat < th_converge and dual_sat < th_converge
        report_convergence(is_conv)

    return iters[-1][1], y, len(iters), {'iters': iters}

solvers = {'ADMM_primal_direct': solver_ADMM_primal_direct}

# If you want to test the effect of tuning hyperparameter t,
# Uncomment below and run >> python test.py gl_ADMM_primal_direct
# The sequence of t in this test is made deliberately the inverse of
#  the sequence of t in gl_ADMM_dual.py respectively.

# solvers = {'ADMM_primal_direct_t_%f' % t: lambda *a, t=t: solver_ADMM_primal_direct(*a, opts={'t': t})
#            for t in [2, 1, 0.2, 0.1, 0.02, 0.01, 0.005, 0.002, 0.001]}

