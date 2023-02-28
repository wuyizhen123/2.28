import numpy as np
from scipy.interpolate import CubicSpline
import plotly.express as px
import plotly.graph_objects as go
from scipy.spatial.transform import Rotation as R
import wellbore_trajectories as wp

def diameter_deal(met_date, type='diameter', point1 = 100):
    """
    met_date: 井径数据，其列数就是臂数,或者臂数除以二
    type: 数据类型,diameter时,为直径，需要除以二;radius时,半径，不用处理
    point1: 横向插值点个数
    """
    data = np.array(met_date)  # 将井径数据转化为矩阵
    # print(data)  # 检查
    # 获取井径数量
    if type == 'diameter':
        num_ = data.shape[-1] * 2
    elif type == 'radius':
        num_ = data.shape[-1]
    
    # 构造插值矩阵
    if type == 'diameter':
        data = data / 2  # 得到半径
        data0 = data[:,0][:,np.newaxis]  # 第一个井径测量值
        data_mat = np.append(data,data,axis=1)
        data_mat = np.append(data_mat, data0, axis=1)
    elif type == 'radius':
        data0 = data[:,0][:,np.newaxis]
        data_mat = np.append(data, data0, axis=1)
    # print(data_mat)  # 检查
    
    # 横向插值
    # 获取角度
    theta = np.linspace(0, 2 * np.pi, num_ + 1)
    # print(theta)  # 检查
    long_num = data.shape[0]  # 测点数量，纵向
    cs = {}
    for i in range(long_num):  # 插值，对象
        cs[i] = CubicSpline(theta, data_mat[i,:], bc_type='periodic')  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
    cs_ = []
    theta_ =np.linspace(0, 2 * np.pi, point1)  # 具体插值数据
    for i in range(long_num):
        cs_.append(list(cs[i](theta_)))
    cs_ = np.array(cs_)
    # print(cs_)
    xx = cs_ * np.cos(theta_) 
    yy = cs_ * np.sin(theta_)
    return xx, yy


class Well_diameter:
    def __init__(self, meter_date, md = None, well = None, type = 'diameter', point1 = 100, point2 = 500):
        self.meter_data = np.array(meter_date)
        self.meter_type = type
        self.point1 = point1
        self.point2 = point2
        self.md = md
        self.well = well
        self.horiz_interp()  # self.cs_ self.theta_获取！
        if self.md != None:
            self.longi_interp()
        self.get_x_y()
        if self.well != None:
            self.get_env()
            self.cal_rot_axi_ang()
            self.cal_rot_vec()
            self.cal_rot_mat()
            self.rot_()
            self.move_()
        
        
    def horiz_interp(self):
        # 获取井径数量
        if self.meter_type == 'diameter':
            self.num_dr = self.meter_data.shape[-1] * 2
        elif self.meter_type == 'radius':
            self.num_dr = self.meter_data.shape[-1]
        
        # 构造插值矩阵
        if self.meter_type == 'diameter':
            self.meter_data = self.meter_data / 2  # 得到半径
            data0 = self.meter_data[:,0][:,np.newaxis]  # 第一个井径测量值
            data_mat = np.append(self.meter_data,self.meter_data,axis=1)
            data_mat = np.append(data_mat, data0, axis=1)
        elif self.meter_type == 'radius':
            data0 = self.meter_data[:,0][:,np.newaxis]
            data_mat = np.append(self.meter_data, data0, axis=1)
         
        # 横向插值
        # 获取角度
        self.theta = np.linspace(0, 2 * np.pi, self.num_dr + 1)
        
        long_num = self.meter_data.shape[0]  # 测点数量，纵向
        cs = {}
        for i in range(long_num):  # 插值，对象
            cs[i] = CubicSpline(self.theta, data_mat[i,:], bc_type='periodic')  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        cs_ = []
        self.theta_ =np.linspace(0, 2 * np.pi, self.point1)  # 具体插值数据
        for i in range(long_num):
            cs_.append(list(cs[i](self.theta_)))
        self.cs_ = np.array(cs_)
      
    def longi_interp(self):
        self.md = np.array(self.md)
        hor_num = self.cs_.shape[-1]  # 测点数量，横向
        cs = {}
        for i in range(hor_num):
            cs[i] = CubicSpline(self.md, self.cs_[:,i])
            
        cs__ = []
        self.md_ = np.linspace(self.md[0], self.md[-1], self.point2)  # 具体插值数据
        for i in range(hor_num):
            cs__.append(list(cs[i](self.md_)))
        self.cs__ = np.array(cs__).T
        pass
    
    def get_x_y(self):
        self.x = self.cs__ * np.cos(self.theta_)
        self.y = self.cs__ * np.sin(self.theta_)
        self.z = np.zeros(self.x.shape)
    
    def get_env(self):
        E = []
        N = []
        V = []
        delta_E = []
        delta_N = []
        delta_V = []
        for i in self.md_:
            point = self.well.get_any_point(i)
            E.append(point['east'])
            N.append(point['north'])
            V.append(point['tvd'])
            delta_E.append(point['delta']['east'])
            delta_N.append(point['delta']['north'])
            delta_V.append(point['delta']['tvd'])
        self.E = E
        self.N = N
        self.V = V
        self.delta_E = delta_E
        self.delta_N = delta_N
        self.delta_V = delta_V
    
    def cal_rot_axi_ang(self):
        vec1 = np.array([0, 0, 1])
        vec2 = np.array(list(zip(self.delta_E, self.delta_N, self.delta_V)))
        rot_axi = []
        rot_ang = []
        for i in range(self.point2):
            axi = np.cross(vec1, vec2[i])
            axi = axi / np.linalg.norm(axi)
            rot_axi.append(axi)
            
            cosang = np.dot(vec1, vec2[i]) / (np.linalg.norm(vec1) * np.linalg.norm(vec2[i]))
            rot_ang.append(np.arccos(cosang))
        self.rotaxi = np.array(rot_axi)
        self.rotang = np.array(rot_ang)
        
    def cal_rot_vec(self):
        rot_vec = []
        for i in range(self.point2):
            rot_vec.append(self.rotang[i] * self.rotaxi[i])
        self.rotvec = np.array(rot_vec)
    
    def cal_rot_mat(self):
        rot_mat = []
        for i in range(self.point2):
            r = R.from_rotvec(self.rotvec[i])
            mat = r.as_matrix()
            rot_mat.append(mat)
        self.rotmat = np.array(rot_mat)
    
    def rot_(self):
        x_rot = []
        y_rot = []
        z_rot = []
        for i in range(self.point2):
            temp_x = self.x[i]
            temp_y = self.y[i]
            temp_z = self.z[i]
            temp = np.vstack((temp_x, temp_y, temp_z))
            temp = self.rotmat[i].dot(temp)
            x_rot.append(temp[0])
            y_rot.append(temp[1])
            z_rot.append(temp[2])
        self.x_rot = np.array(x_rot)
        self.y_rot = np.array(y_rot)
        self.z_rot = np.array(z_rot)
    
    def move_(self):
        x_mov = []
        y_mov = []
        z_mov = []
        for i in range(self.point2):
            temp_x = self.x_rot[i]
            temp_y = self.y_rot[i]
            temp_z = self.z_rot[i]
            temp_x = temp_x + self.E[i]
            temp_y = temp_y + self.N[i]
            temp_z = temp_z + self.V[i]
            x_mov.append(temp_x)
            y_mov.append(temp_y)
            z_mov.append(temp_z)
        self.x_mov = np.array(x_mov)
        self.y_mov = np.array(y_mov)
        self.z_mov = np.array(z_mov)
        
        
if __name__ ==  '__main__':
    aa = np.random.random(size=(9,3))
    md = [1,2,3,4,5,6,7,8,9]
    well = wp.load('HW1113.xlsx')
    # x, y = diameter_deal([[0.2162, 0.2660, 0.2426]], type='diameter')

    # fig = go.Figure(data=[go.Scatter(
    #     x=x[0], 
    #     y=y[0], 
    #     mode='markers', 
    #     marker=dict(size=8,)
    # )])
    # fig.add_trace(go.Scatter(
    #     x=x[0], 
    #     y=y[0], 
    #     mode='lines', 
    #     line=dict(width=2)))
    # fig.update_layout(height=800, width=800)
    # fig.show()
    ooo = Well_diameter(aa, md=md, well=well, point2=100)
    # fig = go.Figure(data=[go.Scatter(
    #     x=ooo.x[0], 
    #     y=ooo.y[0],
    #     mode='markers', 
    #     marker=dict(size=8,)
    # )])
    # fig.show()
    x = ooo.x_mov.reshape(-1)
    y = ooo.y_mov.reshape(-1)
    z = ooo.z_mov.reshape(-1)
    fig = go.Figure(data=[go.Scatter3d(
        x=x, 
        y=y,
        z=z,
        mode='markers', 
        marker=dict(size=1,)
    )])
    fig.update_scenes(zaxis_autorange = 'reversed')
    fig.show()