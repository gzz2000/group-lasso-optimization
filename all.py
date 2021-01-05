
def collect_solvers(modules):
    import importlib
    solvers = {}
    for mod in modules:
        solvers.update(importlib.import_module(mod).solvers)
    return solvers

solvers = collect_solvers([
    'gl_ADMM_dual',
    'gl_ADMM_primal_direct', 'gl_ADMM_primal',
    'gl_FGD_primal', 'gl_FGD_primal_line_search',
    'gl_ProxGD_primal', 'gl_ProxGD_primal_line_search',
    'gl_FProxGD_primal', 'gl_FProxGD_primal_line_search',
    'gl_SGD_primal', 'gl_SGD_primal_normal_sgd',
    'gl_GD_primal', 'gl_GD_primal_normal_gd',
    'gl_cvx',
    'gl_gurobi', 'gl_gurobi_term',
    'gl_mosek',
])

if __name__ == '__main__':
    print('Run python test.py all (not python all.py) to test all solvers.')
