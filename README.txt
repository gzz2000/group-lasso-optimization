
**有关代码测试**
此代码有一套接口符合作业要求中的格式要求，如下：
gl_cvx_gurobi.py  中的 solver_cvx_gurobi
gl_cvx_mosek.py   中的 solver_cvx_mosek
gl_gurobi.py      中的 solver_gurobi
gl_mosek.py       中的 solver_mosek
gl_gurobi_term.py 中的 solver_gubori_term
注：gurobi_term是使用gurobi的addVars而非addMVar实现的，总时间少一些，但是从收敛曲线上看随着迭代次数增加收敛会慢，详见报告。

使用到的模块及版本：
python 3.8.5 (ubuntu 20.04)
gurobi 9.10 linux amd64
gurobipy from python pip
mosek from python pip
cvxpy from python pip
numpy 1.19.3 from python pip

如果想使用自带的测试小工具（介绍见后），还需要安装：
matplotlib from python pip (to make it work, you may need to use `apt install python3-gi-cairo` to install dependencies)
tabulate from python pip

画出报告中的表格和折线图的代码也附上：test.py的使用方法
python3 test.py gl_cvx gl_gurobi gl_mosek gl_gurobi_term
即，在python3 test.py后列出要测试的模块，每个模块下通过solvers字典定位包含的所有求解器，并调用加以测试。

求解器返回的out中，包含额外的信息：
{'iters': iters}
iters = [(0, xxx), (1, xxx), ..., (11, xxx)]
这个是每一步迭代时目标函数的值，用来画曲线。

因为我们在调用gurobi和mosek，而这些信息并没有包含在它们的接口中，因而要使用特殊的技巧，在执行他们的时候把标准输出临时重定向，把他们的输出拿到以后，用正则表达式匹配出log中的迭代步数、迭代中目标函数值的变化信息。这个trick主要在utils.py中实现。

