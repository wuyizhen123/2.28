import numpy as np
import piecewise_utils
import sympy



class CubicSplineInterpolation:
    """
    三次样条插值
    """
    def __init__(self, x, y, dy=None, d2y=None, boundary_type="natural"):
        """
        三次样条插值插值必要参数的初始化，及各健壮性检测
        :param x: 已知数据的x坐标点
        :param y: 已知数据的y坐标点
        """

        self.x = np.asarray(x, dtype=np.float)
        self.y = np.asarray(y, dtype=np.float)  # 类型转换，数据结构采用array

        if len(self.x) > 1 and len(self.x) == len(self.y):
            self.n = len(self.x)  # 已知离散数据点的个数
        else:
            raise ValueError("插值数据（x，y，dy）维度不匹配!")
        self.dy, self.d2y = dy, d2y  # 边界条件的一阶导数值和二阶导数值
        self.boundary_type = boundary_type  # 边界条件类型，默认自然边界条件
        self.polynomial = None  # 最终的插值多项式，符号表示
        self.poly_coefficient = None  # 最终插值多项式的系数向量，幂次从高3到低

        self.y0 = None  # 所求插值点的值，单个值或向量

    def fit_interp(self):
        """
        三次样条插值多项式
        :return:
        """
        t = sympy.Symbol("t")
        self.polynomial = dict()  # 三次多项式函数
        self.poly_coefficient = np.zeros((self.n - 1, 4))
        if self.boundary_type == "complete":  # 给定边界一阶导数且相等
            if self.dy is not None:
                self.dy = np.asarray(self.dy, dtype=np.float)
                self.complete_spline(t, self.x, self.y, self.dy)
            else:
                raise ValueError("第一种边界条件需给定边界处的一阶导数值！")
        elif self.boundary_type == "second":  # 给定边界二阶导数且相等
            if self.d2y is not None:
                self.d2y = np.asarray(self.d2y, dtype=np.float)
                self.second_spline(t, self.x, self.y, self.d2y)
            else:
                raise ValueError("第二种边界条件需给定边界处的二阶导数值！")
        elif self.boundary_type == "natural":
            self.natural_spline(t, self.x, self.y)
        elif self.boundary_type == "periodic":
            self.periodic_spline(t, self.x, self.y)
        else:
            raise ValueError("目前仅支持complete、second、natural、和periodic边界条件")

    def spline_poly(self, t, x, y, m):
        """
        构造三次样条多项式
        :param t: 符号变量
        :param x: 已知数据的的x坐标值
        :param y: 已知数据的的y坐标值
        :param m: 求解的矩阵系数，即多项式中的m系数
        :return:
        """
        for i in range(self.n - 1):
            hi = x[i + 1] - x[i]  # 子区间长度
            pi = y[i] / hi ** 3 * (2 * (t - x[i]) + hi) * (x[i + 1] - t) ** 2 + \
                 y[i + 1] / hi ** 3 * (2 * (x[i + 1] - t) + hi) * (t - x[i]) ** 2 + \
                 m[i] / hi ** 2 * (t - x[i]) * (x[i + 1] - t) ** 2 - \
                 m[i + 1] / hi ** 2 * (x[i + 1] - t) * (t - x[i]) ** 2
            self.polynomial[i] = sympy.simplify(pi)
            poly_obj = sympy.Poly(pi, t)  # 根据多项式构造多项式对象
            # 某项系数可能为0，为防止存储错误，分别对应各阶次存储
            mons = poly_obj.monoms()  # 多项式系数对应的阶次
            for j in range(len(mons)):
                self.poly_coefficient[i, mons[j][0]] = poly_obj.coeffs()[j]  # 获取多项式的系数


    def complete_spline(self, t, x, y, dy):
        """
        求解第一种边界条件
        :param t:
        :return:
        """
        A = np.diag(2 * np.ones(self.n))
        c = np.zeros(self.n)
        for i in range(1, self.n - 1):
            u = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
            lambda_ = (x[i + 1] - x[i]) / (x[i + 1] - x[i - 1])
            c[i] = 3 * lambda_ * (y[i] - y[i - 1]) / (x[i] - x[i - 1]) + \
                   3 * u * (y[i + 1] - y[i]) / (x[i + 1] - x[i])
            A[i, i - 1], A[i, i + 1] = lambda_, u
        c[0], c[-1] = 2 * dy[0], 2 * dy[-1]  # 边界条件
        m = np.linalg.solve(A, c)
        self.spline_poly(t, x, y, m)  # 构造三次样条插值多项式




    def second_spline(self, t, x, y, d2y):
        A = np.diag(2 * np.ones(self.n))
        A[0, 1], A[-1, -2] = 1, 1  # 边界特殊情况
        c = np.zeros(self.n)  # 右端向量构造
        for i in range(1, self.n - 1):
            u = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
            lambda_ = (x[i + 1] - x[i]) / (x[i + 1] - x[i - 1])
            c[i] = 3 * lambda_ * (y[i] - y[i - 1]) / (x[i] - x[i - 1]) + \
                   3 * u * (y[i + 1] - y[i]) / (x[i + 1] - x[i])
            A[i, i - 1], A[i, i + 1] = lambda_, u
        c[0] = 3 * (y[1] - y[0]) / (x[1] - x[0]) - (x[1] - x[0]) * d2y[0] / 2  # 边界条件
        c[-1] = 3 * (y[-1] - y[-2]) / (x[-1] - x[-2]) - (x[-1] - x[-2]) * d2y[-1] / 2  # 边界条件
        m = np.linalg.solve(A, c)
        self.spline_poly(t, x, y, m)  # 构造三次样条插值多项式

    def natural_spline(self, t, x, y):
        """
        求解自然边界条件
        :param t:
        :param x:
        :param y:
        :return:
        """
        d2y = np.array([0, 0])  # 自然边界条件
        self.second_spline(t, x, y, d2y)

    def periodic_spline(self, t, x, y):
        """
        周期边界条件
        :param t:
        :param x:
        :param y:
        :return:
        """
        A = np.diag(2 * np.ones(self.n - 1))
        # 边界特殊情况
        h0, h1, he = x[1] -x[0], x[2] - x[1], x[-1] - x[-2]
        A[0, 1] = h0 / (h1 + h0)  # 表示u_1
        A[0, -1] = 1 - A[0, 1]  # 表示lambda_1
        A[-1, 0] = he / (he + h0)  # 表示u_n
        A[-1, -2] = 1 - A[-1, 0]  # 表示lambda_n
        c = np.zeros(self.n - 1)  # 右端向量构造
        for i in range(1, self.n - 1):  # A矩阵第一行和最后一行的值已经构造完
            u = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
            lambda_ = (x[i + 1] - x[i]) / (x[i + 1] - x[i - 1])
            c[i - 1] = 3 * lambda_ * (y[i] - y[i - 1]) / (x[i] - x[i - 1]) + \
                   3 * u * (y[i + 1] - y[i]) / (x[i + 1] - x[i])
            if i < self.n - 2:
                A[i, i - 1], A[i, i + 1] = lambda_, u

        c[-1] = 3 * (he * (y[1] - y[0]) / h0 + h0 * (y[-1] - y[-2]) / he) / (he + h0)  # 边界条件
        m = np.zeros(self.n)
        m[1:] = np.linalg.solve(A, c)
        m[0] = m[-1]  # 最后一个系数赋值给第一个
        self.spline_poly(t, x, y, m)  # 构造三次样条插值多项式


    def cal_interp_x0(self, x0):
        """
        计算所给定的插值点的数值，即插值
        :param x0: 所求插值的X坐标
        :return:
        """

        # x0 = np.asarray(x0, dtype=np.float)
        # n0 = len(x0)  # 所求插值点个数
        # y_0 = np.zeros(n0)  # 存储插值点x0所对应的插值
        # t = self.polynomial.free_symbols.pop()  # 返回值是集合，获取插值多项式的自由变量
        # for i in range(n0):
        #     y_0[i] = self.polynomial.evalf(subs={t: x0[i]})
        # self.y0 = y_0
        # return y_0
        self.y0 = piecewise_utils.cal_interp_x0(self.polynomial, self.x, x0)
        return self.y0

    def plt_interpolation(self, x0=None, y0=None):
        """
        可视化插值对象和所求插值点
        :return:
        """
        # plt.figure(figsize=(8, 6))
        # plt.plot(self.x, self.y, "ro", label="Interpolation base points")
        # xi = np.linspace(min(self.x), max(self.x), 100)  # 模拟100个值
        # yi = self.cal_interp_x0(xi)
        # plt.plot(xi, yi, "b--", label="Interpolation polynomial")
        # if x0 is not None and y0 is not None:
        #     # y0 = self.cal_interp_x0(x0)
        #     plt.plot(x0, y0, "g*", label="Interpolation point values")
        # plt.legend()
        # plt.xlabel("x", fontdict={"fontsize": 12})
        # plt.ylabel("y", fontdict={"fontsize": 12})
        # plt.title("Lagrange Interpolation polynomial and values", fontdict={"fontsize": 14})
        # plt.grid(ls=":")
        # plt.show()
        title = None
        if self.boundary_type == "complete":  # 给定边界一阶导数且相等
            title = "complete"
        elif self.boundary_type == "second":  # 给定边界二阶导数且相等
            title = "second"
        elif self.boundary_type == "natural":
            title = "natural"
        elif self.boundary_type == "periodic":
            title = "periodic"

        params = (self.polynomial, self.x, self.y, "Cubic spline(%s)" % title, x0, y0)
        piecewise_utils.plt_interpolation(params)