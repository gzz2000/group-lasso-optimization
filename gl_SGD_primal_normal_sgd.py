import cvxpy as cp
import numpy as np
import math
import utils
import pdb

NORM_ZERO_THRESHOLD = 0.000001
ITER = 2000

def solver_SGD_primal_normal_sgd(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]

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
            sg_frob = A.T @ (A @ X - b)
            norm_X = np.linalg.norm(X, axis=1).reshape((-1, 1))
            sg_12norm = X / ((norm_X <= NORM_ZERO_THRESHOLD) + norm_X)
            sg = sg_frob + mu1 * sg_12norm
            if mu1 > mu:
                X -= step * sg
            else:
                X -= step * sg / math.sqrt(max(it, 500)-499)
            objX = obj(X)
            iters.append((it0, objX))
            it0 += 1

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'SGD_primal_normal_sgd': solver_SGD_primal_normal_sgd}
