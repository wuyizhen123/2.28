import numpy as np
import pandas as pd
# import wellbore_trajectories as wp
from copy import deepcopy

try:
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False


class TorqueDrag:
    def __init__(self, well, wellbore, string, fluid_density, name=None, v=1, n=0, wob=None, tob=None, overpull=None):
        """

        :param well:
        :param wellbore:
        :param string:
        :param fluid_density:
        :param name:
        :param v:管柱下行速度，米每秒
        :param n:管柱旋转速度，转每分
        :param wob:
        :param tob:
        :param overpull:
        """
        assert wellbore.complete, "Wellbore not complete"
        assert string.complete, "String not complete"  # 确定加载的管串，井身结构是否完全覆盖井眼

        self.well = well  # 将well类传过来，其中的trajectory是其是一个字典的列表，列表每个元素内包含该测点的信息
        self.trajectory = well.trajectory  # 最后保持的是深拷贝且增加节点的轨迹列表（其值为字典）
        self.wellbore = wellbore  # 传井身结构
        self.string = string  # 传管串数据
        self.fluid_density = fluid_density  # 传钻井液密度
        self.name = name  # 设置名字
        self.add_well_points_from_strings()  # 根据管串结构与井身结构，增加节点

        self.get_buoyancy_factors()  # 获取浮力系数
        self.get_weight_buoyed_and_radius()  # 设置套管重量与外径
        self.get_inc_delta()  # 获取设置井斜角增量与每段井斜角变化率
        self.get_azi_delta()  # 获取每段方位角增量与每段方位角变化率
        self.get_inc_average()  # 获取每段平均井斜角，直接用rad表示
        self.torque, self.tension = {}, {}
        self.get_coeff_friction_sliding(v, n)  # 设置井身结构摩阻系数
        self.get_well_curvature()  # 设置每一测段井眼曲率
        self.index = np.where(self.md == self.string.bottom)[0][0] + 1  # 找到管柱最深处时井深的索引，加一是为了接下来的操作，末尾数不取
        self.get_forces_and_torsion()
        if any((wob, tob, overpull)):
            self.get_forces_and_torsion(wob=wob, tob=tob, overpull=overpull)

    def add_well_points_from_strings(self):
        """
        根据管串结构与井身结构，增加节点
        :return:
        """
        well_copy = deepcopy(self.well)
        trajectory_copy = deepcopy(self.well.trajectory)  # 深拷贝，以免变化影响原数据,这个值是字典的列表
        trajectory = pd.DataFrame(trajectory_copy)  # 将字典的列表转换成Dataframe
        md = np.array(trajectory['md']).tolist()  # 将Dataframe中的md列先转成array，在变成列表

        for k, v in self.wellbore.sections.items():
            if v['bottom'] in md:
                continue
            else:
                well_copy.interp_any_point(v['bottom'])
        for k, v in self.string.sections.items():
            if v['bottom'] in md:
                continue
            else:
                well_copy.interp_any_point(v['bottom'])
        self.trajectory = well_copy.trajectory  # 将self.trajectory这个属性引用的值转移到trajectory上

    def get_buoyancy_factors(self):
        """
        定义浮力因子，给每一段管串数据（钻井液中浮重），并且将此属性加入到管串sections对应段处的字典属性内
        """
        for k, v in self.string.sections.items():
            v['buoyancy_factor'] = buoyancy_factor(self.fluid_density, v['density'])

    def get_weight_buoyed_and_radius(self):
        section = 0
        weights = [0]
        weights_line = [0]  # 单位在流体中的线重
        diameter = [self.get_characteristic_od(section)]
        trajectory = pd.DataFrame(self.trajectory)
        self.md = np.array(trajectory['md'])
        self.delta_md = np.zeros_like(self.md)
        self.delta_md[1:] = self.md[1:] - self.md[:-1]
        for i, j in zip(self.md[1:], self.delta_md[1:]):
            if i > self.string.bottom:
                break
            while 1:
                if self.string.sections[section]['top'] < i <= self.string.sections[section]['bottom']:
                    weights.append(self.string.sections[section]['unit_weight'] * j
                                   * self.string.sections[section]['buoyancy_factor'])  # 注意单位为N
                    weights_line.append(self.string.sections[section]['unit_weight']
                                        * self.string.sections[section]['buoyancy_factor'])  # 单位为N/m
                    diameter.append(self.get_characteristic_od(section))
                    break
                else:
                    section += 1
        self.weight_buoyed = np.array(weights)  # 测段每节点与上一节点部分在钻井液中的浮重，array类型，N
        self.weight_buoyed_line = np.array(weights_line)  # 节点所处部分的单位线重，N/m
        self.radius = np.array(diameter) / 2  # 节点处外半径，array类型

    def get_inc_delta(self):
        trajectory = pd.DataFrame(self.trajectory)
        self.inc = np.array(trajectory['inc'])  # 每测点井斜角，角度表示
        self.inc_rad = np.radians(self.inc)  # 每测点井斜角，用弧度表示
        self.delta_inc = np.zeros_like(self.inc)  # 每测点距离上测点的井斜角变化量,角度表示
        self.delta_inc_rad = np.zeros_like(self.inc_rad)  # 每测点距离上测点的井斜角变化量，弧度表示
        self.delta_inc[1:] = self.inc[1:] - self.inc[:-1]
        self.delta_inc_rad[1:] = self.inc_rad[1:] - self.inc_rad[:-1]

        self.inc_rate = np.zeros_like(self.inc)  # 设置井斜角变化率
        self.inc_rate[1:] = self.delta_inc_rad[1:] / self.delta_md[1:]  # 变化率用rad每米表示

    def get_azi_delta(self):
        trajectory = pd.DataFrame(self.trajectory)
        self.azi = np.array(trajectory['azi'])  # 每测点方位角，角度表示
        self.azi_rad = np.radians(self.azi)  # 每测点方位角，用弧度表示
        self.delta_azi = np.zeros_like(self.azi)  # 每测点距离上测点的方位角变化量,角度表示
        self.delta_azi_rad = np.zeros_like(self.azi_rad)  # 每测点距离上测点的方位角变化量，弧度表示
        self.delta_azi[1:] = self.azi[1:] - self.azi[:-1]
        self.delta_azi_rad[1:] = self.azi_rad[1:] - self.azi_rad[:-1]

        self.azi_rate = np.zeros_like(self.azi)  # 设置井斜角变化率
        self.azi_rate[1:] = self.delta_azi_rad[1:] / self.delta_md[1:]  # 变化率用rad每米表示

    def get_inc_average(self):
        self.inc_average = np.zeros_like(self.inc_rad)
        self.inc_average[1:] = (self.inc_rad[1:] + self.inc_rad[:-1]) / 2

    def get_characteristic_od(self, section):
        if bool(self.string.sections[section].get('tooljoint_od')):
            return self.string.sections[section]['tooljoint_od']
        else:
            return self.string.sections[section]['od']

    def get_coeff_friction_sliding(self, v, n):
        section = 0
        friction = [self.wellbore.sections[section]['coeff_friction_sliding']]
        friction_d = [v / np.sqrt(v ** 2 + (self.radius[0] * np.pi * n * self.radius[0] / 30) ** 2) * friction[0]]  # 轴向摩阻系数
        friction_t = [(self.radius[0] * np.pi * n * self.radius[0] / 30) / \
                      np.sqrt(v ** 2 + (self.radius[0] * np.pi * n * self.radius[0] / 30) ** 2) * friction[0]]  # 周向（切向）摩阻系数
        for i, j in zip(self.md[1:], self.delta_md[1:]):
            if i > self.wellbore.bottom:
                break
            while 1:
                if self.wellbore.sections[section]['top'] < i <= self.wellbore.sections[section]['bottom']:
                    friction.append(self.wellbore.sections[section]['coeff_friction_sliding'])
                    friction_d.append(v / np.sqrt(v ** 2 + (self.radius[0] * np.pi * n * self.radius[0] / 30) ** 2) * \
                                      self.wellbore.sections[section]['coeff_friction_sliding'])
                    friction_t.append((self.radius[0] * np.pi * n * self.radius[0] / 30) / \
                                      np.sqrt(v ** 2 + (self.radius[0] * np.pi * n * self.radius[0] / 30) ** 2) * \
                                      self.wellbore.sections[section]['coeff_friction_sliding'])
                    break
                else:
                    section += 1
        self.coeff_friction_sliding = np.array(friction)  # 测段每一节点与上一节点这一段的摩阻系数
        self.coeff_friction_sliding_d = np.array(friction_d)  # 对应轴向摩阻系数
        self.coeff_friction_sliding_t = np.array(friction_t)  # 对应周向摩阻系数

    def get_well_curvature(self):
        curvature = [self.trajectory[1]['dl'] / self.delta_md[1]]
        for i, j in enumerate(self.md):
            if i == 0:
                continue
            curvature.append(self.trajectory[i]['dl'] / self.delta_md[i])
        self.curvature = np.array(curvature)  # 测段每一点的井眼曲率，单位度每米
        self.curvature_rad = np.radians(self.curvature)  # 测段每一点井眼曲率，单位rad每米

    def get_forces_and_torsion(self, wob=False, tob=False, overpull=False):
        if any((wob, tob)):
            assert tob, "Can't have WOB without TOB"
            assert wob, "Can't have TOB wihtouh WOB"
            ft = [np.array([0.0, -wob, -wob])]
            tn = [tob]
        else:
            ft = [np.zeros(3)]
            tn = [0]
        if overpull:
            ft[0][0] = overpull
        fn = []

        for row in zip(
                self.delta_md[:self.index][::-1],  # 传每测段长度dL
                self.inc_average[:self.index][::-1],  # 传每段平均井斜角α, rad
                self.inc_rate[:self.index][::-1],  # 传井斜变化率，rad/m
                self.azi_rate[:self.index][::-1],  # 传方位变化率，rad/m
                self.weight_buoyed[::-1],  # 传单位重量，N
                self.weight_buoyed_line[::-1],  # 传每段单位线重，N/m
                self.coeff_friction_sliding[:self.index][::-1],  # 传摩阻系数
                self.coeff_friction_sliding_d[:self.index][::-1],  # 传轴向摩阻系数
                self.coeff_friction_sliding_t[:self.index][::-1],  # 传周向摩阻系数
                self.radius[::-1],  # 传管柱外径
                self.curvature_rad[:self.index][::-1],  # 传井眼曲率。rad/m
                self.delta_inc_rad[:self.index][::-1],  # 传井斜角增量，rad
                self.delta_azi_rad[:self.index][::-1],  # 传井方位角增量，rad
        ):
            (delta_md, inc_average, inc_rate, azi_rate, weight_buoyed, weight_buoyed_line,
             coeff_friction_sliding, coeff_friction_sliding_d, coeff_friction_sliding_t, radius, curvature_rad,
             delta_inc_rad, delta_azi_rad) = row
            if curvature_rad == 0:
                fn.append(force_normal(ft[-1], inc_average, delta_inc_rad, delta_azi_rad, weight_buoyed))
                ft.append(ft[-1] + np.array(force_tension_delta(weight_buoyed, inc_average, coeff_friction_sliding, fn[-1])))
                tn.append(tn[-1] + np.array(torsion_delta(coeff_friction_sliding, fn[-1][2], radius)))
                # fn = np.array(fn)[::-1]
                # ft = np.array(ft)[::-1][1:]
                # tn = np.array(tn)[::-1][1:]
                # if wob:
                #     self.tension["drilling"] = ft[:, 2]
                #     self.tension["sliding"] = ft[:, 1]
                # else:
                #     self.tension['slackoff'] = ft[:, 1]
                #     self.tension['rotating'] = ft[:, 2]
                #
                # if tob:
                #     self.torque['drilling'] = tn
                # else:
                #     self.torque['rotating'] = tn
                #
                # if overpull:
                #     self.tension['overpull'] = ft[:, 0]
                # else:
                #     self.tension['pickup'] = ft[:, 0]
                # self.wob, self.tob, self.overpull = wob, tob, overpull
            else:
                sin_contact_angle = []
                cos_contact_angle = []
                fn.append(get_fn(ft[-1], curvature_rad, weight_buoyed_line, inc_rate, inc_average, azi_rate,
                                 coeff_friction_sliding_t))
                sin_contact_angle.append(get_sinangle(weight_buoyed_line, azi_rate, curvature_rad, inc_average, fn[-1],
                                                      coeff_friction_sliding_t, radius, ft[-1], inc_rate))
                cos_contact_angle.append(get_cosangle(ft[-1], curvature_rad, weight_buoyed_line, inc_rate, inc_average,
                                                      coeff_friction_sliding_t, fn[-1], sin_contact_angle[-1]))
                ft.append(ft[-1] + np.array(ft_delta(delta_md, weight_buoyed_line, inc_average, coeff_friction_sliding_d
                                                     , curvature_rad, radius, cos_contact_angle[-1], fn[-1])))
                tn.append(tn[-1] + np.array(tn_delta(coeff_friction_sliding_t, radius, fn[-1])))

        fn = np.array(fn)[::-1]
        ft = np.array(ft)[::-1][1:]
        tn = np.array(tn, dtype=object)[::-1][1:]

        if wob:
            self.tension["drilling"] = ft[:, 2]
            self.tension["sliding"] = ft[:, 1]
        else:
            self.tension['slackoff'] = ft[:, 1]
            self.tension['rotating'] = ft[:, 2]

        if tob:
            self.torque['drilling'] = tn
        else:
            self.torque['rotating'] = tn

        if overpull:
            self.tension['overpull'] = ft[:, 0]
        else:
            self.tension['pickup'] = ft[:, 0]
        self.wob, self.tob, self.overpull = wob, tob, overpull

    def figure(self):
        return figure_string_tension_and_torque(self)


def buoyancy_factor(fluid_density, string_density=7.85):
    """
    Parameters
    ----------
    fluid_density: float
        钻井液密度 in SG.
    string_density: float
        管柱密度.
    Returns
    -------
    result: float
        浮力系数.
    """
    result = (string_density - fluid_density) / string_density

    return result


def force_normal(force_tension, inc_average, inc_delta, azi_delta, weight_buoyed):
    result = np.sqrt((force_tension * azi_delta * np.sin(inc_average)) ** 2
                     + (force_tension * inc_delta + weight_buoyed * np.sin(inc_average)) ** 2)
    return result


def force_tension_delta(weight_buoyed, inc_average, coeff_friction_sliding, force_normal):
    A = weight_buoyed * np.cos(inc_average)
    B = coeff_friction_sliding * force_normal
    pickup, slackoff, rotating = A + B * np.array([1, -1, 0])  # 上提 下放 静置旋转
    return (pickup, slackoff, rotating)


def torsion_delta(coeff_friction_sliding, force_normal, radius):
    result = coeff_friction_sliding * force_normal * radius
    return result


def get_fn(force_tension, curve, w_l, inc_rate, inc, azi_rate, co_fi_t):
    result = np.sqrt((force_tension * curve - w_l * inc_rate / curve * np.sin(inc)) ** 2
                     + (w_l * azi_rate / curve * (np.sin(inc)) ** 2) ** 2) / np.sqrt(1 + co_fi_t ** 2)
    return result


def get_sinangle(w_l, azi_rate, curve, inc, f_n, co_fi_t, rdius, f_t, inc_rate):
    result = (w_l * azi_rate / curve * np.sin(inc) ** 2 + f_n * co_fi_t * rdius * curve - co_fi_t * f_t * curve
              + co_fi_t * w_l * inc_rate / curve * np.sin(inc)) / (f_n * (1 + co_fi_t ** 2))
    return result


def get_cosangle(f_t, curve, w_l, inc_rate, inc, co_fi_t, f_n, sin_angle):
    result = (f_t * curve - w_l * inc_rate / curve * np.sin(inc) + co_fi_t * f_n * sin_angle) / f_n
    return result


def ft_delta(delta_md, w_l, inc, co_fi_d, curve, radius, cos_angle, f_n):
    A = delta_md * w_l * np.cos(inc)
    B = delta_md * co_fi_d * (1 - curve * radius * cos_angle) * f_n
    pickup, slackoff, rotating = A + B * np.array([1, -1, 0])  # 上提 下放 静置旋转
    return (pickup, slackoff, rotating)


def tn_delta(co_fi_t, radius, f_n):
    result = co_fi_t * radius * f_n
    return result


def figure_string_tension_and_torque(td, units=dict(depth='m', tension='N', torque='N*m')):
    assert PLOTLY, "Please install plotly"

    fig = make_subplots(rows=1, cols=2)

    for k, v in td.tension.items():
        fig.add_trace(go.Scatter(x=v, y=td.md, name=f"tension: {k}",), row=1, col=1)

    for k, v, in td.torque.items():
        fig.add_trace(go.Scatter(x=v, y=td.md, name=f"torque: {k}",), row=1, col=2)

    fig.update_layout(
        title_text=(f"<b>wellbore:</b> {td.wellbore.name}<br>" + f"<b>string:</b> {td.string.name}"),
        xaxis=dict(title=f"Tension ({units['tension']})"),
        yaxis=dict(autorange='reversed', title=f"MD ({units['depth']})", exponentformat='none',),
        xaxis2=dict(title=f"Torque ({units['torque']})"),
        yaxis2=dict(autorange='reversed', title=f"MD ({units['depth']})", exponentformat='none',))

    return fig


class HookLoad:
    def __init__(self, well, wellbore, string, fluid_density, step=30, name=None, ff_range=(0.1, 0.4, 0.1)):
        """
        计算大钩载荷随井深变化的类
        Parameters
        ----------
        well:
        wellbore:
        string:
        fluid_density: float
        step: float
        name:
        ff_range: (3) tuple
            摩阻系数的开始，结束，步长变化，
        """
        self.well = well
        self.wellbore = wellbore
        self.string = string
        self.fluid_density = fluid_density
        self.name = name
        self.step = step
        self.get_ff_range(ff_range)
        self.get_data()

    def get_ff_range(self, ff_range):
        self.ff_range = np.arange(*ff_range).tolist()
        self.ff_range.append(ff_range[1])

    def get_data(self):
        self.data = {}
        self.md_range = np.arange(self.string.top + self.step, self.string.bottom, self.step).tolist()
        self.md_range.append(self.string.bottom)

        for ff in self.ff_range:
            wellbore_temp = deepcopy(self.wellbore)
            for k in wellbore_temp.sections.keys():
                wellbore_temp.sections[k]['coeff_friction_sliding'] = ff

            self.data[ff] = {}
            data_temp = []

            for md in self.md_range:
                bha_temp = self.string.depth(md)
                data_temp.append(TorqueDrag(self.well, wellbore_temp, bha_temp, fluid_density=self.fluid_density,
                                            name=self.name))
            for t in data_temp[0].tension.keys():
                self.data[ff][t] = [d.tension[t][0] for d in data_temp]

    def figure(self):
        return figure_hookload(self)


def figure_hookload(hl, units=dict(depth='m', tension='N', torque='N*m')):
    assert PLOTLY, "Please install plotly"
    fig = go.Figure()
    lines = [None, 'dashdot', 'dash', 'dot']
    md = hl.md_range
    annotations = []

    for i, (k, v) in enumerate(hl.data.items()):
        x = v['slackoff']
        fig.add_trace(go.Scatter(x=x, y=md, name=f"SOFF: {k:.2f}", line=dict(color='blue', dash=lines[i])),)
        annotations.append(dict(x=x[-1], y=md[-1], xanchor='center', yanchor='top', text=f'{k:.2f}', showarrow=False,
                                font=dict(color='blue')))
    for i, (k, v) in enumerate(hl.data.items()):
        fig.add_trace(go.Scatter(x=v['rotating'], y=md, name=f"RoffBFF: {k:.2f}", line=dict(color='green')))
        break

    for i, (k, v) in enumerate(hl.data.items()):
        x = v['pickup']
        fig.add_trace(go.Scatter(x=x, y=md, name=f"PUFF: {k:.2f}", line=dict(color='red', dash=lines[i])),)
        annotations.append(dict(x=x[-1], y=md[-1], xanchor='center', yanchor='top', text=f'{k:.2f}', showarrow=False,
                                font=dict(color='red')))

    title_text = ("<b>wellbore:</b>")
    for i, (k, v) in enumerate(hl.wellbore.sections.items()):
        coupler = "" if i == 0 else "and "
        title_text += (f" {coupler}{v['name']}" + f" to {v['bottom']:.0f}" + f"{units['depth']}")
    title_text += "<br><b>string:</b>"

    last = len(hl.string.sections.keys()) - 1
    for i, (k, v) in enumerate(list(hl.string.sections.items())[::-1]):
        coupler = "" if i == 0 else "and "
        if i == last:
            title_text += (f" {coupler}{v['name']}" + " to surface")
        else:
            title_text += (f" {coupler}{v['name']}" + f" ({v['length']:.0f}" + f"{units['depth']})")

    fig.update_layout(title_text=title_text, xaxis=dict(title=f"Hook-Load ({units['tension']})"),
                      yaxis=dict(autorange='reversed', title=f"MD ({units['depth']})", exponentformat='none',),
                      annotations=annotations)

    return fig
