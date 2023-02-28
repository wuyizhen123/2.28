from .equations import *
from .plot import plot_wellpath, plot_top_view, plot_vs
import pandas as pd


class Well(object):
    def __init__(self, data):
        self.info = data['info']
        self.trajectory = data['trajectory']
        for idx, point in enumerate(self.trajectory):
            if idx > 0:
                delta_md = point['md'] - self.trajectory[idx - 1]['md']
                point['dls'] = calc_dls(point, delta_md, resolution=self.info['dlsResolution'])
                point['delta'] = get_delta(point, self.trajectory[idx - 1])
            else:
                point['dls'] = 0
                point['delta'] = get_delta(point)
        self.npoints = len(self.trajectory)

    def plot(self, **kwargs):
        default = {'plot_type': '3d', 'add_well': None, 'names': None, 'style': None, 'y_axis': 'md', 'x_axis': 'inc'}
        for key, value in kwargs.items():
            default[key] = value

        if default['plot_type'] == '3d':
            fig = plot_wellpath(self, add_well=default['add_well'], names=default['names'], style=default['style'])
            return fig
        elif default['plot_type'] == 'top':
            fig = plot_top_view(self, add_well=default['add_well'], names=default['names'], style=default['style'])
            return fig
        elif default['plot_type'] == 'vs':
            fig = plot_vs(self, y_axis=default['y_axis'], x_axis=default['x_axis'], add_well=default['add_well'],
                            names=default['names'], style=default['style'])
            return fig
        else:
            raise ValueError('The plot type "{}" is not recognised'.format(default['plot_type']))

    def df(self):
        dataframe = pd.DataFrame(self.trajectory)
        return dataframe

    def add_location(self, lat, lon):
        """
        设置经纬度
        """
        self.info['location'] = {'lat': lat, 'lon': lon}

    def get_point(self, depth, depth_type='md'):
        """
        得到给定深度处的井的全部信息
        :param depth: 深度值，井深或者垂深, MD or TVD
        :param depth_type: 'md' (默认) or 'tvd'
        :return:
        """
        if depth_type == 'md':
            return interp_pt(depth, self.trajectory)

        elif depth_type == 'tvd':
            return scan_tvd(depth, self.trajectory)

        else:
            raise ValueError(depth_type, ' is not a valid value for depth_type')

    def interp_any_point(self, depth, depth_type='md'):
        """
        任意一点插值，注意改变后端测点的信息，为摩阻计算做准备
        :param depth:
        :param depth_type:
        :return:
        """
        if depth_type == 'md':
            self.npoints += 1
            return interp_pt_any(depth, self.trajectory)

        elif depth_type == 'tvd':
            self.npoints += 1
            return scan_tvd_any(depth, self.trajectory)
        else:
            raise ValueError(depth_type, ' is not a valid value for depth_type')
        
    def get_any_point(self, depth, depth_type='md'):
        """
        任意一点插值，注意改变后端测点的信息，为摩阻计算做准备
        :param depth:
        :param depth_type:
        :return:
        """
        if depth_type == 'md':
            self.npoints += 1
            return get_pt_any(depth, self.trajectory)

        elif depth_type == 'tvd':
            self.npoints += 1
            return get_tvd_any(depth, self.trajectory)
        else:
            raise ValueError(depth_type, ' is not a valid value for depth_type')


def define_section(p2, p1=None):

    if not p1:
        return 'vertical'

    else:
        if p2['inc'] == p1['inc'] == 0:
            return 'vertical'
        else:
            if round(p2['inc'], 2) == round(p1['inc'], 2):
                if int(p2['tvd'] - p1['tvd']) == 0:  # 向0取整？
                    return 'horizontal'  # 水平段
                else:
                    return 'hold'  # 稳斜
            else:
                if p2['inc'] > p1['inc']:
                    return 'build-up'   # 造斜
                if p2['inc'] < p1['inc']:
                    return 'drop-off'   # 降斜


def get_delta(p2, p1=None):

    if not p1:
        return {'md': 0, 'tvd': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'dls': 0, 'north': 0, 'east': 0}

    else:
        delta_dict = {}
        for param in ['md', 'tvd', 'inc', 'azi', 'dl', 'dls', 'north', 'east']:
            delta_dict.update({param: p2[param] - p1[param]})

    return delta_dict
