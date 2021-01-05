
新增代码：
gl_ADMM_dual
gl_ADMM_primal_direct
gl_ADMM_primal

它们的含义参见报告，使用说明同前。

提示：
这些代码中，都有自动演示超参数选取对收敛情况影响的代码，在代码最后，将对应的部分（如gl_ADMM_dual.py末尾的t的选取）取消注释，再使用（以ADMM dual为例）
python3 test.py gl_ADMM_dual
就可以获得一份各种参数下收敛情况的对比表格和曲线图。

使用附带的测试工具执行所有已实现的算法：
python3 test.py all

将会输出如下信息，并打出一个很混乱的收敛曲线图：
Solver                             Objective        Error    Time(s)    Iter    Sparsity
-------------------------------  -----------  -----------  ---------  ------  ----------
ADMM_dual                           0.63208   7.46364e-05  0.133522       52   0.0996094
ADMM_primal_direct                  0.632082  7.56571e-05  0.0607453      51   0.0996094
ADMM_primal                         0.632099  8.93007e-05  0.0563291      47   0.0996094
FGD_primal_0.000001                 0.632059  3.96615e-05  0.60126      1200   0.0996094
FGD_primal_line_search_0.000001     0.632167  0.000309367  0.404386      445   0.507812
ProxGD_primal                       0.632058  3.841e-05    1.98943      4500   0.0996094
ProxGD_primal_line_search           0.632058  3.841e-05    1.89263      1154   0.0996094
FProxGD_primal                      0.632058  3.81504e-05  0.541193     1200   0.0996094
FProxGD_primal_line_search          0.632148  0.000153433  0.442929      415   0.320312
SGD_primal                          0.632061  4.1901e-05   0.375459      389   0.100586
SGD_primal_normal_sgd               0.632061  4.16583e-05  1.97372      4500   0.100586
GD_primal_0.000001                  0.632059  3.99827e-05  0.399346      442   0.100586
GD_primal_normal_gd_0.000001        0.632059  4.01644e-05  1.93456      4500   0.100586
cvx(GUROBI)                         0.632058  3.84376e-05  1.98775        11   0.0996094
cvx(MOSEK)                          0.632058  3.84812e-05  0.981761       12   0.0996094
cvx(CVXOPT)                         0.632058  3.85192e-05  6.69941        13   0.0996094
gurobi_SOCP                         0.632059  3.8983e-05   4.03044        12   0.0996094
gurobi_SOCP_term                    0.632125  7.1033e-05   0.658007       19   0.112305
mosek_SOCP                          0.632058  3.84436e-05  0.824145       12   0.0996094

-----

新增代码：
gl_FGD_primal
gl_FGD_primal_line_search
gl_ProxGD_primal
gl_ProxGD_primal_line_search
gl_FProxGD_primal
gl_FProxGD_primal_line_search

它们的含义请参见报告，使用说明同前。

使用附带的测试工具执行所有测试：
python3 test.py gl_FGD_primal gl_FGD_primal_line_search gl_ProxGD_primal gl_ProxGD_primal_line_search gl_FProxGD_primal gl_FProxGD_primal_line_search gl_SGD_primal gl_SGD_primal_normal_sgd gl_GD_primal gl_GD_primal_normal_gd gl_cvx gl_gurobi gl_mosek gl_gurobi_term

将会输出以下信息并打出一个收敛曲线图：

（略）

对以往代码的小修改：减小了SGD_primal和GD_primal的迭代步数，同时限于篇幅默认不输出对不同smoothing参数的测试，如有需要可以在代码中手动开启。

（以下是第二次作业的README）
-----

代码接口：
gl_SGD_primal             中的 solver_SGD_primal
gl_SGD_primal_normal_sgd  中的 solver_SGD_primal_normal_sgd   （这两个的区别可以看报告里说的）
gl_GD_primal            中的  solver_GD_primal
gl_GD_primal_normal_gd  中的 solver_GD_primal_normal_gd  （这两个包含opts：delta，意义是smoothing的参数，见报告）

全部测试：
python3 test.py gl_SGD_primal gl_SGD_primal_normal_sgd gl_GD_primal gl_GD_primal_normal_gd gl_cvx gl_gurobi gl_mosek gl_gurobi_term

软件环境版本请参见下附的以往README。

本次的数据生成和测试模块修复了上次的一些bug，包括：
error function 的定义以往和老师在matlab里的定义不同，改成了一样的。
生成数据的时候原来老师写的是m*0.1，后来改成了n*0.1，于是我在这次也相应修改了。

（以下是第一次作业的README）

------

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

