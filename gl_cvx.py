import cvxpy as cp
import numpy as np
import utils

def solver_cvx(x0, A, b, mu, solver, opts=[]):
    m, n = A.shape
    l = b.shape[1]
    
    X = cp.Variable((n, l))
    X.value = x0
    objective = cp.Minimize(0.5 * cp.square(cp.norm(A @ X - b, 'fro')) + mu * cp.sum(cp.norm(X, 2, 1)))
    prob = cp.Problem(objective)
    with utils.capture_output() as outs:
        result = prob.solve(solver=solver, verbose=True)
    iters = utils.parse_iters(outs['output'], solver)
    # print('output:', outs['output'])
    # print('CVXPY status: %s' % prob.status)
    # print('Solver stats: %s' % prob.solver_stats)
    return prob.value, X.value, len(iters), {'iters': iters}

solvers = {'cvx(%s)' % solver: lambda *args, solver=solver: solver_cvx(*args, solver)
           for solver in ['GUROBI', 'MOSEK', 'CVXOPT']}

def solver_cvx_gurobi(x0, A, b, mu, opts):
    return solver_cvx(x0, A, b, mu, 'GUROBI', opts)

def solver_cvx_mosek(x0, A, b, mu, opts):
    return solver_cvx(x0, A, b, mu, 'MOSEK', opts)
