import numpy as np
# import matplotlib.pyplot as plt



def cal_interp_x0(polynomial, x, x0):
    """
        计算所给定的插值点的数值，即插值
        :param polynomial: 插值多项式
        :param x: 插值点的x坐标值
        :param x0: 所求插值的X坐标
        :return:
        """

    x0 = np.asarray(x0, dtype=np.float)
    n0 = len(x0)  # 所求插值点个数
    y_0 = np.zeros(n0)  # 存储插值点x0所对应的插值
    t = polynomial[0].free_symbols.pop()  # 获取多项式的自由变量

    for i in range(n0):
        idx = 0  # 子区间索引初始化
        for j in range(len(x) - 1):
            # 查找x0所在的子区间，获取子区间的索引
            if x[j] <= x0[i] <= x[j+1] or x[j+1] <= x0[i] <= x[j]:
                idx = j
                break
        y_0[i] = polynomial[idx].evalf(subs={t: x0[i]})
    return y_0


def plt_interpolation(params):
    """
    可视化插值对象和所求插值点
    :return:
    """
    # polynomial, x, y, title, x0, y0 = params
    # plt.figure(figsize=(8, 6))
    # plt.plot(x, y, "ro", label="Interpolation base points")
    # xi = np.linspace(min(x), max(x), 100)  # 模拟100个值
    # yi = cal_interp_x0(polynomial, x, xi)
    # plt.plot(xi, yi, "b--", label="Interpolation polynomial")
    # if x0 is not None and y0 is not None:
    #     # y0 = self.cal_interp_x0(x0)
    #     plt.plot(x0, y0, "g*", label="Interpolation point values")
    # plt.legend()
    # plt.xlabel("x", fontdict={"fontsize": 12})
    # plt.ylabel("y", fontdict={"fontsize": 12})
    # plt.title(title + "Interpolation polynomial and values", fontdict={"fontsize": 14})
    # plt.grid(ls=":")
    # plt.show()
    pass