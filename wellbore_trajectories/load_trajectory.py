from .well import Well, define_section
import pandas as pd
from .equations import *
from numpy import linspace

def load(data, **kwargs):
    """
    读取轨迹数据
    :param data:轨迹数据，可以是excel文件、dataframe数据或者是元素是字典的列表
    :param kwargs:
        set_start: dict, None
            初始点北坐标东坐标 m {'north': 0, 'east': 0}.
        change_azimuth: float, int, None
           方位改变量（可以不要）
        set_info: dict, None
            dict, {'dlsResolution', 'wellType': 'onshore'|'offshore', 'units': 'metric'|'english'}.
        inner_pts: num
            俩测点间的插值点个数
    :return:一个Well类
    """
    # 参数设置
    set_start = kwargs.get('set_start', None)  # 初始位置
    change_azimuth = kwargs.get('change_azimuth', None)  # 方位改变量
    set_info = kwargs.get('set_info', None)  # 井眼信息读取
    inner_pts = kwargs.get('inner_points', 0)  # 内插点个数

    info = {'dlsResolution': 30, 'wellType': 'offshore', 'units': 'metric'}  # 初始信息设置

    initial_point = {'north': 0, 'east': 0}  # 初始点设置

    base_data = False  #
    data_initial = None
    processed = False

    # PROCESSING DATA

    if isinstance(set_info, dict):
        for param in set_info:  # 改变井眼信息的默认值，通过输入的参数
            if param in info:
                info[param] = set_info[param]

    if isinstance(set_start, dict):
        for x in set_start:  # 通过输入的参数，改变初始点的默认值
            if x in initial_point:
                initial_point[x] = set_start[x]

    if isinstance(data, pd.DataFrame):
        base_data = True
        data_initial = data.copy()  # 保持最初副本
        data.dropna(axis=1, how='all', inplace=True)  # 按列过滤掉某一全为NAN的列
        data.dropna(inplace=True)  # 按行过滤掉某一行，只要有一个数据缺失，就过滤掉
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if ".xlsx" in data:
        base_data = True
        data = pd.read_excel(data)  # 用pandas打开表格
        data_initial = data.copy()
        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if ".csv" in data:
        base_data = True
        data = pd.read_csv(data)  # 用pandas打开csv
        data_initial = data.copy()
        data.dropna(axis=1, how='all', inplace=True)
        data.dropna(inplace=True)
        data = solve_key_similarities(data)
        data = data.to_dict('records')
        processed = True

    if type(data[0]) is dict:
        if not processed:
            data = solve_key_similarities(data)
        md = [x['md'] for x in data]
        inc = [x['inc'] for x in data]
        az = [x['azi'] for x in data]
    else:  # 如果不是字典的列表，而是列表的列表
        md, inc, az = data[:3]

        # 处理缺省数据（连上一步，因为没有处理）
    for x, y in enumerate(md):  # 如果是字符串，那么将值改为数值型
        if type(y) == str:
            md[x] = float(y.split(",", 1)[0])
            inc[x] = float(inc[x].split(",", 1)[0])
            az[x] = float(az[x].split(",", 1)[0])

    # 方位角改变
    if change_azimuth is not None:
        for a in range(len(az)):
            az[a] += change_azimuth

    # 创建轨迹点
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'tvd': 0, 'sectionType': 'vertical', 'pointType': 'survey'}]
    trajectory[-1].update(initial_point)  # 加上初始设置的北、东坐标
    inner_pts += 2  # 一个测段最初有两点

    if md[0] != 0:  # 井口设置
        md = [0] + md
        inc = [0] + inc
        az = [0] + az

    for idx, md in enumerate(md):
        if md > 0:
            dogleg = calc_dogleg(inc[idx - 1], inc[idx], az[idx - 1], az[idx])
            point = {'md': md, 'inc': inc[idx], 'azi': az[idx],
                     'north': calc_north(trajectory[-1]['north'], trajectory[-1]['md'], md,
                                         trajectory[-1]['inc'], inc[idx],
                                         trajectory[-1]['azi'], az[idx],
                                         dogleg),
                     'east': calc_east(trajectory[-1]['east'], trajectory[-1]['md'], md,
                                       trajectory[-1]['inc'], inc[idx],
                                       trajectory[-1]['azi'], az[idx],
                                       dogleg),
                     'tvd': calc_tvd(trajectory[-1]['tvd'], trajectory[-1]['md'], md,
                                     trajectory[-1]['inc'], inc[idx], dogleg),
                     'dl': degrees(dogleg),
                     'pointType': 'survey'
                     }
            point['sectionType'] = define_section(point, trajectory[-1])
            p1 = trajectory[-1]

            if inner_pts > 2:
                dl_unit = point['dl'] / (inner_pts - 1)  # 插值点之间，每小段内狗腿角
                md_segment = linspace(p1['md'], point['md'], inner_pts)[1:-1]  # 内插点井深
                count = 1
                for new_md in md_segment:
                    dl_new = dl_unit * count  # 插值点离这一段起始点的狗腿角
                    inner_point = {'md': new_md, 'dl': dl_unit}
                    inner_pt_calcs(inner_point, p1, point, dl_sv=dl_new, dls_resolution=info['dlsResolution'])
                    count += 1
                    trajectory.append(inner_point)
                point['dl'] = dl_unit
            trajectory.append(point)
    well = Well({'trajectory': trajectory, 'info': info})
    if base_data:
        well._base_data = data_initial

    return well


def solve_key_similarities(data):
    md_similarities = ['MD', 'md(ft)', 'md(m)', 'MD(m)', 'MD(ft)', 'MD (ft)',
                       'measureddepth', 'MeasuredDepth',
                       'measureddepth(m)', 'MeasuredDepth(m)',
                       'measureddepth(ft)', 'MeasuredDepth(ft)', '井深']

    inc_similarities = ['Inclination', 'inclination', 'Inc', 'Incl', 'incl',
                        'inclination(°)', 'Inclination(°)', 'Incl(°)', 'Inc°', 'inc°',
                        'incl(°)', 'Inc(°)', 'inc(°)', 'INC', 'INC(°)', 'INCL',
                        'INCL(°)', 'Inc(deg)', 'inc(deg)', '井斜角']

    azi_similarities = ['az', 'az(°)',
                        'Az', 'Az(°)',
                        'AZ', 'AZ(°)',
                        'Azi', 'Azi(°)',
                        'azi(°)', 'Azi°',
                        'AZI', 'AZI(°)',
                        'Azimuth', 'Azimuth(°)',
                        'azimuth', 'azimuth(°)',
                        'Azi(deg)', 'azi(deg)', '方位角']

    tvd_similarities = ['TVD', 'TVD (m)', 'TVD (ft)', 'TVD(m)', 'TVD(ft)',
                        'tvd (m)', 'tvd (ft)', 'tvd(m)', 'tvd(ft)']

    north_similarities = ['NORTH', 'NORTH(m)', 'NORTH(ft)',
                          'North', 'North(m)', 'North(ft)',
                          'Northing(m)', 'Northing(ft)'
                          'N/S(m)', 'N/S(ft)',
                          'Ns(m)', 'Ns(ft)']

    east_similarities = ['EAST', 'EAST(m)', 'EAST(ft)',
                         'East', 'East(m)', 'East(ft)',
                         'Easting(m)', 'Easting(ft)'
                         'E/W(m)', 'E/W(ft)',
                         'Ew(m)', 'Ew(ft)']

    possible_keys = [md_similarities,
                     tvd_similarities,
                     inc_similarities,
                     azi_similarities,
                     north_similarities,
                     east_similarities]

    correct_keys = ['md', 'tvd', 'inc', 'azi', 'north', 'east']

    true_key = 0
    for i in possible_keys:
        for x in i:
            if isinstance(data, pd.DataFrame):
                data.columns = data.columns.str.replace(' ', '')
                if x in data.columns:
                    data.rename(columns={x: correct_keys[true_key]}, inplace=True)
            else:
                if x.replace(' ', '') in data[0]:
                    for point in data:
                        point[correct_keys[true_key]] = point[x]
        true_key += 1

    return data