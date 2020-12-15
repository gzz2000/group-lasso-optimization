import numpy as np
import math
from utils import provide

ITER = 400

def solver_FGD_primal(x0, A, b, mu, opts={}):
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
        V = X
        step = 0.0001
        
        for it in range(ITER):
            theta = 2 / (it + 1)
            Y = (1 - theta) * X + theta * V
            
            g_frob = A.T @ (A @ Y - b)
            norm_Y = np.linalg.norm(Y, axis=1).reshape((-1, 1))
            g_12norm = Y / np.maximum(norm_Y, delta)
            g = g_frob + mu1 * g_12norm

            t_step = step if mu1 > mu else step / math.sqrt(max(it, 500) - 499)
            X1 = Y - t_step * g
                
            V = X + (X1 - X) / theta
            X = X1
            
            objX = obj(X)
            iters.append((it0, objX))
            it0 += 1
            
    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {# 'FGD_primal_1.0': provide(solver_FGD_primal, delta=1.0),
           # 'FGD_primal_0.1': provide(solver_FGD_primal, delta=0.1),
           # 'FGD_primal_0.01': provide(solver_FGD_primal, delta=0.01),
           # 'FGD_primal_0.001': provide(solver_FGD_primal, delta=0.001),
           # 'FGD_primal_0.0001': provide(solver_FGD_primal, delta=0.0001),
           # 'FGD_primal_0.00001': provide(solver_FGD_primal, delta=0.00001),
           'FGD_primal_0.000001': provide(solver_FGD_primal, delta=0.000001)}
