'''
This is term-based Gurobi implementation.
Origin: TA Yiyang Liu
'''
import gurobipy as gp
import numpy as np
import time
import utils

def blockdiag(n, arr):
    zeronn = np.zeros((n, n))
    ret = [[zeronn for i in range(len(arr))] for j in range(len(arr))]
    for i in range(len(arr)):
        ret[i][i] = arr[i]
    return np.block(ret)

def solver_gurobi_term(x0, A, b, mu, opts=[]):
    m, n = A.shape
    l = b.shape[1]
    
    t1 = time.time_ns()
    model = gp.Model()
    t2 = time.time_ns()
    x = model.addVars(n * l, lb=-gp.GRB.INFINITY)  # actually l * n
    for i in range(n):
        for j in range(l):
            x.start = x0[i, j]
    t = model.addVars(n, lb=0) # order matters
    halfATA = 0.5 * A.T @ A
    zeronn = np.zeros((n, n))
    Q = blockdiag(n, [halfATA for j in range(l)] + [zeronn])
    c = np.block([[(-b.T @ A).reshape(-1, 1)],
                  [mu * np.ones((n, 1))]]).ravel()
    objcon = 0.5 * np.linalg.norm(b.ravel()) ** 2
    model.setMObjective(Q, c, objcon, sense=gp.GRB.MINIMIZE)
    t3 = time.time_ns()
    for i in range(n):
        model.addConstr(gp.quicksum([x[j * n + i] * x[j * n + i] for j in range(l)]) <= t[i] * t[i])
    t4 = time.time_ns()
    # print(t2 - t1, t3 - t2, t4 - t3)
    with utils.capture_output() as outs:
        model.optimize()
    # print(outs['output'])
    iters = utils.parse_iters(outs['output'])
    Xret = np.array([[x[j * n + i].x for j in range(l)] for i in range(n)])
    # print('output:', outs['output'])
    # for i in range(n):
    #     print(np.abs(Xret[i]) > 1e-4)
    return model.objVal, Xret, len(iters), {'iters': iters}

solvers = {'gurobi_SOCP_term': solver_gurobi_term}
