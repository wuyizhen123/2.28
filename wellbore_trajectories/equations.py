from math import *
from numpy import pi


def calc_dogleg(inc1, inc2, azi1, azi2):
    """
    计算两测点间的狗腿角
    :param inc1: 点1井斜角
    :param inc2: 点2井斜角
    :param azi1: 点1方位角
    :param azi2: 点2方位角
    :return: 以rad为单位的狗腿角
    """

    # if inc1 == inc2 and azi1 == azi2:
    #     dl = 0
    # else:
    #     inner_value = cos(radians(inc1)) * cos(radians(inc2)) + sin(radians(inc1)) * sin(radians(inc2)) * \
    #         cos(radians(azi2 - azi1))
    #     if inner_value > 1:
    #         inner_value = 1
    #     if inner_value < -1:
    #         inner_value = -1
    #     dl = acos(inner_value)
    dl = acos(cos(radians(inc1)) * cos(radians(inc2)) +
              sin(radians(inc1)) * sin(radians(inc2)) * cos(radians(azi2 - azi1)))

    return dl


def calc_north(north_prev, md1, md2, inc1, inc2, azi1, azi2, dogleg):
    """
    利用最小曲率法和前一点信息计算当前点的北坐标
    :param north_prev: 前一点北坐标
    :param md1: 前一点井深
    :param md2: 当前点井深
    :param inc1: 前一点井斜角
    :param inc2: 当前点井斜角
    :param azi1: 前一点方位角
    :param azi2: 当前点方位角
    :param dogleg: 此段（包括当前点）狗腿角
    :return: 当前点北坐标
    """
    rf = calc_rf(dogleg, md1, md2)
    # delta_md = md2 - md1
    north_delta = rf * (sin(radians(inc1)) * cos(radians(azi1)) + sin(radians(inc2)) * cos(radians(azi2)))
    north_new = north_prev + north_delta

    return north_new


def calc_east(east_prev, md1, md2, inc1, inc2, azi1, azi2, dogleg):
    """
    利用最小曲率法和前一点信息计算当前点的东坐标
    :param east_prev: 前一点东坐标
    :param md1: 前一点井深
    :param md2: 当前点井深
    :param inc1: 前一点井斜角
    :param inc2: 当前点井斜角
    :param azi1: 前一点方位角
    :param azi2: 当前点方位角
    :param dogleg: 此段（包括当前点）狗腿角
    :return: 当前点东坐标
    """
    rf = calc_rf(dogleg, md1, md2)
    east_delta = rf * (sin(radians(inc1)) * sin(radians(azi1)) + sin(radians(inc2)) * sin(radians(azi2)))
    east_new = east_prev + east_delta

    return east_new


def calc_tvd(tvd_prev, md1, md2, inc1, inc2, dogleg):
    """
    利用最小曲率法和前一点信息计算当前点的垂深
    :param tvd_prev: 前一点垂
    :param md1: 前一点井深
    :param md2: 当前点井深
    :param inc1: 前一点井斜角
    :param inc2: 当前点井斜角
    :param dogleg: 此段（包括当前点）狗腿角
    :return: 当前点垂深
    """
    rf = calc_rf(dogleg, md1, md2)
    tvd_delta = rf * (cos(radians(inc1)) + cos(radians(inc2)))
    tvd_new = tvd_prev + tvd_delta

    return tvd_new


def calc_rf(dogleg, md1, md2):
    """
    计算最小曲率法的辅助系数
    :param dogleg: 这一段的狗腿角
    :param md1: 上一点井深
    :param md2: 当前点井深
    :return:
    """
    # if dogleg == 0:
    #     rf = 1
    # else:
    #     rf = tan(dogleg / 2) / (dogleg / 2)
    if dogleg == 0:
        rf = (md2 - md1) / 2
    else:
        rf = (md2 - md1) / dogleg * tan(dogleg / 2)

    return rf


def calc_dls(point, delta_md, resolution=30):
    """
    利用设定的分辨率计算狗腿严重度
    :param point: 测点
    :param delta_md: 与前一点的井深差
    :param resolution:
    :return: dls
    """

    return point['dl'] * resolution / delta_md


def inner_pt_calcs(inner_point, p1, p2, dl_sv=None, dls_resolution=30):
    if dl_sv is None:       # dogleg from last survey point (not interpolated)
        dl_sv = inner_point['dl']

    delta_md = inner_point['md'] - p1['md']
    inner_point['dls'] = calc_dls(inner_point, delta_md, dls_resolution)  # 这句能否删掉？不能删！ 任意一点插值有用
    inner_point = get_inc_azi(inner_point, p1, p2, dl_sv)

    inner_point['north'] = calc_north(p1['north'], p1['md'],
                                      inner_point['md'],
                                      p1['inc'], inner_point['inc'],
                                      p1['azi'], inner_point['azi'],
                                      radians(inner_point['dl']))
    inner_point['east'] = calc_east(p1['east'], p1['md'],
                                    inner_point['md'],
                                    p1['inc'], inner_point['inc'],
                                    p1['azi'], inner_point['azi'],
                                    radians(inner_point['dl']))
    inner_point['tvd'] = calc_tvd(p1['tvd'], p1['md'], inner_point['md'],
                                  p1['inc'], inner_point['inc'],
                                  radians(inner_point['dl']))
    inner_point['pointType'] = 'interpolated'
    inner_point['sectionType'] = p2['sectionType']

    return inner_point


def adjust_azi(azi, azi1, azi2):
    limits = sorted([azi1, azi2])
    count = 1
    while not limits[0] <= azi <= limits[1]:
        if azi > limits[1]:
            azi -= 90
        else:
            azi += 90
        count += 1
        if count == 4:
            break
    return azi


def component(p, comp):
    if comp == 'n':
        return sin(radians(p['inc'])) * cos(radians(p['azi']))
    if comp == 'e':
        return sin(radians(p['inc'])) * sin(radians(p['azi']))
    if comp == 'v':
        return cos(radians(p['inc']))


def delta(p1, p2, dl_new, comp):
    c1 = sin(radians(p2['dl'])-radians(dl_new)) * component(p1, comp) / sin(radians(p2['dl']))
    c2 = sin(radians(dl_new)) * component(p2, comp) / sin(radians(p2['dl']))
    return c1 + c2


def get_inc_azi(p, p1, p2, dl_new):
    if p2['dl'] == 0:
        p['inc'] = p1['inc']
        p['azi'] = p1['azi']
    else:
        dn = delta(p1, p2, dl_new, 'n')
        de = delta(p1, p2, dl_new, 'e')
        dv = delta(p1, p2, dl_new, 'v')
        if p1['inc'] == p2['inc']:
            p['inc'] = p1['inc']
        else:
            p['inc'] = degrees(atan2((dn ** 2 + de ** 2) ** .5, dv))
        if p1['azi'] == p2['azi']:
            p['azi'] = p1['azi']
        else:
            p['azi'] = degrees((atan2(de, dn) + (2 * pi)) % (2 * pi))
        p['azi'] = adjust_azi(p['azi'], p1['azi'], p2['azi'])
    return p


def interp_pt(md, trajectory):
    """
    使用井深作为输入，获取插值点信息
    :param md: 井深
    :param trajectory: 测点的列表
    :return: 一个包含所有信息的测点
    """

    if md < 0:
        raise ValueError('MD value must be positive')
    if md > trajectory[-1]['md']:
        raise ValueError("MD can't be deeper than deepest trajectory MD")

    # 需要找到正确的p1点和p2点做插值
    p1 = None
    p2 = None
    for idx, point in enumerate(trajectory):
        if point['md'] < md < trajectory[idx + 1]['md']:
            p1 = point
            p2 = trajectory[idx + 1]
            break
        elif point['md'] == md:
            return point

    dl = (md - p1['md']) * p2['dl'] / (p2['md'] - p1['md'])  # 计算距离上测点的狗腿角
    target = {'md': md, 'dl': dl}
    target = inner_pt_calcs(target, p1, p2)
    target['delta'] = get_delta(target, p1)
    return target


def scan_tvd(tvd, trajectory):
    if tvd < 0:
        raise ValueError('TVD value must be positive')
    if tvd > max([p['tvd'] for p in trajectory]):
        raise ValueError("TVD value can't be deeper than deepest trajectory TVD")

    p1 = None
    p2 = None
    for idx, point in enumerate(trajectory):
        if point['tvd'] < tvd:
            if idx < len(trajectory) - 1 and round(tvd, 2) < round(trajectory[idx + 1]['tvd'], 2):
                p1 = point
                p2 = trajectory[idx + 1]
                break
        elif round(point['tvd'], 2) == round(tvd, 2):
            return point

    if p2['sectionType'] == 'vertical':
        return interp_pt(p1['md'] + tvd - p1['tvd'], trajectory)

    # 应用二分法
    new_point = interp_pt((p1['md'] + p2['md']) / 2, trajectory)
    a = p1['md']
    b = p2['md']
    while round(tvd, 2) != round(new_point['tvd'], 2):
        new_md = (a + b) / 2
        new_point = interp_pt(new_md, trajectory)
        if new_point['tvd'] < tvd:
            a = new_md
        else:
            b = new_md

    return new_point


def interp_pt_any(md, trajectory):
    if md < 0:
        raise ValueError('MD value must be positive')
    if md > trajectory[-1]['md']:
        raise ValueError("MD can't be deeper than deepest trajectory MD")

    # 需要找到正确的p1点和p2点做插值
    p1 = None
    p2 = None
    inter_idex = None  # 插入地点的索引
    for idx, point in enumerate(trajectory):
        if point['md'] < md < trajectory[idx + 1]['md']:
            p1 = point
            p2 = trajectory[idx + 1]
            inter_idex = idx + 1
            break
        elif point['md'] == md:
            return trajectory
    dl = (md - p1['md']) * p2['dl'] / (p2['md'] - p1['md'])  # 计算距离上测点的狗腿角
    target = {'md': md, 'dl': dl}
    target = inner_pt_calcs(target, p1, p2)
    p2['dl'] = p2['dl'] - dl  # 改变后一测点的狗腿值，因为中间查了一点
    trajectory.insert(inter_idex, target)  # 在原数据内插入此点

    for idx, point in enumerate(trajectory):
        if idx > 0:
            point['delta'] = get_delta(point, trajectory[idx - 1])
        else:
            point['delta'] = get_delta(point)
    return trajectory


def get_delta(p2, p1=None):
    if not p1:
        return {'md': 0, 'tvd': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'dls': 0, 'north': 0, 'east': 0}
    else:
        delta_dict = {}
        for param in ['md', 'tvd', 'inc', 'azi', 'dl', 'dls', 'north', 'east']:
            delta_dict.update({param: p2[param] - p1[param]})
    return delta_dict


def scan_tvd_any(tvd, trajectory):
    if tvd < 0:
        raise ValueError('TVD value must be positive')
    if tvd > max([p['tvd'] for p in trajectory]):
        raise ValueError("TVD value can't be deeper than deepest trajectory TVD")
    p1 = None
    p2 = None
    for idx, point in enumerate(trajectory):
        if point['tvd'] < tvd:
            if idx < len(trajectory) - 1 and round(tvd, 2) < round(trajectory[idx + 1]['tvd'], 2):
                p1 = point
                p2 = trajectory[idx + 1]
                break
        elif round(point['tvd'], 2) == round(tvd, 2):
            return trajectory
    # 应用二分法
    new_point = interp_pt((p1['md'] + p2['md']) / 2, trajectory)
    a = p1['md']
    b = p2['md']
    while round(tvd, 2) != round(new_point['tvd'], 2):
        new_md = (a + b) / 2
        new_point = interp_pt(new_md, trajectory)
        if new_point['tvd'] < tvd:
            a = new_md
        else:
            b = new_md
    interp_pt_any(new_point['md'], trajectory)
    return trajectory


def get_pt_any(md, trajectory):
    if md < 0:
        raise ValueError('MD value must be positive')
    if md > trajectory[-1]['md']:
        raise ValueError("MD can't be deeper than deepest trajectory MD")

    # 需要找到正确的p1点和p2点做插值
    p1 = None
    p2 = None
    inter_idex = None  # 插入地点的索引
    for idx, point in enumerate(trajectory):
        if point['md'] < md < trajectory[idx + 1]['md']:
            p1 = point
            p2 = trajectory[idx + 1]
            inter_idex = idx + 1
            break
        elif point['md'] == md:
            return point
    dl = (md - p1['md']) * p2['dl'] / (p2['md'] - p1['md'])  # 计算距离上测点的狗腿角
    target = {'md': md, 'dl': dl}
    target = inner_pt_calcs(target, p1, p2)
    p2['dl'] = p2['dl'] - dl  # 改变后一测点的狗腿值，因为中间查了一点
    trajectory.insert(inter_idex, target)  # 在原数据内插入此点

    for idx, point in enumerate(trajectory):
        if idx > 0:
            point['delta'] = get_delta(point, trajectory[idx - 1])
        else:
            point['delta'] = get_delta(point)
    return target


def get_tvd_any(tvd, trajectory):
    if tvd < 0:
        raise ValueError('TVD value must be positive')
    if tvd > max([p['tvd'] for p in trajectory]):
        raise ValueError("TVD value can't be deeper than deepest trajectory TVD")
    p1 = None
    p2 = None
    for idx, point in enumerate(trajectory):
        if point['tvd'] < tvd:
            if idx < len(trajectory) - 1 and round(tvd, 2) < round(trajectory[idx + 1]['tvd'], 2):
                p1 = point
                p2 = trajectory[idx + 1]
                break
        elif round(point['tvd'], 2) == round(tvd, 2):
            return point
    # 应用二分法
    new_point = interp_pt((p1['md'] + p2['md']) / 2, trajectory)
    a = p1['md']
    b = p2['md']
    while round(tvd, 2) != round(new_point['tvd'], 2):
        new_md = (a + b) / 2
        new_point = interp_pt(new_md, trajectory)
        if new_point['tvd'] < tvd:
            a = new_md
        else:
            b = new_md
    return interp_pt_any(new_point['md'], trajectory)
