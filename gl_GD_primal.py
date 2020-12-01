import numpy as np
import math
import utils
from utils import provide

NORM_ZERO_THRESHOLD = 0.000001
ITER = 2000

def solver_GD_primal(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]
    delta = opts.get('delta', 0.00001)

    def obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    iters = []
    X = x0

    it0 = 0
    for mu1 in [100 * mu, 10 * mu, mu]:
        objX = obj(X)
        step = 0.1
        momentum = np.zeros((n, l))
        for it in range(ITER):
            g_frob = A.T @ (A @ X - b)
            norm_X = np.linalg.norm(X, axis=1).reshape((-1, 1))
            g_12norm = X / np.maximum(norm_X, delta)
            g = g_frob + mu1 * g_12norm
            # g = g / (np.linalg.norm(g, 'fro') + 0.01)
            momentum = momentum * 0.9 + g * 0.1
            while obj(X - step * momentum) > objX and step > 1e-6:
                step *= 0.9
            else:
                while obj(X - step / 0.9 * momentum) < objX:
                    step /= 0.9
            if step <= 1e-6:
                break
            X -= step * momentum
            objX = obj(X)
            iters.append((it0, objX))
            it0 += 1
            # if iters[-1][1] > iters[-2][1]:
            #     break

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'GD_primal_1.0': provide(solver_GD_primal, delta=1.0),
           'GD_primal_0.1': provide(solver_GD_primal, delta=0.1),
           'GD_primal_0.01': provide(solver_GD_primal, delta=0.01),
           'GD_primal_0.001': provide(solver_GD_primal, delta=0.001),
           'GD_primal_0.0001': provide(solver_GD_primal, delta=0.0001),
           'GD_primal_0.00001': provide(solver_GD_primal, delta=0.00001),
           'GD_primal_0.000001': provide(solver_GD_primal, delta=0.000001)}
