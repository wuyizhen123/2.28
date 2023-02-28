from ui_widget import Ui_MainWindow
import ui_load
import ui_plot
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget, QFileDialog
import sys
import wellbore_trajectories as wp
from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtQuick import QQuickWindow
from PySide6 import QtCore
from PySide6 import QtQuick

class Widget (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.widget_inc_para_set = []
        self.well = []
        self.well_name = []
        self.setupUi(self)
        self.well_numbers.triggered.connect(self.num)
        self.load_wellprofile.triggered.connect(self.inc_para_set)
        self.plot_well_profile.triggered.connect(self.plot_well)
        
    def num(self):
        value, ok = QInputDialog.getInt(self, "井数量", "选择 : ",1)
        if (ok) :
            self.well_numbers = value
        for _ in range(self.well_numbers):
            temp = Inc_para_set()
            temp.para_signal.connect(self.para_well_set)
            self.widget_inc_para_set.append(temp)
            
    def para_well_set(self, well_dict):
        self.well.append(well_dict['well'])
        self.well_name.append(well_dict['name'])
            
    def inc_para_set(self):
        for i in range(self.well_numbers):
            self.widget_inc_para_set[i].show()
            
    def plot_well(self):
        self.set_plot = Set_plot(self.well, self.well_name)
        self.set_plot.show()
        pass
    
class Inc_para_set(QWidget, ui_load.Ui_Form):
    para_signal = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_2.clicked.connect(self.doOk)
        self.pushButton_3.clicked.connect(self.hide)
        
    def load_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open File", 
                                                        "/home", 
                                                        "xlsx (*.xlsx);;All files(*.*)")
        self.lineEdit.setText(f'{self.file_name}')
        
    def doOk(self):
        start_north = float(self.doubleSpinBox.value())
        start_east = float(self.doubleSpinBox_2.value())
        azi_change = float(self.doubleSpinBox_3.value())
        dls = float(self.doubleSpinBox_4.value())
        if self.comboBox_2.currentText() == '陆地':
            wel_ty = 'offshore'
        else:
            wel_ty = 'onshore'
        if self.comboBox.currentText() == '米制':
            uit = 'metric'
        else:
            uit = 'english'
        inter = int(self.spinBox.value())
        from utils.threads import Sub_thread_1
        self.sub_thread = Sub_thread_1(data=self.file_name, set_start={'north': start_north, 'east': start_east}, change_azimuth=azi_change, 
                                  set_info={'dlsResolution': dls, 'wellType': wel_ty, 'units': uit}, inner_pts=inter)
        self.sub_thread.success.connect(self.sub_load)
        self.sub_thread.start()
        
        self.hide()
        
    def sub_load(self, data1, set_start1, change_azimuth1, set_info1, inner_pts1):
        self.well = wp.load(data=data1, set_start=set_start1, change_azimuth=change_azimuth1, set_info=set_info1, inner_points=inner_pts1)
        if self.lineEdit_2.text() == '':
            self.well_name = None
        else:
            self.well_name = self.lineEdit_2.text()
            
        self.para_signal.emit({'well': self.well, 'name': self.well_name})


class Set_plot(QWidget, ui_plot.Ui_Form):
    def __init__(self, well, well_name):
        super().__init__()
        self.setupUi(self)
        self.well = well
        self.well_name = well_name
        
        self.pushButton.clicked.connect(self.sure_widget)
        self.pushButton_2.clicked.connect(self.close_widget)
        
    def sure_widget(self):
        self.plot_type = self.comboBox.currentText()
        
        if self.comboBox_2.currentText() == '否':
            self.darkMode = False
        else:
            self.darkMode = True
            
        if self.comboBox_3.currentText() == '无':
            self.color = ''
        else:
            self.color = self.comboBox_3.currentText()
            
        self.plot_size = self.spinBox.value()
        
        from utils.threads import Sub_thread_2
        self.sub_thread = Sub_thread_2(self.plot_type, self.darkMode, self.color, self.plot_size)
        self.sub_thread.get_fig.connect(self.fig_get)
        self.sub_thread.start()
        pass
        
    def close_widget(self):
        self.close()
        
    def fig_get(self, plot_type_, darkMode, color, plot_size):
        if color == '':
            color = None
        self.fig = self.well[0].plot(plot_type=plot_type_, add_well=self.well[1:], names=self.well_name, 
                                     style={'darkMode': darkMode, 'color': color, 'size': plot_size})
        # self.fig.show()
        from utils.qt_plotly import PlotlyViewer
        self.plotScreen = PlotlyViewer(fig=self.fig)
        self.plotScreen.settings().setAttribute(self.plotScreen.settings().WebAttribute.WebGLEnabled, True)
        self.plotScreen.show()
        

QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
QQuickWindow.setGraphicsApi(QtQuick.QSGRendererInterface.OpenGLRhi)
app = QApplication(sys.argv)
aa = Widget()
aa.show()
app.exec()