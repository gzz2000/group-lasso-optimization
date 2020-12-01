import numpy as np

# 8026727 is "gzz" in low-end ascii representation
seed = 8026727
np.random.seed(seed)

n = 512
m = 256
A = np.random.randn(m, n)
k = round(n * 0.1)
l = 2
p = np.random.permutation(n)[:k]
u = np.zeros((n, l))
u[p, :] = np.random.randn(k, l)
b = A @ u
mu = 1e-2
# x0 = np.zeros((n, l))  #np.random.rand(n, l)
# x0 = u + np.random.rand(n, l) * 0.001
x0 = np.zeros((n, l))
# x0 = np.random.randn(n, l)
