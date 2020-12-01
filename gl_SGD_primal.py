import cvxpy as cp
import numpy as np
import math
import utils
import pdb

NORM_ZERO_THRESHOLD = 0.000001
ITER = 5000

def solver_SGD_primal(x0, A, b, mu, opts=[]):
    m, n = A.shape
    l = b.shape[1]

    def obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    iters = []
    X = x0

    it0 = 0
    for mu1 in [100 * mu, 30 * mu, 10 * mu, 3 * mu, mu]:
        objX = obj(X)
        step = 1
        momentum = np.zeros((n, l))
        for it in range(ITER):
            sg_frob = A.T @ (A @ X - b)
            norm_X = np.linalg.norm(X, axis=1).reshape((-1, 1))
            sg_12norm = X / ((norm_X <= NORM_ZERO_THRESHOLD) + norm_X)
            sg = sg_frob + mu1 * sg_12norm
            sg = sg / (np.linalg.norm(sg, 'fro') + 0.01)
            momentum = momentum * 0.9 + sg * 0.1
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

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'SGD_primal': solver_SGD_primal}
