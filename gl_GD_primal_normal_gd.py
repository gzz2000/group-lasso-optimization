import numpy as np
import math
from utils import provide

ITER = 2000

def solver_GD_primal_normal_gd(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]
    delta = opts.get('delta', 0.00001)

    def obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    iters = []
    X = x0
    step = 0.001

    it0 = 0
    for mu1 in [100 * mu, 10 * mu, mu]:
        objX = obj(X)
        for it in range(ITER):
            g_frob = A.T @ (A @ X - b)
            norm_X = np.linalg.norm(X, axis=1).reshape((-1, 1))
            g_12norm = X / np.maximum(norm_X, delta)
            g = g_frob + mu1 * g_12norm
            if mu1 > mu:
                X -= step * g
            else:
                X -= step * g / math.sqrt(max(it, 500)-499)
            objX = obj(X)
            iters.append((it0, objX))
            it0 += 1

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'GD_primal_normal_gd_1.0': provide(solver_GD_primal_normal_gd, delta=1.0),
           'GD_primal_normal_gd_0.1': provide(solver_GD_primal_normal_gd, delta=0.1),
           'GD_primal_normal_gd_0.01': provide(solver_GD_primal_normal_gd, delta=0.01),
           'GD_primal_normal_gd_0.001': provide(solver_GD_primal_normal_gd, delta=0.001),
           'GD_primal_normal_gd_0.0001': provide(solver_GD_primal_normal_gd, delta=0.0001),
           'GD_primal_normal_gd_0.00001': provide(solver_GD_primal_normal_gd, delta=0.00001),
           'GD_primal_normal_gd_0.000001': provide(solver_GD_primal_normal_gd, delta=0.000001)}
