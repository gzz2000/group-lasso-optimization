import numpy as np
import math
import utils

ITER = 1500

def solver_ProxGD_primal_line_search(x0, A, b, mu, opts={}):
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
        step = 0.1
        for it in range(ITER):
            # t_step = step if mu1 > mu else step / math.sqrt(max(it, 500) - 499)
            g_frob = A.T @ (A @ X - b)
            def next_X(X, t_step):
                X1 = X - t_step * g_frob
                norm_X = np.linalg.norm(X1, axis=1).reshape((-1, 1))
                X1 = X1 * np.maximum(0, norm_X - mu1 * t_step) / ((norm_X <= mu1 * t_step * 0.1) + norm_X)
                return X1
            while obj(next_X(X, step)) > objX and step > 1e-6:
                step *= 0.9
            else:
                while obj(next_X(X, step / 0.9)) < objX:
                    step /= 0.9
            if step <= 1e-6:
                print(mu1, it)
                break
            X = next_X(X, step)
            objX = obj(X)
            iters.append((it0, objX))
            it0 += 1

    return iters[-1][1], X, len(iters), {'iters': iters}

solvers = {'ProxGD_primal_line_search': solver_ProxGD_primal_line_search}
