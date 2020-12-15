import numpy as np
import math
import utils

ITER = 400

def solver_FProxGD_primal(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]

    def obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    iters = []
    X = x0
    step = 0.0001

    it0 = 0
    for mu1 in [100 * mu, 10 * mu, mu]:
        objX = obj(X)
        V = X
        for it in range(ITER):
            theta = 2 / (it + 1)
            Y = (1 - theta) * X + theta * V
            
            t_step = step if mu1 > mu else step / math.sqrt(max(it, 500) - 499)
            g_frob = A.T @ (A @ Y - b)
            
            X1 = Y - t_step * g_frob
            norm_X = np.linalg.norm(X1, axis=1).reshape((-1, 1))
            X1 = X1 * np.maximum(0, norm_X - mu1 * t_step) / ((norm_X <= mu1 * t_step * 0.1) + norm_X)
            V = X + (X1 - X) / theta
            X = X1
            
            objX = obj(X)
            # print(mu1, it, objX)
            iters.append((it0, objX))
            it0 += 1

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'FProxGD_primal': solver_FProxGD_primal}
